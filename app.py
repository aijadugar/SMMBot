from flask import Flask, request, jsonify, session
import json
import re
import os
import redis
from flask_cors import CORS
from datetime import timedelta
from flask_session import Session
from google.oauth2.service_account import Credentials
from gemini_api import get_gemini_response
import gspread
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'fallback-key-for-dev')

# Session configuration (Redis-based)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.getenv("REDIS_URL"))  # Store in Render env
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_NAME'] = 'idti_session'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

CORS(app, supports_credentials=True, origins=["https://smmbot-p68e.onrender.com", "http://127.0.0.1:5500", "https://www.idti.in"])
os.makedirs('./flask_session_dir', exist_ok=True)
Session(app)

creds_json = os.getenv("GOOGLE_CRED")
if not creds_json:
    raise Exception("GOOGLE_CREDS not loaded")

service_account_info = json.loads(creds_json)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
sheet = gspread.authorize(credentials).open_by_key('1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8').sheet1

@app.before_request
def make_session_permanent():
    session.permanent = True

def append_row(data):
    try:
        sheet.append_row(data)
        print("Saved to Google Sheet:", data)
    except Exception as e:
        print("Error saving to Google Sheet:", e)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if session.get("chat_mode"):
        gemini_response = get_gemini_response(user_message)  
        return jsonify({"response": gemini_response})
    
    if "collected_info" not in session:
        session["collected_info"] = {"name": None, "email": None, "mobile": None}

    info = session["collected_info"]

    # Extract email
    if not info["email"]:
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", user_message)
        if email_match:
            info["email"] = email_match.group().strip()

    # Extract mobile number
    if not info["mobile"]:
        mobile_match = re.search(r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b", user_message)
        if mobile_match:
            info["mobile"] = mobile_match.group().strip()

    # Extract name
    if not info["name"]:
        name_match = re.search(
            r"(?:my name is|i am|this is|it's|its)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
            user_message,
            re.IGNORECASE
        )
        if name_match:
            info["name"] = name_match.group(1).strip()
        else:
            simple_name_match = re.fullmatch(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", user_message.strip(), re.IGNORECASE)
            if simple_name_match:
                info["name"] = simple_name_match.group().strip()

    session["collected_info"] = info

    # If all info is collected
    if all([info["name"], info["email"], info["mobile"]]):
        append_row([info["name"], info["email"], info["mobile"]])
        session.pop("collected_info", None)
        session["chat_mode"] = True 
        return jsonify({
            "response": "Thanks to you! Your details have been saved successfully. You can now chat with me!"
        })

    # Ask for missing fields
    if not info["name"]:
        return jsonify({"response": "Hello! May I know your full name, email and mobile number?", "info": info})
    elif not info["email"]:
        return jsonify({"response": f"Thanks, {info['name']}! Could you share your email address?", "info": info})
    elif not info["mobile"]:
        return jsonify({"response": "Almost done! May I have your mobile number?", "info": info})

    return jsonify({"response": "Please provide your name, email, and mobile number.", "info": info})

if __name__ == '__main__':
    app.run(debug=True) 

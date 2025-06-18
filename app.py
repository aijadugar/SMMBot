from flask import Flask, request, jsonify, session
import json
import re
import os
from flask_cors import CORS
from datetime import timedelta
from flask_session import Session
from google.oauth2.service_account import Credentials
from gemini_api import get_gemini_response
import gspread
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session_dir'  # Create this folder or it will default to temp
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.config['SESSION_USE_SIGNER'] = True

CORS(app, supports_credentials=True)
Session(app)

app.secret_key = '8f4d8f72e6a34670b0a5f4b681a2413e'


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

# Simulated sheet saving function (replace with actual logic)
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
        return jsonify({
            "response": "Thanks to you! Your details have been saved successfully.",
            "info": info
        })

    # Ask for missing fields
    if not info["name"]:
        return jsonify({"response": "Hello! May I know your full name?", "info": info})
    elif not info["email"]:
        return jsonify({"response": f"Thanks, {info['name']}! Could you share your email address?", "info": info})
    elif not info["mobile"]:
        return jsonify({"response": "Almost done! May I have your mobile number?", "info": info})

    return jsonify({"response": "Please provide your name, email, and mobile number.", "info": info})

if __name__ == '__main__':
    app.run(debug=True)

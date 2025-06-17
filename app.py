from flask import Flask, request, jsonify, session
import json
import re
import os
from flask_cors import CORS
from google.oauth2.service_account import Credentials
from gemini_api import get_gemini_response
import gspread
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = '8f4d8f72e6a34670b0a5f4b681a2413e'


creds_json = os.getenv("GOOGLE_CRED")
if not creds_json:
    raise Exception("GOOGLE_CREDS not loaded")

service_account_info = json.loads(creds_json)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
sheet = gspread.authorize(credentials).open_by_key('1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8').sheet1

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if session.get('registered'):
        gemini_response = get_gemini_response(user_message)
        return jsonify({
            "response" : gemini_response,
            "info" : "Hello, I am IDTI Bot, What you want to know about IDTI."
        })

    if "collected_info" not in session:
        session["collected_info"] = {"name": None, "email": None, "mobile": None}

    info = session["collected_info"]

    if not info["email"]:
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", user_message)
        if email_match:
            info["email"] = email_match.group().strip()

    if not info["mobile"]:
        mobile_match = re.search(r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b", user_message)
        if mobile_match:
            info["mobile"] = mobile_match.group().strip()

    if not info["name"]:
        name_match = re.search(r"(?:my name is|i am|this is|it's|its)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", user_message, re.IGNORECASE)
        if name_match:
            info["name"] = name_match.group(1).strip()
        else:
            simple_name_match = re.fullmatch(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", user_message.strip(), re.IGNORECASE)
            if simple_name_match:
                info["name"] = simple_name_match.group().strip()

    session["collected_info"] = info

    if all(info.values()):
        sheet.append_row([info["name"], info["email"], info["mobile"]])
        session.pop("collected_info", None)
        session["registered"] = True
        return jsonify({
            "response": "Thanks to you! Your details have been saved.",
            "info": info
        })

    missing = [k for k, v in info.items() if not v]
    return jsonify({
        "response": f"Got it. Can you please provide your {', '.join(missing)}?",
        "info": info
    })

if __name__ == '__main__':
    app.run(debug=True)

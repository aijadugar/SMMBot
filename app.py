from flask import Flask, request, jsonify, session
import json
import re
from flask_cors import CORS
from google.oauth2.service_account import Credentials
from gemini_api import get_gemini_response
import gspread

app = Flask(__name__)
CORS(app)
app.secret_key = '8f4d8f72e6a34670b0a5f4b681a2413e'


service_account_info = json.loads(os.environ['GOOGLE_CREDS'])
creds = service_account.Credentials.from_service_account_info(service_account_info)
sheet = gspread.authorize(cred).open_by_key('1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8').sheet1



@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    response_text = get_gemini_response(user_message)

    if response_text.startswith("```json") and response_text.endswith("```"):
        response_text = response_text.strip("`")  
        response_text = response_text.replace("json", "", 1).strip()

    print("Cleaned Gemini Response:", response_text)

    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            extracted_info = json.loads(match.group())
        else:
            extracted_info = {}
    except json.JSONDecodeError:
        return jsonify({
            "response": "Sorry, couldn't extract data. Please rephrase.",
            "info": {}
        })

    for key in ['name', 'email', 'mobile']:
        if key in extracted_info and extracted_info[key]:
            session[key] = extracted_info[key]

    if all(k in session for k in ('name', 'email', 'mobile')):
        sheet.append_row([session['name'], session['email'], session['mobile']])
        session.pop('name', None)
        session.pop('email', None)
        session.pop('mobile', None)

        return jsonify({
            "response": "Thanks for your response! Your details have been saved.",
            "info": extracted_info
        })

    return jsonify({
        "response": "Got it. Please continue with the remaining details.",
        "info": extracted_info
    })

if __name__ == '__main__':
    app.run(debug=True)

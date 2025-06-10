from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_api import get_gemini_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    # For now, return a static response
    response_text = get_gemini_response(user_message)

    # extracted_info = {
    #     "name": "",
    #     "email": "",
    #     "mobile": ""
    # }

    return jsonify({
        "response": response_text,
        # "info": extracted_info
    })

if __name__ == '__main__':
    app.run(debug=True)


"""
from flask import Flask, request, session
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session

# Setup Google Sheets
creds = Credentials.from_service_account_file('path-to-credentials.json', scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
])
sheet = gspread.authorize(creds).open("YourSheetName").sheet1

# Route for chatbot messages
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    # Very basic data extraction (replace with NLP if needed)
    if "name is" in user_input.lower():
        session['name'] = user_input.split("name is")[-1].strip()
    elif "email is" in user_input.lower():
        session['email'] = user_input.split("email is")[-1].strip()
    elif "mobile is" in user_input.lower():
        session['mobile'] = user_input.split("mobile is")[-1].strip()

    # Check if all data is collected
    if all(k in session for k in ('name', 'email', 'mobile')):
        # Send to Google Sheet
        row = [session['name'], session['email'], session['mobile']]
        sheet.append_row(row)

        # Clear session data
        session.pop('name')
        session.pop('email')
        session.pop('mobile')
        
        return {"response": "Thanks! Your details have been saved."}
    
    return {"response": "Got it. Please continue..."}

if __name__ == "__main__":
    app.run(debug=True)

"""
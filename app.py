from flask import Flask, request, jsonify
from gemini_api import get_gemini_response

app = Flask(__name__)

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

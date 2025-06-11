import google.generativeai as genai

genai.configure(api_key="AIzaSyC1l9rED1nJeliRvS3LtWD3IxfC_Goue0E")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def get_gemini_response(user_message):
    prompt = f"""
Extract the user's name, email, and mobile number from the message below.

Respond ONLY with a JSON object, nothing else. The format must be:

{{
  "name": "Full Name",
  "email": "email@example.com",
  "mobile": "1234567890"
}}

Do NOT include any text before or after the JSON.

User message:
\"\"\"{user_message}\"\"\"
"""

    response = model.generate_content(prompt)
    return response.text.strip()


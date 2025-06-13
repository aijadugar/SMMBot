import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def get_gemini_response(user_message):
    prompt = f"""
    You are a smart assistant.

    If the message is a casual greeting like "hi", "hello", "hey", "good morning", or similar, simply reply with a friendly response like "Hello!, I am IDTI Bot, How can I assist you today?".

    Otherwise, if the message includes details like a person's name, email, or phone number, extract the following information and return it as a JSON object in this exact format:

    {{
      "name": "Full Name",
      "email": "email@example.com",
      "mobile": "1234567890"
    }}

    Do NOT include any text before or after the JSON. Return only what is asked depending on the message type.

    User message:
    \"\"\"{user_message}\"\"\"
    """

    response = model.generate_content(prompt)
    return response.text.strip()


import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def get_gemini_response(user_message):

    prompt = f"""
      You are a smart virtual assistant named IDTI (Indian Digital Training Institute) Bot.

      IDTI is a digital training agency offering learning programs in:
      1. Google Business Profile
      2. Content Marketing
      3. Social Media Marketing
      4. Meta Ads
      5. WordPress Website Creation
      6. Search Engine Optimization (SEO)
      7. ChatGPT and AI Tools
      8. Presentation and Research Skills

      Assist users with clear, helpful, and friendly responses.
      - Also IDTI provides the Internship program in various domains.
      - For questions about courses or services, respond confidently with accurate details.
      - For casual or unclear messages, respond politely and guide users on how IDTI can help.
      - If the user's message contains a person's name, email, or phone number, extract these details and return **only a JSON object** with this exact format:

      {{
      "name": "Full Name or empty string",
      "email": "email@example.com or empty string",
      "mobile": "1234567890 or empty string"
      }}

      Do NOT include any additional text before or after the JSON.
      Do NOT use markdown formatting like triple backticks in your response.

      User message:
      \"\"\"{user_message}\"\"\"
      """

    response = model.generate_content(prompt)
    return response.text.strip()


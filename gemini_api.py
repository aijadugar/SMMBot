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
    
    User message:
    \"\"\"{user_message}\"\"\"
    """
    response = model.generate_content(prompt)  # assumes `model` is set up
    return response.text.strip()



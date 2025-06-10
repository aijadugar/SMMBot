import google.generativeai as genai

genai.configure(api_key="AIzaSyC1l9rED1nJeliRvS3LtWD3IxfC_Goue0E")

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(user_input)
    return response.text

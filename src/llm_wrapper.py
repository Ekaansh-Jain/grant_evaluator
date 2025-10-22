# src/llm_wrapper.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables first
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Configure the API
genai.configure(api_key=api_key)

def gemini_llm(prompt: str) -> str:
    # Use the latest Gemini Pro model
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

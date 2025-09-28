# src/llm_wrapper.py
import os
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables first
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

def gemini_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

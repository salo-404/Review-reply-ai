import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from project root
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Configure Gemini ONCE
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(f"GEMINI_API_KEY not found at {env_path}")

genai.configure(api_key=api_key)

# LOCK the working model
MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

def generate_reply(prompt: str) -> str:
    response = model.generate_content(prompt)
    return (response.text or "").strip()

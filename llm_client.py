import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load .env locally (won't exist on Streamlit Cloud)
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

# Read API key from environment or Streamlit secrets
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env or Streamlit secrets")

genai.configure(api_key=api_key)

# LOCK the working model
MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

def generate_reply(prompt: str) -> str:
    response = model.generate_content(prompt)
    return (response.text or "").strip()

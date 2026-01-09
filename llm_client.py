import os
from pathlib import Path

import streamlit as st
import google.generativeai as genai

# Try to import dotenv (for local .env). If not installed, it's fine.
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Load .env locally (for your PC only, not needed on Streamlit Cloud)
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists() and load_dotenv is not None:
    load_dotenv(dotenv_path=env_path, override=True)

# Get API key: first from env (.env on your PC), then from Streamlit secrets (on Cloud)
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env or Streamlit secrets")

# Configure Gemini
genai.configure(api_key=api_key)

MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

def generate_reply(prompt: str) -> str:
    response = model.generate_content(prompt)
    # extra safety if .text is missing
    return (getattr(response, "text", "") or "").strip()

import os
from dotenv import load_dotenv

# Load variables from local .env if present
load_dotenv()

# Check local environment variables first, then fallback to Streamlit Cloud secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        import streamlit as st
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file locally or to Streamlit Secrets in deployment."
    )

# Gemini model identifier
GEMINI_MODEL = "gemini-3.5-flash-lite"
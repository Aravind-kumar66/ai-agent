import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file."
    )


# Gemini model
GEMINI_MODEL = "gemini-3.6-flash"
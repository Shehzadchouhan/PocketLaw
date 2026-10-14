"""Gemini AI service – gracefully handles missing API key and missing dependencies."""
import os
import sys

# Try to load dotenv, but don't fail if missing
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
_gemini_available = False
model = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        _gemini_available = True
        print("Gemini AI enabled")
    except Exception as e:
        # Print a plain-text error to avoid Unicode issues on Windows consoles
        print("Gemini init failed:", e)
else:
    print("Gemini API key not set - using built-in RAG + KB fallback")


def is_gemini_available():
    """Returns True if Gemini has been successfully initialized with an API key."""
    return _gemini_available

def get_gemini_response(query):
    if not _gemini_available or model is None:
        raise RuntimeError("Gemini API key not configured. Set GEMINI_API_KEY in .env file.")
    response = model.generate_content(query)
    return response.text


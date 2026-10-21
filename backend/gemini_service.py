"""Gemini AI service – gracefully handles missing API key and missing dependencies."""
import os
import sys
import time
import warnings

# Suppress library deprecation warnings on console
warnings.filterwarnings("ignore", category=FutureWarning)

# Try to load dotenv, but don't fail if missing
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
_gemini_available = False
_active_model = None
_model_candidates = ["gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]
_genai = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        _genai = genai
        _genai.configure(api_key=GEMINI_API_KEY)
        _gemini_available = True
        print("Gemini AI configured; model connection will be checked on demand")
    except Exception as e:
        print("Gemini init failed:", e)
else:
    print("Gemini API key not set - using built-in RAG + KB fallback")


def is_gemini_available():
    """Returns True when Gemini is configured; network access is checked per request."""
    return _gemini_available


def get_gemini_response(query):
    """
    Generates content using Gemini with automatic multi-model failover
    in case of quota limits or transient errors.
    """
    global _active_model
    if not _gemini_available or _genai is None:
        raise RuntimeError("Gemini API key not configured. Set GEMINI_API_KEY in .env file.")

    deadline = time.monotonic() + 8

    def generate(model):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        response = model.generate_content(
            query,
            request_options={"timeout": remaining}
        )
        return response.text if response and response.text else None

    if _active_model is not None:
        try:
            answer = generate(_active_model)
            if answer:
                return answer
        except Exception:
            pass

    for model_name in _model_candidates:
        if time.monotonic() >= deadline:
            break
        try:
            fallback = _genai.GenerativeModel(model_name)
            answer = generate(fallback)
            if answer:
                _active_model = fallback
                return answer
        except Exception:
            continue

    raise RuntimeError("All Gemini model quotas currently exhausted or unavailable.")

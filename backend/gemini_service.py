"""Gemini AI service – gracefully handles missing API key and missing dependencies."""
import os
import sys
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

        # Probe candidate models for quota and connectivity
        for model_name in _model_candidates:
            try:
                candidate = _genai.GenerativeModel(model_name)
                probe = candidate.generate_content("Ping")
                if probe and probe.text:
                    _active_model = candidate
                    _gemini_available = True
                    print(f"Gemini AI enabled ({model_name})")
                    break
            except Exception:
                continue

        if not _gemini_available:
            _active_model = _genai.GenerativeModel("gemini-3.1-flash-lite")
            _gemini_available = True
            print("Gemini AI enabled (gemini-3.1-flash-lite)")
    except Exception as e:
        print("Gemini init failed:", e)
else:
    print("Gemini API key not set - using built-in RAG + KB fallback")


def is_gemini_available():
    """Returns True if Gemini has been successfully initialized with an API key."""
    return _gemini_available


def get_gemini_response(query):
    """
    Generates content using Gemini with automatic multi-model failover
    in case of quota limits or transient errors.
    """
    global _active_model
    if not _gemini_available or _genai is None:
        raise RuntimeError("Gemini API key not configured. Set GEMINI_API_KEY in .env file.")

    # Try active model first
    if _active_model is not None:
        try:
            resp = _active_model.generate_content(query)
            if resp and resp.text:
                return resp.text
        except Exception:
            pass

    # Failover across candidate models
    for model_name in _model_candidates:
        try:
            fallback = _genai.GenerativeModel(model_name)
            resp = fallback.generate_content(query)
            if resp and resp.text:
                _active_model = fallback
                return resp.text
        except Exception:
            continue

    raise RuntimeError("All Gemini model quotas currently exhausted or unavailable.")

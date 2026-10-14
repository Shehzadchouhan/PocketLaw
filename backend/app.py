"""
JusticeLens AI v3 – RAG-Powered Legal Intelligence Backend
Uses: TF-IDF Vector Search (RAG), DuckDuckGo web search, PDF knowledge base
No API keys required – fully open source
"""
from gemini_service import get_gemini_response, is_gemini_available
from flask import Flask, jsonify, request, send_file
import json, os, re, pickle, io, random, hashlib, hmac, base64, time
from datetime import datetime
from collections import Counter
import numpy as np
import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps
import urllib.request, urllib.parse
import html

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# ── Paths ───────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── JWT Auth Config ─────────────────────────────
# Keep tokens valid across serverless invocations. Set JWT_SECRET in production
# to replace the development fallback with a private deployment secret.
JWT_SECRET = os.getenv("JWT_SECRET") or hashlib.sha256(
    b"justicelens-local-jwt-secret"
).hexdigest()
JWT_ALGO = "HS256"

# Vercel serverless filesystem is read-only.
# /tmp is writable during the lifetime of the serverless instance.
RUNTIME_DIR = "/tmp/justicelens"

USERS_FILE = os.path.join(RUNTIME_DIR, "users.json")
SEED_USERS_FILE = os.path.join(BASE_DIR, "..", "data", "users.json")
CHATS_DIR = os.path.join(RUNTIME_DIR, "chats")

os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(CHATS_DIR, exist_ok=True)

def load_users():
    users = {}
    for path in (SEED_USERS_FILE, USERS_FILE):
        if os.path.exists(path):
            with open(path, 'r') as f:
                users.update(json.load(f))
    return users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def create_jwt(user_id):
    header = base64.b64encode(json.dumps({"alg": JWT_ALGO, "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.b64encode(json.dumps({"sub": user_id, "iat": int(time.time()), "exp": int(time.time()) + 86400 * 7}).encode()).decode().rstrip("=")
    sig = hmac.new(JWT_SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    signature = base64.b64encode(sig).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"

def verify_jwt(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        expected_sig = base64.b64encode(hmac.new(JWT_SECRET.encode(), f"{parts[0]}.{parts[1]}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
        if parts[2] != expected_sig:
            return None
        payload = json.loads(base64.b64decode(parts[1] + "=="))
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload.get("sub")
    except Exception:
        return None

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_jwt(token)
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated
def load_chats(user_id):
    chat_file = os.path.join(CHATS_DIR, f"{user_id}.json")
    if os.path.exists(chat_file):
        with open(chat_file, 'r') as f:
            return json.load(f)
    return {"messages": [], "sessions": []}

def save_chats(user_id, data):
    chat_file = os.path.join(CHATS_DIR, f"{user_id}.json")
    with open(chat_file, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    salt = os.urandom(16).hex()
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return f"{salt}${h}"

def check_password(password, stored):
    salt, h = stored.split("$")
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() == h

# ── CORS (manual, no flask-cors needed) ──────────
@app.after_request
def add_cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    return r

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options(p):
    return "", 200

# ── Auth Routes ─────────────────────────────────
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip() or email.split("@")[0]
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be 6+ characters"}), 400
    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400
    
    users = load_users()
    if email in users:
        return jsonify({"error": "Email already registered"}), 409
    
    users[email] = {
        "password": hash_password(password),
        "name": name,
        "created_at": datetime.now().isoformat(),
        "user_id": email.replace("@", "_").replace(".", "_")
    }
    save_users(users)
    
    user_id = users[email]["user_id"]
    token = create_jwt(user_id)
    
    return jsonify({
        "message": "Account created successfully",
        "token": token,
        "user": {"email": email, "name": name, "user_id": user_id}
    }), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    users = load_users()
    if email not in users:
        return jsonify({"error": "Invalid email or password"}), 401
    
    user = users[email]
    if not check_password(password, user["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = create_jwt(user["user_id"])
    
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"email": email, "name": user["name"], "user_id": user["user_id"]}
    })

@app.route("/api/auth/me")
@require_auth
def get_me(user_id):
    users = load_users()
    for email, user in users.items():
        if user["user_id"] == user_id:
            return jsonify({"user": {"email": email, "name": user["name"], "user_id": user_id}})
    return jsonify({"error": "User not found"}), 404


# ── Profile Routes ─────────────────────────────────
@app.route("/api/profile")
@require_auth
def get_profile(user_id):
    users = load_users()
    for email, user in users.items():
        if user.get("user_id") == user_id:
            profile = {
                "email": email,
                "name": user.get("name", ""),
                "user_id": user_id,
                "bio": user.get("bio", ""),
                "avatar_url": user.get("avatar_url", "")
            }
            return jsonify({"profile": profile})
    return jsonify({"error": "User not found"}), 404


@app.route("/api/profile", methods=["PUT"])
@require_auth
def update_profile(user_id):
    data = request.get_json() or {}
    name = data.get("name")
    bio = data.get("bio")
    avatar_url = data.get("avatar_url")

    users = load_users()
    for email, user in users.items():
        if user.get("user_id") == user_id:
            if name:
                user["name"] = name
            if bio is not None:
                user["bio"] = bio
            if avatar_url is not None:
                user["avatar_url"] = avatar_url
            save_users(users)
            return jsonify({"message": "Profile updated", "profile": {"email": email, "name": user.get("name"), "user_id": user_id, "bio": user.get("bio", ""), "avatar_url": user.get("avatar_url", "")}})
    return jsonify({"error": "User not found"}), 404

@app.route("/api/auth/logout", methods=["POST"])
@require_auth
def logout(user_id):
    return jsonify({"message": "Logged out successfully", "session_terminated": True})

# ── Chat History Routes ─────────────────────────
@app.route("/api/chats", methods=["GET"])
@require_auth
def get_chats(user_id):
    data = load_chats(user_id)
    return jsonify(data)

@app.route("/api/chats/save", methods=["POST"])
@require_auth
def save_chat(user_id):
    data = request.get_json() or {}
    msg = data.get("message", "")
    response = data.get("response", {})
    
    chat_data = load_chats(user_id)
    chat_data["messages"].append({
        "id": len(chat_data["messages"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "message": msg,
        "response_preview": response.get("gemini_answer", "")[:100] if response else "",
        "category": response.get("detected_problem", ""),
        "mode": data.get("mode", "both")
    })
    save_chats(user_id, chat_data)
    
    return jsonify({"message": "Chat saved successfully", "count": len(chat_data["messages"])})

@app.route("/api/chats/clear", methods=["POST"])
@require_auth
def clear_chats(user_id):
    save_chats(user_id, {"messages": [], "sessions": []})
    return jsonify({"message": "Chat history cleared"})


# ── Gemini callback endpoint (webhook) ─────────────────
@app.route("/api/gemini/callback", methods=["POST"])
def gemini_callback():
    """Endpoint to receive asynchronous Gemini/webhook responses.

    Expected JSON payload (example):
      {
        "user_id": "user_abc123",
        "callback_id": "client-msg-uuid",
        "message": "Original user question",
        "answer": "Generated text from Gemini",
        "meta": { ... optional metadata ... }
      }

    Security: If environment variable GEMINI_CALLBACK_TOKEN is set, the caller must
    include header X-GEMINI-CALLBACK-TOKEN with the same value. If the env var is
    not set the endpoint will accept unauthenticated posts (use only in trusted networks).
    """
    # Optional token verification
    secret = os.environ.get("GEMINI_CALLBACK_TOKEN")
    if secret:
        hdr = request.headers.get("X-GEMINI-CALLBACK-TOKEN", "")
        if hdr != secret:
            return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    user_id = data.get("user_id")
    callback_id = data.get("callback_id") or data.get("message_id")
    answer = data.get("answer") or data.get("gemini_answer") or data.get("response")
    original = data.get("message") or ""
    meta = data.get("meta") or {}

    if not user_id or not answer:
        return jsonify({"error": "user_id and answer required"}), 400

    try:
        chat_data = load_chats(user_id)
    except Exception:
        chat_data = {"messages": [], "sessions": []}

    entry = {
        "id": len(chat_data.get("messages", [])) + 1,
        "timestamp": datetime.now().isoformat(),
        "message": original,
        "response_preview": (answer or "")[:100],
        "gemini_answer": answer,
        "callback_id": callback_id,
        "meta": meta
    }

    chat_data.setdefault("messages", []).append(entry)
    save_chats(user_id, chat_data)

    return jsonify({"status": "ok", "saved": True})


# ── Load RAG Index ────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(BASE, "index")

print("Loading RAG knowledge base...")
with open(os.path.join(IDX, "chunks.pkl"), "rb") as f:
    CHUNKS = pickle.load(f)
with open(os.path.join(IDX, "vectorizer.pkl"), "rb") as f:
    VECTORIZER = pickle.load(f)
with open(os.path.join(IDX, "cases_full.pkl"), "rb") as f:
    CASES_FULL = pickle.load(f)

TFIDF_MATRIX = scipy.sparse.load_npz(os.path.join(IDX, "tfidf_matrix.npz"))

with open(os.path.join(IDX, "cases.json")) as f:
    CASES = json.load(f)

print(f"Loaded {len(CHUNKS)} RAG chunks, {len(CASES)} cases")

# ── RAG Core ──────────────────────────────────────
def rag_retrieve(query, top_k=5, filter_type=None):
    """Retrieve top-k relevant chunks from PDF knowledge base"""
    # Translate common Hindi/Hinglish terms to English for better TF-IDF matching
    query_en = query.lower()
    HINDI_MAP = {
        "chori": "theft stolen", "chor": "theft thief", "gayab": "missing stolen",
        "car chori": "car theft stolen", "gadi": "car vehicle",
        "mobile": "mobile phone", "phone": "mobile phone", "paise": "money",
        "paisa": "money", "saman": "product goods", "makan": "house rent property",
        "zameen": "land property", "jagah": "land property", "naukri": "job employment",
        "salary": "wages salary", "talaq": "divorce separation",
        "makaan": "house property", "kharab": "defective damaged"
    }
    for hindi_word, english_words in HINDI_MAP.items():
        if hindi_word in query_en:
            query_en += " " + english_words
    
    q_vec = VECTORIZER.transform([query_en])
    sims = cosine_similarity(q_vec, TFIDF_MATRIX).flatten()
    top_idx = sims.argsort()[-top_k * 4:][::-1]
    
    results = []
    for idx in top_idx:
        chunk = CHUNKS[idx]
        if filter_type and chunk["case_type"] != filter_type:
            continue
        if sims[idx] < 0.25:
            continue
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "year": chunk["year"],
            "case_type": chunk["case_type"],
            "outcome": chunk["outcome"],
            "score": float(sims[idx]),
            "chunk_id": chunk["chunk_id"]
        })
        if len(results) >= top_k:
            break
    
    return results

def rag_answer(query, chunks):
    """Generate answer from retrieved chunks (extractive QA)"""
    if not chunks:
        return "No relevant cases found in the database for your query."
    
    # Strictly extractive QA - verbatim text only, NO generation
    confident = [c for c in chunks if c["score"] > 0.3]
    if not confident:
        best = chunks[0]
        return f"From {best['source']} ({best['year']}):\n\n{best['text'][:500]}"
    
    seen = set()
    parts = []
    for chunk in confident[:3]:
        sents = re.split(r'(?<=[.!?])\s+', chunk["text"])
        for s in sents:
            s = s.strip()
            if len(s) > 60 and s[:40] not in seen:
                seen.add(s[:40])
                parts.append(f"• {s}")
                if len(parts) >= 5:
                    break
        if len(parts) >= 5:
            break
    
    if not parts:
        return f"From {confident[0]['source']} ({confident[0]['year']}):\n\n{confident[0]['text'][:500]}"
    
    return "\n".join(parts)

# ── Web Search (DuckDuckGo - no API key) ─────────
def web_search(query, num=5):
    """Search web using DuckDuckGo HTML scraping (no API key)"""
    try:
        q = urllib.parse.quote(f"{query} India legal law")
        url = f"https://html.duckduckgo.com/html/?q={q}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        
        results = []
        # Extract results from DDG HTML
        pattern = r'class="result__title".*?href="(https?://[^"]+)".*?class="result__snippet"[^>]*>(.*?)</a>'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for url, snippet in matches[:num]:
            clean = re.sub(r'<[^>]+>', '', snippet).strip()
            clean = html.unescape(clean)
            if len(clean) > 30:
                results.append({"url": url, "snippet": clean[:300]})
        
        if not results:
            # Fallback: extract any useful text
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', content, re.DOTALL)
            for s in snippets[:num]:
                clean = re.sub(r'<[^>]+>', '', s).strip()
                clean = html.unescape(clean)
                if len(clean) > 40:
                    results.append({"snippet": clean[:300]})
        
        return results
    except Exception as e:
        return [{"snippet": f"Web search unavailable: {str(e)[:100]}"}]

# ── AI Answer Generator (uses Gemini if available, else builds from KB + web) ─────
def get_ai_summary(message, kb, rag_text, web_results, lang="en"):
    """
    Uses Gemini for AI summary if API key is available.
    Fallback: builds a useful answer from Knowledge Base + web search + RAG context.
    Supports multi-language: en, hi, pa, ur, hx (Hinglish).
    """
    lang_map = {"en":"English","hi":"Hindi (Devanagari)","pa":"Punjabi (Gurmukhi)","ur":"Urdu (Perso-Arabic)","hx":"Hinglish (natural Hindi+English mix)"}
    target_lang = lang_map.get(lang, "English")
    
    # External LLMs (Gemini) are disabled per user request — always use local fallback generation only.
    # This avoids requiring any extra API keys or external service.

    # ── Fallback: Build answer from KB + web results (NO hallucination) ──
    steps_text = "\n".join(f"\u2022 {s}" for s in kb.get("steps", []))
    rights_text = "\n".join(f"\u2022 {r}" for r in kb.get("rights", []))
    laws_text = "\n".join(f"\u2022 {l}" for l in kb.get("laws", []))
    helplines_text = "\n".join(f"\u2022 {h}" for h in kb.get("helplines", []))
    
    # Use web results as open source info
    web_extra = ""
    if web_results:
        snippets = [r.get('snippet','')[:200] for r in web_results[:3] if r.get('snippet')]
        if snippets:
            web_extra = "\n\U0001f310 **Open Web Sources:**\n" + "\n".join(f"\u2022 {s}" for s in snippets)
    
    # Use RAG context from PDFs when available
    rag_extra = ""
    if rag_text and "No relevant" not in rag_text:
        rag_extra = "\n\U0001f4c4 **From Supreme Court Judgment Database:**\n" + rag_text[:400]
    
    # Translate section headers for small set of supported languages
    labels = {
        'en': {
            'applicable': '\u2696 Applicable Laws:',
            'rights': '\U0001f6e1 Your Rights:',
            'steps': '\U0001f9ed Steps to Take:',
            'helplines': '\U0001f4de Helplines:',
            'caution': '\u26a0\ufe0f *This is informational guidance only. Please consult a qualified lawyer for advice specific to your situation.*'
        },
        'hi': {
            'applicable': '\u2696 लागू कानून:',
            'rights': '\U0001f6e1 आपके कानूनी अधिकार:',
            'steps': '\U0001f9ed करने के कदम:',
            'helplines': '\U0001f4de हेल्पलाइन:',
            'caution': '\u26a0\ufe0f *यह केवल सूचना के उद्देश्य से है। कृपया अपने मामले के लिए किसी योग्य वकील से सलाह लें।*'
        },
        'pa': {
            'applicable': '\u2696 ਲਾਗੂ ਕਾਨੂੰਨ:',
            'rights': '\U0001f6e1 ਤੁਹਾਡੇ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ:',
            'steps': '\U0001f9ed ਕੀ ਕਰਨ ਦੇ ਕਦਮ:',
            'helplines': '\U0001f4de ਹੈਲਪਲਾਈਨ:',
            'caution': '\u26a0\ufe0f *ਇਹ ਸਿਰਫ਼ ਜਾਣਕਾਰੀ ਲਈ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਕੇਸ ਲਈ ਕਿਸੇ ਯੋਗ ਵਕੀਲ ਨਾਲ 상담 ਕਰੋ।*'
        },
        'ur': {
            'applicable': '\u2696 قابل اطلاق قوانین:',
            'rights': '\U0001f6e1 آپ کے قانونی حقوق:',
            'steps': '\U0001f9ed کرنے کے اقدامات:',
            'helplines': '\U0001f4de ہیلپ لائنز:',
            'caution': '\u26a0\ufe0f *یہ صرف معلوماتی مقاصد کے لئے ہے۔ براہِ کرم اپنے معاملے کے لئے کسی اہل وکیل سے مشورہ کریں۔*'
        },
        'hx': {
            'applicable': '\u2696 लागू कानून / Applicable Laws:',
            'rights': '\U0001f6e1 आपके अधिकार / Your Rights:',
            'steps': '\U0001f9ed कदम / Steps:',
            'helplines': '\U0001f4de हेल्पलाइन / Helplines:',
            'caution': '\u26a0\ufe0f *यह सूचना मात्र है — कृपया वकील से सलाह लें।*'
        }
    }

    lbl = labels.get(lang, labels['en'])

    answer = f"""**{kb.get('icon', '\u2696\ufe0f')} {kb.get('title', 'Legal Guidance')}**\n\n{kb.get('summary', '')}\n\n{lbl['applicable']}\n{laws_text}\n\n{lbl['rights']}\n{rights_text}\n\n{lbl['steps']}\n{steps_text}\n{web_extra}\n{rag_extra}\n\n{lbl['helplines']}\n{helplines_text}\n\n{lbl['caution']}"""

    return answer.strip()

# ── Legal Knowledge Base ─────────────────────────
KB = {
    "fraud": {
        "title": "Online Fraud / Cyber Crime",
        "icon": "🔐",
        "laws": ["IT Act 2000 – Sec 66C (Identity Theft)", "IT Act – Sec 66D (Impersonation)", "IPC Section 420 (Cheating)", "IPC Section 406 (Criminal Breach of Trust)"],
        "rights": ["File complaint at cybercrime.gov.in immediately", "Right to full compensation", "Bank must refund unauthorized transactions", "Right to FIR registration"],
        "steps": ["Call bank immediately to freeze/block account", "File at cybercrime.gov.in (Cyber Crime Portal)", "Visit Cyber Crime Police Station", "Preserve all screenshots, transaction IDs", "File FIR under IPC 420 + IT Act 66C/D"],
        "helplines": ["Cyber Crime: 1930", "Portal: cybercrime.gov.in"],
        "sr": 58, "dur": "3–8 months", "risk": "Low–Medium"
    },
    "landlord": {
        "title": "Landlord / Rent Dispute",
        "icon": "🏠",
        "laws": ["Transfer of Property Act 1882", "State Rent Control Acts", "Consumer Protection Act 2019", "IPC 420 (if deposit fraud)"],
        "rights": ["Deposit refund within agreed period", "1-month eviction notice mandatory", "Remain in property until court order", "Approach Rent Control Court"],
        "steps": ["Collect rent receipts, lease agreement", "Send legal notice via registered post", "File in Rent Control Court or Civil Court", "Consumer Forum if registered housing"],
        "helplines": ["Legal Aid: 15100 (NALSA)", "Consumer: 1800-11-4000"],
        "sr": 68, "dur": "4–12 months", "risk": "Low"
    },
    "harassment": {
        "title": "Workplace Harassment (POSH)",
        "icon": "⚠️",
        "laws": ["POSH Act 2013", "IPC 354 (Outraging Modesty)", "IPC 354A (Sexual Harassment)", "IPC 509"],
        "rights": ["Safe working environment (mandatory)", "File with Internal Complaints Committee (ICC)", "Confidentiality guaranteed", "Right to compensation", "Protection from retaliation"],
        "steps": ["Document all incidents with dates/times", "File ICC complaint within 3 months", "If no ICC: approach District Officer", "File police complaint under IPC 354", "Approach State Women Commission"],
        "helplines": ["Women Helpline: 181", "NCW: 7827170170", "Police: 112"],
        "sr": 61, "dur": "2–6 months", "risk": "Medium"
    },
    "accident": {
        "title": "Road / Vehicle Accident",
        "icon": "🚗",
        "laws": ["Motor Vehicles Act 1988 Sec 166", "IPC 279 (Rash Driving)", "IPC 338 (Grievous Hurt)", "IPC 304A (Causing Death)"],
        "rights": ["Free first aid at any hospital", "MACT compensation claim", "Full insurance claim", "FIR filing right"],
        "steps": ["Call 112 immediately", "Preserve all medical bills", "File FIR at nearest police station", "Notify insurance within 48 hours", "File MACT claim petition"],
        "helplines": ["Emergency: 112", "Insurance Ombudsman: 155255"],
        "sr": 74, "dur": "6–18 months", "risk": "Low"
    },
    "consumer": {
        "title": "Consumer Rights Violation",
        "icon": "🛒",
        "laws": ["Consumer Protection Act 2019", "Sale of Goods Act 1930", "BIS Act 2016", "Legal Metrology Act 2009"],
        "rights": ["Right to Safety, Information, Choice", "Free complaint up to ₹50 lakh", "Right to Redressal & Education", "Compensation for mental agony"],
        "steps": ["Keep purchase receipt & warranty", "Send complaint to company first (30 days)", "File FREE at edaakhil.nic.in", "District Forum: up to ₹50 lakh", "State Commission: up to ₹2 crore"],
        "helplines": ["Consumer: 1800-11-4000 (Free)", "Portal: edaakhil.nic.in"],
        "sr": 71, "dur": "3–9 months", "risk": "Low"
    },
    "divorce": {
        "title": "Divorce / Family Dispute",
        "icon": "👨‍👩‍👧",
        "laws": ["Hindu Marriage Act 1955 Sec 13", "DV Act 2005", "Special Marriage Act 1954", "Muslim Personal Law"],
        "rights": ["Maintenance/alimony right", "Child custody right", "Share in marital property", "Protection from domestic violence"],
        "steps": ["Consult family lawyer or legal aid", "Mutual consent: 6 months process", "Contested: file in Family Court", "DV complaint: Magistrate Court directly", "Mediation recommended first"],
        "helplines": ["Women: 181", "Legal Aid: 15100", "Family Court: District Court"],
        "sr": 77, "dur": "6 months–3 years", "risk": "Medium"
    },
    "property": {
        "title": "Property / Land Dispute",
        "icon": "🏗️",
        "laws": ["Transfer of Property Act 1882", "Registration Act 1908", "Limitation Act 1963", "RERA 2016", "Specific Relief Act 1963"],
        "rights": ["Registered title deed right", "Peaceful possession right", "Contest fraudulent transfers", "RERA complaint for builder"],
        "steps": ["Get all documents verified by lawyer", "Check title at Sub-Registrar", "File civil suit for title declaration", "Apply for temporary injunction", "RERA complaint for builder issues"],
        "helplines": ["Legal Aid: 15100", "RERA: State portal", "Revenue: Contact Tehsildar"],
        "sr": 55, "dur": "1–5 years", "risk": "High"
    },
    "employment": {
        "title": "Employment / Labour Dispute",
        "icon": "💼",
        "laws": ["Industrial Disputes Act 1947", "Payment of Wages Act 1936", "Minimum Wages Act 1948", "Gratuity Act 1972", "EPF Act 1952"],
        "rights": ["Minimum wage right", "Gratuity after 5 years", "EPF contributions", "Challenge wrongful termination", "Safe working conditions"],
        "steps": ["Collect appointment letter, salary slips", "Send legal notice to employer", "File with Labour Commissioner", "Labour Court for reinstatement", "File EPF complaint at epfigms.gov.in"],
        "helplines": ["Labour: 14567", "EPF: 1800-118-005", "ESIC: 1800-11-2526"],
        "sr": 63, "dur": "6–24 months", "risk": "Medium"
    },
    "theft": {
        "title": "Theft / Robbery / Stolen Property",
        "icon": "🚨",
        "laws": ["IPC Section 378 – Theft", "IPC Section 379 – Punishment for Theft", "IPC Section 380 – Theft in Dwelling House", "IPC Section 382 – Theft after Preparation", "IPC Section 392 – Robbery", "IPC Section 401 – Habitual Thief"],
        "rights": ["Right to file FIR immediately", "Right to claim insurance if vehicle/property insured", "Right to police investigation and recovery", "Right to compensation from accused upon conviction"],
        "steps": ["Call 112 / 100 immediately to report", "File FIR at nearest police station as soon as possible", "Provide vehicle/property details: make, model, registration number, identifying marks", "Notify insurance company within 24 hours if insured", "Check CCTV footage in the area", "Track vehicle via GPS/smartwatch if available", "Keep FIR copy, insurance papers, purchase proof safe"],
        "helplines": ["Police: 112", "Emergency: 112", "Vehicle Tracking: VAHAN portal"],
        "sr": 65, "dur": "2–12 months", "risk": "Low"
    },
    "default": {
        "title": "General Legal Guidance",
        "icon": "⚖️",
        "laws": ["Constitution of India – Fundamental Rights Art 12-35", "IPC 1860", "CPC 1908", "Legal Services Authorities Act 1987"],
        "rights": ["Equality before law (Art 14)", "Right to legal representation", "Right to fair trial", "Free legal aid if income below threshold"],
        "steps": ["Call NALSA: 15100 for free legal aid", "Identify exact type of legal problem", "Approach nearest District Legal Aid Center", "Collect and preserve all evidence", "File complaint within limitation period"],
        "helplines": ["NALSA: 15100 (Free Legal Aid)", "Police: 112", "Women: 181"],
        "sr": 60, "dur": "Varies", "risk": "Medium"
    },
    "law_definition": {
        "title": "Understanding Law",
        "icon": "📚",
        "summary": "Law is a system of rules made or recognised by a legitimate authority to regulate behaviour, protect rights, resolve disputes, and provide remedies. In India, the Constitution is the highest law, followed by legislation, delegated rules, and judicial decisions.",
        "laws": ["The Constitution of India is the supreme law", "Acts are laws passed by Parliament or a State Legislature", "Rules and regulations explain how an Act is applied", "Courts interpret and enforce laws"],
        "rights": ["Everyone is equal before the law", "You can seek legal representation", "You can approach a court or legal-aid authority", "You should receive a fair hearing"],
        "steps": ["Identify the subject and jurisdiction", "Read the relevant Act and current rules", "Collect facts and supporting documents", "Get advice from a qualified lawyer or free legal-aid service"],
        "helplines": ["NALSA free legal aid: 15100"],
        "sr": 60, "dur": "Varies", "risk": "Medium"
    },
    "legal_case": {
        "title": "Legal Case Basics",
        "icon": "⚖️",
        "summary": "A legal case is a formal dispute or proceeding brought before a court or tribunal. The court examines facts, evidence, and applicable law before issuing an order or judgment.",
        "laws": ["Civil cases generally concern rights, money, property, or contracts", "Criminal cases concern offences investigated and prosecuted by the State", "The Constitution and procedural laws govern court remedies"],
        "rights": ["Notice of proceedings", "Opportunity to present evidence and arguments", "Legal representation", "Appeal or review where permitted by law"],
        "steps": ["Identify whether the matter is civil, criminal, family, consumer, or constitutional", "Preserve notices, contracts, messages, and other evidence", "Check limitation periods and the correct court", "Consult a lawyer or legal-aid service before filing"],
        "helplines": ["NALSA free legal aid: 15100", "Emergency: 112"],
        "sr": 60, "dur": "Varies", "risk": "Medium"
    }
}

LAWS_DB = {
    "IPC 1860": {"full": "Indian Penal Code, 1860", "desc": "Primary criminal law governing all offences including murder, theft, fraud, assault, defamation.", "sections": ["Sec 302–Murder", "Sec 420–Cheating", "Sec 376–Rape", "Sec 379–Theft", "Sec 354–Outraging Modesty"], "cat": "Criminal"},
    "IT Act 2000": {"full": "Information Technology Act, 2000", "desc": "Governs cyber crimes, hacking, online fraud, digital signatures, data protection.", "sections": ["Sec 66C–Identity Theft", "Sec 66D–Impersonation", "Sec 67–Obscene Material", "Sec 43–Damage to Computer"], "cat": "Cyber"},
    "Consumer Protection Act 2019": {"full": "Consumer Protection Act, 2019", "desc": "Protects consumer rights against defective goods, deficient services, unfair trade practices.", "sections": ["Sec 2(7)–Consumer", "Sec 35–District Forum", "Sec 47–State Commission", "Sec 58–National Commission"], "cat": "Consumer"},
    "POSH Act 2013": {"full": "Sexual Harassment of Women at Workplace Act, 2013", "desc": "Mandatory for all organizations with 10+ employees to prevent sexual harassment.", "sections": ["Sec 4–ICC", "Sec 6–Local Committee", "Sec 11–Inquiry", "Sec 13–Recommendations"], "cat": "Labour"},
    "RTI Act 2005": {"full": "Right to Information Act, 2005", "desc": "Every citizen can request information from any public authority. Fee: ₹10.", "sections": ["Sec 6–Application", "Sec 7–30 Day Limit", "Sec 8–Exemptions", "Sec 19–Appeal"], "cat": "Constitutional"},
    "DV Act 2005": {"full": "Protection of Women from Domestic Violence Act, 2005", "desc": "Civil and criminal remedies for women facing domestic violence.", "sections": ["Sec 12–Application", "Sec 17–Right to Home", "Sec 18–Protection Order", "Sec 20–Monetary Relief"], "cat": "Family"},
    "Motor Vehicles Act 1988": {"full": "Motor Vehicles Act, 1988", "desc": "Road accidents, traffic offences, insurance, MACT compensation.", "sections": ["Sec 140–No-fault liability", "Sec 166–Claim Application", "Sec 163A–Structured Formula"], "cat": "Motor"},
    "Hindu Marriage Act 1955": {"full": "Hindu Marriage Act, 1955", "desc": "Marriage, divorce, alimony for Hindus, Sikhs, Jains, Buddhists.", "sections": ["Sec 13–Divorce", "Sec 13B–Mutual Consent", "Sec 24–Interim Maintenance", "Sec 25–Permanent Alimony"], "cat": "Family"},
    "RERA 2016": {"full": "Real Estate (Regulation & Development) Act, 2016", "desc": "Regulates real estate, protects homebuyers from builder delays and fraud.", "sections": ["Sec 3–Registration", "Sec 12–False Info", "Sec 18–Return Amount", "Sec 31–Complaint"], "cat": "Property"},
    "Industrial Disputes Act 1947": {"full": "Industrial Disputes Act, 1947", "desc": "Labour disputes, wrongful termination, retrenchment, dispute resolution.", "sections": ["Sec 2A–Individual Disputes", "Sec 10–Reference to Tribunal", "Sec 25F–Retrenchment", "Sec 33C–Recovery"], "cat": "Labour"},
    "CrPC 1973": {"full": "Code of Criminal Procedure, 1973", "desc": "Procedure for FIR, arrest, bail, trial, sentencing in criminal cases.", "sections": ["Sec 154–FIR", "Sec 125–Maintenance", "Sec 436–Bail", "Sec 482–HC Powers"], "cat": "Criminal"},
    "Constitution of India": {"full": "Constitution of India (1950)", "desc": "Supreme law. Part III (Art 12–35) grants Fundamental Rights enforceable by courts.", "sections": ["Art 14–Equality", "Art 19–Freedom", "Art 21–Life & Liberty", "Art 32–Remedies"], "cat": "Constitutional"}
}

# ── NLP Problem Detection ────────────────────────
def detect_problem(text):
    t = text.lower()
    if any(phrase in t for phrase in ("what is law", "meaning of law", "define law", "law kya hai", "kanun kya hai")):
        return "law_definition"
    if any(phrase in t for phrase in ("what is a legal case", "what is legal case", "meaning of legal case", "legal case kya hai")):
        return "legal_case"
    kw = {
        "theft": ["chori","chor","stolen","steal","thief","robbery","snatch","lift","gayab","missing","lost","chura","चोरी","చోరి","ચોરી","hack","hawala"],
        "fraud": ["fraud","scam","cheat","cyber","online","phishing","hack","upi","debit","money stolen","account","otp","fake call"],
        "landlord": ["landlord","deposit","rent","eviction","tenant","flat","house","lease","pg","hostel","accommodation","makan","makan malik"],
        "harassment": ["harassment","harass","bully","abuse","workplace","office","boss","posh","sexual","molestation","hostile"],
        "accident": ["accident","crash","vehicle","car","bike","road","injury","hit","collision","mact","motor"],
        "consumer": ["product","refund","defective","warranty","purchase","company","service","amazon","flipkart","ecommerce","bought","saman"],
        "divorce": ["divorce","separation","custody","alimony","spouse","marriage","domestic violence","husband","wife","matrimonial","talaq"],
        "property": ["property","land","title","possession","builder","plot","registry","encroach","rera","construction","boundary","jagah","zameen"],
        "employment": ["salary","fired","terminated","job","employer","pf","gratuity","esic","increment","retrenchment","wage","dismissed","naukri"]
    }
    scores = {k: sum(1 for w in ws if w in t) for k, ws in kw.items()}
    best = max(scores,key=scores.get)
    return best if scores[best] > 0 else "default"

# ── Document Generators ──────────────────────────
def gen_fir(d):
    yr = datetime.now().strftime('%Y')
    dt = datetime.now().strftime('%d %B %Y')
    ts = datetime.now().strftime('%H:%M')
    crime_type = d.get('crime_type','[Offence]')
    station = d.get('station','[Police Station Name]')
    district = d.get('district','[District]')
    state = d.get('state','[State]')
    fir_no = f"{station[0:3].upper()}/{yr}/{district[0:3].upper()}/{(datetime.now().strftime('%j'))}"
    return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FIRST INFORMATION REPORT                           ║
║                    (Under Section 154, Code of Criminal Procedure, 1973)    ║
║                    JusticeLens AI · Legal Document Generator                ║
╚══════════════════════════════════════════════════════════════════════════════╝

FIR No. : {fir_no}
Date    : {dt}
Time    : {ts}

═══════════════════════════════════════════════════════════════════════════════
                     TO, THE STATION HOUSE OFFICER
═══════════════════════════════════════════════════════════════════════════════
Police Station : {station}
District       : {district}
State          : {state}

═══════════════════════════════════════════════════════════════════════════════
                          PARTICULARS OF COMPLAINANT
═══════════════════════════════════════════════════════════════════════════════

Name                 : {d.get('name','[Full Name]')}
Father's/Husband's   : {d.get('guardian','[Father/Husband Name]')}
Age                  : {d.get('age','[Age]')} Years
Occupation           : {d.get('occupation','[Occupation]')}
Nationality          : Indian
Residential Address  : {d.get('address','[Complete Address]')}
Mobile No.           : {d.get('phone','[Phone Number]')}
Email ID             : {d.get('email','[Email Address]')}
Identity Proof       : Aadhaar / Voter ID / Passport No. [__________]

═══════════════════════════════════════════════════════════════════════════════
                        PARTICULARS OF THE INCIDENT
═══════════════════════════════════════════════════════════════════════════════

Type of Offence     : {crime_type}
Date of Occurrence  : {d.get('date','[Date of Incident]')}
Time of Occurrence  : {d.get('time','[Time of Incident]')}
Place of Occurrence : {d.get('place','[Place/Location of Incident]')}
Police Station      : {station}
District            : {district}
State               : {state}

═══════════════════════════════════════════════════════════════════════════════
                         DETAILED DESCRIPTION OF FACTS
═══════════════════════════════════════════════════════════════════════════════

I, the undersigned, do hereby lodge this First Information Report and state
as follows:

1.  I am the complainant above-named and am competent to file this report.

2.  On the date and time mentioned above, at the place specified, the
    following incident occurred:

    {d.get('description','[Describe the incident in detail chronologically]')}

3.  The said act/incident constitutes the offence of {crime_type} and is
    punishable under the relevant provisions of law.

4.  The incident has been caused/committed by the following person(s)
    known/unknown to me:

    Name(s) & Description: {d.get('accused','[Name/Description of Accused]')}

═══════════════════════════════════════════════════════════════════════════════
                                LIST OF WITNESSES
═══════════════════════════════════════════════════════════════════════════════

The following persons have witnessed the incident and may be examined:

{d.get('witnesses','1. [Name, Address, Phone]\\n2. [Name, Address, Phone]')}

═══════════════════════════════════════════════════════════════════════════════
                          LIST OF EVIDENCE / DOCUMENTS
═══════════════════════════════════════════════════════════════════════════════

I am enclosing/producing the following documents as evidence:

{d.get('evidence','1. [Document Name & Description]\\n2. [Document Name & Description]\\n3. [Photographs/CCTV Footage etc.]')}

═══════════════════════════════════════════════════════════════════════════════
                          PROVISIONS OF LAW INVOKED
═══════════════════════════════════════════════════════════════════════════════

1.  Section 154, Code of Criminal Procedure, 1973 — First Information Report
2.  Section {d.get('section','[Relevant IPC/IT Act Section]')} — {crime_type}
3.  Other relevant provisions as applicable

═══════════════════════════════════════════════════════════════════════════════
                              RELIEF SOUGHT
═══════════════════════════════════════════════════════════════════════════════

{d.get('relief','1. Immediate investigation into the matter\\n2. Registration of FIR and legal action against accused\\n3. Recovery of the property/amount involved\\n4. Any other relief deemed fit')}

═══════════════════════════════════════════════════════════════════════════════
                               DECLARATION
═══════════════════════════════════════════════════════════════════════════════

I, {d.get('name','[Complainant Name]')}, do hereby solemnly declare that:

1.  All the facts stated above are true and correct to the best of my
    knowledge and belief.
2.  Nothing material has been concealed or suppressed.
3.  I understand that making a false complaint is punishable under law.
4.  I shall produce all relevant documents and witnesses as required during
    investigation.
5.  I shall cooperate with the investigating officer in the matter.

                                    ╔═══════════════════╗
                                    ║  LEFT THUMB       ║
                                    ║  IMPRESSION       ║
                                    ╚═══════════════════╝

Date  : {dt}
Place : {district}

                                        SIGNATURE OF COMPLAINANT
                                        _______________________________
                                        Name : {d.get('name','[Name]')}

═══════════════════════════════════════════════════════════════════════════════
                          OFFICE USE ONLY
═══════════════════════════════════════════════════════════════════════════════

FIR Registered vide No. : ____________
Date & Time of Entry    : ____________
Booked Under Sections   : ____________
Investigating Officer   : ____________
Remarks                 : ____________

═══════════════════════════════════════════════════════════════════════════════
DISCLAIMER: This is an AI-generated draft for reference purposes only.
Consult a qualified advocate before submission to the police station.
Generated by JusticeLens AI on {dt}
═══════════════════════════════════════════════════════════════════════════════"""

def gen_notice(d):
    return f"""{'='*60}
                    LEGAL NOTICE
     JusticeLens AI | {datetime.now().strftime('%d %B %Y')}
{'='*60}

FROM:
{d.get('sender_name','[Your Name]')}
{d.get('sender_address','[Your Address]')}
Phone: {d.get('sender_phone','')} | Email: {d.get('sender_email','')}

TO:
{d.get('recipient_name','[Recipient]')}
{d.get('recipient_address','[Recipient Address]')}

Date: {datetime.now().strftime('%d %B %Y')}

SUBJECT: Legal Notice – {d.get('subject','[Matter]')}

Under legal advice, I serve this LEGAL NOTICE:

FACTS:
{d.get('facts','[State all facts]')}

LEGAL BASIS: {d.get('law','[Applicable Law]')}

DEMAND:
{d.get('demand','[State demand clearly]')}

You are hereby required to comply within {d.get('days','15')} days of receipt.
Non-compliance will result in legal proceedings at your cost.

{d.get('sender_name','[Your Name]')}
{'='*60}
Send via: Registered Post + WhatsApp + Email
Keep delivery proof for court proceedings.
Generated by JusticeLens AI
{'='*60}"""

def gen_affidavit(d):
    return f"""{'='*60}
                    AFFIDAVIT
     JusticeLens AI | {datetime.now().strftime('%d %B %Y')}
{'='*60}

I, {d.get('name','[Name]')}, Age: {d.get('age','__')} years,
{d.get('occupation','[Occupation]')},
S/O D/O W/O: {d.get('guardian','[Guardian]')},
Residing at: {d.get('address','[Address]')},

do hereby solemnly affirm and declare on oath:

PURPOSE: {d.get('purpose','[Purpose]')}

STATEMENT:
{d.get('statement','[State all facts clearly]')}

I declare the above contents are true and correct.
Nothing material has been concealed.

Date: {datetime.now().strftime('%d %B %Y')}
Place: {d.get('city','[City]')}

Signature: _______________
Name: {d.get('name','[Name]')}

─────────────────────────────────────────────────────
VERIFICATION: Verified at {d.get('city','[City]')} on {datetime.now().strftime('%d %B %Y')}

SWORN before me:
Notary/Oath Commissioner: _______________
Registration No.: _______________
{'='*60}
Must be executed before a Notary. AI-generated template.
Generated by JusticeLens AI
{'='*60}"""

def gen_complaint(d):
    return f"""{'='*60}
           CONSUMER COMPLAINT
     Under Consumer Protection Act, 2019
     JusticeLens AI | {datetime.now().strftime('%d %B %Y')}
{'='*60}

TO: District Consumer Disputes Redressal Commission
    {d.get('district','[District]')}, {d.get('state','[State]')}

COMPLAINANT:
Name: {d.get('name','[Name]')}
Address: {d.get('address','[Address]')}
Phone: {d.get('phone','')} | Email: {d.get('email','')}

OPPOSITE PARTY:
{d.get('company','[Company/Seller]')}
{d.get('company_address','[Company Address]')}

COMPLAINT DETAILS:
Date of Purchase: {d.get('purchase_date','[Date]')}
Amount Paid: ₹{d.get('amount','[Amount]')}
Product/Service: {d.get('product','[Product]')}
Invoice No: {d.get('invoice','[Invoice]')}

FACTS:
{d.get('facts','[Describe defect/deficiency]')}

RELIEF SOUGHT:
{d.get('relief','[State demand: refund/replacement/compensation]')}

DOCUMENTS ENCLOSED:
{d.get('documents','1. Invoice/Receipt 2. Warranty 3. Correspondence')}

I declare the above is true and correct.
Date: {datetime.now().strftime('%d %B %Y')}

Signature: _______________
Name: {d.get('name','[Name]')}

{'='*60}
File FREE online at: edaakhil.nic.in
Helpline: 1800-11-4000
Generated by JusticeLens AI
{'='*60}"""

# ══════════════════════════════════════════════
#  API ROUTES
# ══════════════════════════════════════════════

@app.route("/")
def index():
    return jsonify({
        "name": "JusticeLens AI – RAG Legal Intelligence",
        "version": "3.0.0",
        "rag": f"{len(CHUNKS)} chunks, {len(CASES)} SC cases",
        "endpoints": ["/api/chat", "/api/stats", "/api/search", "/api/laws", "/api/websearch", "/api/download/fir", "/api/download/notice", "/api/download/affidavit", "/api/download/complaint", "/api/health"]
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "chunks": len(CHUNKS), "cases": len(CASES), "rag": "active"})

@app.route("/api/chat", methods=["POST"])
def chat():
    # Chat is available to guests; only authenticated users get persistent history.
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_jwt(token)
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    mode = data.get("mode", "rag")  # rag | web | both
    lang = data.get("lang", "en")   # en | hi | pa | ur | hx (hinglish)

    if not message:
        return jsonify({"error": "Message required"}), 400

    key = detect_problem(message)
    kb = KB.get(key, KB["default"])

    # ── RAG Retrieval from PDFs ──
    informational = key in ("law_definition", "legal_case")
    rag_chunks = [] if informational else rag_retrieve(message, top_k=5)
    rag_text = "" if informational else rag_answer(message, rag_chunks)

    # ── Web Search (if mode includes web) ──
    web_results = []
    if mode in ("web", "both"):
        web_results = web_search(message, num=4)

# ── Prediction ──
    # ── Similar Cases: filter by relevance to query instead of random ──
    query_words = set(message.lower().split())
    scored_cases = []
    for c in CASES:
        case_text = f"{c.get('case_type','')} {c.get('summary','')} {c.get('outcome','')} {c.get('year','')}".lower()
        relevance = sum(1 for w in query_words if w in case_text)
        scored_cases.append((relevance, c))
    scored_cases.sort(key=lambda x: x[0], reverse=True)
    top_scored = [] if informational else [c for score, c in scored_cases[:5] if score > 0]
    if not top_scored and not informational:
        # Fallback: match by detected problem category
        top_scored = [c for c in CASES if key.lower() in c.get("case_type","").lower() or key.lower() in c.get("summary","").lower()][:3]
    if not top_scored and not informational:
        top_scored = CASES[:3]

    # ── Gemini AI Answer (grounded on RAG + web results above, in selected language) ──
    gemini_answer = get_ai_summary(message, kb, rag_text, web_results, lang)

    # Save history only when the request belongs to a valid authenticated user.
    if user_id:
        chat_data = load_chats(user_id)
        chat_data["messages"].append({
            "id": len(chat_data["messages"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response_preview": gemini_answer[:100],
            "category": key,
            "mode": mode
        })
        save_chats(user_id, chat_data)
    
    return jsonify({
        "gemini_answer": gemini_answer,
        "detected_problem": key,
        "analysis": {
            "title": kb["title"],
            "icon": kb["icon"],
            "laws": kb["laws"],
            "rights": kb["rights"],
            "steps": kb["steps"],
            "helplines": kb["helplines"]
        },
        "prediction": {
            "success_rate": kb["sr"],
            "duration": kb["dur"],
            "risk_level": kb["risk"]
        },
        "rag_results": {
            "answer": rag_text,
            "source_chunks": rag_chunks[:3],
            "total_retrieved": len(rag_chunks)
        },
        "web_results": web_results,
        "similar_cases": [
            {"year": c.get("year"), "type": c.get("case_type"),
             "outcome": c.get("outcome"), "summary": (c.get("summary") or "")[:180]}
            for c in top_scored[:3]
        ],
        "meta": {
            "total_cases": len(CASES),
            "rag_chunks": len(CHUNKS),
            "informational": informational,
            "timestamp": datetime.now().isoformat()
        }
    })

@app.route("/api/ask-gemini", methods=["POST"])
def ask_gemini():
    """Standalone endpoint to sanity-check the Gemini API key/connection directly."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400
    try:
        answer = get_gemini_response(query)
        return jsonify({"query": query, "answer": answer})
    except Exception as e:
        return jsonify({"error": f"Gemini call failed: {str(e)}"}), 502

@app.route("/api/websearch")
def websearch():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "Query required"}), 400

    results = web_search(q, num=6)
    return jsonify({"results": results})

# ══════════════════════════════════════════════
#  MISSING API ROUTES (added for frontend compatibility)
# ══════════════════════════════════════════════

@app.route("/api/stats")
def stats():
    """Dashboard analytics: case types, outcomes, timeline"""
    case_types = Counter()
    outcomes = Counter()
    years_timeline = Counter()
    
    for c in CASES:
        ct = c.get("case_type", "Unknown")
        case_types[ct] += 1
        outcomes[c.get("outcome", "Unknown")] += 1
        yr = c.get("year")
        if yr:
            years_timeline[yr] += 1
    
    success_count = outcomes.get("Allowed", 0)
    total_decided = success_count + outcomes.get("Dismissed", 0) + outcomes.get("Partially Allowed", 0)
    success_rate = round(success_count / max(total_decided, 1) * 100, 1)
    
    return jsonify({
        "total_cases": len(CASES),
        "total_chunks": len(CHUNKS),
        "case_types": dict(case_types),
        "outcomes": dict(outcomes),
        "years_timeline": dict(years_timeline),
        "success_rate": success_rate
    })

@app.route("/api/search")
def search():
    """Search SC judgments with filters and pagination"""
    q = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    outcome = request.args.get("outcome", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    
    # Build a lookup dict for easy access by id
    cases_full_lookup = {}
    for cf in CASES_FULL:
        cases_full_lookup[cf.get("id")] = cf.get("full_text", "")
    
    results = []
    for c in CASES:
        # Apply filters
        if category and c.get("case_type", "") != category:
            continue
        if outcome and c.get("outcome", "") != outcome:
            continue
        if q:
            search_text = f"{c.get('case_type','')} {c.get('outcome','')} {c.get('summary','')} {c.get('filename','')} {c.get('year','')}".lower()
            if q not in search_text:
                continue
        cid = c.get("id", 0)
        results.append({
            "id": cid,
            "case_type": c.get("case_type"),
            "outcome": c.get("outcome"),
            "year": c.get("year"),
            "summary": (c.get("summary") or "")[:300],
            "filename": c.get("filename", ""),
            "full_text": (cases_full_lookup.get(cid) or "")[:500]
        })
    
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    page_results = results[start:end]
    
    return jsonify({
        "results": page_results,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, -(-total // per_page))
    })

@app.route("/api/case/<int:case_id>")
def case_detail(case_id):
    """Get full details of a single case"""
    # Build lookup from CASES_FULL (list of dicts)
    cases_full_lookup = {}
    for cf in CASES_FULL:
        cases_full_lookup[cf.get("id")] = cf.get("full_text", "")
    
    for c in CASES:
        if c.get("id") == case_id:
            cid = c.get("id")
            full_text = cases_full_lookup.get(cid, "")
            return jsonify({
                **c,
                "full_text": full_text[:2000],
                "filename": c.get("filename", "")
            })
    return jsonify({"error": "Case not found"}), 404

@app.route("/api/laws")
def laws():
    """Return the laws database"""
    return jsonify(LAWS_DB)

@app.route("/api/rag")
def rag():
    """Direct RAG vector search endpoint"""
    q = request.args.get("q", "")
    category = request.args.get("category", "")
    
    if not q:
        return jsonify({"error": "Query required"}), 400
    
    chunks = rag_retrieve(q, top_k=8, filter_type=category if category else None)
    answer = rag_answer(q, chunks)
    
    chunk_results = []
    for ch in chunks:
        chunk_results.append({
            "text": ch["text"],
            "source": ch["source"],
            "year": ch["year"],
            "case_type": ch["case_type"],
            "outcome": ch["outcome"],
            "score": ch["score"],
            "chunk_id": ch["chunk_id"]
        })
    
    return jsonify({
        "query": q,
        "answer": answer,
        "chunks": chunk_results,
        "total": len(chunk_results)
    })

# ── Document Download Routes ──────────────────

@app.route("/api/download/fir", methods=["POST"])
def download_fir():
    data = request.get_json() or {}
    text = gen_fir(data)
    return send_file(
        io.BytesIO(text.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"FIR_Draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

@app.route("/api/download/notice", methods=["POST"])
def download_notice():
    data = request.get_json() or {}
    text = gen_notice(data)
    return send_file(
        io.BytesIO(text.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"Legal_Notice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

@app.route("/api/download/affidavit", methods=["POST"])
def download_affidavit():
    data = request.get_json() or {}
    text = gen_affidavit(data)
    return send_file(
        io.BytesIO(text.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"Affidavit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

@app.route("/api/download/complaint", methods=["POST"])
def download_complaint():
    data = request.get_json() or {}
    text = gen_complaint(data)
    return send_file(
        io.BytesIO(text.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"Consumer_Complaint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )


if __name__ == "__main__":
    print("JusticeLens AI Backend Started")
    app.run(host="0.0.0.0", port=5000, debug=True)

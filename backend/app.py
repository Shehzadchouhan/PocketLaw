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

# ── Database & Document Engines ──────────────────
import database
import document_generator as dg
database.init_db()

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
    session = database.db_session()
    try:
        db_users = session.query(database.User).all()
        if db_users:
            return {
                u.email: {
                    "password": u.password_hash,
                    "name": u.name,
                    "created_at": u.created_at.isoformat() if u.created_at else "",
                    "user_id": u.user_id,
                    "bio": u.bio or "",
                    "avatar_url": u.avatar_url or "",
                    "role": u.role or "user"
                }
                for u in db_users
            }
    except Exception as e:
        pass
    finally:
        session.close()

    users = {}
    for path in (SEED_USERS_FILE, USERS_FILE):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                users.update(json.load(f))
    return users

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
    except Exception:
        pass

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
    
    existing = database.get_user_by_email(email)
    if existing:
        return jsonify({"error": "Email already registered"}), 409
    
    u_id = email.replace("@", "_").replace(".", "_")
    pw_hash = hash_password(password)
    user_dict = database.create_user(email=email, password_hash=pw_hash, name=name, user_id=u_id)
    token = create_jwt(u_id)
    
    return jsonify({
        "message": "Account created successfully",
        "token": token,
        "user": {"email": email, "name": name, "user_id": u_id}
    }), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user = database.get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not check_password(password, user.password_hash):
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = create_jwt(user.user_id)
    
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"email": email, "name": user.name, "user_id": user.user_id}
    })

@app.route("/api/auth/me")
@require_auth
def get_me(user_id):
    user = database.get_user_by_id(user_id)
    if user:
        return jsonify({"user": {"email": user.email, "name": user.name, "user_id": user.user_id}})
    return jsonify({"error": "User not found"}), 404

# ── Profile Routes ─────────────────────────────────
@app.route("/api/profile")
@require_auth
def get_profile(user_id):
    user = database.get_user_by_id(user_id)
    if user:
        profile = {
            "email": user.email,
            "name": user.name or "",
            "user_id": user.user_id,
            "bio": user.bio or "",
            "avatar_url": user.avatar_url or "",
            "role": user.role or "user"
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

    updated = database.update_user_profile(user_id, name=name, bio=bio, avatar_url=avatar_url)
    if updated:
        return jsonify({
            "message": "Profile updated",
            "profile": {
                "email": updated["email"],
                "name": updated["name"],
                "user_id": updated["user_id"],
                "bio": updated["bio"],
                "avatar_url": updated["avatar_url"]
            }
        })
    return jsonify({"error": "User not found"}), 404

@app.route("/api/auth/change-password", methods=["POST"])
@require_auth
def change_password(user_id):
    data = request.get_json() or {}
    old_pw = data.get("current_password", "").strip()
    new_pw = data.get("new_password", "").strip()

    if not old_pw or not new_pw:
        return jsonify({"error": "Current and new password are required"}), 400
    if len(new_pw) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400

    user = database.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password(old_pw, user.password_hash):
        return jsonify({"error": "Current password is incorrect"}), 401

    new_hash = hash_password(new_pw)
    database.update_user_profile(user_id, password_hash=new_hash)
    return jsonify({"message": "Password updated successfully"})

@app.route("/api/auth/logout", methods=["POST"])
@require_auth
def logout(user_id):
    return jsonify({"message": "Logged out successfully", "session_terminated": True})

# ── Chat History Routes ─────────────────────────
@app.route("/api/chats", methods=["GET"])
@require_auth
def get_chats(user_id):
    data = database.get_user_chats(user_id)
    return jsonify(data)

@app.route("/api/chats/save", methods=["POST"])
@require_auth
def save_chat(user_id):
    data = request.get_json() or {}
    msg = data.get("message", "")
    response = data.get("response", {})
    preview = response.get("gemini_answer", "")[:100] if response else ""
    cat = response.get("detected_problem", "") if response else ""
    mode = data.get("mode", "both")

    res = database.save_user_chat(user_id, msg, response_preview=preview, category=cat, mode=mode)
    return jsonify({"message": "Chat saved successfully", "count": res.get("count", 1)})

@app.route("/api/chats/clear", methods=["POST"])
@require_auth
def clear_chats(user_id):
    database.clear_user_chats(user_id)
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
        if sims[idx] < 0.05:
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
    confident = [c for c in chunks if c["score"] > 0.08]
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

# ── AI Answer Generator (Hybrid: Gemini if configured, else offline KB + RAG) ─────
def get_ai_summary(message, kb, rag_text, web_results, lang="en"):
    """
    Hybrid Legal Synthesizer:
    - If Gemini API is available, synthesizes natural legal guidance strictly grounded
      on retrieved Supreme Court chunks and Indian statutes (zero hallucination).
    - If offline / no API key, seamlessly builds an extractive structured answer
      from Knowledge Base + RAG context + Web sources.
    Supports multi-language: en, hi, pa, ur, hx (Hinglish).
    """
    lang_map = {
        "en": "English",
        "hi": "Hindi (Devanagari)",
        "pa": "Punjabi (Gurmukhi)",
        "ur": "Urdu (Perso-Arabic)",
        "hx": "Hinglish (natural Hindi+English mix)"
    }
    target_lang = lang_map.get(lang, "English")
    
    # ── Attempt Grounded Gemini Synthesis if configured ──
    if is_gemini_available():
        try:
            grounding_prompt = f"""You are PocketLaw AI, a professional Indian legal intelligence assistant.
A citizen has presented this legal problem:
"{message}"

Authoritative legal knowledge and Supreme Court context:
- Legal Domain / Issue: {kb.get('title', 'Legal Matter')}
- Applicable Statutes: {', '.join(kb.get('laws', []))}
- Citizen Legal Rights: {', '.join(kb.get('rights', []))}
- Immediate Steps to Take: {', '.join(kb.get('steps', []))}
- Official Helplines: {', '.join(kb.get('helplines', []))}
- Supreme Court Precedent Context:
{rag_text[:600] if rag_text and "No relevant" not in rag_text else "General Supreme Court principles on natural justice and statutory remedies apply."}

INSTRUCTIONS:
1. Provide a concise, professional executive legal assessment in {target_lang} (1-2 clear paragraphs).
2. Synthesize how Indian law, modern criminal codes (BNS 2023 / BNSS 2023 where applicable), and Supreme Court principles apply to this situation.
3. CRITICAL: DO NOT dump raw bulleted lists of laws, rights, steps, or helplines, because those exact bullet items are already rendered in dedicated interactive cards directly beneath your message. Focus purely on insightful legal analysis, judicial reasoning, and practical perspective.
4. End with: "*Review your matched statutory sections, constitutional rights, survival steps, and helplines organized in the cards below.*"
5. Do NOT hallucinate facts outside Indian law."""

            ai_output = get_gemini_response(grounding_prompt)
            if ai_output and len(ai_output.strip()) > 80:
                return ai_output.strip()
        except Exception:
            pass

    # ── Local Deterministic Fallback: Executive Analysis + SC Precedents (100% Offline) ──
    # Synthesizes an executive narrative and judicial context without repeating the
    # raw bullet points that are already rendered in the dedicated cards below.
    first_law = kb.get('laws', ['Indian statutory law'])[0]
    narratives = {
        'en': {
            'overview': f"Based on Indian statutory law and judicial precedents regarding **{kb.get('title', 'this legal matter')}**, established procedural remedies and legal safeguards are available under modern legislation.",
            'principles': f"The legal framework governing this issue balances statutory rights with procedural fairness. Key provisions under {first_law} provide the primary statutory framework for relief.",
            'rag_head': "📄 **From Supreme Court Judgment Database:**",
            'web_head': "🌐 **Related Public Resources:**",
            'pointer': "*Review your matched statutory sections, constitutional rights, survival steps, and helplines organized in the cards below.*"
        },
        'hi': {
            'overview': f"**{kb.get('title', 'इस कानूनी मामले')}** के संबंध में भारतीय कानूनों और अदालती फैसलों के अनुसार आपके पास वैधानिक अधिकार और प्रक्रियात्मक उपाय उपलब्ध हैं।",
            'principles': f"इस मामले में मुख्य राहत और कानूनी प्रक्रिया {first_law} के प्रावधानों द्वारा नियंत्रित होती है।",
            'rag_head': "📄 **सर्वोच्च न्यायालय के मुख्य निर्णय (Supreme Court Precedents):**",
            'web_head': "🌐 **संबंधित सार्वजनिक स्रोत:**",
            'pointer': "*लागू धाराएं, आपके अधिकार, जरूरी कदम और हेल्पलाइन नीचे दिए गए कार्ड्स में देखें।*"
        },
        'pa': {
            'overview': f"**{kb.get('title', 'ਇਸ ਕਾਨੂੰਨੀ ਮਾਮਲੇ')}** ਬਾਰੇ ਭਾਰਤੀ ਕਾਨੂੰਨਾਂ ਅਤੇ ਸੁਪਰੀਮ ਕੋਰਟ ਦੇ ਫੈਸਲਿਆਂ ਅਨੁਸਾਰ ਤੁਹਾਡੇ ਕੋਲ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ ਅਤੇ ਉਪਾਅ ਮੌਜੂਦ ਹਨ।",
            'principles': f"ਇਸ ਮਾਮਲੇ ਵਿੱਚ ਕਾਨੂੰਨੀ ਕਾਰਵਾਈ ਅਤੇ ਰਾਹਤ ਮੁੱਖ ਤੌਰ 'ਤੇ {first_law} ਦੇ ਉਪਬੰਧਾਂ ਅਧੀਨ ਆਉਂਦੀ ਹੈ।",
            'rag_head': "📄 **ਮੁੱਖ ਅਦਾਲਤੀ ਫੈਸਲੇ (Supreme Court Context):**",
            'web_head': "🌐 **ਸੰਬੰਧਿਤ ਸਰੋਤ:**",
            'pointer': "*ਲਾਗੂ ਧਾਰਾਵਾਂ, ਅਧਿਕਾਰ, ਕਦਮ ਅਤੇ ਹੈਲਪਲਾਈਨ ਹੇਠਾਂ ਦਿੱਤੇ ਕਾਰਡਾਂ ਵਿੱਚ ਦੇਖੋ।*"
        },
        'ur': {
            'overview': f"**{kb.get('title', 'اس قانونی معاملے')}** کے حوالے سے ہندوستانی قوانین اور سپریم کورٹ کے فیصلوں کے مطابق آپ کے پاس قانونی حقوق اور چارہ جوئی دستیاب ہے۔",
            'principles': f"اس ضمن میں بنیادی راحت اور قانونی کارروائی {first_law} کے تحت فراہم کی جاتی ہے۔",
            'rag_head': "📄 **اہم عدالتی نظائر (Supreme Court):**",
            'web_head': "🌐 **متعلقہ ذرائع:**",
            'pointer': "*متعلقہ دفعات، حقوق، اقدامات اور ہیلپ لائنز نیچے کارڈز میں دیکھیں۔*"
        },
        'hx': {
            'overview': f"**{kb.get('title', 'इस मामले')}** mein Indian statutory provisions aur court rulings ke mutabiq aapke paas legitimate legal rights aur procedural remedies available hain.",
            'principles': f"Is issue mein main relief aur legal procedure {first_law} ke under govern hota hai.",
            'rag_head': "📄 **Supreme Court Precedent Context:**",
            'web_head': "🌐 **Web Resources:**",
            'pointer': "*Applicable sections, rights, steps aur helplines niche cards mein dekhein.*"
        }
    }

    n = narratives.get(lang, narratives['en'])
    parts = [
        f"**{kb.get('icon', '⚖️')} {kb.get('title', 'Legal Guidance')}**\n\n{n['overview']}\n\n{n['principles']}"
    ]

    if rag_text and "No relevant" not in rag_text:
        parts.append(f"{n['rag_head']}\n{rag_text[:450].strip()}")

    if web_results:
        snippets = [r.get('snippet', '')[:180] for r in web_results[:2] if r.get('snippet')]
        if snippets:
            parts.append(f"{n['web_head']}\n" + "\n".join(f"• {s}" for s in snippets))

    parts.append(n['pointer'])
    return "\n\n".join(parts)

# ── Legal Knowledge Base (Cross-Mapped: BNS 2023 & IPC/CrPC) ─────────────────
KB = {
    "fraud": {
        "title": "Online Fraud / Cyber Crime",
        "icon": "🔐",
        "laws": [
            "BNS 2023 Sec 318(4) – Cheating & Fraud (ex-IPC 420)",
            "BNS 2023 Sec 316 – Criminal Breach of Trust (ex-IPC 406)",
            "IT Act 2000 – Sec 66C (Identity Theft / Phishing)",
            "IT Act 2000 – Sec 66D (Cheating by Impersonation using Computer)"
        ],
        "rights": ["Immediate Golden-Hour complaint at cybercrime.gov.in (Toll-Free 1930)", "Right to complete bank reversal of unauthorized transactions within 3 days", "Mandatory FIR registration under Section 173 BNSS (Zero FIR anywhere)", "Right to seek compensation under IT Act Adjudicating Officer"],
        "steps": ["Call 1930 immediately within 2 hours to freeze recipient financial trail", "Report incident on National Cybercrime Reporting Portal (cybercrime.gov.in)", "Visit Cyber Crime Police Station / Local PS to file Zero FIR", "Preserve transaction IDs, SMS alerts, UPI handles, and call recordings", "Submit written dispute letter to home bank branch with FIR acknowledgment copy"],
        "helplines": ["Cyber Crime Helpline: 1930", "Portal: cybercrime.gov.in", "RBI Ombudsman: 14448"],
        "sr": 62, "dur": "2–6 months", "risk": "Low–Medium"
    },
    "landlord": {
        "title": "Landlord / Tenant Rent Dispute",
        "icon": "🏠",
        "laws": [
            "Transfer of Property Act 1882 – Section 106 (Notice of Termination)",
            "State Rent Control Acts (Model Tenancy Act 2021)",
            "Consumer Protection Act 2019 (Applicable for registered property brokers / societies)",
            "BNS 2023 Sec 318 – Cheating (ex-IPC 420, if deposit fraudulently misappropriated)"
        ],
        "rights": ["Refund of entire security deposit upon peaceful handover of premises", "Mandatory 30-day written eviction notice requirement prior to eviction", "Protection against unlawful utility disconnection (water/electricity)", "Right to remain in possession until lawful order of Rent Controller / Civil Court"],
        "steps": ["Gather lease agreement, rent receipts, bank payment statements, and handover videos", "Serve formal Section 80 CPC style Legal Notice via Registered Speed Post granting 15 days", "Approach Rent Authority / Rent Tribunal under State Tenancy Act", "If commercial or broker dispute, file Consumer Complaint on edaakhil.nic.in"],
        "helplines": ["NALSA Free Legal Aid: 15100", "National Consumer Helpline: 1915 / 1800-11-4000"],
        "sr": 70, "dur": "3–9 months", "risk": "Low"
    },
    "harassment": {
        "title": "Workplace Harassment (POSH & Criminal Law)",
        "icon": "⚠️",
        "laws": [
            "Sexual Harassment of Women at Workplace (POSH) Act 2013",
            "BNS 2023 Sec 74 – Assault / Criminal Force to Outrage Modesty (ex-IPC 354)",
            "BNS 2023 Sec 75 – Sexual Harassment (ex-IPC 354A)",
            "BNS 2023 Sec 79 – Word, Gesture or Act Intended to Insult Modesty (ex-IPC 509)"
        ],
        "rights": ["Mandatory safe and harassment-free working environment in all establishments with 10+ employees", "Right to file formal complaint before Internal Complaints Committee (ICC) within 3 months", "Statutory guarantee of strict confidentiality during all inquiry proceedings", "Right to interim relief including 3 months paid leave or department transfer", "Protection against retaliatory termination, unfavorable reviews, or harassment"],
        "steps": ["Record contemporary notes with dates, exact spoken words, emails, and WhatsApp screenshots", "Submit written formal complaint to employer Internal Committee (ICC) or Local Committee", "If management fails to act within 90 days, file police complaint under BNS Sec 74/75", "Lodge complaint with National Commission for Women (NCW) portal or State Women Commission"],
        "helplines": ["Women Emergency Helpline: 181 / 112", "NCW 24/7 Helpline: 7827170170", "She-Box Portal: shebox.wcd.gov.in"],
        "sr": 65, "dur": "2–5 months", "risk": "Medium"
    },
    "accident": {
        "title": "Road / Motor Vehicle Accident Claim",
        "icon": "🚗",
        "laws": [
            "Motor Vehicles (Amendment) Act 2019 – Section 166 (Compensation Claim)",
            "BNS 2023 Sec 281 – Rash or Negligent Driving on Public Way (ex-IPC 279)",
            "BNS 2023 Sec 125 – Act Endangering Life or Personal Safety (ex-IPC 336/337)",
            "BNS 2023 Sec 106(1) – Causing Death by Negligence (ex-IPC 304A)"
        ],
        "rights": ["Immediate cashless emergency medical treatment at any hospital during Golden Hour", "Right to file claim before Motor Accident Claims Tribunal (MACT) without limitation period", "Interim compensation under No-Fault Liability clause", "Right to claim complete repair/loss from third-party insurance"],
        "steps": ["Dial 112 immediately for emergency medical help and police spot panchnama", "Photograph vehicles, skid marks, number plates, and driver license details", "Ensure police register FIR under Section 173 BNSS and prepare Detailed Accident Report (DAR)", "Notify insurer within 48 hours and preserve all hospital discharge summaries & bills", "File MACT Claim Petition through Legal Aid Advocate at District Court"],
        "helplines": ["National Emergency Number: 112", "Ambulance: 108", "Insurance Regulatory (IRDAI): 155255"],
        "sr": 76, "dur": "6–18 months", "risk": "Low"
    },
    "consumer": {
        "title": "Consumer Rights & Defective Goods/Services",
        "icon": "🛒",
        "laws": [
            "Consumer Protection Act 2019 – Section 35 (District Commission Jurisdiction)",
            "Consumer Protection Act 2019 – Section 2(10) [Defect] & Section 2(11) [Deficiency]",
            "Consumer Protection Act 2019 – Section 2(47) [Unfair Trade Practices]",
            "Consumer Protection (E-Commerce) Rules 2020"
        ],
        "rights": ["Right to safety, truthful information, choice, and consumer education", "Right to replacement, repair, or 100% refund with interest for defective goods", "Statutory compensation for mental agony, harassment, and litigation expenses", "Free online filing on National E-Daakhil portal without requiring a lawyer"],
        "steps": ["Preserve tax invoice, warranty card, product photographs, and error screenshots", "Issue formal Legal Notice / Email giving seller/company 15 days to resolve", "File complaint online at National Consumer Helpline (consumerhelpline.gov.in)", "File formal Consumer Complaint on edaakhil.nic.in before District Commission (up to ₹50 Lakhs)"],
        "helplines": ["National Consumer Helpline: 1915 / 1800-11-4000", "Online Portal: edaakhil.nic.in"],
        "sr": 74, "dur": "3–9 months", "risk": "Low"
    },
    "divorce": {
        "title": "Matrimonial & Family Dispute",
        "icon": "👨‍👩‍👧",
        "laws": [
            "Hindu Marriage Act 1955 – Section 13 (Contested) & 13B (Mutual Consent)",
            "Protection of Women from Domestic Violence Act 2005 (PWDVA)",
            "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 Sec 144 – Maintenance (ex-CrPC 125)",
            "Special Marriage Act 1954 / Guardians and Wards Act 1890"
        ],
        "rights": ["Right to interim and permanent maintenance/alimony for spouse and minor children", "Right to residence in shared household under Domestic Violence Act", "Right to custody / visitation rights prioritizing welfare of the minor child", "Right to return of complete Stridhan property"],
        "steps": ["Participate in pre-litigation family counselling or court mediation", "For mutual consent: joint petition under Section 13B (6 months cooling period can be waived)", "For domestic violence: direct application to Magistrate under DV Act Section 12", "For maintenance: petition under Section 144 BNSS / Section 24 HMA"],
        "helplines": ["Women Helpline: 181", "NALSA Legal Aid: 15100", "National Commission for Women: 7827170170"],
        "sr": 78, "dur": "6 months–2 years", "risk": "Medium"
    },
    "property": {
        "title": "Property, Land & Real Estate Dispute",
        "icon": "🏗️",
        "laws": [
            "Real Estate (Regulation and Development) Act 2016 (RERA) – Sec 18 (Refund & Interest)",
            "Transfer of Property Act 1882 – Section 54 (Sale) & Section 53A (Part Performance)",
            "Specific Relief Act 1963 – Injunction and Specific Performance",
            "BNS 2023 Sec 329 – Criminal Trespass (ex-IPC 441/447)"
        ],
        "rights": ["Statutory right to full refund with SBI MCLR + 2% interest for delayed builder possession under RERA", "Right to peaceful possession under registered conveyance deed", "Right to obtain temporary and permanent injunction against illegal trespass", "Right to inspect encumbrance certificate at Sub-Registrar Office"],
        "steps": ["Obtain complete chain of title documents and certified registry copy", "For builder delay: file online complaint before State RERA Authority", "For boundary / title dispute: file Civil Suit for Declaration and Injunction", "Apply for interim injunction under Order 39 Rules 1 & 2 CPC to prevent third-party creation"],
        "helplines": ["NALSA Free Legal Aid: 15100", "State RERA Web Portals", "Revenue Department / Tehsildar"],
        "sr": 58, "dur": "1–3 years", "risk": "High"
    },
    "employment": {
        "title": "Employment, Salary & Labour Rights",
        "icon": "💼",
        "laws": [
            "Payment of Wages Act 1936 & Code on Wages 2019",
            "Industrial Disputes Act 1947 – Section 25F (Retrenchment Compensation)",
            "Payment of Gratuity Act 1972 (Mandatory gratuity after 5 years continuous service)",
            "Employees' Provident Funds and Miscellaneous Provisions Act 1952"
        ],
        "rights": ["Right to full payment of earned salary by the 7th/10th of every calendar month", "Mandatory notice period salary or retrenchment compensation prior to termination", "Statutory entitlement to Gratuity, accumulated PF, and encashment of leaves", "Right to challenge arbitrary termination before Labour Conciliation Officer"],
        "steps": ["Preserve offer letter, employment contract, salary slips, and resignation/termination emails", "Send formal Demand Notice via Registered Post giving 15 days to clear dues", "File grievance on Ministry of Labour portal (samadhan.labour.gov.in)", "Lodge EPF evasion complaint on EPFiGMS portal (epfigms.gov.in)"],
        "helplines": ["Ministry of Labour Shram Suvidha: 14567", "EPFO Toll-Free: 1800-118-005", "ESIC: 1800-11-2526"],
        "sr": 66, "dur": "4–14 months", "risk": "Medium"
    },
    "theft": {
        "title": "Theft, Robbery & Stolen Property",
        "icon": "🚨",
        "laws": [
            "BNS 2023 Sec 303(2) – Punishment for Theft (ex-IPC 379)",
            "BNS 2023 Sec 305 – Theft in Dwelling House or Transport (ex-IPC 380)",
            "BNS 2023 Sec 309 – Robbery (ex-IPC 392)",
            "BNS 2023 Sec 317 – Receiving Stolen Property (ex-IPC 411)",
            "BNSS 2023 Sec 173 – Mandatory Registration of FIR / Zero FIR (ex-CrPC 154)"
        ],
        "rights": ["Right to have FIR registered immediately without delay (Zero FIR anywhere in India)", "Right to receive free certified copy of FIR under Section 173(2) BNSS", "Right to claim insurance indemnity upon police Untraced Report / Non-Recovery Certificate", "Right to apply for interim custody of recovered property (Superdari) under BNSS"],
        "steps": ["Call 112 immediately to record first response police call time", "Visit nearest police station and file written FIR draft with complete item identifiers (IMEI, chassis number, receipts)", "For mobile phones, block IMEI immediately on CEIR portal (ceir.gov.in)", "Inform insurance company in writing within 24–48 hours", "Collect signed FIR copy with GD Number from the Duty Officer"],
        "helplines": ["National Emergency: 112", "CEIR Mobile Block: ceir.gov.in", "VAHAN Portal: vahan.parivahan.gov.in"],
        "sr": 68, "dur": "2–8 months", "risk": "Low"
    },
    "gov_scheme": {
        "title": "Government Housing & Welfare Scheme (PMAY / Subsidies)",
        "icon": "🏛️",
        "laws": [
            "Pradhan Mantri Awas Yojana (PMAY-U 2.0 / PMAY-G) Operational Guidelines",
            "Constitution of India - Article 21 (Right to Shelter as a Fundamental Right)",
            "State Right to Public Services Act (Statutory Time-Bound Delivery of Public Services)",
            "Right to Information (RTI) Act 2005 - Section 6 (Mandatory Time-Bound Disclosure)"
        ],
        "rights": [
            "Statutory entitlement to timely verification and DBT installment release under PMAY mission directives",
            "Right to written inspection report and recorded reasons if any installment or subsidy is held up",
            "Right to file first and second appeals under State Right to Public Services Act for municipal delays",
            "Right to demand certified file movement records, geo-tagging notes, and subsidy status under RTI within 30 days"
        ],
        "steps": [
            "Track online application status on PMAY-MIS portal (pmaymis.gov.in) using your Application / Beneficiary ID",
            "Submit formal written grievance to the Executive Officer / Commissioner of the Municipal Committee with Inward Stamp",
            "Escalate complaint online to State Urban Development Department and Central CPGRAMS portal (pgportal.gov.in)",
            "File Form 'A' RTI application with Municipal Public Information Officer (PIO) demanding file movement sheet within 30 days"
        ],
        "helplines": [
            "PMAY Toll-Free Helpline: 1800-11-6163 / 1800-11-3377",
            "Central Public Grievance (CPGRAMS): pgportal.gov.in",
            "National RTI Portal: rtionline.gov.in"
        ],
        "sr": 75, "dur": "1-4 months", "risk": "Low"
    },
    "public_grievance": {
        "title": "Municipal Inaction, Public Grievance & RTI",
        "icon": "🏢",
        "laws": [
            "Right to Information (RTI) Act 2005 - Sections 6, 7 & 19 (Appeals against Public Authority)",
            "State Municipal Corporation & Municipal Committee Acts",
            "State Right to Public Services Act (Penalties on Defaulting Public Officials)",
            "Constitution of India - Article 226 (Writ of Mandamus against Inactive Authorities)"
        ],
        "rights": [
            "Right to time-bound public service delivery without arbitrary bureaucratic delays",
            "Right to obtain certified copies of government files, noting sheets, and official orders under RTI",
            "Right to seek statutory penalty against errant officials under Right to Service Act",
            "Right to file Writ Petition (Mandamus) before High Court to compel official duty"
        ],
        "steps": [
            "Always submit applications in duplicate and obtain stamped Inward Diary Number from the municipal office",
            "Lodge formal grievance on CPGRAMS (pgportal.gov.in) and State CM Window",
            "File formal RTI application with the Public Information Officer (PIO) seeking noting sheets and reasons for delay",
            "If public servant demands illegal gratification, lodge complaint with State Vigilance Bureau / Anti-Corruption Branch"
        ],
        "helplines": [
            "CPGRAMS Central Portal: pgportal.gov.in",
            "Citizen / Consumer Helpline: 1915",
            "Central Vigilance Commission: 1964"
        ],
        "sr": 70, "dur": "1–3 months", "risk": "Low"
    },
    "police_inaction": {
        "title": "Police Inaction, Refusal of FIR & Corruption",
        "icon": "🛡️",
        "laws": [
            "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 Sec 173(4) – Representation to SP/DCP",
            "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 Sec 175(3) – Magistrate Order to Register FIR (ex-CrPC 156(3))",
            "BNS 2023 Sec 198 – Public Servant Disobeying Law to Cause Injury (ex-IPC 166)",
            "Prevention of Corruption Act 1988 – Demand of Bribe / Undue Advantage"
        ],
        "rights": [
            "Mandatory registration of FIR for cognizable offences without preliminary enquiry (Lalita Kumari v. Govt of UP)",
            "Right to send written complaint to Superintendent of Police (SP) under Sec 173(4) BNSS",
            "Right to petition Judicial Magistrate under Sec 175(3) BNSS for court-ordered FIR",
            "Right to free copy of FIR immediately upon registration under Section 173(2) BNSS"
        ],
        "steps": [
            "Send written complaint copy via Registered Speed Post with postal receipt to Superintendent of Police (SP/DCP)",
            "If police still fail to act within 15 days, file application under Sec 175(3) BNSS before Judicial Magistrate",
            "For bribe or corruption demands, report immediately to State Anti-Corruption Bureau / Vigilance Bureau",
            "Approach State Human Rights Commission or Police Complaints Authority if subjected to harassment"
        ],
        "helplines": [
            "Police Emergency: 112",
            "Anti-Corruption / Vigilance Helpline: 1064",
            "National Human Rights Commission: 14433"
        ],
        "sr": 68, "dur": "1–6 months", "risk": "Medium"
    },
    "default": {
        "title": "General Legal Guidance",
        "icon": "⚖️",
        "laws": [
            "Constitution of India – Fundamental Rights (Articles 14, 19, 21)",
            "Bharatiya Nyaya Sanhita (BNS) 2023 – Modern Substantive Criminal Code",
            "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 – Modern Criminal Procedure",
            "Legal Services Authorities Act 1987 – Free Legal Aid for Citizens"
        ],
        "rights": ["Fundamental Right to Equality before Law and Equal Protection (Article 14)", "Right to Life and Personal Liberty with fair procedure (Article 21)", "Right to Free Legal Services under Section 12 of Legal Services Authorities Act", "Right to approach High Court (Article 226) or Supreme Court (Article 32)"],
        "steps": ["Call National Legal Services Authority (NALSA) toll-free on 15100", "Consult District Legal Services Authority (DLSA) at your District Court for a free empanelled advocate", "Gather and catalog all factual proof, agreements, and notices", "Check the statutory limitation period applicable to your remedy before filing"],
        "helplines": ["NALSA Free Legal Aid: 15100", "National Emergency: 112", "Women Helpline: 181"],
        "sr": 62, "dur": "Varies by Forum", "risk": "Medium"
    },
    "law_definition": {
        "title": "Understanding Indian Law & Hierarchy",
        "icon": "📚",
        "summary": "In India, the Constitution of India is the supreme Grundnorm. All parliamentary statutes (such as the BNS 2023, BNSS 2023, BSA 2023, and Civil Procedure Code) derive their validity from the Constitution. Judgments of the Supreme Court under Article 141 form binding law throughout India.",
        "laws": [
            "Constitution of India – Supreme Grundnorm of the Indian Republic",
            "Statutory Acts of Parliament (Central) & State Legislatures",
            "Delegated Legislation (Rules, Regulations, and Notifications)",
            "Judicial Precedents of the Supreme Court of India (Article 141)"
        ],
        "rights": ["Equality before the law without arbitrary discrimination", "Right to judicial review against unconstitutional laws (Article 13)", "Right to fair trial, impartial hearing, and reasoned orders", "Right to legal representation and legal aid"],
        "steps": ["Identify whether the issue is Constitutional, Civil, Criminal, or Regulatory", "Consult the latest enacted statutes (such as BNS 2023 rather than repealed codes)", "Review Supreme Court rulings on the exact legal proposition", "Seek professional guidance from a registered High Court / Supreme Court Advocate"],
        "helplines": ["NALSA Free Legal Aid: 15100"],
        "sr": 60, "dur": "Educational", "risk": "Low"
    },
    "legal_case": {
        "title": "Legal Case Dynamics & Procedure",
        "icon": "⚖️",
        "summary": "A legal case is a formal dispute presented before a competent judicial forum. Civil cases resolve property, contract, and monetary disputes on the balance of probabilities, whereas criminal cases are prosecuted by the State under the Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 beyond reasonable doubt.",
        "laws": [
            "Code of Civil Procedure, 1908 (CPC) – Regulates Civil Suits & Appeals",
            "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) – Regulates Criminal Procedure & Bail",
            "Bharatiya Sakshya Adhiniyam, 2023 (BSA) – Regulates Evidence & Digital Proof",
            "Limitation Act, 1963 – Prescribes strict time limits for instituting actions"
        ],
        "rights": ["Right to receiving complete copies of pleadings, chargesheets, and documents", "Right to cross-examine adverse witnesses", "Right to legal counsel of choice or court-appointed legal aid", "Right to appeal before Sessions Court, High Court, and Supreme Court"],
        "steps": ["Determine whether the cause of action is civil, criminal, consumer, or tribunal-bound", "Preserve all original evidence, contracts, financial receipts, and digital records", "Draft notice or plaint strictly within the prescribed limitation period", "Approach the appropriate court having pecuniary and territorial jurisdiction"],
        "helplines": ["NALSA Free Legal Aid: 15100", "National Emergency: 112"],
        "sr": 62, "dur": "Case Specific", "risk": "Medium"
    }
}

# ── Indian Laws Database (Modernized: BNS 2023, BNSS 2023, BSA 2023 & Key Acts) ───
LAWS_DB = {
    "BNS 2023": {
        "full": "Bharatiya Nyaya Sanhita, 2023 (Replaces IPC 1860)",
        "desc": "India's modern criminal code effective July 1, 2024. Modernizes criminal jurisprudence with community service punishments, strict terrorism and organized crime definitions, and streamlined offences.",
        "sections": [
            "Sec 103 – Murder (ex-IPC 302)",
            "Sec 318 – Cheating & Fraud (ex-IPC 420)",
            "Sec 303 – Theft (ex-IPC 379)",
            "Sec 74 – Outraging Modesty of Woman (ex-IPC 354)",
            "Sec 75 – Sexual Harassment (ex-IPC 354A)",
            "Sec 316 – Criminal Breach of Trust (ex-IPC 406)",
            "Sec 85/86 – Cruelty by Husband or Relatives (ex-IPC 498A)"
        ],
        "cat": "Criminal"
    },
    "BNSS 2023": {
        "full": "Bharatiya Nagarik Suraksha Sanhita, 2023 (Replaces CrPC 1973)",
        "desc": "India's modern procedural code governing criminal justice. Mandates electronic FIRs (Zero FIR), audio-video recording of search & seizure, strict forensic investigation timelines, and electronic summons.",
        "sections": [
            "Sec 173 – Information in Cognizable Cases & Zero FIR (ex-CrPC 154)",
            "Sec 35 – Notice of Appearance before Police (ex-CrPC 41A)",
            "Sec 144 – Maintenance for Wives, Children & Parents (ex-CrPC 125)",
            "Sec 482 – Direction for Grant of Bail / Anticipatory Bail (ex-CrPC 438)",
            "Sec 528 – Inherent Powers of High Court (ex-CrPC 482)"
        ],
        "cat": "Criminal"
    },
    "BSA 2023": {
        "full": "Bharatiya Sakshya Adhiniyam, 2023 (Replaces IEA 1872)",
        "desc": "Modernized Indian evidence law granting electronic and digital records (server logs, emails, smartphone messages, cloud files) primary evidence status on par with physical documents.",
        "sections": [
            "Sec 61 – Admissibility of Electronic Records in Court",
            "Sec 63 – Certificate for Electronic / Digital Evidence",
            "Sec 22 – Confessions and Admissions",
            "Sec 104 – Burden of Proof in Criminal Proceedings"
        ],
        "cat": "Criminal"
    },
    "IPC 1860": {
        "full": "Indian Penal Code, 1860 (Historic Code)",
        "desc": "Colonial-era criminal code governing offences committed prior to July 1, 2024. For all newer offences, the Bharatiya Nyaya Sanhita (BNS) 2023 applies.",
        "sections": ["Sec 302–Murder (BNS 103)", "Sec 420–Cheating (BNS 318)", "Sec 376–Rape (BNS 64)", "Sec 379–Theft (BNS 303)", "Sec 354–Outraging Modesty (BNS 74)"],
        "cat": "Criminal"
    },
    "IT Act 2000": {
        "full": "Information Technology Act, 2000 (Amended 2008)",
        "desc": "Governs cyber offenses, unauthorized computer access, electronic contracts, digital signatures, phishing, and online identity theft across India.",
        "sections": ["Sec 66C–Identity Theft & Phishing", "Sec 66D–Cheating by Impersonation", "Sec 67–Obscene Electronic Material", "Sec 43–Damage to Computer Systems & Data Compensation"],
        "cat": "Cyber"
    },
    "Consumer Protection Act 2019": {
        "full": "Consumer Protection Act, 2019",
        "desc": "Comprehensive modern law protecting consumer rights against defective goods, deficient services, misleading ads, and unfair trade practices with nationwide E-Daakhil filing.",
        "sections": ["Sec 2(7)–Definition of Consumer", "Sec 35–District Commission (up to ₹50L)", "Sec 47–State Commission (₹50L to ₹2Cr)", "Sec 58–National Commission (> ₹2Cr)", "Sec 84–Product Liability Action"],
        "cat": "Consumer"
    },
    "POSH Act 2013": {
        "full": "Sexual Harassment of Women at Workplace (Prevention, Prohibition & Redressal) Act, 2013",
        "desc": "Mandates every employer with 10+ employees to establish an Internal Complaints Committee (ICC) and enforce strict anti-harassment mechanisms.",
        "sections": ["Sec 4–Constitution of Internal Committee (ICC)", "Sec 9–Complaint of Sexual Harassment", "Sec 11–Inquiry into Complaint", "Sec 13–Inquiry Report & Recommendations"],
        "cat": "Labour"
    },
    "RTI Act 2005": {
        "full": "Right to Information Act, 2005",
        "desc": "Empowers Indian citizens to request official records, contracts, inspection reports, and information from any public authority within 30 days.",
        "sections": ["Sec 6–Request for Obtaining Information", "Sec 7–Disposal of Request within 30 Days", "Sec 8–Exemptions from Disclosure", "Sec 19–First and Second Appeals"],
        "cat": "Constitutional"
    },
    "DV Act 2005": {
        "full": "Protection of Women from Domestic Violence Act, 2005",
        "desc": "Comprehensive civil-criminal law providing protection orders, residence rights, monetary relief, and custody orders to aggrieved women in shared households.",
        "sections": ["Sec 12–Application to Magistrate", "Sec 17–Right to Reside in Shared Household", "Sec 18–Protection Orders against Violence", "Sec 20–Monetary Relief & Maintenance"],
        "cat": "Family"
    },
    "Motor Vehicles Act 1988": {
        "full": "Motor Vehicles Act, 1988 (Amended 2019)",
        "desc": "Regulates vehicular traffic, road safety, driver licensing, mandatory third-party insurance, and MACT tribunal compensation claims.",
        "sections": ["Sec 140–Liability without Fault in Accidents", "Sec 166–Application for Compensation before MACT", "Sec 161–Hit and Run Special Compensation Scheme"],
        "cat": "Motor"
    },
    "Hindu Marriage Act 1955": {
        "full": "Hindu Marriage Act, 1955",
        "desc": "Governs marriage, judicial separation, restitution of conjugal rights, divorce, alimony, and custody for Hindus, Sikhs, Jains, and Buddhists.",
        "sections": ["Sec 13–Grounds for Contested Divorce", "Sec 13B–Divorce by Mutual Consent", "Sec 24–Maintenance Pendente Lite (Interim)", "Sec 25–Permanent Alimony and Maintenance"],
        "cat": "Family"
    },
    "RERA 2016": {
        "full": "Real Estate (Regulation and Development) Act, 2016",
        "desc": "Protects real estate buyers from project delays, false advertisements, and structural defects. Mandates 70% funds escrow deposit for projects.",
        "sections": ["Sec 3–Mandatory Project Registration", "Sec 12–Obligations on Accuracy of Prospectus", "Sec 18–Return of Amount & Interest for Project Delay", "Sec 31–Filing Complaint before RERA Authority"],
        "cat": "Property"
    },
    "Industrial Disputes Act 1947": {
        "full": "Industrial Disputes Act, 1947",
        "desc": "Governs employment disputes, lay-offs, retrenchment, strikes, unfair labour practices, and dispute adjudication before Labour Tribunals.",
        "sections": ["Sec 2A–Dismissal Deemed Industrial Dispute", "Sec 10–Reference of Disputes to Boards/Tribunals", "Sec 25F–Conditions Precedent to Retrenchment", "Sec 33C–Recovery of Money Due from Employer"],
        "cat": "Labour"
    },
    "CrPC 1973": {
        "full": "Code of Criminal Procedure, 1973 (Historic Code)",
        "desc": "Historic procedural code governing criminal procedure for pre-July 2024 matters. Succeeded by Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023.",
        "sections": ["Sec 154–FIR (BNSS 173)", "Sec 125–Maintenance (BNSS 144)", "Sec 436–Bail in Bailable Offences", "Sec 482–Inherent Powers of High Court (BNSS 528)"],
        "cat": "Criminal"
    },
    "Constitution of India": {
        "full": "Constitution of India (1950)",
        "desc": "Supreme law of the Republic of India. Part III (Articles 12–35) guarantees Fundamental Rights enforceable through High Courts and the Supreme Court.",
        "sections": ["Art 14–Equality before Law", "Art 19–Protection of Fundamental Freedoms", "Art 21–Protection of Life & Personal Liberty", "Art 32–Remedies for Enforcement of Rights (Supreme Court)"],
        "cat": "Constitutional"
    }
}

# ── NLP Problem Detection (Boundary-Aware & Weighted Multi-Domain Classifier) ─
def detect_problem(text):
    t = text.lower()
    if any(phrase in t for phrase in ("what is law", "meaning of law", "define law", "law kya hai", "kanun kya hai")):
        return "law_definition"
    if any(phrase in t for phrase in ("what is a legal case", "what is legal case", "meaning of legal case", "legal case kya hai")):
        return "legal_case"

    kw = {
        "gov_scheme": [
            "pmay", "pm awas", "awas yojana", "pmay scheme", "housing scheme", "pm-kisan",
            "pm kisan", "ayushman", "ayushman bharat", "ration card", "ration", "subsidy",
            "second entry", "installment", "instalment", "kist", "govt scheme", "government scheme",
            "sarkari yojana", "yojana", "dbt", "pension", "old age pension", "widow pension",
            "scheme 2.0", "pmay 2.0", "scheme"
        ],
        "public_grievance": [
            "municipal committee", "municipal corporation", "muncipal comittee", "municipality",
            "nagar nigam", "nagar palika", "tehsildar", "sdm", "collector", "chandigarh office",
            "government office", "govt office", "red tape", "delay in service", "inaction",
            "not resolving", "public grievance", "cpgrams", "cm window", "right to service",
            "rti", "right to information"
        ],
        "police_inaction": [
            "police refusing", "refusing to register", "police not registering", "refusing fir",
            "police inaction", "fake fir", "bribe", "corruption", "vigilance", "lokayukta",
            "police harassment", "illegal detention"
        ],
        "theft": [
            "chori", "chor", "stolen", "steal", "thief", "robbery", "snatch", "lift",
            "gayab", "missing", "chura", "theft", "stolen bike", "stolen car", "stolen phone", "stolen property"
        ],
        "fraud": [
            "fraud", "scam", "cheat", "cyber", "phishing", "upi", "debit card",
            "credit card", "money stolen", "otp scam", "fake call", "online scam",
            "cyber crime", "cheating"
        ],
        "landlord": [
            "landlord", "security deposit", "deposit", "rent", "eviction",
            "tenant", "lease", "pg", "hostel", "makan malik", "rent control", "unlawful eviction"
        ],
        "harassment": [
            "workplace harassment", "office harassment", "harassment at work", "harass",
            "harassed", "posh", "icc", "internal complaints committee", "sexual harassment",
            "molestation", "outrage modesty", "eve teasing", "stalking", "unwanted touch",
            "sexual assault", "boss harassing"
        ],
        "accident": [
            "accident", "crash", "collision", "hit and run", "rash driving",
            "mact", "motor vehicle", "car accident", "bike accident", "road accident"
        ],
        "consumer": [
            "defective product", "refund", "warranty", "consumer court",
            "amazon", "flipkart", "defective", "deficiency in service",
            "ecommerce", "consumer complaint"
        ],
        "divorce": [
            "divorce", "child custody", "custody", "alimony", "maintenance",
            "domestic violence", "husband", "wife", "matrimonial", "stridhan",
            "talaq", "separation", "498a"
        ],
        "property": [
            "property", "land", "builder", "rera", "flat", "apartment", "possession",
            "encroachment", "registry", "title deed", "plot", "construction",
            "boundary", "trespass", "zameen", "jagah"
        ],
        "employment": [
            "salary", "wage", "fired", "terminated", "job", "employer",
            "pf", "gratuity", "retrenchment", "labour court", "naukri", "wrongful termination"
        ]
    }

    scores = {}
    for k, ws in kw.items():
        score = 0
        for w in ws:
            pattern = r'(?:\b|\A)' + re.escape(w) + r'(?:\b|\Z)'
            if re.search(pattern, t):
                weight = 5 if (' ' in w or w in ('pmay', 'posh', 'rera', 'mact', 'rti', 'dbt', 'cpgrams')) else 2
                score += weight
        scores[k] = score

    best = max(scores, key=scores.get)
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
    default_witnesses = "1. [Name, Address, Phone]\n2. [Name, Address, Phone]"
    default_evidence = "1. [Document Name & Description]\n2. [Document Name & Description]\n3. [Photographs/CCTV Footage etc.]"
    default_relief = "1. Immediate investigation into the matter\n2. Registration of FIR and legal action against accused\n3. Recovery of the property/amount involved\n4. Any other relief deemed fit"
    witnesses_val = d.get('witnesses', default_witnesses)
    evidence_val = d.get('evidence', default_evidence)
    relief_val = d.get('relief', default_relief)
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

{witnesses_val}

═══════════════════════════════════════════════════════════════════════════════
                          LIST OF EVIDENCE / DOCUMENTS
═══════════════════════════════════════════════════════════════════════════════

I am enclosing/producing the following documents as evidence:

{evidence_val}

═══════════════════════════════════════════════════════════════════════════════
                          PROVISIONS OF LAW INVOKED
═══════════════════════════════════════════════════════════════════════════════

1.  Section 154, Code of Criminal Procedure, 1973 — First Information Report
2.  Section {d.get('section','[Relevant IPC/IT Act Section]')} — {crime_type}
3.  Other relevant provisions as applicable

═══════════════════════════════════════════════════════════════════════════════
                              RELIEF SOUGHT
═══════════════════════════════════════════════════════════════════════════════

{relief_val}

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
    db_stats = database.get_database_stats()
    return jsonify({
        "status": "ok",
        "chunks": len(CHUNKS),
        "cases": len(CASES),
        "rag": "active",
        "database": db_stats.get("status", "connected"),
        "db_engine": db_stats.get("database_engine", "SQLite")
    })

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
        database.save_user_chat(
            user_id=user_id,
            message=message,
            response_preview=gemini_answer[:200],
            category=key,
            mode=mode
        )
    
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
        "success_rate": success_rate,
        "database": database.get_database_stats()
    })

@app.route("/api/db/stats")
def db_stats():
    """Return database engine status and operational record counts"""
    return jsonify(database.get_database_stats())

# ── Document Persistence Routes ───────────────
@app.route("/api/documents/save", methods=["POST"])
@require_auth
def save_user_document(user_id):
    data = request.get_json() or {}
    doc_type = data.get("doc_type", "fir")
    title = data.get("title", f"{doc_type.upper()} Draft")
    form_payload = data.get("form_payload", {})
    rendered_content = data.get("rendered_content", "")

    if not rendered_content:
        return jsonify({"error": "rendered_content is required"}), 400

    saved = database.save_document(user_id, doc_type, title, form_payload, rendered_content)
    return jsonify({"message": "Document saved successfully", "document": saved}), 201

@app.route("/api/documents", methods=["GET"])
@require_auth
def list_user_documents(user_id):
    doc_type = request.args.get("type")
    docs = database.get_user_documents(user_id, doc_type=doc_type)
    return jsonify({"documents": docs, "total": len(docs)})

@app.route("/api/documents/<doc_id>", methods=["DELETE"])
@require_auth
def delete_document(user_id, doc_id):
    ok = database.delete_user_document(user_id, doc_id)
    if ok:
        return jsonify({"message": "Document deleted successfully"})
    return jsonify({"error": "Document not found"}), 404

# ── Case Bookmarks Routes ─────────────────────
@app.route("/api/bookmarks", methods=["GET"])
@require_auth
def get_bookmarks(user_id):
    bookmarks = database.get_user_bookmarks(user_id)
    return jsonify({"bookmarks": bookmarks, "total": len(bookmarks)})

@app.route("/api/bookmarks", methods=["POST"])
@require_auth
def add_bookmark(user_id):
    data = request.get_json() or {}
    case_id = data.get("case_id")
    if case_id is None:
        return jsonify({"error": "case_id is required"}), 400

    bm = database.bookmark_case(
        user_id=user_id,
        case_id=int(case_id),
        case_type=data.get("case_type", ""),
        year=data.get("year", ""),
        summary=data.get("summary", ""),
        notes=data.get("notes", "")
    )
    return jsonify({"message": "Case bookmarked successfully", "bookmark": bm}), 201

@app.route("/api/bookmarks/<int:case_id>", methods=["DELETE"])
@require_auth
def remove_bookmark_route(user_id, case_id):
    ok = database.remove_bookmark(user_id, case_id)
    if ok:
        return jsonify({"message": "Bookmark removed"})
    return jsonify({"error": "Bookmark not found"}), 404

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

@app.route("/api/rag/eval")
def rag_eval():
    """
    Academic RAG Evaluation Suite
    Measures quantitative retrieval metrics across representative Indian law query domains:
    - Precision@3 & Precision@5
    - Mean Reciprocal Rank (MRR)
    - Query Latency (ms)
    - Vocabulary dimensionality & TF-IDF sparsity
    """
    test_suite = [
        {"q": "online upi cyber fraud unauthorized money debited from bank account", "cat": "Criminal", "kw": ["cyber", "fraud", "it act", "theft", "bank"]},
        {"q": "landlord refusing to refund security deposit after tenant vacated flat", "cat": "Civil", "kw": ["tenant", "rent", "landlord", "deposit", "property"]},
        {"q": "road accident victim motor vehicle claim rash driving compensation MACT", "cat": "Motor", "kw": ["accident", "motor", "mact", "vehicle", "injury"]},
        {"q": "defective mobile phone warranty refused consumer court complaint refund", "cat": "Consumer", "kw": ["consumer", "defective", "goods", "refund", "warranty"]},
        {"q": "workplace sexual harassment POSH ICC inquiry committee hostile environment", "cat": "Criminal", "kw": ["harassment", "posh", "woman", "workplace", "modesty"]},
        {"q": "builder delayed flat possession RERA refund with interest agreement breach", "cat": "Property", "kw": ["builder", "rera", "possession", "flat", "property"]},
        {"q": "stolen vehicle bike theft FIR registration police station", "cat": "Criminal", "kw": ["theft", "stolen", "fir", "vehicle", "police"]},
        {"q": "illegal termination from employment without notice or gratuity payment", "cat": "Labour", "kw": ["termination", "workman", "labour", "wages", "employment"]},
        {"q": "mutual consent divorce petition maintenance custody Hindu Marriage Act", "cat": "Family", "kw": ["divorce", "marriage", "custody", "maintenance", "alimony"]},
        {"q": "criminal breach of trust cheating contract dispute BNS 318 Section 420", "cat": "Criminal", "kw": ["cheating", "fraud", "breach", "trust", "contract"]}
    ]

    benchmark_results = []
    precisions_3 = []
    precisions_5 = []
    reciprocal_ranks = []
    latencies = []

    for t in test_suite:
        t0 = time.time()
        chunks = rag_retrieve(t["q"], top_k=5)
        elapsed_ms = round((time.time() - t0) * 1000, 2)
        latencies.append(elapsed_ms)

        target_cat = t["cat"].lower()
        target_kws = t["kw"]

        # Relevance matching
        matches = []
        for ch in chunks:
            text_lower = ch["text"].lower()
            ch_type = ch.get("case_type", "").lower()
            is_relevant = (ch_type == target_cat) or any(k in text_lower for k in target_kws)
            matches.append(is_relevant)

        p3 = sum(matches[:3]) / 3.0 if chunks else 0.0
        p5 = sum(matches[:5]) / 5.0 if chunks else 0.0
        precisions_3.append(p3)
        precisions_5.append(p5)

        rr = 0.0
        for rank_idx, m in enumerate(matches):
            if m:
                rr = 1.0 / (rank_idx + 1)
                break
        reciprocal_ranks.append(rr)

        top_score = chunks[0]["score"] if chunks else 0.0

        benchmark_results.append({
            "query": t["q"],
            "expected_category": t["cat"],
            "top_score": round(top_score, 4),
            "latency_ms": elapsed_ms,
            "precision_at_3": round(p3, 2),
            "precision_at_5": round(p5, 2),
            "reciprocal_rank": round(rr, 2),
            "top_source": chunks[0]["source"] if chunks else "N/A"
        })

    avg_p3 = round(sum(precisions_3) / len(precisions_3) * 100, 1)
    avg_p5 = round(sum(precisions_5) / len(precisions_5) * 100, 1)
    mrr = round(sum(reciprocal_ranks) / len(reciprocal_ranks), 3)
    avg_latency = round(sum(latencies) / len(latencies), 2)

    matrix_shape = TFIDF_MATRIX.shape
    sparsity = round((1.0 - (TFIDF_MATRIX.nnz / (matrix_shape[0] * matrix_shape[1]))) * 100, 2)

    return jsonify({
        "status": "success",
        "eval_timestamp": datetime.now().isoformat(),
        "summary": {
            "mean_precision_at_3": f"{avg_p3}%",
            "mean_precision_at_5": f"{avg_p5}%",
            "mean_reciprocal_rank_mrr": mrr,
            "average_latency_ms": avg_latency,
            "test_queries_count": len(test_suite),
            "index_chunks": len(CHUNKS),
            "total_features": len(VECTORIZER.get_feature_names_out()),
            "matrix_sparsity": f"{sparsity}%"
        },
        "benchmarks": benchmark_results
    })

# ── Document Download Routes ──────────────────

# ── Document Generation & Preview Routes ──────

@app.route("/api/documents/preview", methods=["POST"])
def preview_document():
    data = request.get_json() or {}
    doc_type = data.get("doc_type", "fir").lower()
    rendered_text, _ = dg.generate_document_pdf(doc_type, data)
    return jsonify({
        "doc_type": doc_type,
        "rendered_text": rendered_text,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/download/fir", methods=["POST"])
def download_fir():
    data = request.get_json() or {}
    text, pdf_stream = dg.generate_document_pdf("fir", data)
    
    # Save to user account if authenticated
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_jwt(token)
    if user_id:
        try:
            database.save_document(user_id, "fir", f"FIR Draft - {data.get('name', 'General')}", data, text)
        except Exception:
            pass

    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"FIR_Draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

@app.route("/api/download/notice", methods=["POST"])
def download_notice():
    data = request.get_json() or {}
    text, pdf_stream = dg.generate_document_pdf("notice", data)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_jwt(token)
    if user_id:
        try:
            database.save_document(user_id, "notice", f"Legal Notice - {data.get('subject', 'General')}", data, text)
        except Exception:
            pass

    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Legal_Notice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

@app.route("/api/download/affidavit", methods=["POST"])
def download_affidavit():
    data = request.get_json() or {}
    text, pdf_stream = dg.generate_document_pdf("affidavit", data)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_jwt(token)
    if user_id:
        try:
            database.save_document(user_id, "affidavit", f"Affidavit - {data.get('purpose', 'Sworn')}", data, text)
        except Exception:
            pass

    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Affidavit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

@app.route("/api/download/complaint", methods=["POST"])
def download_complaint():
    data = request.get_json() or {}
    text, pdf_stream = dg.generate_document_pdf("complaint", data)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_jwt(token)
    if user_id:
        try:
            database.save_document(user_id, "complaint", f"Consumer Complaint - {data.get('product', 'Defect')}", data, text)
        except Exception:
            pass

    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Consumer_Complaint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )


@app.route("/api/download/consultation", methods=["POST"])
def download_consultation():
    data = request.get_json() or {}
    pdf_stream = dg.generate_consultation_pdf(data)
    cat = (data.get("category") or "Consultation").replace(" ", "_")
    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Legal_Consultation_{cat}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"JusticeLens AI Backend Started on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)

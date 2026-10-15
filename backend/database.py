"""
PocketLaw - Relational Database Layer & ORM
Uses SQLite with SQLAlchemy ORM for robust ACID compliance, structured schemas,
and concurrency support. Automatically migrates legacy JSON files on startup.
"""

import os
import json
import logging
from datetime import datetime
import uuid

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Index, inspect, select, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship

logger = logging.getLogger("pocketlaw.database")
Base = declarative_base()

# ── Paths & Setup ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Select database path: persistent data directory, falling back to /tmp if read-only
PRIMARY_DB_PATH = os.path.join(DATA_DIR, "pocketlaw.db")
FALLBACK_DB_PATH = "/tmp/justicelens/pocketlaw.db"

def _resolve_db_uri():
    try:
        # Test if DATA_DIR is writable
        test_file = os.path.join(DATA_DIR, ".write_test")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        db_path = PRIMARY_DB_PATH
    except Exception:
        os.makedirs("/tmp/justicelens", exist_ok=True)
        db_path = FALLBACK_DB_PATH

    # For Windows SQLite paths, ensure 4 slashes or normalized path
    norm_path = os.path.abspath(db_path).replace("\\", "/")
    return f"sqlite:///{norm_path}", db_path

DATABASE_URI, DB_FILE_PATH = _resolve_db_uri()

# Create SQLAlchemy engine with connection pool & SQLite settings
engine = create_engine(
    DATABASE_URI,
    connect_args={"check_same_thread": False, "timeout": 30},
    pool_pre_ping=True
)

# Enable WAL (Write-Ahead Logging) mode and foreign keys for SQLite
from sqlalchemy import event
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
    except Exception as e:
        logger.warning(f"Could not set SQLite PRAGMA: {e}")
    finally:
        cursor.close()

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionFactory)


# ── Database Models ───────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(120), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(150), default="")
    avatar_url = Column(Text, default="")
    bio = Column(Text, default="")
    role = Column(String(30), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("SavedDocument", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("CaseBookmark", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url or "",
            "bio": self.bio or "",
            "role": self.role or "user",
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(120), unique=True, nullable=False, index=True)
    user_id = Column(String(120), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="New Legal Consultation")
    category = Column(String(100), default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.timestamp")

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "title": self.title,
            "category": self.category,
            "message_count": len(self.messages),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(120), ForeignKey("chat_sessions.session_id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(String(120), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), default="user")  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    response_preview = Column(Text, default="")
    category = Column(String(100), default="general")
    mode = Column(String(50), default="both")
    meta_json = Column(Text, default="{}")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="messages")
    session = relationship("ChatSession", back_populates="messages")

    def to_dict(self):
        meta = {}
        try:
            if self.meta_json:
                meta = json.loads(self.meta_json)
        except Exception:
            pass
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "role": self.role,
            "message": self.message,
            "response_preview": self.response_preview or "",
            "category": self.category or "general",
            "mode": self.mode or "both",
            "meta": meta,
            "timestamp": self.timestamp.isoformat() if self.timestamp else datetime.utcnow().isoformat()
        }


class SavedDocument(Base):
    __tablename__ = "saved_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(String(120), unique=True, nullable=False, index=True)
    user_id = Column(String(120), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    doc_type = Column(String(50), nullable=False, index=True)  # 'fir', 'notice', 'affidavit', 'complaint'
    title = Column(String(255), nullable=False)
    form_payload = Column(Text, default="{}")
    rendered_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="documents")

    def to_dict(self):
        payload = {}
        try:
            if self.form_payload:
                payload = json.loads(self.form_payload)
        except Exception:
            pass
        return {
            "id": self.id,
            "doc_id": self.doc_id,
            "user_id": self.user_id,
            "doc_type": self.doc_type,
            "title": self.title,
            "form_payload": payload,
            "rendered_content": self.rendered_content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class CaseBookmark(Base):
    __tablename__ = "case_bookmarks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(120), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    case_id = Column(Integer, nullable=False, index=True)
    case_type = Column(String(100), default="")
    year = Column(String(20), default="")
    summary = Column(Text, default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "case_id": self.case_id,
            "case_type": self.case_type,
            "year": self.year,
            "summary": self.summary,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ── Initialization & Auto-Migration ──────────────────────────────────────────

def init_db():
    """Initializes database tables and executes automatic migration from legacy JSON."""
    Base.metadata.create_all(bind=engine)
    migrate_legacy_data()

def migrate_legacy_data():
    """Seamlessly migrates users.json and chats/*.json into SQLite."""
    session = db_session()
    try:
        # 1. Migrate Users
        seed_users_file = os.path.join(DATA_DIR, "users.json")
        runtime_users_file = "/tmp/justicelens/users.json"

        user_map = {}
        for path in (seed_users_file, runtime_users_file):
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            user_map.update(data)
                except Exception as e:
                    logger.warning(f"Error reading user file {path}: {e}")

        for email, u in user_map.items():
            clean_email = email.strip().lower()
            u_id = u.get("user_id") or clean_email.replace("@", "_").replace(".", "_")
            existing = session.query(User).filter((User.email == clean_email) | (User.user_id == u_id)).first()
            if not existing:
                created_dt = datetime.utcnow()
                if u.get("created_at"):
                    try:
                        created_dt = datetime.fromisoformat(u["created_at"])
                    except Exception:
                        pass
                new_user = User(
                    user_id=u_id,
                    email=clean_email,
                    password_hash=u.get("password", ""),
                    name=u.get("name") or clean_email.split("@")[0],
                    bio=u.get("bio", ""),
                    avatar_url=u.get("avatar_url", ""),
                    role="user",
                    created_at=created_dt
                )
                session.add(new_user)
        session.commit()

        # 2. Migrate Chats
        chats_dirs = [
            os.path.join(DATA_DIR, "chats"),
            "/tmp/justicelens/chats"
        ]
        for cdir in chats_dirs:
            if not os.path.exists(cdir):
                continue
            for fname in os.listdir(cdir):
                if not fname.endswith(".json"):
                    continue
                user_id = fname[:-5]  # strip .json
                # Check user exists
                user_obj = session.query(User).filter_by(user_id=user_id).first()
                if not user_obj:
                    continue

                filepath = os.path.join(cdir, fname)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        chat_content = json.load(f)
                        msgs = chat_content.get("messages", [])
                        
                        # Check existing messages count for this user
                        existing_count = session.query(func.count(ChatMessage.id)).filter_by(user_id=user_id).scalar()
                        if existing_count == 0 and msgs:
                            # Create a default session
                            sess_id = f"sess_{user_id}_default"
                            default_sess = session.query(ChatSession).filter_by(session_id=sess_id).first()
                            if not default_sess:
                                default_sess = ChatSession(
                                    session_id=sess_id,
                                    user_id=user_id,
                                    title="Consultations History",
                                    category="general"
                                )
                                session.add(default_sess)
                                session.flush()

                            for m in msgs:
                                msg_dt = datetime.utcnow()
                                if m.get("timestamp"):
                                    try:
                                        msg_dt = datetime.fromisoformat(m["timestamp"])
                                    except Exception:
                                        pass
                                new_msg = ChatMessage(
                                    session_id=sess_id,
                                    user_id=user_id,
                                    role="user",
                                    message=m.get("message", ""),
                                    response_preview=m.get("response_preview", ""),
                                    category=m.get("category", "general"),
                                    mode=m.get("mode", "both"),
                                    timestamp=msg_dt
                                )
                                session.add(new_msg)
                            session.commit()
                except Exception as e:
                    logger.warning(f"Error migrating chat file {filepath}: {e}")
                    session.rollback()

    except Exception as e:
        logger.error(f"Migration error: {e}")
        session.rollback()
    finally:
        session.close()


# ── High-Level Service Methods ────────────────────────────────────────────────

def get_user_by_email(email):
    session = db_session()
    try:
        return session.query(User).filter_by(email=email.strip().lower()).first()
    finally:
        session.close()

def get_user_by_id(user_id):
    session = db_session()
    try:
        return session.query(User).filter_by(user_id=user_id).first()
    finally:
        session.close()

def create_user(email, password_hash, name="", user_id=None):
    clean_email = email.strip().lower()
    u_id = user_id or clean_email.replace("@", "_").replace(".", "_")
    session = db_session()
    try:
        user = User(
            user_id=u_id,
            email=clean_email,
            password_hash=password_hash,
            name=name or clean_email.split("@")[0],
            created_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        return user.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_user_profile(user_id, name=None, bio=None, avatar_url=None, password_hash=None):
    session = db_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return None
        if name is not None:
            user.name = name
        if bio is not None:
            user.bio = bio
        if avatar_url is not None:
            user.avatar_url = avatar_url
        if password_hash is not None:
            user.password_hash = password_hash
        user.updated_at = datetime.utcnow()
        session.commit()
        return user.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_chats(user_id):
    session = db_session()
    try:
        messages = (
            session.query(ChatMessage)
            .filter_by(user_id=user_id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )
        sessions = (
            session.query(ChatSession)
            .filter_by(user_id=user_id)
            .order_by(ChatSession.updated_at.desc())
            .all()
        )
        return {
            "messages": [m.to_dict() for m in messages],
            "sessions": [s.to_dict() for s in sessions]
        }
    finally:
        session.close()

def save_user_chat(user_id, message, response_preview="", category="general", mode="both", meta=None):
    session = db_session()
    try:
        # Check or create default session
        default_sess = session.query(ChatSession).filter_by(user_id=user_id).order_by(ChatSession.updated_at.desc()).first()
        if not default_sess:
            sess_id = f"sess_{user_id}_{int(datetime.utcnow().timestamp())}"
            default_sess = ChatSession(
                session_id=sess_id,
                user_id=user_id,
                title=message[:40] if message else "Legal Consultation",
                category=category
            )
            session.add(default_sess)
            session.flush()

        msg = ChatMessage(
            session_id=default_sess.session_id,
            user_id=user_id,
            role="user",
            message=message,
            response_preview=response_preview[:300] if response_preview else "",
            category=category,
            mode=mode,
            meta_json=json.dumps(meta or {}),
            timestamp=datetime.utcnow()
        )
        session.add(msg)
        default_sess.updated_at = datetime.utcnow()
        session.commit()

        total = session.query(func.count(ChatMessage.id)).filter_by(user_id=user_id).scalar()
        return {"id": msg.id, "count": total}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def clear_user_chats(user_id):
    session = db_session()
    try:
        session.query(ChatMessage).filter_by(user_id=user_id).delete()
        session.query(ChatSession).filter_by(user_id=user_id).delete()
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_document(user_id, doc_type, title, form_payload, rendered_content):
    session = db_session()
    try:
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        doc = SavedDocument(
            doc_id=doc_id,
            user_id=user_id,
            doc_type=doc_type,
            title=title or f"{doc_type.upper()} Draft",
            form_payload=json.dumps(form_payload) if isinstance(form_payload, dict) else str(form_payload),
            rendered_content=rendered_content,
            created_at=datetime.utcnow()
        )
        session.add(doc)
        session.commit()
        return doc.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_documents(user_id, doc_type=None):
    session = db_session()
    try:
        q = session.query(SavedDocument).filter_by(user_id=user_id)
        if doc_type:
            q = q.filter_by(doc_type=doc_type)
        docs = q.order_by(SavedDocument.created_at.desc()).all()
        return [d.to_dict() for d in docs]
    finally:
        session.close()

def delete_user_document(user_id, doc_id):
    session = db_session()
    try:
        doc = session.query(SavedDocument).filter_by(user_id=user_id, doc_id=doc_id).first()
        if not doc:
            return False
        session.delete(doc)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def bookmark_case(user_id, case_id, case_type="", year="", summary="", notes=""):
    session = db_session()
    try:
        existing = session.query(CaseBookmark).filter_by(user_id=user_id, case_id=case_id).first()
        if existing:
            existing.notes = notes or existing.notes
            session.commit()
            return existing.to_dict()
        bm = CaseBookmark(
            user_id=user_id,
            case_id=case_id,
            case_type=case_type,
            year=str(year),
            summary=summary[:400] if summary else "",
            notes=notes or "",
            created_at=datetime.utcnow()
        )
        session.add(bm)
        session.commit()
        return bm.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_bookmarks(user_id):
    session = db_session()
    try:
        bms = session.query(CaseBookmark).filter_by(user_id=user_id).order_by(CaseBookmark.created_at.desc()).all()
        return [b.to_dict() for b in bms]
    finally:
        session.close()

def remove_bookmark(user_id, case_id):
    session = db_session()
    try:
        bm = session.query(CaseBookmark).filter_by(user_id=user_id, case_id=case_id).first()
        if not bm:
            return False
        session.delete(bm)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_database_stats():
    session = db_session()
    try:
        user_count = session.query(func.count(User.id)).scalar() or 0
        message_count = session.query(func.count(ChatMessage.id)).scalar() or 0
        doc_count = session.query(func.count(SavedDocument.id)).scalar() or 0
        bm_count = session.query(func.count(CaseBookmark.id)).scalar() or 0
        return {
            "database_engine": "SQLite (WAL mode)",
            "db_path": DB_FILE_PATH,
            "total_users": user_count,
            "total_messages": message_count,
            "total_documents": doc_count,
            "total_bookmarks": bm_count,
            "status": "connected"
        }
    finally:
        session.close()

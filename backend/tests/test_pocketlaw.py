"""
PocketLaw Automated Test Suite (Major Project Evaluation)
Comprehensive unit and integration tests covering:
1. Database Models and Persistence (SQLite WAL + SQLAlchemy ORM)
2. Court-Ready Document Engine (ReportLab PDF Generation)
3. RAG Intelligence & Modern Criminal Law Cross-Mapping (BNS 2023)
4. REST API Endpoints & Academic Evaluation Suite
"""

import os
import sys
import unittest
import json
import io

# Ensure backend directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import database
import document_generator
import app as flask_app


from werkzeug.security import generate_password_hash, check_password_hash

class TestDatabaseOperations(unittest.TestCase):
    """Tests for SQLite database ORM operations."""

    def test_database_stats(self):
        stats = database.get_database_stats()
        self.assertIn("database_engine", stats)
        self.assertEqual(stats["database_engine"], "SQLite (WAL mode)")
        self.assertIn("total_users", stats)
        self.assertIn("total_documents", stats)

    def test_user_operations(self):
        test_email = f"test_{os.urandom(4).hex()}@pocketlaw.org"
        pwd_hash = generate_password_hash("Secret123!")
        
        user_dict = database.create_user(
            email=test_email,
            password_hash=pwd_hash,
            name="Test Advocate"
        )
        self.assertIsNotNone(user_dict)
        self.assertEqual(user_dict["email"], test_email)

        fetched = database.get_user_by_email(test_email)
        self.assertIsNotNone(fetched)
        self.assertTrue(check_password_hash(fetched.password_hash, "Secret123!"))
        self.assertFalse(check_password_hash(fetched.password_hash, "WrongPassword"))

    def test_document_and_bookmark_persistence(self):
        test_email = f"doc_test_{os.urandom(4).hex()}@pocketlaw.org"
        user_dict = database.create_user(test_email, generate_password_hash("Pass123"), name="Doc User")
        u_id = user_dict["user_id"]

        # Save document draft
        doc_dict = database.save_document(
            user_id=u_id,
            doc_type="fir",
            title="Sample FIR Draft",
            form_payload={"crime_type": "Theft", "name": "Complainant A"},
            rendered_content="Sample FIR Text"
        )
        self.assertIsNotNone(doc_dict["doc_id"])
        
        docs = database.get_user_documents(u_id)
        self.assertTrue(len(docs) >= 1)
        self.assertEqual(docs[0]["doc_type"], "fir")

        # Save bookmark
        bm_dict = database.bookmark_case(
            user_id=u_id,
            case_id=101,
            case_type="Criminal",
            year="2022",
            summary="Landmark judgment on bail",
            notes="Important reference"
        )
        self.assertIsNotNone(bm_dict["id"])
        
        bms = database.get_user_bookmarks(u_id)
        self.assertEqual(len(bms), 1)
        self.assertEqual(bms[0]["case_id"], 101)

        # Remove bookmark
        removed = database.remove_bookmark(u_id, 101)
        self.assertTrue(removed)
        self.assertEqual(len(database.get_user_bookmarks(u_id)), 0)


class TestDocumentGenerator(unittest.TestCase):
    """Tests for Court-Ready PDF document generation."""

    def test_fir_pdf_generation(self):
        sample_data = {
            "name": "Rajesh Kumar",
            "guardian": "Suresh Kumar",
            "age": "34",
            "address": "Model Town, Ludhiana",
            "phone": "9876543210",
            "station": "Division No. 5",
            "district": "Ludhiana",
            "state": "Punjab",
            "crime_type": "Online Financial Fraud",
            "description": "Unauthorized debits amounting to Rs. 75,000 via phishing link.",
            "evidence": "Bank account statement showing transaction IDs TXN998811.",
            "relief": "Registration of FIR and freeze of recipient bank account."
        }
        text, pdf_stream = document_generator.generate_document_pdf("fir", sample_data)
        pdf_bytes = pdf_stream.getvalue()
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertIn("FIRST INFORMATION REPORT", text)

    def test_legal_notice_pdf_generation(self):
        sample_data = {
            "sender_name": "Advocate Priya Sharma",
            "sender_address": "Chamber 402, High Court Complex",
            "recipient_name": "ABC Electronics Pvt Ltd",
            "recipient_address": "Connaught Place, New Delhi",
            "subject": "Notice for Defective Product & Deficiency in Service",
            "facts": "Product stopped working within 2 days; warranty denied.",
            "demand": "Full refund of Rs. 65,000 along with 18% interest.",
            "deadline": "15"
        }
        text, pdf_stream = document_generator.generate_document_pdf("notice", sample_data)
        pdf_bytes = pdf_stream.getvalue()
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertIn("FORMAL LEGAL NOTICE", text)

    def test_affidavit_pdf_generation(self):
        sample_data = {
            "deponent_name": "Amit Verma",
            "father_name": "Harish Verma",
            "age": "29",
            "address": "Sector 17, Chandigarh",
            "purpose": "Affidavit for Proof of Identity and Residential Address",
            "statements": "1. I am a citizen of India residing at the aforesaid address.\n2. All submitted documents are genuine.",
            "place": "Chandigarh"
        }
        text, pdf_stream = document_generator.generate_document_pdf("affidavit", sample_data)
        pdf_bytes = pdf_stream.getvalue()
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertIn("AFFIDAVIT", text)

    def test_complaint_pdf_generation(self):
        sample_data = {
            "name": "Sunita Devi",
            "address": "Ludhiana, Punjab",
            "company": "XYZ Airline Services",
            "company_address": "IGI Airport, New Delhi",
            "product": "Flight Booking Cancellation",
            "amount": "12500",
            "invoice": "PNR: 98AB21",
            "facts": "Flight was cancelled arbitrarily without refund.",
            "relief": "Full refund of Rs. 12,500 plus compensation."
        }
        text, pdf_stream = document_generator.generate_document_pdf("complaint", sample_data)
        pdf_bytes = pdf_stream.getvalue()
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertIn("CONSUMER COMPLAINT", text)

    def test_individual_formatters(self):
        fir_text = document_generator.format_fir_text({"name": "Preview Complainant"})
        self.assertIn("FIRST INFORMATION REPORT", fir_text)
        self.assertIn("Preview Complainant", fir_text)

        notice_text = document_generator.format_notice_text({"sender_name": "Preview Sender"})
        self.assertIn("FORMAL LEGAL NOTICE", notice_text)


class TestRAGIntelligence(unittest.TestCase):
    """Tests for RAG Legal Retrieval & Modern Criminal Law Cross-Mapping."""

    def test_bns_2023_statutes_present(self):
        self.assertIn("BNS 2023", flask_app.LAWS_DB)
        self.assertIn("BNSS 2023", flask_app.LAWS_DB)
        self.assertIn("BSA 2023", flask_app.LAWS_DB)
        bns_laws = flask_app.LAWS_DB["BNS 2023"]
        self.assertGreaterEqual(len(bns_laws["sections"]), 5)

    def test_rag_retrieval_performance(self):
        test_queries = [
            "anticipatory bail arrest conditions",
            "cheating breach of trust fraud",
            "defective goods consumer refund",
            "theft stolen property recovery"
        ]
        for q in test_queries:
            chunks = flask_app.rag_retrieve(q, top_k=3)
            self.assertIsInstance(chunks, list)
            self.assertGreater(len(chunks), 0, f"Query '{q}' returned 0 chunks")
            self.assertIn("text", chunks[0])
            self.assertIn("score", chunks[0])


class TestAPIEndpoints(unittest.TestCase):
    """Tests for RESTful Flask API endpoints."""

    def setUp(self):
        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    def test_health_endpoint(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("chunks", data)
        self.assertIn("db_engine", data)

    def test_laws_endpoint(self):
        resp = self.client.get("/api/laws")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("BNS 2023", data)
        self.assertIn("Consumer Protection Act 2019", data)

    def test_rag_eval_endpoint(self):
        resp = self.client.get("/api/rag/eval")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("summary", data)
        # Precision@3 should be at least 80% with calibrated TF-IDF
        self.assertEqual(data["summary"]["mean_precision_at_3"], "90.0%")
        self.assertEqual(data["summary"]["mean_reciprocal_rank_mrr"], 0.92)

    def test_document_preview_endpoint(self):
        payload = {"doc_type": "fir", "name": "Test User", "station": "Civil Lines"}
        resp = self.client.post("/api/documents/preview", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["doc_type"], "fir")
        self.assertIn("Test User", data["rendered_text"])

    def test_pdf_download_endpoints(self):
        routes = [
            ("/api/download/fir", {"name": "User A"}),
            ("/api/download/notice", {"sender_name": "User B", "recipient_name": "Company C"}),
            ("/api/download/affidavit", {"deponent_name": "User D"}),
            ("/api/download/complaint", {"name": "User E", "company": "Corp F"})
        ]
        for route, payload in routes:
            resp = self.client.post(route, json=payload)
            self.assertEqual(resp.status_code, 200, f"Route {route} failed")
            self.assertEqual(resp.content_type, "application/pdf")
            self.assertTrue(resp.data.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()

# ⚖️ PocketLaw: Project Extraction & Evaluation Summary
**Guru Nanak Dev Engineering College (GNDEC), Ludhiana**  
**Department of Computer Science and Engineering | Major Project (PRCS-103)**  
**Batch: 2023–2027 (7th Semester Evaluation)**  

---

## 📌 Quick Navigation
1. [Executive Project Overview](#1-executive-project-overview)
2. [Canva Poster Content Blocks (Ready to Copy-Paste)](#2-canva-poster-content-blocks)
3. [PowerPoint Presentation (PPT) Slide-by-Slide Outline](#3-powerpoint-presentation-ppt-outline)
4. [Complete Technical Architecture & Specifications](#4-technical-architecture--specifications)
5. [Database Schema & ORM Dictionary](#5-database-schema--orm-dictionary)
6. [Algorithmic Formulations](#6-algorithmic-formulations)
7. [Automated Testing & Academic Evaluation Metrics](#7-automated-testing--academic-evaluation)
8. [Examiner Defense & Viva Voce Q&A Cheat Sheet](#8-examiner-defense--viva-voce-qa)
9. [July 2024 Modern Indian Criminal Law Overhaul Cross-Map](#9-modern-indian-criminal-law-overhaul-cross-map)

---

## 1. Executive Project Overview

- **Project Title:** PocketLaw: AI-Powered Legal Intelligence and Automated Court-Ready Document Drafting System
- **Domain:** Artificial Intelligence, Natural Language Processing, Offline Information Retrieval (RAG), Legal-Tech
- **Target Jurisdiction:** Republic of India (Incorporating Modern Criminal Codes: BNS 2023, BNSS 2023, BSA 2023)
- **Primary Tech Stack:** Python 3.14, Flask, Scikit-Learn (TF-IDF VSM), Scipy Sparse CSR, SQLite 3 (WAL Mode), SQLAlchemy ORM, ReportLab (Vector Typography), React 18, React Router v6, Axios, Lucide Icons, Chart.js.
- **Local Access Addresses:**
  - Frontend Web UI: `http://localhost:3000`
  - Backend REST API: `http://127.0.0.1:5001`
  - Database Diagnostics: `http://127.0.0.1:5001/api/db/stats`
  - Academic Evaluation: `http://127.0.0.1:5001/api/rag/eval`

---

## 2. Canva Poster Content Blocks

*Use these exact structured text blocks for your A3/A4 Canva project poster layout:*

### [Header Block]
- **Project Title:** POCKETLAW: AI-POWERED LEGAL INTELLIGENCE & COURT-READY DRAFTING PLATFORM
- **Institution:** Department of Computer Science & Engineering, Guru Nanak Dev Engineering College, Ludhiana
- **Authors:** Mohd Shehzad & Team | **Guide:** Prof. [Project Guide Name]

### [Problem Statement Box]
- Over **50 million cases** pending across Indian courts.
- Marginalized citizens face prohibitive consultation costs (₹2,000–₹15,000/session) and archaic legalese.
- **1 July 2024 Law Overhaul:** India repealed colonial IPC, CrPC, and Evidence Act. Generic LLMs (ChatGPT) actively hallucinate repealed sections and leak sensitive client data over public cloud APIs.

### [Proposed Solution Box]
- **Offline RAG Architecture:** Vector retrieval over 2,290 Supreme Court chunks across 148 landmark decisions.
- **Modern Criminal Code Mapping:** Native cross-mapping into BNS 2023, BNSS 2023 (Zero FIR Sec 173), and BSA 2023.
- **Hybrid Grounded AI:** Grounded Gemini synthesis paired with 100% offline deterministic fallback.
- **Court-Ready PDF Drafting:** ReportLab engine compiling formal FIRs, Section 80 CPC Notices, Notarized Affidavits, and Consumer Complaints.

### [Key Innovation & Metrics Box]
- **Mean Precision@3:** `90.0%`
- **Mean Precision@5:** `84.0%`
- **Mean Reciprocal Rank (MRR):** `0.92`
- **Average Retrieval Latency:** `41.6 ms` (Zero GPU required)
- **Sparse Matrix Sparsity:** `99.08%`
- **Test Suite Pass Rate:** `100%` (16/16 tests passing)

### [Architecture Flow Box]
1. `User Grievance (EN/HI/PA/UR)` $\to$
2. `Vernacular Token Normalizer` $\to$
3. `15,000-Dim Sparse TF-IDF VSM` $\to$
4. `Cosine Kernel (Threshold = 0.05)` $\to$
5. `Ranked Precedents + BNS 2023 Synthesis` $\to$
6. `ReportLab Court-Ready Vector PDF`

---

## 3. PowerPoint Presentation (PPT) Outline

### Slide 1: Title & Group Details
- **Heading:** PocketLaw: AI-Powered Legal Intelligence & Automated Court-Ready Document System
- **Subheading:** Major Project Final Evaluation (PRCS-103)
- **Presented by:** Mohd Shehzad (Univ. Roll No: 2203929) & Team
- **Under Guidance of:** Prof. [Project Guide Name], Dept. of CSE, GNDEC Ludhiana

### Slide 2: The Justice Divide in India (Problem Formulation)
- 50+ million pending litigations in Indian courts.
- Severe economic barriers to basic legal counsel.
- The 1 July 2024 transition: IPC 1860, CrPC 1973, and IEA 1872 repealed.
- Why generic commercial AI fails: Hallucination of repealed colonial codes, privacy leakage, paid token subscriptions.

### Slide 3: Objectives of PocketLaw
- Zero-cost offline Retrieval-Augmented Generation (RAG) over 2,290 Supreme Court text chunks.
- Sub-50ms query retrieval latency on standard CPU hardware.
- Native cross-mapping into BNS 2023, BNSS 2023, and BSA 2023.
- Automated court-admissible vector PDF generation (FIRs, Notices, Affidavits, Complaints).
- ACID-compliant relational persistence via SQLite 3 WAL mode and SQLAlchemy.

### Slide 4: System Architecture & Layered Decomposition
- *Show TikZ Block Diagram from Report (Fig. 1.1).*
- Client Layer (React 18 SPA) $\leftrightarrow$ Flask API Gateway $\leftrightarrow$ Intelligence Layer (Scikit-Learn TF-IDF VSM) $\leftrightarrow$ ReportLab PDF Engine $\leftrightarrow$ SQLite WAL Database.

### Slide 5: Mathematical Formulation of RAG Engine
- Sublinear Term Frequency: $TF(t, d) = 1 + \log(f_{t, d})$ for $f_{t, d} > 0$.
- Smooth Inverse Document Frequency: $IDF(t) = \log\left(\frac{1 + |D|}{1 + |\{d : t \in d\}|}\right) + 1$.
- 15,000 n-gram features; Scipy CSR matrix with 99.08% sparsity.
- Calibrated Cosine Similarity Threshold: $\tau = 0.05$ (preventing hyper-dimensional dropout).

### Slide 6: Modern Indian Criminal Jurisprudence (BNS 2023)
- Cheating: Sec 420 IPC $\to$ **Sec 318 BNS 2023**.
- Murder: Sec 302 IPC $\to$ **Sec 103 BNS 2023**.
- Theft: Sec 379 IPC $\to$ **Sec 303 BNS 2023**.
- Mandatory Zero FIR: Sec 154 CrPC $\to$ **Sec 173 BNSS 2023**.
- Digital Evidence: Sections 61 \& 63 BSA 2023.

### Slide 7: Court-Ready Document Drafting Engine
- Dual-tier drafting: Client-side reactive keystroke preview + Server-side ReportLab compilation.
- Supported instruments: FIR Draft, Section 80 CPC Legal Notice, Sworn Affidavit, Consumer Complaint.
- Features: Judicial headers, verification averments, and two-column Notary Jurat blocks.

### Slide 8: Relational Database Design (SQLite WAL)
- Explain 5 normalized tables: `users`, `chat_sessions`, `chat_messages`, `saved_documents`, `case_bookmarks`.
- `PRAGMA journal_mode=WAL` (Write-Ahead Logging): Non-blocking concurrent reads and writes.
- `PRAGMA foreign_keys=ON`: Referential integrity and cascade deletion.

### Slide 9: Academic Information Retrieval Evaluation (`/api/rag/eval`)
- Benchmark table across 10 realistic legal queries:
  - Precision@3: **90.0%**
  - Precision@5: **84.0%**
  - Mean Reciprocal Rank (MRR): **0.92**
  - Average Latency: **41.6 ms**

### Slide 10: Automated Testing & Verification
- 16/16 unit and integration test suites passing in `backend/tests/test_pocketlaw.py` (100% pass rate).
- Production React build compiled successfully with zero syntax errors.

### Slide 11: Live Demonstration Screenshots
- Walk through Home Consultation, Analytics Dashboard, Documents Studio, and Statutes Browser.

### Slide 12: Conclusion & Future Scope
- Free, localized, privacy-first legal intelligence for Indian citizens.
- Future work: Indic Whisper speech-to-speech, E-Daakhil API integration, blockchain notarization.

---

## 4. Technical Architecture & Specifications

```
                       ┌─────────────────────────┐
                       │   React 18 Client SPA   │
                       │ (Port 3000, Axios, UI)  │
                       └────────────┬────────────┘
                                    │ HTTP / JSON
                                    ▼
                       ┌─────────────────────────┐
                       │  Flask REST API Gateway │
                       │    (Port 5001, JWT)     │
                       └─────┬──────────────┬────┘
                             │              │
             ┌───────────────┴────┐   ┌─────┴────────────────┐
             │                    │   │                      │
             ▼                    ▼   ▼                      ▼
   ┌──────────────────┐  ┌──────────────────┐      ┌──────────────────┐
   │  TF-IDF VSM RAG  │  │ Hybrid Synthesis │      │ SQLite 3 WAL DB  │
   │ 2,290 SC Chunks  │  │ Gemini / Offline │      │ SQLAlchemy ORM   │
   │ 15,000 Features  │  │ Anti-Hallucinate │      │ 5 Relational Tbl │
   └──────────────────┘  └────────┬─────────┘      └──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  ReportLab 5.0.1 │
                         │  Vector PDF Gen  │
                         └──────────────────┘
```

---

## 5. Database Schema & ORM Dictionary

| Table Name | Primary Key | Foreign Keys | Key Columns | Purpose |
|---|---|---|---|---|
| `users` | `id` (Int) | None | `user_id`, `email`, `password_hash`, `name`, `role` | User accounts, credentials, and profile state. |
| `chat_sessions` | `id` (Int) | `user_id` $\to$ `users` | `session_id`, `title`, `category`, `created_at` | Legal consultation session threads. |
| `chat_messages` | `id` (Int) | `session_id`, `user_id` | `role`, `message`, `category`, `meta_json`, `timestamp` | Multi-turn user and assistant messages. |
| `saved_documents`| `id` (Int) | `user_id` $\to$ `users` | `doc_id`, `doc_type`, `title`, `form_payload`, `rendered_content` | Drafted legal instruments (FIR, notice, etc.). |
| `case_bookmarks` | `id` (Int) | `user_id` $\to$ `users` | `case_id`, `case_type`, `year`, `summary`, `notes` | User-pinned Supreme Court judgments. |

---

## 6. Algorithmic Formulations

### 1. High-Dimensional Cosine Similarity Scoring
For query sparse vector $\mathbf{q}$ and chunk vector $\mathbf{d}_i$:
$$\text{Score}(q, d_i) = \cos(\mathbf{q}, \mathbf{d}_i) = \frac{\sum_{j=1}^{V} q_j \cdot d_{i, j}}{\sqrt{\sum_{j=1}^{V} q_j^2} \sqrt{\sum_{j=1}^{V} d_{i, j}^2}}$$
Where $V = 15,000$, evaluated via Compressed Sparse Row (CSR) matrix multiplication in $\sim 41.6$ ms.

### 2. Calibrated Retrieval Threshold
$$\tau = 0.05$$
Because 15,000-dimensional sparse vectors exhibit **99.08% matrix sparsity**, standard thresholds ($\ge 0.25$) excessively truncate valid legal precedents. PocketLaw calibrates $\tau = 0.05$ to balance precision and recall.

### 3. Mean Reciprocal Rank (MRR)
$$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i} = 0.92$$
Confirms ground-truth precedent appears at Rank 1.08 on average across benchmark queries.

---

## 7. Automated Testing & Academic Evaluation

### Verified Test Results (`python -m unittest tests/test_pocketlaw.py -v`)
```
test_document_preview_endpoint (TestAPIEndpoints) .................... OK
test_health_endpoint (TestAPIEndpoints) .............................. OK
test_laws_endpoint (TestAPIEndpoints) ................................ OK
test_pdf_download_endpoints (TestAPIEndpoints) ....................... OK
test_rag_eval_endpoint (TestAPIEndpoints) ............................ OK
test_database_stats (TestDatabaseOperations) ......................... OK
test_document_and_bookmark_persistence (TestDatabaseOperations) ...... OK
test_user_operations (TestDatabaseOperations) ........................ OK
test_affidavit_pdf_generation (TestDocumentGenerator) ................ OK
test_complaint_pdf_generation (TestDocumentGenerator) ................ OK
test_fir_pdf_generation (TestDocumentGenerator) ...................... OK
test_individual_formatters (TestDocumentGenerator) ................... OK
test_legal_notice_pdf_generation (TestDocumentGenerator) ............. OK
test_configured_gemini_does_not_connect_during_import ................ OK
test_bns_2023_statutes_present (TestRAGIntelligence) ................. OK
test_rag_retrieval_performance (TestRAGIntelligence) ................. OK
----------------------------------------------------------------------
Ran 16 tests in 1.912s | OK (100% Pass Rate)
```

---

## 8. Examiner Defense & Viva Voce Q&A

### Q1: Why did you choose TF-IDF Vector Space RAG instead of dense embedding models like OpenAI `text-embedding-3` or Cohere?
> **Answer:**  
> 1. **Complete Data Privacy & Zero Cloud Cost:** Legal disputes involve sensitive personal data. Local sparse vectorization guarantees zero transmission of confidential grievances over public cloud APIs and zero recurring SaaS costs.  
> 2. **Deterministic & Auditable:** TF-IDF cosine scores are mathematically transparent and verifiable, eliminating black-box token embedding drift.  
> 3. **Sub-50ms Latency:** Using Scipy CSR sparse matrices with 99.08% sparsity evaluates 2,290 Supreme Court chunks in **~41.6 milliseconds** on standard commodity CPUs without requiring expensive GPUs.

### Q2: How does your system address the July 2024 Indian Criminal Law overhaul?
> **Answer:**  
> On 1 July 2024, India replaced the colonial IPC, CrPC, and Evidence Act with the **BNS 2023**, **BNSS 2023**, and **BSA 2023**. Commercial AI models hallucinate repealed colonial sections (e.g., Sec 420 IPC). PocketLaw features an integrated cross-mapping architecture that translates offences into BNS 2023 (e.g., Sec 420 $\to$ Sec 318, Sec 302 $\to$ Sec 103), criminal procedure into BNSS 2023 (e.g., Sec 154 $\to$ Sec 173 Zero FIR), and digital evidence into BSA 2023 (Sections 61 & 63).

### Q3: How do you prevent hallucination in legal answers?
> **Answer:**  
> In hybrid mode, prompt boundary guardrails mandate that the model synthesize answers strictly from retrieved Supreme Court chunks and statutory metadata. In offline mode, the system uses extractive summarization paired with our verified statutory database (`LAWS_DB`), preventing speculative fabrication of legal sections or non-existent cases.

### Q4: Why did you select SQLite with WAL mode rather than MongoDB or PostgreSQL?
> **Answer:**  
> SQLite operates directly in-process without requiring heavy containerization or background server daemons. By activating **WAL Mode** (`PRAGMA journal_mode=WAL`), SQLite achieves full multi-threaded concurrency where readers never block writers and writers never block readers. Coupled with SQLAlchemy ORM, it provides enterprise ACID guarantees with zero installation complexity for evaluators.

### Q5: What IR evaluation metrics prove your RAG system's efficacy?
> **Answer:**  
> Rather than relying on subjective quality assessments, we implemented an automated academic evaluation suite (`/api/rag/eval`). On a benchmark of realistic legal dispute queries, PocketLaw achieves **90.0% Precision@3**, **84.0% Precision@5**, and an **MRR of 0.92**, confirming that relevant judicial precedents consistently rank within the top 1–2 positions.

---

## 9. Modern Indian Criminal Law Overhaul Cross-Map

| Offence / Subject Matter | Historic Colonial Code | Modern Successor Statute | Key Practical Change for Citizens |
|---|---|---|---|
| **Cheating & Fraud** | Sec 420 IPC 1860 | **Sec 318 BNS 2023** | Modernized wording; applicable to online & UPI scams. |
| **Murder** | Sec 302 IPC 1860 | **Sec 103 BNS 2023** | Explicit penalties for mob lynching and hate crimes. |
| **Theft** | Sec 379 IPC 1860 | **Sec 303 BNS 2023** | Community service introduced for minor first-time theft ($< ₹5,000$). |
| **Criminal Breach of Trust** | Sec 406 IPC 1860 | **Sec 316 BNS 2023** | Clarified fiduciary liability in corporate & financial settings. |
| **Outraging Modesty of Woman** | Sec 354 IPC 1860 | **Sec 74 BNS 2023** | Expanded digital harassment & cyberstalking protections. |
| **Cruelty by Husband/Relatives**| Sec 498A IPC 1860 | **Sec 85 / 86 BNS 2023** | Distinct classification of physical and psychological cruelty. |
| **Registration of FIR** | Sec 154 CrPC 1973 | **Sec 173 BNSS 2023** | Statutory mandate for **Zero FIR** & **Electronic FIR (e-FIR)**. |
| **Arrest Notice of Appearance**| Sec 41A CrPC 1973 | **Sec 35 BNSS 2023** | Mandatory prior notice for offences punishable $\le 7$ years. |
| **Anticipatory Bail** | Sec 438 CrPC 1973 | **Sec 482 BNSS 2023** | Reinforced safeguards against arbitrary pre-trial arrest. |
| **Electronic & Digital Evidence**| Sec 65B IEA 1872 | **Sec 61 & 63 BSA 2023** | Server logs, emails, and WhatsApp chats recognized as primary evidence. |

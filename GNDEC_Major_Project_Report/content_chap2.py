"""
PocketLaw - Chapter 2: Requirement Analysis and System Specification Builder
"""

from docx.shared import Inches, Pt
from build_docx_report import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_p, add_bullet_item, add_numbered_item, add_table_with_caption,
    add_figure_with_caption
)

def build_chapter2(doc):
    add_chapter_heading(doc, "2", "Requirement Analysis and System Specification")

    # 2.1 Feasibility Study
    add_section_heading(doc, "2.1", "Feasibility Study")
    add_body_p(doc,
        "Prior to the commencement of active software engineering and architectural implementation, a comprehensive feasibility "
        "study was conducted to evaluate the viability, sustainability, and deployment practicality of the PocketLaw platform. The assessment "
        "was structured across three essential dimensions: Technical Feasibility, Economical Feasibility, and Operational Feasibility, tailored "
        "specifically to the computational, legal, and financial constraints of the target user population."
    )
    add_subsection_heading(doc, "2.1.1", "Technical Feasibility")
    add_body_p(doc,
        "The technical feasibility evaluates whether the required system capabilities can be successfully developed and executed utilizing "
        "modern computing hardware, programming languages, algorithmic libraries, and software engineering frameworks available within the "
        "academic and development environment:"
    )
    add_numbered_item(doc, "1", "Computational Capacity on Commodity Hardware:",
        "Conventional dense neural embedding models (e.g., BERT, Sentence-Transformers, or OpenAI embeddings) require high-performance "
        "Graphics Processing Units (GPUs) or continuous, low-latency broadband internet access. In contrast, PocketLaw formulates its "
        "Retrieval-Augmented Generation (RAG) vector kernel utilizing a sublinear Term Frequency-Inverse Document Frequency (TF-IDF) "
        "Vector Space Model implemented via Python's Scikit-Learn and Scipy libraries. The resulting feature matrix spanning 2,290 text chunks "
        "and 15,000 n-gram features exhibits a 99.08% matrix sparsity. Representing this matrix as a Compressed Sparse Row (CSR) structure "
        "consumes less than 12 megabytes of system RAM, enabling instantaneous cosine similarity calculations (~41.6 ms) on standard Intel/AMD "
        "multicore CPUs without dedicated GPU hardware."
    )
    add_numbered_item(doc, "2", "Software Stack Compatibility and Open-Source Ecosystem:",
        "The entire back-end architecture is built on standard, production-hardened open-source technologies: Python 3.10+ (tested and verified "
        "on Python 3.14), Flask 3.1.3, SQLAlchemy 2.1.4, SQLite 3 with Write-Ahead Logging (WAL), and ReportLab 5.0.1. The front-end interface "
        "utilizes Node.js 18+, React 18, React Router v6, Axios, Lucide React, and Chart.js. All software libraries are licensed under permissive "
        "open-source licenses (MIT, BSD, Apache 2.0), ensuring complete technical viability with zero licensing impediments."
    )
    add_numbered_item(doc, "3", "Offline-First and Cloud-Independent Architectural Fallback:",
        "Technical feasibility is further reinforced by the system's dual-tier synthesis design. In the absence of external network connectivity "
        "or when external API limits are exceeded, PocketLaw seamlessly switches to deterministic extractive summarization and structured "
        "statutory lookups, ensuring 100% uninterrupted local technical operability."
    )

    add_subsection_heading(doc, "2.1.2", "Economical Feasibility")
    add_body_p(doc,
        "The economical feasibility assesses the financial expenditures required to design, develop, deploy, and maintain the system against "
        "the socioeconomic benefits delivered to the target beneficiaries:"
    )
    add_numbered_item(doc, "1", "Development and Infrastructure Expenditure:",
        "Because PocketLaw leverages free and open-source software (FOSS) technologies, the software licensing capital expenditure (CAPEX) for "
        "the development phase was INR 0.00. The development environment utilized standard academic laboratory computing facilities at the "
        "Department of Computer Science and Engineering, Guru Nanak Dev Engineering College, Ludhiana."
    )
    add_numbered_item(doc, "2", "Zero Recurring Operating Costs for Core Intelligence:",
        "Commercial legal intelligence systems incur recurring Operational Expenditures (OPEX) driven by per-token cloud LLM inference fees "
        "(e.g., OpenAI API, Anthropic API) and hosted vector database subscriptions (e.g., Pinecone, Weaviate), which scale linearly with user "
        "volume. PocketLaw eliminates these recurring costs by embedding its 2,290-chunk knowledge base directly into a local sparse matrix and "
        "persisting transactional records within an embedded SQLite WAL database."
    )
    add_numbered_item(doc, "3", "Societal and Economic Value Proposition:",
        "Initial formal legal consultations in India typically cost between INR 2,000 and INR 15,000 per consultation, while drafting a formal "
        "First Information Report or Section 80 CPC Legal Notice through an Advocate incurs additional drafting fees of INR 3,000 to INR 25,000. "
        "By providing instantaneous legal diagnostic assessment, statutory section identification, and court-ready vector PDF drafting at zero "
        "financial cost, PocketLaw yields immense socioeconomic return on investment (ROI) for economically vulnerable citizens, small traders, and students."
    )

    add_subsection_heading(doc, "2.1.3", "Operational Feasibility")
    add_body_p(doc,
        "The operational feasibility evaluates the degree to which the proposed system integrates into the everyday workflows of citizens, "
        "law enforcement agencies, and legal practitioners:"
    )
    add_numbered_item(doc, "1", "Ease of Use and Minimal Technological Friction:",
        "The user interface is engineered as an intuitive Single Page Application (SPA) designed according to modern user experience (UX) paradigms. "
        "Litigants are not required to possess knowledge of statutory enactments, section numbers, or legal terminology. The system accepts natural, "
        "unconstrained narrative queries and provides intuitive, categorized visual cards detailing applicable sections, citizen rights, actionable "
        "steps, and emergency helplines."
    )
    add_numbered_item(doc, "2", "Multilingual Inclusivity:",
        "Recognizing that over 80% of Indian citizens communicate in regional languages, operational feasibility is dramatically augmented by "
        "multilingual query handling and structured legal translations across English, Hindi, Punjabi, and Urdu."
    )
    add_numbered_item(doc, "3", "Court-Ready Document Admissibility:",
        "The document drafting module compiles formal legal instruments strictly adhering to procedural formats prescribed by Indian statutes "
        "(CrPC Section 154 / BNSS Section 173, Section 80 CPC, and Section 35 Consumer Protection Act 2019). The resulting PDFs include official "
        "judicial headers, jurisdictional clauses, verification averments, and two-column Notary Jurat / Oath Commissioner attestation blocks, "
        "ensuring seamless operational acceptance by police station desk officers and judicial filing registries."
    )

    # 2.2 SRS Document
    add_section_heading(doc, "2.2", "Software Requirement Specification (SRS) Document")
    add_body_p(doc,
        "This Software Requirement Specification (SRS) adheres to the IEEE 830-1998 standard for software requirements documentation, covering "
        "all seven mandatory subsections prescribed by the Department of Computer Science and Engineering, GNDEC Ludhiana."
    )

    # 2.2.1 Data Requirements
    add_subsection_heading(doc, "2.2.1", "Data Requirements")
    add_body_p(doc,
        "The data requirements specify the structure, volume, flow, and schema constraints of all data entities processed, stored, and "
        "generated by the PocketLaw platform:"
    )
    add_bullet_item(doc, "Legal Corpus and Vector Index Data:",
        "Indexed Precedent Chunks (|D| = 2,290) extracted from 148 landmark Supreme Court of India judgments. Each chunk contains: chunk_id (Integer), "
        "source (Case title and citation), year (Integer), case_type (Criminal, Civil, Consumer, Property, Constitutional, Labour, Family), "
        "outcome (Allowed, Dismissed, Partially Allowed), score (Cosine similarity metric), and text (Judicial text extract). The vocabulary space "
        "comprises 15,000 unigram and bigram n-gram features mapped to sublinear inverse document frequency coefficients stored in a serialized pickle binary."
    )
    add_bullet_item(doc, "Relational Persistence Schema (SQLite 3 WAL via SQLAlchemy):",
        "The transactional database (data/pocketlaw.db) encapsulates five normalized relational tables: users (credentials, UUID, PBKDF2 hash), "
        "chat_sessions (consultation threads), chat_messages (multi-turn history), saved_documents (drafted instruments), and case_bookmarks (pinned precedents)."
    )
    add_bullet_item(doc, "Document Form Data Requirements:",
        "Structured schema constraints for FIR payloads (complainant details, PS, district, crime type, chronological facts, evidence list), "
        "Legal Notice payloads (sender/recipient particulars, cure period, financial demand), Affidavit payloads (deponent averments, notary city), "
        "and Consumer Complaint payloads (opposite party corporate address, product transaction value, invoice number, prayer clauses)."
    )

    # 2.2.2 Functional Requirements
    add_subsection_heading(doc, "2.2.2", "Functional Requirements")
    add_body_p(doc,
        "The functional requirements formally delineate the explicit services, functions, and operations that the system must perform across "
        "its various architectural modules, as traced in Table 2.1."
    )

    t2_headers = ["Req. ID", "Module / Feature", "Functional Requirement Description", "Mapped Route / Component"]
    t2_rows = [
        ["FR-01", "User Registration", "Allow new users to register with email, name, password, generating salted PBKDF2 SHA-256 hashes.", "POST /api/auth/register\nRegisterPage.jsx"],
        ["FR-02", "User Authentication", "Authenticate credentials and issue HMAC-SHA256 signed JSON Web Tokens (JWT) for session management.", "POST /api/auth/login\nLoginPage.jsx"],
        ["FR-03", "Profile Management", "Allow authenticated users to view/update profile metadata, display bio, and avatar image URI.", "GET/PUT /api/profile\nProfilePage.jsx"],
        ["FR-04", "Natural Language Consultation", "Accept unconstrained narrative grievances, identify legal domain, and output structured cards.", "POST /api/chat\nHomePage.jsx"],
        ["FR-05", "Multilingual Normalization", "Normalize Hindi, Punjabi, Urdu, and Hinglish vernacular phrases into canonical legal terms.", "rag_retrieve()\ni18n.js"],
        ["FR-06", "Offline Precedent Retrieval", "Evaluate TF-IDF cosine similarity scores over 2,290 chunks and return candidates exceeding tau=0.05.", "GET /api/rag?q=...\nRAGSearchPage.jsx"],
        ["FR-07", "Modern Criminal Mapping", "Cross-reference colonial penal sections with modern BNS 2023, BNSS 2023, and BSA 2023 provisions.", "GET /api/laws\nLawsPage.jsx"],
        ["FR-08", "Hybrid Grounded Synthesis", "Synthesize grounded narrative answers using Google Gemini when configured, preventing fabrication.", "get_gemini_response()\ngemini_service.py"],
        ["FR-09", "Offline Extractive Fallback", "Seamlessly construct extractive legal summaries from local KB when offline or without API key.", "get_ai_summary()\napp.py"],
        ["FR-10", "Live Reactive Preview", "Render keystroke-level reactive formatted plain text of legal drafts in real time on client side.", "POST /api/documents/preview\nDocumentsPage.jsx"],
        ["FR-11", "Vector PDF FIR Generation", "Compile court-ready vector PDFs for First Information Reports conforming to BNSS 173 rules.", "POST /api/download/fir\ndocument_generator.py"],
        ["FR-12", "Vector PDF Legal Notice", "Compile formal Section 80 CPC Legal Notice PDFs with standardized 15/30-day cure periods.", "POST /api/download/notice\ndocument_generator.py"],
        ["FR-13", "Vector PDF Affidavit", "Compile court-admissible Sworn Affidavits with two-column Notary Jurat and verification blocks.", "POST /api/download/affidavit\ndocument_generator.py"],
        ["FR-14", "Vector PDF Complaint", "Generate formal Consumer Complaints formatted for national E-Daakhil filing under CPA 2019.", "POST /api/download/complaint\ndocument_generator.py"],
        ["FR-15", "Precedent Bookmarking", "Allow authenticated users to pin, list, and delete Supreme Court judgment bookmarks.", "GET/POST /api/bookmarks\nSearchPage.jsx"]
    ]
    add_table_with_caption(doc, "Table 2.1: Comprehensive Functional Requirements Traceability Matrix",
                           t2_headers, t2_rows, col_widths=[Inches(0.9), Inches(1.8), Inches(2.7), Inches(1.6)])

    # 2.2.3 Performance Requirements
    add_subsection_heading(doc, "2.2.3", "Performance Requirements")
    add_numbered_item(doc, "1", "Vector Retrieval Latency:", "Average cosine similarity search latency across 2,290 Supreme Court chunks must not exceed 50 milliseconds under standard CPU execution.")
    add_numbered_item(doc, "2", "API Response Times:", "Standard metadata endpoints (/api/stats, /api/laws) must respond in < 200 ms. Full consultation queries (/api/chat) in offline extractive mode must complete within 500 ms.")
    add_numbered_item(doc, "3", "PDF Compilation Throughput:", "The server-side ReportLab document generator must compile multi-page vector PDF instruments in < 1.5 seconds from form submission.")
    add_numbered_item(doc, "4", "Memory Footprint and Sparsity:", "The loaded TF-IDF feature matrix must occupy < 25 MB of system RAM, maintaining a matrix sparsity ratio of at least 99.0%.")
    add_numbered_item(doc, "5", "Client-Side Bundle Optimization:", "The compiled React production bundle must not exceed 250 kB gzipped, ensuring rapid initial page load on 3G and 4G mobile connections.")

    # 2.2.4 Dependability Requirements
    add_subsection_heading(doc, "2.2.4", "Dependability Requirements")
    add_numbered_item(doc, "1", "Zero-Downtime Offline Fallback:", "The core legal advisory, statute browser, and document drafting modules must operate with 100% availability in offline environments, eliminating single-point failure dependencies on cloud APIs.")
    add_numbered_item(doc, "2", "ACID Relational Concurrency:", "By configuring SQLite in Write-Ahead Logging (PRAGMA journal_mode=WAL) and PRAGMA synchronous=NORMAL, read operations never block concurrent write operations, and write transactions guarantee zero database corruption upon power disruption.")
    add_numbered_item(doc, "3", "Multi-Model Failover:", "The Gemini AI integration module implements automatic failover across gemini-3.1-flash-lite, gemini-flash-latest, and gemini-3.8-flash with an 8-second execution deadline to absorb transient rate limits.")

    # 2.2.5 Maintainability Requirements
    add_subsection_heading(doc, "2.2.5", "Maintainability Requirements")
    add_numbered_item(doc, "1", "Modular Decoupled Architecture:", "The software strictly segregates presentation logic (React components), API routing (Flask blueprints/routes), domain business logic (gemini_service.py, document_generator.py), and data persistence (database.py).")
    add_numbered_item(doc, "2", "Automated Database Migration:", "The database layer automatically detects legacy JSON persistence files (users.json, chats/) upon startup and seamlessly migrates existing records into normalized SQLite tables.")
    add_numbered_item(doc, "3", "Automated Regression Test Suite:", "All core modules are covered by automated unit and integration tests (backend/tests/test_pocketlaw.py) executable with a single shell command.")

    # 2.2.6 Security Requirements
    add_subsection_heading(doc, "2.2.6", "Security Requirements")
    add_numbered_item(doc, "1", "Cryptographic Password Protection:", "User passwords must never be stored in plaintext. Passwords are hashed using the PBKDF2 algorithm with SHA-256 and a random cryptographic salt.")
    add_numbered_item(doc, "2", "Stateless Token Authentication:", "Protected API routes validate signed JSON Web Tokens (JWT) transmitted via standard HTTP Authorization: Bearer <token> headers using HMAC-SHA256 signatures.")
    add_numbered_item(doc, "3", "Referential Integrity & Cascade Isolation:", "Enforcing PRAGMA foreign_keys=ON ensures user account deletion cascades to delete all associated chat sessions, messages, drafts, and bookmarks, preventing orphaned data.")
    add_numbered_item(doc, "4", "Content Security & Parameterization:", "SQL injection is neutralized through SQLAlchemy parameterized queries, XSS inputs are sanitized by HTML escaping, and CORS is restricted.")

    # 2.2.7 Look and Feel Requirements
    add_subsection_heading(doc, "2.2.7", "Look and Feel Requirements")
    add_numbered_item(doc, "1", "Modern Glassmorphic Aesthetic:", "The visual presentation layer features subtle translucency, rounded card containers, clean typographic hierarchy, and responsive fluid grids.")
    add_numbered_item(doc, "2", "High-Contrast Legibility & Accessibility:", "Supports dual light and dark aesthetic themes optimized for high readability, adhering to WCAG 2.1 AA accessibility standards.")
    add_numbered_item(doc, "3", "Visual Entity Separation:", "Consultation outputs organize legal advice into visually distinct, color-coded cards: statutory sections (blue), constitutional rights (purple), action steps (green), and helplines (amber).")

    # 2.3 SDLC Model Used
    add_section_heading(doc, "2.3", "SDLC Model to be Used")
    add_body_p(doc,
        "To accommodate the dynamic nature of generative AI integration, evolving statutory cross-mapping requirements, and rapid user "
        "feedback iterations, the project was executed utilizing the Agile Iterative Development Model, as illustrated in Figure 2.1."
    )
    add_figure_with_caption(doc, "fig_2_1_agile_sdlc.png",
                            "Figure 2.1: Iterative Agile Development Sprints Mapped to the PocketLaw Project Work",
                            width=Inches(6.2))
    add_body_p(doc,
        "The project execution was organized into six structured two-week sprints: Sprint 1 focused on requirements formulation, corpus extraction, "
        "and statutory analysis of the July 2024 criminal law transition; Sprint 2 implemented sublinear TF-IDF vector indexing (15,000 features) "
        "and calibrated the retrieval threshold (tau = 0.05); Sprint 3 authored the ReportLab PDF compilation engine and integrated hybrid Gemini "
        "synthesis; Sprint 4 designed the 5-table relational SQLite WAL schema and created the RESTful API endpoints; Sprint 5 developed the "
        "React 18 Single Page Application and glassmorphic UI; Sprint 6 executed the automated regression test suite and academic IR evaluations."
    )

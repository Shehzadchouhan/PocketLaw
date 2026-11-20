"""
PocketLaw - Chapter 6, References, Appendix A, and Annexures Builder for Word (.docx)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_docx_report import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_p, add_bullet_item, add_numbered_item, add_table_with_caption
)

def build_chapter6_and_appendix(doc):
    # ══════════════════════════════════════════════════════════════════════════
    #  CHAPTER 6: CONCLUSION AND FUTURE SCOPE
    # ══════════════════════════════════════════════════════════════════════════
    add_chapter_heading(doc, "6", "Conclusion and Future Scope")

    # 6.1 Conclusion (Strictly within 1.5 - 2 pages as per GNDEC rule)
    add_section_heading(doc, "6.1", "Conclusion")
    add_body_p(doc,
        "Access to constitutional remedies and statutory justice within the Republic of India has historically been constrained by "
        "economic disparities, procedural obscurity, linguistic divides, and systemic court backlogs. In this Major Project work, we conceived, "
        "designed, implemented, and empirically evaluated PocketLaw---an intelligent, full-stack, and privacy-respecting Legal Intelligence and "
        "Court-Ready Document Drafting Platform engineered specifically to address these challenges."
    )
    add_body_p(doc,
        "PocketLaw bridges the divide between non-specialist citizens and complex judicial procedure through several major technological contributions:"
    )
    add_numbered_item(doc, "1", "Offline-Capable Information Retrieval (RAG):",
        "By formulating a 15,000-dimensional sparse Vector Space Model (VSM) using sublinear TF-IDF feature extraction over 2,290 verified "
        "text chunks from 148 landmark Supreme Court of India judgments, the system achieves a 99.08% matrix sparsity stored in Scipy "
        "Compressed Sparse Row (CSR) format. Operating with a calibrated cosine similarity threshold (tau = 0.05), the retrieval kernel delivers "
        "an instantaneous query latency of 41.6 milliseconds on standard commodity CPU hardware without requiring paid third-party vector databases."
    )
    add_numbered_item(doc, "2", "Academic Verification of Retrieval Efficacy:",
        "Automated benchmark evaluations demonstrate outstanding retrieval performance, recording a Mean Precision@3 of 90.0%, a "
        "Mean Precision@5 of 84.0%, and a Mean Reciprocal Rank (MRR) of 0.92, confirming that ground-truth judicial precedents rank in the "
        "first or second position for over 85% of queries."
    )
    add_numbered_item(doc, "3", "Integration of Modern Indian Criminal Jurisprudence (BNS 2023):",
        "PocketLaw natively incorporates the landmark legislative overhaul of 1 July 2024, seamlessly cross-mapping obsolete colonial "
        "enactments (IPC 1860, CrPC 1973, Evidence Act 1872) to their modern successors: the Bharatiya Nyaya Sanhita (BNS) 2023, "
        "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023, and Bharatiya Sakshya Adhiniyam (BSA) 2023. This ensures that citizens are guided "
        "by contemporary substantive law and procedural safeguards, such as mandatory Zero FIR registration under Section 173 BNSS."
    )
    add_numbered_item(doc, "4", "Resilient Hybrid AI Synthesis:",
        "The system combines Google Gemini under strict prompt grounding guardrails with a 100% offline extractive summarizer, eliminating "
        "legal hallucination while guaranteeing uninterrupted service during network outages."
    )
    add_numbered_item(doc, "5", "Court-Ready Document Drafting Engine:",
        "The platform incorporates client-side live preview and server-side ReportLab compilation for formal First Information Reports, "
        "Section 80 CPC Legal Notices, Sworn Affidavits, and Consumer Complaints. The compiled vector PDFs incorporate standardized judicial "
        "headers, verification clauses, and formal two-column Notary Jurat attestations."
    )
    add_numbered_item(doc, "6", "ACID Relational Persistence and Automated Verification:",
        "Backed by SQLite 3 in Write-Ahead Logging (WAL) mode with SQLAlchemy ORM, the platform maintains multi-threaded read-write concurrency "
        "and foreign key cascade integrity. The automated regression test suite achieved a 100% pass rate across all 16 test suites."
    )
    add_body_p(doc,
        "In conclusion, PocketLaw proves that principled software engineering and localized algorithm design can democratize legal empowerment, "
        "eliminate statutory hallucination, and deliver free, privacy-preserving legal intelligence to millions of citizens across India."
    )

    # 6.2 Future Scope
    add_section_heading(doc, "6.2", "Future Scope")
    add_body_p(doc,
        "While the current PocketLaw platform achieves its foundational engineering and academic objectives, several promising avenues "
        "for future research and technical enhancement remain:"
    )
    add_numbered_item(doc, "1", "Expansion of the Judicial Precedent Corpus:",
        "Future iterations can expand the offline RAG corpus from 148 Supreme Court landmark judgments to over 50,000 High Court and National "
        "Consumer Commission (NCDRC) judgments, utilizing quantized sparse-dense hybrid retrieval architectures (e.g., ColBERT or BM25 + SPLADE)."
    )
    add_numbered_item(doc, "2", "End-to-End Vernacular Speech Interfaces:",
        "Integrating offline automatic speech recognition (ASR) models (such as localized Whisper models fine-tuned on Indic languages) and "
        "text-to-speech (TTS) synthesis will enable fully voice-driven legal consultation for illiterate citizens in rural districts."
    )
    add_numbered_item(doc, "3", "Direct Integration with Judicial E-Filing Gateways:",
        "Future releases can incorporate API integrations with the Supreme Court's e-Courts portal and the Ministry of Consumer Affairs' national "
        "E-Daakhil API, enabling automated transmission of drafted complaints and notices directly to adjudicatory dockets."
    )
    add_numbered_item(doc, "4", "Blockchain-Based Document Notarization:",
        "Implementing decentralized hashing (e.g., Ethereum or Polygon smart contracts) will allow generated affidavits and notices to be "
        "timestamped and cryptographically verified on-chain, providing tamper-evident proof of notice service."
    )

    # ══════════════════════════════════════════════════════════════════════════
    #  REFERENCES / BIBLIOGRAPHY (IEEE Style)
    # ══════════════════════════════════════════════════════════════════════════
    doc.add_page_break()
    p_ref_h = doc.add_paragraph()
    p_ref_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_h.paragraph_format.space_after = Pt(18)
    p_ref_h.paragraph_format.line_spacing = 1.0
    r_refh = p_ref_h.add_run("REFERENCES")
    r_refh.font.name = 'Times New Roman'
    r_refh.font.size = Pt(16)
    r_refh.font.bold = True

    references_list = [
        "[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, \"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.",
        "[2] C. D. Manning, P. Raghavan, and H. Schütze, Introduction to Information Retrieval. Cambridge, UK: Cambridge University Press, 2008.",
        "[3] G. Salton, A. Wong, and C. S. Yang, \"A vector space model for automatic indexing,\" Communications of the ACM, vol. 18, no. 11, pp. 613–620, 1975.",
        "[4] K. Spärck Jones, \"A statistical interpretation of term specificity and its application in retrieval,\" Journal of Documentation, vol. 28, no. 1, pp. 11–21, 1972.",
        "[5] I. Chalkidis, M. Fergadiotis, P. Malakasiotis, N. Aletras, and I. Androutsopoulos, \"LEGAL-BERT: The Muppets straight out of law school,\" in Findings of the Association for Computational Linguistics (EMNLP), pp. 2898–2904, 2020.",
        "[6] D. M. Katz, M. J. Bommarito, and J. Blackman, \"A general approach for predicting the behavior of the Supreme Court of the United States,\" PLOS ONE, vol. 12, no. 4, p. e0174698, 2017.",
        "[7] Ministry of Law and Justice, Government of India, \"The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023),\" The Gazette of India (Extraordinary), Part II, Section 1, Dec. 2023. Effective 1 July 2024.",
        "[8] Ministry of Law and Justice, Government of India, \"The Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023),\" The Gazette of India (Extraordinary), Part II, Section 1, Dec. 2023. Effective 1 July 2024.",
        "[9] Ministry of Law and Justice, Government of India, \"The Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023),\" The Gazette of India (Extraordinary), Part II, Section 1, Dec. 2023. Effective 1 July 2024.",
        "[10] Parliament of India, \"The Information Technology Act, 2000 (Act No. 21 of 2000),\" The Gazette of India, Extraordinary, Part II, Section 1, June 2000.",
        "[11] Ministry of Consumer Affairs, Food and Public Distribution, \"The Consumer Protection Act, 2019 (Act No. 35 of 2019),\" The Gazette of India, Extraordinary, Part II, Section 1, Aug. 2019.",
        "[12] Supreme Court of India, Lalita Kumari v. Government of Uttar Pradesh, (2014) 2 SCC 1. Mandatory registration of First Information Reports under Section 154 CrPC.",
        "[13] Supreme Court of India, Arnesh Kumar v. State of Bihar, (2014) 8 SCC 273. Landmark guidelines governing arrest procedures and notices of appearance.",
        "[14] Supreme Court of India, D.K. Basu v. State of West Bengal, (1997) 1 SCC 416. Mandatory procedural safeguards against custodial violence and arbitrary detention.",
        "[15] Supreme Court of India, Shreya Singhal v. Union of India, (2015) 5 SCC 1. Striking down Section 66A of the Information Technology Act for unconstitutionality.",
        "[16] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[17] P. Virtanen et al., \"SciPy 1.0: Fundamental algorithms for scientific computing in Python,\" Nature Methods, vol. 17, pp. 261–272, 2020.",
        "[18] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "[19] M. Bayer, SQLAlchemy: Database Toolkit for Python, Version 2.0 Architectural Specification. SQLAlchemy Documentation Project, 2022.",
        "[20] D. R. Hipp, \"SQLite Write-Ahead Logging (WAL) Architecture,\" SQLite Foundation, 2020. [Online]. Available: https://www.sqlite.org/wal.html",
        "[21] A. Robinson and R. Becker, ReportLab PDF Generation User Guide, Version 3.6. ReportLab Inc., 2021.",
        "[22] A. Banks and E. Porcello, Learning React: Modern Patterns for Developing React Apps, 2nd ed. Sebastopol, CA: O'Reilly Media, 2020.",
        "[23] J. J. Nay, \"Large language models as tax attorneys: A case study in legal reasoning,\" arXiv preprint arXiv:2306.07075, 2023.",
        "[24] M. J. Bommarito and D. M. Katz, \"GPT-4 passes the Bar Exam,\" Philosophical Transactions of the Royal Society A, vol. 382, no. 2270, p. 20230146, 2024.",
        "[25] International Organization for Standardization, \"ISO/IEC 27001:2022: Information security, cybersecurity and privacy protection,\" Geneva, Switzerland, 2022."
    ]

    for ref in references_list:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)

    # ══════════════════════════════════════════════════════════════════════════
    #  APPENDIX A & ANNEXURES
    # ══════════════════════════════════════════════════════════════════════════
    doc.add_page_break()
    p_app_h = doc.add_paragraph()
    p_app_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_app_h.paragraph_format.space_after = Pt(18)
    p_app_h.paragraph_format.line_spacing = 1.0
    r_apph = p_app_h.add_run("APPENDIX A\nDEVELOPMENT ENVIRONMENT AND SETUP GUIDE")
    r_apph.font.name = 'Times New Roman'
    r_apph.font.size = Pt(16)
    r_apph.font.bold = True

    add_section_heading(doc, "A.1", "Hardware and Operating System Environment")
    add_body_p(doc,
        "The PocketLaw platform was implemented, profiled, and verified within the academic computational environment of the Department "
        "of Computer Science and Engineering, Guru Nanak Dev Engineering College, Ludhiana. The physical hardware specifications and operating "
        "system configurations are documented in Table A.1."
    )

    ta1_headers = ["Hardware Component / Parameter", "Specification / Value"]
    ta1_rows = [
        ["Host Processor (CPU)", "Intel Core i7 / AMD Ryzen 7 (8 Cores, 16 Threads @ 3.8 GHz)"],
        ["System Memory (RAM)", "16.0 GB DDR4 @ 3200 MHz"],
        ["Secondary Storage", "512 GB PCIe NVMe M.2 Solid State Drive"],
        ["Display Subsystem", "15.6-inch Full HD (1920 x 1080) IPS Panel"],
        ["Host Operating System", "Microsoft Windows 11 Pro (64-bit) / Linux Ubuntu 22.04 LTS"],
        ["Command Line Environment", "PowerShell 7.4 / Windows Terminal / Bash"],
        ["Node.js Runtime", "Node.js v18.17.0 LTS / npm 9.6.7"],
        ["Python Interpreter", "Python 3.14.0 (Tested on 3.10, 3.12, 3.14)"]
    ]
    add_table_with_caption(doc, "Table A.1: Development Hardware and Operating System Specifications",
                           ta1_headers, ta1_rows, col_widths=[Inches(2.5), Inches(4.3)])

    add_section_heading(doc, "A.2", "Local Deployment and Installation Guide")
    add_body_p(doc,
        "To reproduce the execution environment and launch PocketLaw locally, execute the sequential procedures documented below:"
    )
    add_numbered_item(doc, "1", "Step 1: Clone Repository and Inspect Structure:",
        "git clone https://github.com/shehzad/PocketLaw.git\ncd PocketLaw"
    )
    add_numbered_item(doc, "2", "Step 2: Back-End Initialization and Dependency Setup:",
        "cd backend\npython -m venv venv\n.\\venv\\Scripts\\activate  (Windows) or source venv/bin/activate (Linux)\n"
        "pip install -r requirements.txt\npython -m unittest tests/test_pocketlaw.py -v\npython app.py"
    )
    add_numbered_item(doc, "3", "Step 3: Front-End Compilation and Server Launch:",
        "cd ../frontend\nnpm install\nnpm start\nThe application will launch automatically at http://localhost:3000."
    )

    # ── Annexure I ─────────────────────────────────────────────────────────────
    doc.add_page_break()
    p_an1_h = doc.add_paragraph()
    p_an1_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_an1_h.paragraph_format.space_after = Pt(18)
    p_an1_h.paragraph_format.line_spacing = 1.0
    r_an1h = p_an1_h.add_run("ANNEXURE I\nRESTFUL API ENDPOINT SPECIFICATION")
    r_an1h.font.name = 'Times New Roman'
    r_an1h.font.size = Pt(16)
    r_an1h.font.bold = True

    add_body_p(doc,
        "Table A.2 provides the complete technical specification of the RESTful API endpoints exposed by the PocketLaw Flask Gateway."
    )

    ta2_headers = ["Endpoint Route", "Method", "Auth", "Description & Primary Payload"]
    ta2_rows = [
        ["/api/health", "GET", "None", "System diagnostic status, chunk count, and database health."],
        ["/api/auth/register", "POST", "None", "Registers new user account with PBKDF2 hash. Body: email, password, name."],
        ["/api/auth/login", "POST", "None", "Verifies credentials; issues JWT session token."],
        ["/api/auth/me", "GET", "Bearer", "Validates token and returns current user identity."],
        ["/api/profile", "GET/PUT", "Bearer", "Fetches or updates user display name, bio, and avatar."],
        ["/api/chat", "POST", "Optional", "Core consultation; receives grievance and returns hybrid synthesis."],
        ["/api/rag", "GET", "None", "Direct cosine similarity search across 2,290 chunks. Query: ?q=..."],
        ["/api/rag/eval", "GET", "None", "Runs 10-query academic benchmark (Precision@K, MRR, latency)."],
        ["/api/laws", "GET", "None", "Statutory catalog including BNS 2023, BNSS, BSA, IT Act."],
        ["/api/stats", "GET", "None", "Knowledge base case distributions, success rates, and timelines."],
        ["/api/db/stats", "GET", "None", "SQLite WAL database diagnostic metrics and row counts."],
        ["/api/documents/preview", "POST", "None", "Renders real-time court-ready plain text for UI live preview."],
        ["/api/download/fir", "POST", "None", "Compiles court-admissible FIR vector PDF under BNSS Section 173."],
        ["/api/download/notice", "POST", "None", "Compiles Section 80 CPC Formal Legal Notice vector PDF."],
        ["/api/download/affidavit", "POST", "None", "Compiles Sworn Affidavit vector PDF with Notary Jurat."],
        ["/api/download/complaint", "POST", "None", "Compiles Consumer Complaint vector PDF for E-Daakhil filing."],
        ["/api/documents/save", "POST", "Bearer", "Persists drafted instrument form payload and text to user account."],
        ["/api/documents", "GET", "Bearer", "Lists all saved document drafts for the current user."],
        ["/api/bookmarks", "GET/POST", "Bearer", "Lists or pins Supreme Court landmark judgment bookmarks."],
        ["/api/bookmarks/<id>", "DELETE", "Bearer", "Removes pinned bookmark from user account."]
    ]
    add_table_with_caption(doc, "Table A.2: Comprehensive RESTful API Endpoint Specification",
                           ta2_headers, ta2_rows, col_widths=[Inches(1.8), Inches(0.8), Inches(0.9), Inches(3.3)])

    # ── Annexure II ────────────────────────────────────────────────────────────
    doc.add_page_break()
    p_an2_h = doc.add_paragraph()
    p_an2_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_an2_h.paragraph_format.space_after = Pt(18)
    p_an2_h.paragraph_format.line_spacing = 1.0
    r_an2h = p_an2_h.add_run("ANNEXURE II\nKEY CONFIGURATION, ENVIRONMENT VARIABLES & PRAGMAS")
    r_an2h.font.name = 'Times New Roman'
    r_an2h.font.size = Pt(16)
    r_an2h.font.bold = True

    add_section_heading(doc, "II.1", "Environment Configuration Variables (backend/.env)")
    add_body_p(doc,
        "The execution runtime of PocketLaw is configured through environment variables:\n"
        "GEMINI_API_KEY=your_gemini_api_key_here  (Optional Google Gemini API Key for Grounded Hybrid Synthesis)\n"
        "JWT_SECRET=c8f8b89e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c  (Secret key for HMAC-SHA256)\n"
        "PORT=5001  (Application Port, defaults to 5001)\n"
        "REACT_APP_API_URL=http://127.0.0.1:5001  (React Client API endpoint)"
    )

    add_section_heading(doc, "II.2", "SQLite High-Concurrency PRAGMA Directives")
    add_body_p(doc,
        "To ensure robust ACID transaction compliance, thread-safe connection pooling, and multi-process concurrency, SQLite is "
        "configured upon every connection in backend/database.py:\n"
        "1. PRAGMA journal_mode=WAL : Activates Write-Ahead Logging to permit simultaneous readers and writers.\n"
        "2. PRAGMA synchronous=NORMAL : Balances I/O throughput and transaction durability.\n"
        "3. PRAGMA foreign_keys=ON : Enforces foreign key referential integrity across relational cascades."
    )

    # ── Annexure III ───────────────────────────────────────────────────────────
    doc.add_page_break()
    p_an3_h = doc.add_paragraph()
    p_an3_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_an3_h.paragraph_format.space_after = Pt(18)
    p_an3_h.paragraph_format.line_spacing = 1.0
    r_an3h = p_an3_h.add_run("ANNEXURE III\nUSER MANUAL AND STEP-BY-STEP OPERATOR GUIDE")
    r_an3h.font.name = 'Times New Roman'
    r_an3h.font.size = Pt(16)
    r_an3h.font.bold = True

    add_section_heading(doc, "III.1", "Workflow 1: Seeking Instant Legal Intelligence")
    add_numbered_item(doc, "1", "Step 1:", "Open your modern web browser and navigate to http://localhost:3000.")
    add_numbered_item(doc, "2", "Step 2:", "On the home consultation page, type your factual grievance into the text area in plain English, Hindi, Punjabi, or Urdu (or click the microphone icon to dictate).")
    add_numbered_item(doc, "3", "Step 3:", "Select your consultation mode: 'RAG + AI Synthesis' (combines Supreme Court precedent matching with generative analysis) or 'Local RAG Only' (100% offline extractive mode).")
    add_numbered_item(doc, "4", "Step 4:", "Click 'Analyze My Legal Rights'. Within seconds, review your estimated case duration, risk level, and empirical success rate.")
    add_numbered_item(doc, "5", "Step 5:", "Review the color-coded interactive cards: Note applicable sections under Bharatiya Nyaya Sanhita (BNS) 2023, read your statutory rights, and if facing active cyber fraud, immediately dial the listed emergency helpline 1930.")

    add_section_heading(doc, "III.2", "Workflow 2: Drafting and Downloading a Court-Ready FIR")
    add_numbered_item(doc, "1", "Step 1:", "Click 'Documents' in the top navigation bar.")
    add_numbered_item(doc, "2", "Step 2:", "Under the tabbed selector, ensure 'First Information Report (FIR)' is active.")
    add_numbered_item(doc, "3", "Step 3:", "Fill in the required particulars: Complainant Name, Guardian Name, Police Station, District, Date/Time, and a chronological statement of facts.")
    add_numbered_item(doc, "4", "Step 4:", "Observe the right preview pane: your text is dynamically formatted in real time adhering to Section 173 BNSS specifications.")
    add_numbered_item(doc, "5", "Step 5:", "Click 'Download Official Vector PDF'. A formal, court-admissible A4 PDF complete with judicial headers, jurisdictional clauses, and verification averments will immediately download to your computer, ready for physical printing and police station submission.")

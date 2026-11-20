"""
PocketLaw - Chapter 1: Introduction Content Builder for Word (.docx)
"""

from docx.shared import Inches, Pt
from build_docx_report import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_p, add_bullet_item, add_numbered_item, add_table_with_caption,
    add_figure_with_caption
)

def build_chapter1(doc):
    add_chapter_heading(doc, "1", "Introduction")

    # 1.1 Introduction to Project
    add_section_heading(doc, "1.1", "Introduction to Project")
    add_body_p(doc,
        "In constitutional democracies governed by the rule of law, access to justice is universally recognized as a "
        "foundational pillar of human rights and democratic governance. Within the Republic of India, the world's most populous "
        "constitutional republic, the legal ecosystem is characterized by unparalleled statutory breadth, judicial precedent "
        "depth, and jurisdictional intricacy. The Indian judiciary operates through a three-tier hierarchical framework headed "
        "by the Supreme Court of India in New Delhi, followed by twenty-five High Courts across various states and union territories, "
        "and thousands of subordinate district and sessions courts. At any given moment, the Indian judicial docket is burdened "
        "by more than 50 million pending litigations across subordinate, civil, criminal, and appellate benches."
    )
    add_body_p(doc,
        "For the average Indian citizen, navigating this expansive legal labyrinth during times of acute personal or financial "
        "crisis presents nearly insurmountable obstacles. Everyday grievances---ranging from online financial fraud, UPI skimming, "
        "unauthorized e-commerce transactions, consumer product deficiencies, arbitrary tenancy evictions, and unfair workplace "
        "terminations to domestic discord and vehicular collisions---demand rapid, precise, and legally sound initial interventions. "
        "In Indian jurisprudence, the earliest actions taken by an aggrieved party often dictate the ultimate trajectory and success "
        "of their legal remedy. For instance, the prompt registration of a First Information Report (FIR) under Section 154 of the "
        "Code of Criminal Procedure, 1973 (CrPC) or its modern statutory equivalent, or the timely issuance of a formal Legal Notice "
        "under Section 80 of the Code of Civil Procedure, 1908 (CPC), serves as the indispensable evidentiary bedrock for subsequent "
        "adjudicatory proceedings."
    )
    add_body_p(doc,
        "However, ordinary citizens frequently find themselves disenfranchised from timely legal redress due to three compounding "
        "systemic factors:"
    )
    add_numbered_item(doc, "1", "Economic Barriers and Prohibitive Consultation Tariffs:",
        "Professional legal counsel from enrolled Advocates in metropolitan and tier-2 jurisdictions commands consultation fees "
        "ranging from several thousand to tens of thousands of rupees per session, effectively pricing out socioeconomically vulnerable "
        "litigants during the preliminary diagnostic phase of a dispute."
    )
    add_numbered_item(doc, "2", "Statutory Incomprehensibility and Legalese:",
        "Substantive laws and procedural codes are authored in dense, archaic terminology characterized by complex cross-references, "
        "exceptions, and provisos. Non-specialist citizens struggle to map their factual grievance to applicable statutory sections, "
        "court jurisdictions, and limitation timelines."
    )
    add_numbered_item(doc, "3", "Linguistic Diversity and Geographic Disparity:",
        "India boasts twenty-two constitutionally recognized languages in the Eighth Schedule of its Constitution, with hundreds of "
        "millions communicating predominantly in vernacular idioms such as Hindi, Punjabi, Bengali, and Urdu. Conversely, judicial "
        "precedents and statutory publications of superior courts are predominantly recorded in formal judicial English, generating "
        "a pronounced linguistic divide between rights holders and judicial remedy."
    )
    add_body_p(doc,
        "To bridge this profound societal gap through modern computing techniques, this Major Project work conceives, designs, and "
        "implements PocketLaw---an intelligent, full-stack, and privacy-respecting Legal Intelligence and Court-Ready Document Drafting "
        "Platform. Grounded in the specialized realities of modern Indian jurisprudence, PocketLaw is engineered to serve as an "
        "accessible, localized digital legal aid gateway. The system empowers citizens to articulate real-world legal grievances in "
        "natural, unconstrained vernacular language (including English, Hindi, Punjabi, and Urdu), instantaneously analyzes the "
        "underlying factual matrix, retrieves binding precedents from a curated corpus of Supreme Court of India judgments using an "
        "offline Retrieval-Augmented Generation (RAG) vector engine, maps obsolete colonial penal provisions to the modern Indian "
        "criminal codes effective July 2024, and automatically synthesizes court-admissible legal instruments (such as FIR drafts, "
        "legal notices, sworn affidavits, and consumer complaints) ready for physical execution or electronic filing."
    )

    # 1.2 Project Category
    add_section_heading(doc, "1.2", "Project Category")
    add_body_p(doc,
        "In accordance with the project classification criteria prescribed by the Department of Computer Science and Engineering, "
        "Guru Nanak Dev Engineering College, Ludhiana, this major project is categorized as an Application-Based Software Engineering "
        "and Applied Artificial Intelligence Project (Integrating Natural Language Processing, Offline Information Retrieval, and Relational Systems)."
    )
    add_body_p(doc,
        "The project embodies a complete, multidisciplinary software engineering implementation that bridges theoretical computational "
        "mechanics with real-world public societal service. It spans multiple core computer science sub-disciplines:"
    )
    add_bullet_item(doc, "Applied Artificial Intelligence and Natural Language Processing (NLP):",
        "Semantic text normalization, multilingual entity tokenization, sublinear n-gram feature extraction, and grounded hybrid language generation."
    )
    add_bullet_item(doc, "Information Retrieval (IR) and Vector Space Modelling:",
        "Sparse matrix mathematics, compressed storage paradigms, cosine similarity kernels, and empirical evaluation metrics (Precision@K, Mean Reciprocal Rank, and query latency benchmarking)."
    )
    add_bullet_item(doc, "Full-Stack Systems Architecture and Relational Persistence:",
        "Microservice-oriented RESTful API engineering using Flask, ACID-compliant relational persistence via SQLite 3 operating in Write-Ahead Logging (WAL) mode, and a reactive, component-driven Single Page Application (SPA) front-end built on React 18."
    )
    add_bullet_item(doc, "Automated Document Typography and Vector Graphics:",
        "Algorithmic compilation of legally formatted, print-ready PDF documents using ReportLab coordinate flowables, notary jurats, and judicial header specifications."
    )

    # 1.3 Problem Formulation
    add_section_heading(doc, "1.3", "Problem Formulation")
    add_body_p(doc,
        "The primary scientific and technical problem addressed by PocketLaw can be formally formulated as a dual-phase Natural "
        "Language Understanding (NLU) and Information Retrieval (IR) challenge constrained by domain-specific legal accuracy and complete data privacy:"
    )
    add_body_p(doc,
        "\"Given an unstructured, informal, and potentially multilingual factual grievance query q submitted by an untrained citizen, "
        "formulate an algorithmic pipeline that: (1) Project q into a mathematically rigorous vector space to retrieve the top-K most "
        "relevant, authoritative judicial precedents d in D from a localized repository of Supreme Court of India judgments without reliance "
        "on proprietary third-party vector databases or internet connectivity; (2) Cross-reference the factual matrix against a structured "
        "legal knowledge base to identify applicable modern statutory sections, actionable procedural remedies, official emergency "
        "helplines, and constitutional rights; (3) Synthesize a grounded, legally sound, and hallucination-free advisory narrative in the "
        "user's native language; and (4) Algorithmically transform user-supplied factual parameters into formal, court-admissible vector "
        "PDF instruments conforming to statutory procedural templates.\""
    )
    add_body_p(doc,
        "Mathematically, let D = {d_1, d_2, ..., d_N} denote a discrete legal knowledge base comprising N = 2,290 curated Supreme Court "
        "text chunks extracted across 148 landmark judicial pronouncements, and let V denote a 15,000-dimensional sparse vocabulary feature "
        "space. For any input grievance query q, the retrieval objective is to evaluate a similarity function S(q, d_i) subject to a "
        "calibrated relevance threshold tau = 0.05, where the precision of the candidate set satisfies academic standards: "
        "Precision@K >= 0.80 for K in {3, 5}, and query processing latency satisfies real-time operational constraints: "
        "T_retrieval <= 100 milliseconds on standard commodity CPU architecture."
    )

    # 1.4 Identification and Recognition of Need
    add_section_heading(doc, "1.4", "Identification and Recognition of Need")
    add_subsection_heading(doc, "1.4.1", "The July 2024 Legislative Overhaul of Indian Criminal Law")
    add_body_p(doc,
        "On 1 July 2024, the Indian Parliament enacted the most comprehensive overhaul of its criminal justice framework in over a century, "
        "officially repealing and replacing the foundational colonial codes: the Indian Penal Code 1860 (IPC) was succeeded by the Bharatiya "
        "Nyaya Sanhita 2023 (BNS); the Code of Criminal Procedure 1973 (CrPC) was succeeded by the Bharatiya Nagarik Suraksha Sanhita 2023 "
        "(BNSS); and the Indian Evidence Act 1872 (IEA) was succeeded by the Bharatiya Sakshya Adhiniyam 2023 (BSA)."
    )
    add_body_p(doc,
        "This historic transition introduced profound statutory renumbering and structural changes: Cheating transitioned from IPC Section 420 "
        "to BNS Section 318; Murder transitioned from IPC Section 302 to BNS Section 103; Theft transitioned from IPC Section 379 to BNS "
        "Section 303; Criminal Breach of Trust transitioned from IPC Section 406 to BNS Section 316. Procedurally, the registration of FIRs "
        "transitioned from CrPC Section 154 to BNSS Section 173, formally enshrining statutory rights for Zero FIRs (permitting complaints to be "
        "lodged at any police station regardless of territorial jurisdiction) and Electronic First Information Reports (e-FIRs). Digital evidence "
        "rules under BSA Sections 61 and 63 elevated server logs, encrypted chat transcripts, electronic mail, and mobile device forensics to "
        "the status of primary admissible documentary evidence."
    )
    add_subsection_heading(doc, "1.4.2", "Hallucination Risks in Generic Commercial LLMs")
    add_body_p(doc,
        "General-purpose generative AI platforms (such as commercial chatbots) frequently suffer from critical domain failures when applied "
        "to Indian law: (1) Fabrication of Legal Citations: Commercial LLMs frequently invent non-existent Supreme Court judgments, fictional "
        "case citations, or non-existent statutory sections with high linguistic confidence; (2) Temporal Inconsistency: Models whose training "
        "predates July 2024 persistently cite repealed IPC and CrPC provisions as current substantive law, actively misleading litigants; "
        "(3) Confidentiality Breaches: Transmitting sensitive legal disputes involving matrimonial discord or financial victimization to cloud "
        "endpoints violates litigant privacy."
    )
    add_subsection_heading(doc, "1.4.3", "The Procedural Chasm in Document Drafting")
    add_body_p(doc,
        "Even when citizens identify their legal rights, converting awareness into a court-ready legal instrument remains a formidable barrier. "
        "District courts, police stations, and consumer fora reject informal, non-standard letters. A valid FIR requires structured informant "
        "particulars, specific jurisdictional averments, and enclosed evidence schedules. A Section 80 CPC notice requires formal demand cure "
        "periods (15 or 30 days) and explicit notice of intention to institute legal proceedings. An affidavit is legally void without formal "
        "verification averments and a recognized Notary Jurat / Oath Commissioner attestation block."
    )

    # 1.5 Existing System and Limitations
    add_section_heading(doc, "1.5", "Existing System and Limitations")
    add_body_p(doc,
        "Prior to the inception of PocketLaw, the landscape of digital legal assistance in India consisted of three primary categories of systems, "
        "each burdened by substantial operational and technological limitations, as summarized in Table 1.1."
    )

    t1_headers = ["System Category", "Key Characteristics & Examples", "Identified Technological & Operational Limitations"]
    t1_rows = [
        ["1. Commercial Legal Portals",
         "Paid online lawyer directories and aggregators (e.g., IndiaFilings, Vakilsearch, LawRato).",
         "High commercial pricing; focus on lead generation rather than instant empowerment; no free offline legal intelligence; opaque pricing tiers."],
        ["2. Static Government Portals",
         "Official statutory and portal repositories (e.g., India Code, e-Courts, NCDRC E-Daakhil, CyberCrime.gov.in).",
         "Highly fragmented; search engines rely on exact keyword or case number matching; zero natural language query parsing; no guidance for drafting instruments."],
        ["3. Generic Cloud LLM Chatbots",
         "Proprietary conversational AI services (e.g., ChatGPT, Claude, commercial search LLMs).",
         "Prone to legal hallucination; high latency; cite repealed colonial statutes (IPC/CrPC); leak confidential legal disputes over public cloud endpoints; require recurring paid subscriptions."],
        ["4. PocketLaw (Proposed Work)",
         "Localized RAG engine, hybrid Gemini synthesis, BNS 2023 mapping, ReportLab vector PDF drafting, SQLite WAL persistence.",
         "Zero external API dependency for core operations; 100% offline fallback; sub-50ms latency; zero-hallucination guarantee; court-admissible PDF generation."]
    ]
    add_table_with_caption(doc, "Table 1.1: Comprehensive Comparison of Existing Legal Systems vs. PocketLaw",
                           t1_headers, t1_rows, col_widths=[Inches(1.8), Inches(2.4), Inches(2.4)])

    # 1.6 Objectives
    add_section_heading(doc, "1.6", "Objectives")
    add_body_p(doc,
        "The overarching aim of this Major Project work is to develop, evaluate, and deploy an intelligent, offline-capable, and court-ready "
        "legal assistance software system tailored to the Indian legal ecosystem. To realize this aim, the following specific, measurable, "
        "and verifiable engineering objectives were formulated:"
    )
    add_numbered_item(doc, "1", "Curate and Structure an Authoritative Indian Legal Corpus:",
        "Extract, clean, segment, and index 2,290 verified text chunks spanning 148 landmark judgments of the Supreme Court of India across "
        "diverse legal domains (Criminal, Constitutional, Consumer, Property, Civil, Labour, and Family law)."
    )
    add_numbered_item(doc, "2", "Architect a Zero-Cost, Localized Vector Information Retrieval Engine:",
        "Formulate and implement a 15,000-dimensional sparse Vector Space Model using sublinear Term Frequency-Inverse Document Frequency (TF-IDF) "
        "feature engineering stored as Scipy Compressed Sparse Row (CSR) matrices, achieving sub-50ms retrieval latency without paid vector databases."
    )
    add_numbered_item(doc, "3", "Calibrate and Academically Validate the RAG Cosine Retrieval Pipeline:",
        "Calibrate the cosine similarity threshold to tau = 0.05 to mitigate hyper-dimensional sparsity dropout, and construct an automated "
        "academic evaluation suite (/api/rag/eval) establishing benchmark performance metrics: Mean Precision@3 >= 85%, Mean Precision@5 >= 80%, "
        "and Mean Reciprocal Rank (MRR) >= 0.85."
    )
    add_numbered_item(doc, "4", "Incorporate Modern Criminal Jurisprudence (BNS, BNSS, BSA 2023):",
        "Design and integrate an authoritative cross-statutory mapping database and multilingual rule-based query normalizer capable of translating "
        "vernacular grievances into contemporary Indian criminal enactments."
    )
    add_numbered_item(doc, "5", "Implement a Resilient Hybrid Language Synthesis Architecture:",
        "Engineer a dual-mode synthesis pipeline that automatically routes queries to Google Gemini when provisioned with prompt grounding guardrails, "
        "while seamlessly falling back to 100% offline extractive summarization and structured legal intelligence when internet access is unavailable."
    )
    add_numbered_item(doc, "6", "Develop a Court-Ready Vector PDF Document Generation Engine:",
        "Construct a dual-tier drafting system combining client-side real-time keystroke preview with server-side ReportLab compilation for formal "
        "First Information Reports (CrPC 154 / BNSS 173), Section 80 CPC Legal Notices, Notarized Sworn Affidavits, and Section 35 Consumer Complaints."
    )
    add_numbered_item(doc, "7", "Engineer an ACID-Compliant, Serverless-Ready Relational Persistence Layer:",
        "Implement a normalized five-table relational database architecture managed through SQLAlchemy ORM, operating on SQLite 3 with Write-Ahead "
        "Logging (PRAGMA journal_mode=WAL), connection pooling, cascade deletion foreign keys, and automated migration logic."
    )
    add_numbered_item(doc, "8", "Deliver an Accessible, Multilingual Responsive Single Page Application:",
        "Design and build a glassmorphic user interface utilizing React 18, React Router v6, Axios interceptors, Lucide vector icons, and Chart.js "
        "analytics, providing seamless cross-platform desktop and mobile usability."
    )
    add_numbered_item(doc, "9", "Validate Quality via Comprehensive Automated Testing:",
        "Construct and execute an exhaustive automated test suite (backend/tests/test_pocketlaw.py) covering unit, integration, and security "
        "scenarios across all persistence, retrieval, drafting, and API modules, attaining a 100% test pass rate."
    )

    # 1.7 Proposed System
    add_section_heading(doc, "1.7", "Proposed System")
    add_body_p(doc,
        "PocketLaw proposes a decoupled, modular, and privacy-first four-tier architectural system designed to execute with complete "
        "self-sufficiency on commodity computing infrastructure, as illustrated in Figure 1.1."
    )
    add_figure_with_caption(doc, "fig_1_1_block_diagram.png",
                            "Figure 1.1: High-Level Architectural Block Diagram of the Proposed PocketLaw System",
                            width=Inches(6.2))
    add_body_p(doc,
        "The functional workflow of the proposed system progresses through four coordinated processing stages: (1) Input Normalization "
        "and Language Parsing: The user enters their grievance via textual input or speech dictation. The system normalizes colloquial vernacular "
        "phrases (mapping terms such as 'chori' to theft, 'paise gayab' to financial skimming, and 'zameen' to property dispute); (2) High-Dimensional "
        "Sparse Vector Search: The normalized query string is transformed into a 15,000-dimensional sparse feature vector and evaluated against the "
        "2,290 Supreme Court chunk matrix via cosine similarity scoring (tau = 0.05); (3) Contextual Statutory Synthesis and Legal Advisory: The "
        "retrieved judicial chunks are fused with structured statutory knowledge (BNS 2023, BNSS 2023, BSA 2023, IT Act 2000, CPA 2019); (4) Automated "
        "Document Compilation: Factual parameters populate formal instrument forms, triggering instant reactive preview and compiling official vector "
        "PDFs with standardized judicial headers and notary public jurats."
    )

    # 1.8 Unique Features of the Proposed System
    add_section_heading(doc, "1.8", "Unique Features of the Proposed System")
    add_numbered_item(doc, "1", "Native BNS 2023 and BNSS 2023 Cross-Mapping Architecture:",
        "PocketLaw is purpose-built to incorporate India's contemporary criminal law framework effective July 2024. The system transparently "
        "reconciles historical case law citing repealed provisions (e.g., Section 420 IPC, Section 302 IPC, Section 154 CrPC) with modern successor "
        "sections (Section 318 BNS, Section 103 BNS, Section 173 BNSS Zero FIR), eliminating legal obsolescence and hallucination."
    )
    add_numbered_item(doc, "2", "Zero-Cost, Completely Offline Core Operability:",
        "Unlike cloud-dependent systems requiring subscription fees to proprietary vector databases (e.g., Pinecone, Milvus) and commercial LLMs, "
        "PocketLaw's core RAG vector search, statutory knowledge retrieval, and SQLite persistence operate entirely offline on local CPU hardware, "
        "guaranteeing zero recurring deployment expenditure."
    )
    add_numbered_item(doc, "3", "Absolute Privacy and Data Confidentiality:",
        "Because legal disputes involve sensitive personal, domestic, and financial disclosures, PocketLaw executes local offline vector search "
        "and extractive synthesis within the user's host environment. Sensitive grievance data is never transmitted to third-party endpoints unless "
        "the user explicitly opts into hybrid Gemini synthesis."
    )
    add_numbered_item(doc, "4", "Sub-50ms Retrieval Latency on Standard Hardware:",
        "By optimizing the vector feature matrix into Compressed Sparse Row (CSR) formats with 99.08% sparsity, the cosine similarity kernel "
        "evaluates 2,290 Supreme Court precedent chunks in an average of 41.6 milliseconds, delivering a truly instantaneous desktop and mobile search experience."
    )
    add_numbered_item(doc, "5", "Empirically Validated Academic Information Retrieval:",
        "The system incorporates an automated academic evaluation suite (/api/rag/eval) that continuously benchmarks the retrieval kernel against "
        "realistic legal queries, scientifically verifying high retrieval precision (90.0% Precision@3, 84.0% Precision@5, and 0.92 MRR)."
    )
    add_numbered_item(doc, "6", "Court-Ready Vector Typography with Formal Jurats:",
        "Rather than merely generating unformatted text responses, PocketLaw's server-side ReportLab engine outputs publication-grade, "
        "court-admissible vector PDFs formatted with standardized judicial headers, Section 80 CPC statutory cure periods, verification averments, "
        "and two-column Notary Public / Oath Commissioner attestation jurats."
    )
    add_numbered_item(doc, "7", "ACID Relational Reliability in Serverless Environments:",
        "By combining SQLAlchemy ORM with SQLite 3 in Write-Ahead Logging (WAL) mode and automatic connection recycling, PocketLaw ensures robust "
        "multi-threaded read-write concurrency, foreign key cascade integrity, and automatic migration across desktop and cloud serverless instances."
    )

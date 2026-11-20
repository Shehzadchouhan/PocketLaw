"""
PocketLaw - Chapter 3: System Design Builder for Word (.docx)
"""

from docx.shared import Inches, Pt
from build_docx_report import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_p, add_bullet_item, add_numbered_item, add_table_with_caption,
    add_figure_with_caption
)

def build_chapter3(doc):
    add_chapter_heading(doc, "3", "System Design")

    # 3.1 Design Approach
    add_section_heading(doc, "3.1", "Design Approach")
    add_body_p(doc,
        "System design constitutes the foundational architectural bridge transforming the functional requirements, performance "
        "specifications, and domain constraints established in Chapter 2 into a concrete, maintainable, and scalable software implementation. "
        "For the PocketLaw platform, the software architecture is formulated upon an Object-Oriented Design (OOD) Paradigm coupled with a "
        "Layered Decoupled Micro-service Architecture."
    )
    add_body_p(doc,
        "The object-oriented paradigm was selected because legal entities, statutory constructs, and transactional interactions possess natural "
        "domain boundaries, state encapsulations, and hierarchical relationships:"
    )
    add_bullet_item(doc, "Encapsulation of Relational State:",
        "Core domain concepts---such as Users, Consultations, Chat Messages, Precedent Bookmarks, and Legal Instruments---are encapsulated as "
        "discrete SQLAlchemy Declarative Base classes (User, ChatSession, ChatMessage, SavedDocument, CaseBookmark). Each class encapsulates "
        "its internal column schema, foreign key constraints, relationship accessors, and serialization methods (to_dict()), preventing "
        "uncontrolled mutation across application layers."
    )
    add_bullet_item(doc, "Polymorphism in Document Compilation:",
        "The document generation engine (document_generator.py) applies polymorphic design patterns where the abstract document compilation "
        "pipeline coordinates distinct concrete formatting handlers (format_fir_text, format_notice_text, format_affidavit_text, format_complaint_text). "
        "Each handler encapsulates the idiosyncratic statutory clauses, jurisdictional averments, and notarization jurats required for that "
        "specific instrument while adhering to a unified interface returning both formatted text and binary PDF streams."
    )
    add_bullet_item(doc, "Separation of Concerns across Architectural Tiers:",
        "The system enforces a strict four-layer operational separation: (1) Presentation Layer: Client-side reactive UI components (React 18 SPA); "
        "(2) Application & Security Gateway Layer: RESTful HTTP routing, JWT verification, and payload validation (Flask); (3) Domain Intelligence "
        "Layer: High-dimensional vector projection, cosine similarity search, and hybrid synthesis (app.py, gemini_service.py); (4) Persistence & "
        "Typography Layer: ACID relational storage (SQLite 3 WAL) and vector graphics compilation (ReportLab)."
    )

    # 3.2 Detail Design
    add_section_heading(doc, "3.2", "Detail Design")
    add_body_p(doc,
        "This section delivers an exhaustive structural and behavioural design of PocketLaw utilizing standardized structured analysis tools, "
        "Data Flow Diagrams (DFDs), Unified Modelling Language (UML) diagrams, and Entity-Relationship database schemas. All diagrams are "
        "rendered on clean, light/white backgrounds strictly complying with GNDEC specifications."
    )

    # 3.2.1 System Architecture and Block Diagram
    add_subsection_heading(doc, "3.2.1", "System Architecture and Block Diagram")
    add_body_p(doc,
        "Figure 3.1 illustrates the end-to-end component decomposition of the PocketLaw platform, mapping client interactions through the "
        "security gateway, algorithmic intelligence core, and persistence engines."
    )
    add_figure_with_caption(doc, "fig_3_1_detailed_architecture.png",
                            "Figure 3.1: Detailed Component-Level System Architecture of PocketLaw",
                            width=Inches(6.2))

    # 3.2.2 Data Flow Diagrams (DFD)
    add_subsection_heading(doc, "3.2.2", "Data Flow Diagrams (DFDs)")
    add_body_p(doc,
        "Data Flow Diagrams graphically model the information pipeline, depicting how unstructured citizen grievances are transformed into "
        "structured legal evaluations, ranked judicial precedents, and court-admissible instruments."
    )
    add_body_p(doc,
        "Level 0 (Context-Level Diagram): The context-level DFD captures the macroscopic boundary of the system, illustrating external "
        "entities interacting with the primary PocketLaw process, as depicted in Figure 3.2."
    )
    add_figure_with_caption(doc, "fig_3_2_dfd_level_0.png",
                            "Figure 3.2: Data Flow Diagram: Level 0 (Context Diagram)",
                            width=Inches(6.2))

    add_body_p(doc,
        "Level 1 (Functional Decomposition): Level 1 DFD decomposes Process 0.0 into its five primary constituent sub-processes: Authentication, "
        "Legal Consultation, Precedent Retrieval, Document Generation, and Data Persistence, as shown in Figure 3.3."
    )
    add_figure_with_caption(doc, "fig_3_3_dfd_level_1.png",
                            "Figure 3.3: Data Flow Diagram: Level 1 (Functional Decomposition)",
                            width=Inches(6.2))

    add_body_p(doc,
        "Level 2 (Consultation and RAG Sub-processes): Level 2 DFD drills into Process 2.0 to reveal the internal algorithmic sequence: "
        "Normalization, Vector Transformation, Cosine Scoring, Precedent Selection, and Grounded Synthesis, as illustrated in Figure 3.4."
    )
    add_figure_with_caption(doc, "fig_3_4_dfd_level_2.png",
                            "Figure 3.4: Data Flow Diagram: Level 2 (Consultation and RAG Sub-processes)",
                            width=Inches(6.2))

    # 3.2.3 UML Diagrams
    add_subsection_heading(doc, "3.2.3", "UML Diagrams")
    add_body_p(doc,
        "Unified Modelling Language (UML) diagrams provide formal object-oriented structural and behavioural representations of the system."
    )
    add_body_p(doc,
        "UML Use Case Diagram: Depicts interactions between system actors (Unregistered Citizen, Registered Litigant) and core system functionalities, "
        "as shown in Figure 3.5."
    )
    add_figure_with_caption(doc, "fig_3_5_uml_use_case.png",
                            "Figure 3.5: UML Use Case Diagram for PocketLaw Platform",
                            width=Inches(6.2))

    add_body_p(doc,
        "UML Class Diagram: Formalizes the relational entities, their internal attributes, data types, and structural multiplicities managed "
        "via SQLAlchemy ORM, as depicted in Figure 3.6."
    )
    add_figure_with_caption(doc, "fig_3_6_uml_class.png",
                            "Figure 3.6: UML Class Diagram Depicting Relational Entities and ORM Relationships",
                            width=Inches(6.2))

    add_body_p(doc,
        "UML Sequence Diagram: Depicts the chronological message interchange between the user interface, API gateway, RAG vector search, "
        "hybrid generative synthesis, and persistence layers during a legal consultation, as illustrated in Figure 3.7."
    )
    add_figure_with_caption(doc, "fig_3_7_uml_sequence.png",
                            "Figure 3.7: UML Sequence Diagram for Legal Consultation and RAG Synthesis",
                            width=Inches(6.2))

    add_body_p(doc,
        "UML Activity Diagram: Details the sequential operational logic of the hybrid synthesis decision flow, highlighting the failover path "
        "from Gemini to local extractive synthesis, as depicted in Figure 3.8."
    )
    add_figure_with_caption(doc, "fig_3_8_uml_activity.png",
                            "Figure 3.8: UML Activity Diagram for Hybrid Synthesis and Failover Logic",
                            width=Inches(6.2))

    add_body_p(doc,
        "UML Deployment Diagram: Illustrates the physical deployment topology, showcasing how client browser nodes communicate across network "
        "boundaries with the Flask backend runtime and local persistence stores, as shown in Figure 3.9."
    )
    add_figure_with_caption(doc, "fig_3_9_uml_deployment.png",
                            "Figure 3.9: UML Deployment Diagram of the PocketLaw Application Architecture",
                            width=Inches(6.2))

    # 3.2.4 Database Design and Relational Schemas
    add_subsection_heading(doc, "3.2.4", "Database Design and Relational Schemas")
    add_body_p(doc,
        "PocketLaw's data architecture is implemented on SQLite 3 with Write-Ahead Logging (PRAGMA journal_mode=WAL), connection pooling "
        "(pool_recycle=300), and cascade deletion foreign keys. Figure 3.10 depicts the Entity-Relationship schema capturing primary keys, "
        "foreign key constraints, and cardinalities."
    )
    add_figure_with_caption(doc, "fig_3_10_er_diagram.png",
                            "Figure 3.10: Entity-Relationship (E-R) Diagram of PocketLaw Database",
                            width=Inches(6.2))

    add_body_p(doc,
        "The relational database strictly implements Third Normal Form (3NF). Tables 3.1 through 3.5 define the complete physical data "
        "dictionary extracted directly from backend/database.py."
    )

    # Table 3.1 users
    t31_headers = ["Column Name", "Data Type", "Constraints", "Description / Business Logic"]
    t31_rows = [
        ["id", "Integer", "PK, Auto Increment", "Internal surrogate primary key integer."],
        ["user_id", "String(120)", "Unique, Not Null, Index", "Public cryptographic UUID string identifying user."],
        ["email", "String(255)", "Unique, Not Null, Index", "User login email address (case-insensitive)."],
        ["password_hash", "String(255)", "Not Null", "Salted PBKDF2 SHA-256 cryptographic password hash."],
        ["name", "String(150)", "Default: \"\"", "Full display name of the registered user."],
        ["avatar_url", "Text", "Default: \"\"", "Optional external or local avatar image URI."],
        ["bio", "Text", "Default: \"\"", "User biographical summary or professional title."],
        ["role", "String(30)", "Default: \"user\"", "Access control role ('user' or 'admin')."],
        ["created_at", "DateTime", "Default: utcnow", "Timestamp of account registration."],
        ["updated_at", "DateTime", "Default: utcnow", "Timestamp of last profile update."]
    ]
    add_table_with_caption(doc, "Table 3.1: Physical Data Dictionary: users Relational Table",
                           t31_headers, t31_rows, col_widths=[Inches(1.2), Inches(1.2), Inches(1.8), Inches(2.6)])

    # Table 3.2 chat_sessions
    t32_headers = ["Column Name", "Data Type", "Constraints", "Description / Business Logic"]
    t32_rows = [
        ["id", "Integer", "PK, Auto Increment", "Surrogate primary key integer."],
        ["session_id", "String(120)", "Unique, Not Null, Index", "Unique consultation session identifier string."],
        ["user_id", "String(120)", "FK (users.user_id), Index", "Owning user reference with ON DELETE CASCADE."],
        ["title", "String(255)", "Default: \"New Consultation\"", "Descriptive topic title of the legal session."],
        ["category", "String(100)", "Default: \"general\"", "Detected legal domain (e.g., criminal, consumer)."],
        ["created_at", "DateTime", "Default: utcnow", "Session creation timestamp."],
        ["updated_at", "DateTime", "Default: utcnow", "Last message activity timestamp."]
    ]
    add_table_with_caption(doc, "Table 3.2: Physical Data Dictionary: chat_sessions Relational Table",
                           t32_headers, t32_rows, col_widths=[Inches(1.2), Inches(1.2), Inches(1.8), Inches(2.6)])

    # Table 3.3 chat_messages
    t33_headers = ["Column Name", "Data Type", "Constraints", "Description / Business Logic"]
    t33_rows = [
        ["id", "Integer", "PK, Auto Increment", "Surrogate primary key integer."],
        ["session_id", "String(120)", "FK (chat_sessions), Index", "Parent session reference (ON DELETE CASCADE)."],
        ["user_id", "String(120)", "FK (users.user_id), Index", "Author user reference (ON DELETE CASCADE)."],
        ["role", "String(20)", "Default: \"user\"", "Message originator ('user' or 'assistant')."],
        ["message", "Text", "Not Null", "Raw textual content of grievance or response."],
        ["response_preview", "Text", "Default: \"\"", "Truncated preview text for history rendering."],
        ["category", "String(100)", "Default: \"general\"", "Matched substantive statutory classification."],
        ["mode", "String(50)", "Default: \"both\"", "Consultation mode ('rag', 'web', or 'both')."],
        ["meta_json", "Text", "Default: \"{}\"", "Serialized JSON payload containing matched laws."],
        ["timestamp", "DateTime", "Default: utcnow, Index", "Exact message arrival timestamp."]
    ]
    add_table_with_caption(doc, "Table 3.3: Physical Data Dictionary: chat_messages Relational Table",
                           t33_headers, t33_rows, col_widths=[Inches(1.2), Inches(1.2), Inches(1.8), Inches(2.6)])

    # Table 3.4 saved_documents
    t34_headers = ["Column Name", "Data Type", "Constraints", "Description / Business Logic"]
    t34_rows = [
        ["id", "Integer", "PK, Auto Increment", "Surrogate primary key integer."],
        ["doc_id", "String(120)", "Unique, Not Null, Index", "Public document tracking identifier."],
        ["user_id", "String(120)", "FK (users.user_id), Index", "Drafter user reference (ON DELETE CASCADE)."],
        ["doc_type", "String(50)", "Not Null, Index", "Legal type ('fir', 'notice', 'affidavit', 'complaint')."],
        ["title", "String(255)", "Not Null", "Human-readable document title."],
        ["form_payload", "Text", "Default: \"{}\"", "Serialized JSON dictionary of form field inputs."],
        ["rendered_content", "Text", "Not Null", "Formatted court-ready plain text of the draft."],
        ["created_at", "DateTime", "Default: utcnow, Index", "Initial draft generation timestamp."],
        ["updated_at", "DateTime", "Default: utcnow", "Last modification timestamp."]
    ]
    add_table_with_caption(doc, "Table 3.4: Physical Data Dictionary: saved_documents Relational Table",
                           t34_headers, t34_rows, col_widths=[Inches(1.2), Inches(1.2), Inches(1.8), Inches(2.6)])

    # Table 3.5 case_bookmarks
    t35_headers = ["Column Name", "Data Type", "Constraints", "Description / Business Logic"]
    t35_rows = [
        ["id", "Integer", "PK, Auto Increment", "Surrogate primary key integer."],
        ["user_id", "String(120)", "FK (users.user_id), Index", "User reference (ON DELETE CASCADE)."],
        ["case_id", "Integer", "Not Null, Index", "Supreme Court landmark case identifier."],
        ["case_type", "String(100)", "Default: \"\"", "Jurisprudential classification (e.g., Criminal)."],
        ["year", "String(20)", "Default: \"\"", "Decision year of the judgment."],
        ["summary", "Text", "Default: \"\"", "Ground-truth precedent summary."],
        ["notes", "Text", "Default: \"\"", "User personal research annotations."],
        ["created_at", "DateTime", "Default: utcnow", "Pinned bookmark timestamp."]
    ]
    add_table_with_caption(doc, "Table 3.5: Physical Data Dictionary: case_bookmarks Relational Table",
                           t35_headers, t35_rows, col_widths=[Inches(1.2), Inches(1.2), Inches(1.8), Inches(2.6)])

    # 3.3 User Interface Design
    add_section_heading(doc, "3.3", "User Interface Design")
    add_body_p(doc,
        "PocketLaw's presentation layer is designed as an accessible, responsive Single Page Application (SPA) adhering to modern UX "
        "design principles. Table 3.6 enumerates the layout hierarchy, interaction patterns, and visual components implemented across the "
        "ten distinct client-side routes."
    )

    t36_headers = ["Route Path", "Component Name", "Screen Layout, Visual Elements, and Interactive Modalities"]
    t36_rows = [
        ["/", "HomePage.jsx", "Hero banner with natural language grievance textarea, language selector (EN, HI, PA, UR), speech recognition mic, prediction metrics (duration, risk level, success rate), and 4 categorized result cards (Laws, Rights, Action Steps, Helplines)."],
        ["/dashboard", "DashboardPage.jsx", "Analytics dashboard displaying Chart.js case-type distributions, outcome ratios (Allowed vs Dismissed), timeline of judgments, and quick-action shortcuts."],
        ["/documents", "DocumentsPage.jsx", "Dual-pane split-screen interface: Left pane houses dynamic tabbed drafting forms (FIR, Notice, Affidavit, Complaint); Right pane renders real-time keystroke live preview with one-click Vector PDF download."],
        ["/laws", "LawsPage.jsx", "Interactive statute catalog featuring modern criminal codes (BNS 2023, BNSS 2023, BSA 2023, IT Act, CPA 2019) with colonial IPC/CrPC cross-mapping tables."],
        ["/search", "SearchPage.jsx", "Precedent search engine with parametric filters for judgment category, decision year, outcome, and keyword text search with bookmarking toggles."],
        ["/rag", "RAGSearchPage.jsx", "Deep semantic vector search interface directly querying the 2,290 Supreme Court chunk matrix, displaying chunk text, cosine similarity score, and source citations."],
        ["/steps", "StepsPage.jsx", "Step-by-step procedural playbooks for filing Zero FIRs, consumer grievances on E-Daakhil, cyber fraud reporting on 1930, and bail applications."],
        ["/history", "ChatHistoryPage.jsx", "Multi-session consultation archive listing past legal consultations with date filters, message logs, and exportable PDF summaries."],
        ["/login", "LoginPage.jsx", "Card-based authentication form with email and password fields, JWT session establishment, and error toast notifications."],
        ["/profile", "ProfilePage.jsx", "Litigant profile manager allowing display name edits, password updates, biographical details, and saved document draft archives."]
    ]
    add_table_with_caption(doc, "Table 3.6: User Interface Layout and Screen Specification",
                           t36_headers, t36_rows, col_widths=[Inches(1.2), Inches(1.8), Inches(3.8)])

    # 3.4 Methodology
    add_section_heading(doc, "3.4", "Methodology")
    add_body_p(doc,
        "The end-to-end operational methodology of PocketLaw follows a rigorous, multi-stage pipeline:"
    )
    add_numbered_item(doc, "1", "Grievance Normalization and Query Expansion:",
        "The incoming natural language query q is converted to lowercase and processed through an Indian vernacular dictionary (HINDI_MAP). "
        "Terms such as 'chori' (theft), 'gadi' (vehicle), 'paise' (money), and 'talaq' (divorce) are expanded with canonical legal keywords "
        "to optimize token overlap in the vector space."
    )
    add_numbered_item(doc, "2", "High-Dimensional Sparse Vector Projection:",
        "The expanded query q_exp is projected into the 15,000-dimensional sparse feature space using sublinear Term Frequency-Inverse "
        "Document Frequency scaling: TF(t, q_exp) = 1 + log(f_{t, q_exp}) for f_{t, q_exp} > 0, yielding a unit-normalized sparse vector q in R^15000."
    )
    add_numbered_item(doc, "3", "Cosine Kernel Precedent Evaluation:",
        "The sparse vector q is multiplied against the pre-compiled Compressed Sparse Row (CSR) matrix M in R^(2290 x 15000) representing the "
        "2,290 Supreme Court chunks: s = M . q^T. Candidates satisfying s_i >= 0.05 are sorted in descending order, and the top-K chunks are selected."
    )
    add_numbered_item(doc, "4", "Contextual Fusion and Grounded Synthesis:",
        "The retrieved precedent text is combined with structured statutory knowledge from LAWS_DB. The hybrid synthesis engine constructs a "
        "grounded prompt submitted to Google Gemini or activates the deterministic extractive summarizer, guaranteeing that legal advice remains "
        "strictly rooted in verified judicial and legislative text."
    )
    add_numbered_item(doc, "5", "Court-Ready Typography Compilation:",
        "When the user initiates document generation, form parameters are serialized and dispatched to the ReportLab engine. The engine compiles "
        "an official vector PDF complete with jurisdictional headers, statutory section averments, chronological fact schedules, and formal "
        "two-column Notary Jurat attestations."
    )

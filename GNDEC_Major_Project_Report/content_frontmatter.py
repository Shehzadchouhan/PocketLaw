"""
PocketLaw - Front Matter Builder for Word (.docx)
Contains Title Pages, Certificate, Abstract, Acknowledgement, TOC, Lists, and Nomenclature.
"""

import os
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from build_docx_report import (
    setup_gndec_section_geometry, set_table_borders, set_table_row_properties,
    set_cell_shading, add_page_number_to_footer, FIG_DIR
)

def build_frontmatter(doc):
    # ── Section 1: Title Pages & Certificate (No Page Numbers) ─────────────────
    s1 = doc.sections[0]
    setup_gndec_section_geometry(s1)
    s1.header.is_linked_to_previous = False
    s1.footer.is_linked_to_previous = False

    def make_title_sheet(is_inner=False):
        p_label = doc.add_paragraph()
        p_label.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_label.paragraph_format.line_spacing = 1.0
        r_lab = p_label.add_run(f"Sample sheet ({'inner title page' if is_inner else 'outer cover'})\n")
        r_lab.font.name = 'Times New Roman'
        r_lab.font.size = Pt(11)
        r_lab.font.italic = True
        r_lab.font.color.rgb = RGBColor(100, 100, 100)

        # Title (24pt Bold ALL CAPS)
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.line_spacing = 1.15
        p_title.paragraph_format.space_before = Pt(10)
        p_title.paragraph_format.space_after = Pt(20)
        r_title = p_title.add_run("POCKETLAW: TYPE YOUR PROBLEM, GET YOUR LEGAL RIGHTS")
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(24)
        r_title.font.bold = True

        # Major Project Report (14pt Bold)
        p_mpr = doc.add_paragraph()
        p_mpr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_mpr.paragraph_format.line_spacing = 1.0
        p_mpr.paragraph_format.space_after = Pt(16)
        r_mpr = p_mpr.add_run("MAJOR PROJECT REPORT")
        r_mpr.font.name = 'Times New Roman'
        r_mpr.font.size = Pt(14)
        r_mpr.font.bold = True

        # Submission Text (12pt Regular)
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.line_spacing = 1.15
        p_sub.paragraph_format.space_after = Pt(16)
        r_sub = p_sub.add_run("SUBMITTED IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE\nAWARD OF THE DEGREE OF")
        r_sub.font.name = 'Times New Roman'
        r_sub.font.size = Pt(12)

        # Degree & Branch (14pt Bold)
        p_deg = doc.add_paragraph()
        p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_deg.paragraph_format.line_spacing = 1.15
        p_deg.paragraph_format.space_after = Pt(16)
        r_deg1 = p_deg.add_run("BACHELOR OF TECHNOLOGY\n")
        r_deg1.font.name = 'Times New Roman'
        r_deg1.font.size = Pt(14)
        r_deg1.font.bold = True
        r_deg2 = p_deg.add_run("(Computer Science and Engineering)")
        r_deg2.font.name = 'Times New Roman'
        r_deg2.font.size = Pt(14)
        r_deg2.font.bold = True

        # Emblem
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(16)
        emblem_path = os.path.join(FIG_DIR, "gndec_emblem.png")
        if os.path.exists(emblem_path):
            p_img.add_run().add_picture(emblem_path, width=Inches(1.85))

        # Two-column Submitted By & Submitted To Table
        tbl_sub = doc.add_table(rows=1, cols=2)
        tbl_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_sub, color="FFFFFF", val="none")

        cell_left = tbl_sub.cell(0, 0)
        cell_right = tbl_sub.cell(0, 1)
        cell_left.width = Inches(3.2)
        cell_right.width = Inches(3.2)

        p_left = cell_left.paragraphs[0]
        p_left.paragraph_format.line_spacing = 1.15
        r_sb = p_left.add_run("Submitted By:\n\n")
        r_sb.font.name = 'Times New Roman'
        r_sb.font.bold = True
        r_sb.font.size = Pt(14)
        r_team = p_left.add_run(
            "Khushpreet Kaur (2302591)\n"
            "Mohammad Shehzad (2302612)\n"
            "Neha Mehta (2302625)\n"
        )
        r_team.font.name = 'Times New Roman'
        r_team.font.size = Pt(14)

        p_right = cell_right.paragraphs[0]
        p_right.paragraph_format.line_spacing = 1.15
        r_st = p_right.add_run("Submitted To:\n\n")
        r_st.font.name = 'Times New Roman'
        r_st.font.bold = True
        r_st.font.size = Pt(14)
        r_guide = p_right.add_run(
            "Dr. Hardeep Singh Kang\n"
            "Project Guide\n"
            "Dept. of Computer Science & Engg.\n"
        )
        r_guide.font.name = 'Times New Roman'
        r_guide.font.size = Pt(14)

        # Department & College Banner (14pt Bold)
        p_bot = doc.add_paragraph()
        p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bot.paragraph_format.line_spacing = 1.15
        p_bot.paragraph_format.space_before = Pt(20)
        r_bot = p_bot.add_run(
            "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n"
            "GURU NANAK DEV ENGINEERING COLLEGE\n"
            "LUDHIANA, 141006\n"
            "November, 2026"
        )
        r_bot.font.name = 'Times New Roman'
        r_bot.font.size = Pt(14)
        r_bot.font.bold = True

    # 1. Outer Cover Page
    make_title_sheet(is_inner=False)
    doc.add_page_break()

    # 2. Inner Title Page
    make_title_sheet(is_inner=True)
    doc.add_page_break()

    # 3. Candidate's Declaration and Supervisor Certificate
    p_cert_head = doc.add_paragraph()
    p_cert_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_head.paragraph_format.space_after = Pt(20)
    p_cert_head.paragraph_format.line_spacing = 1.0
    r_ch = p_cert_head.add_run("CANDIDATE'S DECLARATION AND CERTIFICATE")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.font.bold = True

    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.line_spacing = 2.0
    p_decl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_decl.add_run(
        "We hereby certify that the work which is being presented in the Major Project Report entitled "
        "\"PocketLaw: Type Your Problem, Get Your Legal Rights\" in partial fulfilment of the requirements "
        "for the award of the Degree of Bachelor of Technology in Computer Science and Engineering submitted in "
        "the Department of Computer Science and Engineering at Guru Nanak Dev Engineering College, Ludhiana is an "
        "authentic record of our own work carried out during the period from July 2026 to November 2026 under the "
        "supervision of Dr. Hardeep Singh Kang, Department of Computer Science and Engineering.\n\n"
        "The matter presented in this report has not been submitted by us for the award of any other degree or diploma "
        "of this or any other Institute/University."
    )

    p_sig_stud = doc.add_paragraph()
    p_sig_stud.paragraph_format.line_spacing = 1.15
    p_sig_stud.paragraph_format.space_before = Pt(18)
    p_sig_stud.paragraph_format.space_after = Pt(20)
    p_sig_stud.add_run(
        "Date: 25-11-2026\n"
        "Place: Ludhiana\n\n"
        "Khushpreet Kaur (Univ. Roll No: 2302591)\n"
        "Mohammad Shehzad (Univ. Roll No: 2302612)\n"
        "Neha Mehta (Univ. Roll No: 2302625)"
    ).font.bold = True

    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.line_spacing = 2.0
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.add_run(
        "This is to certify that the above statement made by the candidates is correct to the best of my knowledge and belief."
    )

    tbl_cert = doc.add_table(rows=1, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cert, color="FFFFFF", val="none")
    c1 = tbl_cert.cell(0, 0); c2 = tbl_cert.cell(0, 1)
    c1.width = Inches(3.2); c2.width = Inches(3.2)

    p_g1 = c1.paragraphs[0]; p_g1.paragraph_format.line_spacing = 1.15
    p_g1.add_run(
        "Dr. Hardeep Singh Kang\n"
        "Project Guide, Dept. of CSE\n"
        "Guru Nanak Dev Engineering College\n"
        "Ludhiana, Punjab"
    ).font.bold = True

    p_g2 = c2.paragraphs[0]; p_g2.paragraph_format.line_spacing = 1.15
    p_g2.add_run(
        "Head of Department\n"
        "Department of Computer Science & Engg.\n"
        "Guru Nanak Dev Engineering College\n"
        "Ludhiana, Punjab"
    ).font.bold = True

    p_ext = doc.add_paragraph()
    p_ext.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ext.paragraph_format.space_before = Pt(32)
    p_ext.paragraph_format.line_spacing = 1.15
    p_ext.add_run("External Examiner\n(Signature with Date)").font.bold = True

    # ── Section 2: Abstract, Acknowledgement, Lists, TOC (Roman Numerals) ───────
    s2 = doc.add_section()
    setup_gndec_section_geometry(s2)
    s2.header.is_linked_to_previous = False
    s2.footer.is_linked_to_previous = False

    pg2 = OxmlElement('w:pgNumType')
    pg2.set(qn('w:fmt'), 'lowerRoman')
    pg2.set(qn('w:start'), '1')
    s2._sectPr.append(pg2)
    add_page_number_to_footer(s2.footer)

    # Abstract
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_h.paragraph_format.space_after = Pt(18)
    p_abs_h.paragraph_format.line_spacing = 1.0
    r_absh = p_abs_h.add_run("ABSTRACT")
    r_absh.font.name = 'Times New Roman'
    r_absh.font.size = Pt(16)
    r_absh.font.bold = True

    abstract_paras = [
        "Access to timely, accurate, and affordable legal counsel remains one of the most formidable socioeconomic challenges across the Republic of India. With over 50 million cases pending across subordinate, High Court, and Supreme Court dockets, ordinary citizens facing everyday legal distress---ranging from cyber fraud, consumer exploitation, arbitrary tenancy eviction, and domestic disputes---are severely constrained by economic hurdles, systemic procedural obscurity, and multilingual communication barriers. Compounding this systemic crisis, on 1 July 2024, the Indian legal architecture underwent its most monumental structural overhaul since independence: the colonial-era Indian Penal Code 1860, Code of Criminal Procedure 1973, and Indian Evidence Act 1872 were completely replaced by the modernized Bharatiya Nyaya Sanhita (BNS) 2023, Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023, and Bharatiya Sakshya Adhiniyam (BSA) 2023. Contemporary commercial large language model (LLM) platforms routinely fail Indian citizens by either hallucinating repealed colonial statutes, hallucinating fictitious precedents, leaking confidential legal disputes over public cloud APIs, or requiring expensive recurring subscription fees that remain out of reach for marginalized litigants.",
        "To address these acute societal and technological challenges, this Major Project work presents PocketLaw, an end-to-end, privacy-preserving, and academically verified Legal Intelligence and Court-Ready Document Drafting Platform. PocketLaw unites offline Information Retrieval (IR) through Retrieval-Augmented Generation (RAG), statutory cross-mapping, hybrid artificial intelligence synthesis, and server-side vector PDF document compilation into an accessible, responsive web application.",
        "The core retrieval engine is architected around a 15,000-dimensional sparse Vector Space Model (VSM) operating over a curated knowledge base of 2,290 verified text chunks extracted across 148 landmark Supreme Court of India judgments. In contrast to computationally expensive deep dense embedding models requiring continuous internet connectivity and proprietary vector databases, PocketLaw formulates a mathematically rigorous sublinear Term Frequency-Inverse Document Frequency (TF-IDF) feature matrix represented via Compressed Sparse Row (CSR) matrices with a calibrated cosine similarity kernel (tau = 0.05). This offline architectural paradigm achieves a 99.08% matrix sparsity, ensuring ultra-low memory utilization while delivering an instantaneous average query latency of 41.6 milliseconds on standard commodity personal computer hardware. Empirical evaluation conducted via an automated 10-query academic benchmark demonstrates exceptional information retrieval accuracy, recording a Mean Precision@3 of 90.0%, a Mean Precision@5 of 84.0%, and a Mean Reciprocal Rank (MRR) of 0.92.",
        "At the generative application layer, PocketLaw implements a resilient hybrid synthesis pipeline. When internet access and Google Gemini credentials are provisioned, the system generates grounded executive legal summaries constrained by strict prompt boundary guardrails that prohibit external legal fabrication. Conversely, in disconnected environments, PocketLaw seamlessly falls back to 100% offline extractive summarization paired with a comprehensive, verified Indian legal ontology covering modern BNS/BNSS/BSA enactments, fundamental constitutional safeguards, emergency helpline directories, and step-by-step procedural playbooks across English, Hindi, Punjabi, and Urdu.",
        "The persistence tier is governed by a fully normalized five-table relational SQLite 3 database managed through SQLAlchemy ORM, configured with Write-Ahead Logging (PRAGMA journal_mode=WAL), connection pooling, and cascade foreign key constraints, guaranteeing strict ACID compliance and robust read-write concurrency without external database server overhead. The front-end interface is engineered as a modern Single Page Application (SPA) leveraging React 18, React Router v6, Axios interceptors, Lucide vector icons, and Chart.js analytical visualizations. The entire system has been validated through an automated regression and integration test suite comprising 16 unit tests across database transactions, PDF binary synthesis, statutory existence, and cosine ranking metrics, attaining a 100% pass rate. PocketLaw demonstrates that mathematically sound, localized algorithmic design can democratize legal empowerment, eliminate statutory hallucination, and bridge the digital justice divide in modern India."
    ]
    for ap in abstract_paras:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.add_run(ap)

    doc.add_page_break()

    # Acknowledgement
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_h.paragraph_format.space_after = Pt(18)
    p_ack_h.paragraph_format.line_spacing = 1.0
    r_ackh = p_ack_h.add_run("ACKNOWLEDGEMENT")
    r_ackh.font.name = 'Times New Roman'
    r_ackh.font.size = Pt(16)
    r_ackh.font.bold = True

    ack_paras = [
        "We are highly grateful to Dr. Sehijpal Singh, Principal, Guru Nanak Dev Engineering College (GNDEC), Ludhiana, for providing this opportunity to carry out the major project work at Guru Nanak Dev Engineering College, Ludhiana.",
        "The constant guidance and encouragement received from the Head of Department, Computer Science and Engineering Department, GNDEC Ludhiana, has been of great help in carrying out the project work and is acknowledged with reverential thanks.",
        "We would like to express a deep sense of gratitude and thanks profusely to our project guide, Dr. Hardeep Singh Kang, Department of Computer Science and Engineering, without his wise counsel and able guidance, it would have been impossible to complete the project in this manner. His constructive criticism, continuous technical reviews, and academic insights have enriched this project report substantially.",
        "We express gratitude to other faculty members and technical staff of the Computer Science and Engineering Department of GNDEC for their intellectual support throughout the course of this work.",
        "Finally, we are indebted to our parents, family members, and all friends whosoever have contributed directly or indirectly in this report work."
    ]
    for ap in ack_paras:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 2.0
        p.add_run(ap)

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.line_spacing = 1.15
    p_ack_sig.paragraph_format.space_before = Pt(20)
    p_ack_sig.add_run(
        "Khushpreet Kaur (Univ. Roll No: 2302591)\n"
        "Mohammad Shehzad (Univ. Roll No: 2302612)\n"
        "Neha Mehta (Univ. Roll No: 2302625)\n"
        "Batch: 2023-2027\n"
        "Department of Computer Science and Engineering\n"
        "Guru Nanak Dev Engineering College, Ludhiana"
    ).font.bold = True

    doc.add_page_break()

    # Table of Contents
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_after = Pt(18)
    p_toc_h.paragraph_format.line_spacing = 1.0
    r_toch = p_toc_h.add_run("TABLE OF CONTENTS")
    r_toch.font.name = 'Times New Roman'
    r_toch.font.size = Pt(16)
    r_toch.font.bold = True

    toc_entries = [
        ("Abstract", "i"),
        ("Acknowledgement", "ii"),
        ("List of Figures", "iv"),
        ("List of Tables", "v"),
        ("Notations and Nomenclature", "vi"),
        ("Chapter 1: Introduction", "1"),
        ("    1.1 Introduction to Project", "1"),
        ("    1.2 Project Category (Application Based)", "3"),
        ("    1.3 Problem Formulation", "4"),
        ("    1.4 Identification / Recognition of Need", "5"),
        ("    1.5 Existing System and Its Limitations", "8"),
        ("    1.6 Objectives", "10"),
        ("    1.7 Proposed System", "12"),
        ("    1.8 Unique Features of the Proposed System", "14"),
        ("Chapter 2: Requirement Analysis and System Specification", "16"),
        ("    2.1 Feasibility Study (Technical, Economical, Operational)", "16"),
        ("    2.2 Software Requirement Specification (SRS) Document", "19"),
        ("        2.2.1 Data Requirements", "19"),
        ("        2.2.2 Functional Requirements", "21"),
        ("        2.2.3 Performance Requirements", "25"),
        ("        2.2.4 Dependability Requirements", "26"),
        ("        2.2.5 Maintainability Requirements", "27"),
        ("        2.2.6 Security Requirements", "28"),
        ("        2.2.7 Look and Feel Requirements", "29"),
        ("    2.3 SDLC Model to be Used (Iterative Agile Sprints)", "30"),
        ("Chapter 3: System Design", "33"),
        ("    3.1 Design Approach (Object-Oriented & Layered Microservice)", "33"),
        ("    3.2 Detail Design", "35"),
        ("        3.2.1 System Architecture and Block Diagram", "35"),
        ("        3.2.2 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)", "37"),
        ("        3.2.3 UML Diagrams (Use Case, Class, Sequence, Activity, Deployment)", "42"),
        ("        3.2.4 Database Design and Normalized Relational Schemas", "52"),
        ("    3.3 User Interface Design (Screen Hierarchy & Layout)", "58"),
        ("    3.4 Methodology", "60"),
        ("Chapter 4: Implementation and Testing", "63"),
        ("    4.1 Introduction to Languages, IDEs, Tools, and Technologies Used", "63"),
        ("    4.2 Algorithms and Pseudocode Used", "67"),
        ("        Algorithm 1: Sublinear TF-IDF Sparse Feature Matrix Construction", "68"),
        ("        Algorithm 2: Calibrated Cosine Similarity Precedent Retrieval", "70"),
        ("        Algorithm 3: Hybrid Grounded Legal Synthesis and Failover", "72"),
        ("        Algorithm 4: Court-Ready Vector PDF Document Generation", "74"),
        ("    4.3 Testing Techniques: In Context of Project Work", "76"),
        ("    4.4 Test Cases Designed for the Project Work", "78"),
        ("Chapter 5: Results and Discussions", "83"),
        ("    5.1 User Interface Representation", "83"),
        ("        5.1.1 Brief Description of Various Modules of the System", "83"),
        ("    5.2 Snapshots of System with Brief Detail of Each and Discussion", "86"),
        ("    5.3 Back-End Representation (Database Tables and Engine Diagnostics)", "94"),
        ("Chapter 6: Conclusion and Future Scope", "98"),
        ("    6.1 Conclusion", "98"),
        ("    6.2 Future Scope", "99"),
        ("References", "101"),
        ("Appendix A: Development Environment and Setup Guide", "104"),
        ("Annexure I: Complete RESTful API Endpoint Specification", "106"),
        ("Annexure II: Key Configuration, Environment Variables & SQLite Pragmas", "108"),
        ("Annexure III: User Manual and Operator Guide", "110"),
    ]

    tbl_toc = doc.add_table(rows=len(toc_entries)+1, cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc, color="CBD5E0", sz="2")
    set_table_row_properties(tbl_toc.rows[0], is_header=True)
    c00 = tbl_toc.cell(0, 0); c01 = tbl_toc.cell(0, 1)
    c00.width = Inches(5.6); c01.width = Inches(1.0)
    set_cell_shading(c00, "E8EEF5"); set_cell_shading(c01, "E8EEF5")
    p00 = c00.paragraphs[0]; p00.paragraph_format.line_spacing = 1.0; r = p00.add_run("Contents"); r.font.bold = True
    p01 = c01.paragraphs[0]; p01.paragraph_format.line_spacing = 1.0; p01.alignment = WD_ALIGN_PARAGRAPH.RIGHT; r = p01.add_run("Page No."); r.font.bold = True

    for i, (title, pg) in enumerate(toc_entries):
        row = tbl_toc.rows[i+1]
        set_table_row_properties(row)
        c_t = row.cells[0]; c_p = row.cells[1]
        c_t.width = Inches(5.6); c_p.width = Inches(1.0)
        p_t = c_t.paragraphs[0]; p_t.paragraph_format.line_spacing = 1.15
        p_p = c_p.paragraphs[0]; p_p.paragraph_format.line_spacing = 1.15; p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_t = p_t.add_run(title)
        if title.startswith("Chapter") or title in ["Abstract", "Acknowledgement", "References"]:
            r_t.font.bold = True
        r_p = p_p.add_run(pg)
        if title.startswith("Chapter"):
            r_p.font.bold = True

    doc.add_page_break()

    # List of Figures
    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_h.paragraph_format.space_after = Pt(18)
    p_lof_h.paragraph_format.line_spacing = 1.0
    r_lofh = p_lof_h.add_run("LIST OF FIGURES")
    r_lofh.font.name = 'Times New Roman'
    r_lofh.font.size = Pt(16)
    r_lofh.font.bold = True

    lof_entries = [
        ("Figure 1.1", "High-Level Architectural Block Diagram of the Proposed PocketLaw System", "13"),
        ("Figure 2.1", "Iterative Agile Development Sprints Mapped to the PocketLaw Project Work", "31"),
        ("Figure 3.1", "Detailed Component-Level System Architecture of PocketLaw", "36"),
        ("Figure 3.2", "Data Flow Diagram: Level 0 (Context Diagram)", "38"),
        ("Figure 3.3", "Data Flow Diagram: Level 1 (Functional Decomposition)", "39"),
        ("Figure 3.4", "Data Flow Diagram: Level 2 (Consultation and RAG Sub-processes)", "41"),
        ("Figure 3.5", "UML Use Case Diagram for PocketLaw Platform", "43"),
        ("Figure 3.6", "UML Class Diagram Depicting Relational Entities and ORM Relationships", "45"),
        ("Figure 3.7", "UML Sequence Diagram for Legal Consultation and RAG Synthesis", "47"),
        ("Figure 3.8", "UML Activity Diagram for Hybrid Synthesis and Failover Logic", "49"),
        ("Figure 3.9", "UML Deployment Diagram of the PocketLaw Application Architecture", "51"),
        ("Figure 3.10", "Entity-Relationship (E-R) Diagram of PocketLaw Database", "53"),
        ("Figure 5.1", "Visual Wireframe of the Natural Language Consultation Interface", "87"),
        ("Figure 5.2", "Visual Wireframe of the Analytical Intelligence Dashboard", "89"),
        ("Figure 5.3", "Visual Wireframe of the Dual-Pane Document Drafting Studio", "91"),
        ("Figure 5.4", "Visual Wireframe of the Modern Criminal Statutes Catalog Interface", "93"),
    ]

    tbl_lof = doc.add_table(rows=len(lof_entries)+1, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lof, color="CBD5E0", sz="2")
    set_table_row_properties(tbl_lof.rows[0], is_header=True)
    for idx, (col_w, text, align) in enumerate([(Inches(1.4), "Fig. No.", WD_ALIGN_PARAGRAPH.LEFT),
                                                (Inches(4.4), "Figure Description", WD_ALIGN_PARAGRAPH.LEFT),
                                                (Inches(0.8), "Page No.", WD_ALIGN_PARAGRAPH.RIGHT)]):
        cell = tbl_lof.cell(0, idx); cell.width = col_w; set_cell_shading(cell, "E8EEF5")
        p = cell.paragraphs[0]; p.paragraph_format.line_spacing = 1.0; p.alignment = align
        r = p.add_run(text); r.font.bold = True

    for i, (f_num, f_desc, f_pg) in enumerate(lof_entries):
        row = tbl_lof.rows[i+1]
        set_table_row_properties(row)
        c0 = row.cells[0]; c1 = row.cells[1]; c2 = row.cells[2]
        c0.width = Inches(1.4); c1.width = Inches(4.4); c2.width = Inches(0.8)
        p0 = c0.paragraphs[0]; p0.paragraph_format.line_spacing = 1.15; p0.add_run(f_num).font.bold = True
        p1 = c1.paragraphs[0]; p1.paragraph_format.line_spacing = 1.15; p1.add_run(f_desc)
        p2 = c2.paragraphs[0]; p2.paragraph_format.line_spacing = 1.15; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(f_pg)

    doc.add_page_break()

    # List of Tables
    p_lot_h = doc.add_paragraph()
    p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_h.paragraph_format.space_after = Pt(18)
    p_lot_h.paragraph_format.line_spacing = 1.0
    r_loth = p_lot_h.add_run("LIST OF TABLES")
    r_loth.font.name = 'Times New Roman'
    r_loth.font.size = Pt(16)
    r_loth.font.bold = True

    lot_entries = [
        ("Table 1.1", "Comprehensive Comparison of Existing Legal Systems vs. PocketLaw", "9"),
        ("Table 2.1", "Comprehensive Functional Requirements Traceability Matrix", "22"),
        ("Table 3.1", "Physical Data Dictionary: users Relational Table", "54"),
        ("Table 3.2", "Physical Data Dictionary: chat_sessions Relational Table", "55"),
        ("Table 3.3", "Physical Data Dictionary: chat_messages Relational Table", "55"),
        ("Table 3.4", "Physical Data Dictionary: saved_documents Relational Table", "56"),
        ("Table 3.5", "Physical Data Dictionary: case_bookmarks Relational Table", "57"),
        ("Table 3.6", "User Interface Layout and Screen Specification", "59"),
        ("Table 4.1", "Comprehensive Automated Test Case Execution Matrix", "79"),
        ("Table 5.1", "Empirical Information Retrieval Evaluation Benchmark Results (/api/rag/eval)", "92"),
        ("Table 5.2", "Live SQLite WAL Relational Database Engine Diagnostics (/api/db/stats)", "95"),
        ("Table 5.3", "Sample Populated Records: users Relational Table", "96"),
        ("Table 5.4", "Sample Populated Records: saved_documents Relational Table", "97"),
        ("Table A.1", "Development Hardware and Operating System Specifications", "104"),
        ("Table A.2", "Comprehensive RESTful API Endpoint Specification", "106"),
    ]

    tbl_lot = doc.add_table(rows=len(lot_entries)+1, cols=3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_lot, color="CBD5E0", sz="2")
    set_table_row_properties(tbl_lot.rows[0], is_header=True)
    for idx, (col_w, text, align) in enumerate([(Inches(1.4), "Table No.", WD_ALIGN_PARAGRAPH.LEFT),
                                                (Inches(4.4), "Table Description", WD_ALIGN_PARAGRAPH.LEFT),
                                                (Inches(0.8), "Page No.", WD_ALIGN_PARAGRAPH.RIGHT)]):
        cell = tbl_lot.cell(0, idx); cell.width = col_w; set_cell_shading(cell, "E8EEF5")
        p = cell.paragraphs[0]; p.paragraph_format.line_spacing = 1.0; p.alignment = align
        r = p.add_run(text); r.font.bold = True

    for i, (t_num, t_desc, t_pg) in enumerate(lot_entries):
        row = tbl_lot.rows[i+1]
        set_table_row_properties(row)
        c0 = row.cells[0]; c1 = row.cells[1]; c2 = row.cells[2]
        c0.width = Inches(1.4); c1.width = Inches(4.4); c2.width = Inches(0.8)
        p0 = c0.paragraphs[0]; p0.paragraph_format.line_spacing = 1.15; p0.add_run(t_num).font.bold = True
        p1 = c1.paragraphs[0]; p1.paragraph_format.line_spacing = 1.15; p1.add_run(t_desc)
        p2 = c2.paragraphs[0]; p2.paragraph_format.line_spacing = 1.15; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT; p2.add_run(t_pg)

    doc.add_page_break()

    # Notations and Nomenclature
    p_nom_h = doc.add_paragraph()
    p_nom_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_nom_h.paragraph_format.space_after = Pt(18)
    p_nom_h.paragraph_format.line_spacing = 1.0
    r_nomh = p_nom_h.add_run("NOTATIONS AND NOMENCLATURE")
    r_nomh.font.name = 'Times New Roman'
    r_nomh.font.size = Pt(16)
    r_nomh.font.bold = True

    nom_data = [
        ("D", "Total legal corpus consisting of indexed document chunks (|D| = 2,290)"),
        ("V", "Vocabulary space size of extracted n-gram features (V = 15,000)"),
        ("TF(t, d)", "Sublinear Term Frequency of token t in document chunk d"),
        ("IDF(t)", "Smooth Inverse Document Frequency of token t across corpus D"),
        ("q, d", "Normalized 15,000-dimensional sparse vectors for query q and chunk d"),
        ("tau", "Calibrated Cosine Similarity Retrieval Threshold (tau = 0.05)"),
        ("P@K", "Precision at Rank K (proportion of relevant chunks within top-K candidates)"),
        ("MRR", "Mean Reciprocal Rank across evaluated benchmark queries"),
        ("ACID", "Atomicity, Consistency, Isolation, Durability"),
        ("API", "Application Programming Interface"),
        ("BNS 2023", "Bharatiya Nyaya Sanhita, 2023 (Successor to IPC 1860)"),
        ("BNSS 2023", "Bharatiya Nagarik Suraksha Sanhita, 2023 (Successor to CrPC 1973)"),
        ("BSA 2023", "Bharatiya Sakshya Adhiniyam, 2023 (Successor to IEA 1872)"),
        ("CDRC", "Consumer Disputes Redressal Commission"),
        ("CPC 1908", "Code of Civil Procedure, 1908 (Section 80 Statutory Notice)"),
        ("CSR", "Compressed Sparse Row (Scipy Matrix Storage Format)"),
        ("DFD", "Data Flow Diagram"),
        ("E-Daakhil", "Government of India Online Consumer Grievance Filing Portal"),
        ("FIR", "First Information Report (Section 154 CrPC / Section 173 BNSS)"),
        ("GNDEC", "Guru Nanak Dev Engineering College, Ludhiana"),
        ("IPC 1860", "Indian Penal Code, 1860 (Repealed 1 July 2024)"),
        ("IR", "Information Retrieval"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token (RFC 7519)"),
        ("LLM", "Large Language Model"),
        ("ORM", "Object-Relational Mapping (SQLAlchemy)"),
        ("RAG", "Retrieval-Augmented Generation"),
        ("REST", "Representational State Transfer"),
        ("SPA", "Single Page Application"),
        ("SRS", "Software Requirement Specification"),
        ("TF-IDF", "Term Frequency - Inverse Document Frequency"),
        ("UML", "Unified Modelling Language"),
        ("VSM", "Vector Space Model"),
        ("WAL", "Write-Ahead Logging (SQLite Concurrency Mechanism)"),
    ]

    tbl_nom = doc.add_table(rows=len(nom_data)+1, cols=2)
    tbl_nom.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_nom, color="CBD5E0", sz="2")
    set_table_row_properties(tbl_nom.rows[0], is_header=True)
    c0 = tbl_nom.cell(0, 0); c1 = tbl_nom.cell(0, 1)
    c0.width = Inches(2.0); c1.width = Inches(4.6)
    set_cell_shading(c0, "E8EEF5"); set_cell_shading(c1, "E8EEF5")
    p = c0.paragraphs[0]; p.paragraph_format.line_spacing = 1.0; r = p.add_run("Notation / Acronym"); r.font.bold = True
    p = c1.paragraphs[0]; p.paragraph_format.line_spacing = 1.0; r = p.add_run("Description / Meaning"); r.font.bold = True

    for i, (notat, desc) in enumerate(nom_data):
        row = tbl_nom.rows[i+1]
        set_table_row_properties(row)
        c0 = row.cells[0]; c1 = row.cells[1]
        c0.width = Inches(2.0); c1.width = Inches(4.6)
        p0 = c0.paragraphs[0]; p0.paragraph_format.line_spacing = 1.15; p0.add_run(notat).font.bold = True
        p1 = c1.paragraphs[0]; p1.paragraph_format.line_spacing = 1.15; p1.add_run(desc)

    # ── Section 3 Setup ────────────────────────────────────────────────────────
    s3 = doc.add_section()
    setup_gndec_section_geometry(s3)
    s3.header.is_linked_to_previous = False
    s3.footer.is_linked_to_previous = False

    pg3 = OxmlElement('w:pgNumType')
    pg3.set(qn('w:fmt'), 'decimal')
    pg3.set(qn('w:start'), '1')
    s3._sectPr.append(pg3)
    add_page_number_to_footer(s3.footer)

    return s3

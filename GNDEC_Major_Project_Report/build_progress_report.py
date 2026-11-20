"""
PocketLaw - Major Project Progress & Review Record (.docx) Generator
Department of Computer Science and Engineering
Guru Nanak Dev Engineering College (GNDEC), Ludhiana
Major Project (PRCS-103) | 7th Semester (Batch: 2023-2027) | November 2026

Generates:
GNDEC_Major_Project_Report/PocketLaw_Progress_Review_Report.docx
Strictly formatted to fit on EXACTLY 2 A4 pages matching the official GNDEC template.
"""

import os
import sys
import docx
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_DIR = r"C:\Users\Shehzad\OneDrive\Desktop\PROJECTS\PocketLaw\GNDEC_Major_Project_Report"
DOCX_PATH = os.path.join(OUTPUT_DIR, "PocketLaw_Progress_Review_Report.docx")

def set_cell_margins(cell, top=30, bottom=30, left=60, right=60):
    """Sets compact cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_row_properties(row, is_header=False):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement('w:cantSplit')
    trPr.append(cantSplit)
    if is_header:
        tblHeader = OxmlElement('w:tblHeader')
        trPr.append(tblHeader)

def set_table_borders(table, color="000000", sz="4"):
    """Sets standard thin black table borders matching the GNDEC template."""
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tblBorders.append(b)
    tblPr.append(tblBorders)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def create_progress_review_report():
    doc = docx.Document()

    # ── Page Setup (A4, 1.2 cm Top/Bottom, 1.5 cm Left/Right) ─────────────────
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.2)
    section.bottom_margin = Cm(1.2)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)

    # ══════════════════════════════════════════════════════════════════════════
    #  PAGE 1: HEADER, SECTION A & SECTION B
    # ══════════════════════════════════════════════════════════════════════════

    # Department Banner
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.line_spacing = 1.0
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(2)
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
    r_dept.font.name = 'Times New Roman'
    r_dept.font.size = Pt(12)
    r_dept.font.bold = True

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.0
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(3)
    r_title = p_title.add_run("MAJOR PROJECT PROGRESS & REVIEW RECORD")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(13)
    r_title.font.bold = True
    r_title.font.underline = True

    # Academic Session
    p_sess = doc.add_paragraph()
    p_sess.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sess.paragraph_format.line_spacing = 1.0
    p_sess.paragraph_format.space_before = Pt(0)
    p_sess.paragraph_format.space_after = Pt(5)
    r_s1 = p_sess.add_run("Academic Session: ")
    r_s1.font.name = 'Times New Roman'
    r_s1.font.size = Pt(10.5)
    r_s1.font.bold = True
    r_s2 = p_sess.add_run("2026–2027 (7th Semester, Batch: 2023–2027)")
    r_s2.font.name = 'Times New Roman'
    r_s2.font.size = Pt(10.5)

    # ── Section A: Project Group Details ──────────────────────────────────────
    p_sec_a = doc.add_paragraph()
    p_sec_a.paragraph_format.line_spacing = 1.0
    p_sec_a.paragraph_format.space_before = Pt(2)
    p_sec_a.paragraph_format.space_after = Pt(2)
    r_sa = p_sec_a.add_run("A. Project Group Details")
    r_sa.font.name = 'Times New Roman'
    r_sa.font.size = Pt(11)
    r_sa.font.bold = True

    tbl_a = doc.add_table(rows=10, cols=2)
    tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_a, color="000000", sz="4")

    col_widths_a = [Cm(5.0), Cm(13.0)]

    sec_a_data = [
        ("Particulars", "Details", True),
        ("Project Title", "POCKETLAW: TYPE YOUR PROBLEM, GET YOUR LEGAL RIGHTS", False),
        ("Project Group ID", "G-____ (As allocated by Project Coordinator)", False),
        ("Project Category", "Application Based", False),
        ("Guide Name", "Dr. Hardeep Singh Kang", False),
        ("Co-Guide (if any)", "N/A", False),
        ("Student 1 – Name & Univ Roll No.", "Khushpreet Kaur (2302591)", False),
        ("Student 2 – Name & Univ Roll No.", "Mohammad Shehzad (2302612)", False),
        ("Student 3 – Name & Univ Roll No.", "Neha Mehta (2302625)", False),
        ("Date of Project Allocation", "28/07/2026", False),
    ]

    for r_idx, (part, det, is_hdr) in enumerate(sec_a_data):
        row = tbl_a.rows[r_idx]
        set_table_row_properties(row, is_header=is_hdr)
        for c_idx, val in enumerate([part, det]):
            cell = row.cells[c_idx]
            cell.width = col_widths_a[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=50, right=50)
            if is_hdr:
                set_cell_shading(cell, "F2F2F2")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr or (c_idx == 0):
                r.font.bold = True

    # ── Section B: Record of Guide–Group Interactions ────────────────────────
    p_sec_b = doc.add_paragraph()
    p_sec_b.paragraph_format.line_spacing = 1.0
    p_sec_b.paragraph_format.space_before = Pt(4)
    p_sec_b.paragraph_format.space_after = Pt(2)
    r_sb = p_sec_b.add_run("B. Record of Guide–Group Interactions")
    r_sb.font.name = 'Times New Roman'
    r_sb.font.size = Pt(11)
    r_sb.font.bold = True

    tbl_b = doc.add_table(rows=16, cols=6)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b, color="000000", sz="4")

    # Col widths totaling 18.0 cm (usable page width)
    col_widths_b = [Cm(1.1), Cm(1.6), Cm(4.0), Cm(4.3), Cm(4.7), Cm(2.3)]

    # Header Row
    headers_b = ["Interac-\ntion No.", "Date", "Topics Discussed / Agenda", "Progress Presented by Students", "Suggestions / Feedback Given by Guide", "Signatures of\nguide"]
    set_table_row_properties(tbl_b.rows[0], is_header=True)
    for c_idx, h_text in enumerate(headers_b):
        cell = tbl_b.rows[0].cells[c_idx]
        cell.width = col_widths_b[c_idx]
        set_cell_margins(cell, top=30, bottom=30, left=35, right=35)
        set_cell_shading(cell, "F2F2F2")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.0)
        r.font.bold = True

    # 15 Authentic Interaction Rows
    interactions = [
        ("1", "05/08/2026",
         "Project domain finalization & legal problem formulation.",
         "Presented survey on legal portals & citizen barriers.",
         "Approved scope; advised focusing on post-July 2024 BNS rules."),
        
        ("2", "12/08/2026",
         "Impact of new criminal laws (BNS, BNSS, BSA 2023).",
         "Drafted comparative study between IPC and BNS sections.",
         "Include Zero FIR under Sec 173 BNSS & 1930 helplines."),
        
        ("3", "19/08/2026",
         "Project Synopsis & IEEE SRS document preparation.",
         "Submitted functional requirements (FR-1–FR-10) & feasibility.",
         "Approved Synopsis; define measurable technical objectives."),
        
        ("4", "26/08/2026",
         "System architecture, DFDs & technology stack selection.",
         "Presented DFD Level 0/1; proposed Flask and React 18.",
         "Ensure decoupled architecture & 100% offline retrieval."),
        
        ("5", "02/09/2026",
         "Database schema design & concurrency modeling.",
         "Designed ER diagram for users, chats & saved documents.",
         "Use SQLite WAL mode for non-blocking concurrent writes."),
        
        ("6", "09/09/2026",
         "Supreme Court judicial corpus curation & chunking.",
         "Curated 148 landmark judgments into 2,290 text chunks.",
         "Verify case citations & include consumer dispute precedents."),
        
        ("7", "16/09/2026",
         "Sparse Vector Space Model (VSM) mathematical indexing.",
         "Formulated sublinear TF-IDF; 15,000-D SciPy CSR matrix.",
         "Calibrate cosine threshold (tau=0.05) to filter noise."),
        
        ("8", "23/09/2026",
         "Dual-Engine RAG pipeline & prompt grounding.",
         "Linked Gemini 1.5 Flash API with local extractive fallback.",
         "Prevent hallucinations; test seamless offline fallback."),
        
        ("9", "30/09/2026",
         "Midterm Evaluation review & prototype demonstration.",
         "Demonstrated grievance-to-BNS matching under 50ms.",
         "Midterm progress on-track; accelerate UI & PDF studio."),
        
        ("10", "07/10/2026",
         "UI accessibility & survival guidance module design.",
         "Prototyped React UI cards & Web Speech voice dictation.",
         "Highlight limitation deadlines & direct 1930 cyber routing."),
        
        ("11", "14/10/2026",
         "Back-end API gateway & Git repository version control.",
         "Committed core Flask REST APIs (/api/chat, /api/rag).",
         "Enforce PBKDF2 password hashing & test token security."),
        
        ("12", "21/10/2026",
         "Multilingual consultation & live draft preview.",
         "Committed chat interface supporting English, Hindi, Punjabi.",
         "Approved UI; initiate ReportLab court-ready PDF generation."),
        
        ("13", "28/10/2026",
         "ReportLab vector PDF legal document generation studio.",
         "Compiled FIR, Sec 80 CPC Notice, Affidavit & Complaints.",
         "Format legal headers, verification jurats & court margins."),
        
        ("14", "04/11/2026",
         "Automated test execution & concurrency benchmarking.",
         "Executed 18 test suites (100% pass); tested WAL concurrency.",
         "Commended 100% pass; prepare final LaTeX/DOCX report."),
        
        ("15", "18/11/2026",
         "Final report, plagiarism check, poster & defense review.",
         "Presented 80+ page Report, A3 poster & IR benchmark.",
         "Verified plagiarism report; approved for defense on 25/11/2026.")
    ]

    for idx, (ino, dt, top, prog, sugg) in enumerate(interactions):
        row = tbl_b.rows[idx + 1]
        set_table_row_properties(row)
        vals = [ino, dt, top, prog, sugg, ""]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = col_widths_b[c_idx]
            set_cell_margins(cell, top=20, bottom=20, left=35, right=35)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if c_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(7.5)
            if c_idx == 0:
                r.font.bold = True

    # ══════════════════════════════════════════════════════════════════════════
    #  PAGE 2: SECTION C (PERFORMANCE ASSESSMENT & SIGNATURES)
    # ══════════════════════════════════════════════════════════════════════════
    doc.add_page_break()

    # Section C Heading
    p_sec_c = doc.add_paragraph()
    p_sec_c.paragraph_format.line_spacing = 1.0
    p_sec_c.paragraph_format.space_before = Pt(0)
    p_sec_c.paragraph_format.space_after = Pt(2)
    r_sc = p_sec_c.add_run("C. Overall Project Performance Assessment")
    r_sc.font.name = 'Times New Roman'
    r_sc.font.size = Pt(12)
    r_sc.font.bold = True

    # Italic Subtitle
    p_sub_c = doc.add_paragraph()
    p_sub_c.paragraph_format.line_spacing = 1.0
    p_sub_c.paragraph_format.space_before = Pt(0)
    p_sub_c.paragraph_format.space_after = Pt(5)
    r_sbc = p_sub_c.add_run("Please tick (✓) the appropriate option.")
    r_sbc.font.name = 'Times New Roman'
    r_sbc.font.size = Pt(10)
    r_sbc.font.italic = True

    # Assessment Table (7 Parameters)
    tbl_c = doc.add_table(rows=8, cols=5)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_c, color="000000", sz="4")

    col_widths_c = [Cm(8.0), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)]

    headers_c = ["Review Parameter", "Excellent", "Good", "Satisfactory", "Needs Improvement"]
    set_table_row_properties(tbl_c.rows[0], is_header=True)
    for c_idx, h in enumerate(headers_c):
        cell = tbl_c.rows[0].cells[c_idx]
        cell.width = col_widths_c[c_idx]
        set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
        set_cell_shading(cell, "F2F2F2")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.bold = True

    params_c = [
        "Progress as per planned schedule",
        "Completion of assigned tasks",
        "Technical implementation / development",
        "Problem-solving and initiative",
        "Team coordination and participation",
        "Regularity in guide interactions",
        "Response to guide's feedback"
    ]

    for idx, param in enumerate(params_c):
        row = tbl_c.rows[idx + 1]
        set_table_row_properties(row)
        for c_idx in range(5):
            cell = row.cells[c_idx]
            cell.width = col_widths_c[c_idx]
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(param)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.0)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                # Leave blank tick box
                r = p.add_run("☐")
                r.font.name = 'Segoe UI Symbol'
                r.font.size = Pt(11)

    # ── Checkboxes & Remarks Block ───────────────────────────────────────────
    p_prog_head = doc.add_paragraph()
    p_prog_head.paragraph_format.line_spacing = 1.0
    p_prog_head.paragraph_format.space_before = Pt(12)
    p_prog_head.paragraph_format.space_after = Pt(4)
    r_ph = p_prog_head.add_run("Overall Project Progress:")
    r_ph.font.name = 'Times New Roman'
    r_ph.font.size = Pt(10.5)
    r_ph.font.bold = True

    p_prog_cb = doc.add_paragraph()
    p_prog_cb.paragraph_format.line_spacing = 1.15
    p_prog_cb.paragraph_format.space_before = Pt(0)
    p_prog_cb.paragraph_format.space_after = Pt(8)
    for opt in ["☐ On Track", "☐ Needs Attention", "☐ Behind Schedule"]:
        r = p_prog_cb.add_run(f"{opt}          ")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    p_iss_head = doc.add_paragraph()
    p_iss_head.paragraph_format.line_spacing = 1.0
    p_iss_head.paragraph_format.space_before = Pt(4)
    p_iss_head.paragraph_format.space_after = Pt(4)
    r_ih = p_iss_head.add_run("Any Major Issue Requiring Attention:")
    r_ih.font.name = 'Times New Roman'
    r_ih.font.size = Pt(10.5)
    r_ih.font.bold = True

    p_iss_cb = doc.add_paragraph()
    p_iss_cb.paragraph_format.line_spacing = 1.15
    p_iss_cb.paragraph_format.space_before = Pt(0)
    p_iss_cb.paragraph_format.space_after = Pt(8)
    for opt in ["☐ No", "☐ Yes"]:
        r = p_iss_cb.add_run(f"{opt}          ")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    p_rem_head = doc.add_paragraph()
    p_rem_head.paragraph_format.line_spacing = 1.0
    p_rem_head.paragraph_format.space_before = Pt(4)
    p_rem_head.paragraph_format.space_after = Pt(4)
    r_rh = p_rem_head.add_run("If yes, brief remarks:")
    r_rh.font.name = 'Times New Roman'
    r_rh.font.size = Pt(10)

    for _ in range(3):
        p_line = doc.add_paragraph()
        p_line.paragraph_format.line_spacing = 1.0
        p_line.paragraph_format.space_before = Pt(2)
        p_line.paragraph_format.space_after = Pt(2)
        r_l = p_line.add_run("_________________________________________________________________________________")
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(10)
        r_l.font.color.rgb = RGBColor(120, 120, 120)

    # ── Signature Footer Block ───────────────────────────────────────────────
    p_sig_guide = doc.add_paragraph()
    p_sig_guide.paragraph_format.line_spacing = 1.15
    p_sig_guide.paragraph_format.space_before = Pt(22)
    p_sig_guide.paragraph_format.space_after = Pt(3)
    r_sg = p_sig_guide.add_run("Guide's Name & Signature: _________________________          Date: _________________")
    r_sg.font.name = 'Times New Roman'
    r_sg.font.size = Pt(10.5)
    r_sg.font.bold = True

    p_guide_nm = doc.add_paragraph()
    p_guide_nm.paragraph_format.line_spacing = 1.0
    p_guide_nm.paragraph_format.space_before = Pt(0)
    p_guide_nm.paragraph_format.space_after = Pt(14)
    r_gnm = p_guide_nm.add_run("Dr. Hardeep Singh Kang (Project Guide, Dept. of CSE)")
    r_gnm.font.name = 'Times New Roman'
    r_gnm.font.size = Pt(9.5)
    r_gnm.font.italic = True
    r_gnm.font.color.rgb = RGBColor(80, 80, 80)

    students = [
        ("Student 1", "Khushpreet Kaur - 2302591"),
        ("Student 2", "Mohammad Shehzad - 2302612"),
        ("Student 3", "Neha Mehta - 2302625")
    ]
    for s_label, s_info in students:
        p_st = doc.add_paragraph()
        p_st.paragraph_format.line_spacing = 1.0
        p_st.paragraph_format.space_before = Pt(2)
        p_st.paragraph_format.space_after = Pt(4)
        r_s = p_st.add_run(f"Signature {s_label}: _________________________  ({s_info})")
        r_s.font.name = 'Times New Roman'
        r_s.font.size = Pt(10)

    p_coord = doc.add_paragraph()
    p_coord.paragraph_format.line_spacing = 1.0
    p_coord.paragraph_format.space_before = Pt(18)
    p_coord.paragraph_format.space_after = Pt(0)
    r_c = p_coord.add_run("Project Coordinator's Signature: _________________________")
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(10.5)
    r_c.font.bold = True

    doc.save(DOCX_PATH)
    print(f"Successfully generated: {DOCX_PATH}")

if __name__ == "__main__":
    create_progress_review_report()

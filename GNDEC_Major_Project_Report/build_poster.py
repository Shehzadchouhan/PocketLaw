"""
PocketLaw - Major Project Academic Poster Generator (A3 Portrait 300 DPI)
Department of Computer Science and Engineering
Guru Nanak Dev Engineering College (GNDEC), Ludhiana
Major Project (PRCS-103) | 7th Semester (Batch: 2023-2027) | November 2026

Generates:
1. PocketLaw_Project_Poster_A3.pdf (Print-ready A3 vector PDF, 297mm x 420mm)
2. PocketLaw_Project_Poster_A3.png (High-resolution 300 DPI raster preview, 3508 x 4961 px)
"""

import os
import sys
import fitz # PyMuPDF
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUTPUT_DIR = r"C:\Users\Shehzad\OneDrive\Desktop\PROJECTS\PocketLaw\GNDEC_Major_Project_Report"
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")
PDF_PATH = os.path.join(OUTPUT_DIR, "PocketLaw_Project_Poster_A3.pdf")
PNG_PATH = os.path.join(OUTPUT_DIR, "PocketLaw_Project_Poster_A3.png")

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY_DARK = colors.HexColor('#0F172A')    # Deep Slate Navy
NAVY_CARD = colors.HexColor('#1E293B')    # Card Header Navy
GOLD = colors.HexColor('#B45309')         # Warm Amber / Gold
GOLD_LIGHT = colors.HexColor('#FEF3C7')   # Soft Gold Tint
GOLD_BRIGHT = colors.HexColor('#F59E0B')  # Accent Gold
WHITE = colors.HexColor('#FFFFFF')
CARD_BG = colors.HexColor('#FFFFFF')
BORDER_COLOR = colors.HexColor('#CBD5E1')
TEXT_PRIMARY = colors.HexColor('#0F172A')
TEXT_MUTED = colors.HexColor('#475569')

def create_poster():
    w_page, h_page = A3
    c = canvas.Canvas(PDF_PATH, pagesize=A3)

    # 1. Background Fill (Crisp Light Slate)
    c.setFillColor(colors.HexColor('#F8FAFC'))
    c.rect(0, 0, w_page, h_page, fill=1, stroke=0)

    # ── Styles ────────────────────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    style_card_title = ParagraphStyle(
        'CardTitle',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=12.5,
        textColor=WHITE
    )

    style_body = ParagraphStyle(
        'CardBody',
        fontName='Helvetica',
        fontSize=8.1,
        leading=10.2,
        textColor=TEXT_PRIMARY
    )

    style_body_muted = ParagraphStyle(
        'CardBodyMuted',
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.5,
        textColor=TEXT_MUTED
    )

    style_obj = ParagraphStyle(
        'ObjText',
        fontName='Helvetica-Bold',
        fontSize=8.1,
        leading=10.1,
        textColor=NAVY_DARK
    )

    def draw_card_shell(x, y, w, h, title_text, title_bg=NAVY_CARD, border_color=BORDER_COLOR, card_bg=CARD_BG):
        # Base Card
        c.setFillColor(card_bg)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.0)
        c.roundRect(x, y, w, h, 3.5*mm, fill=1, stroke=1)

        # Header Pill
        header_h = 7.5*mm
        c.setFillColor(title_bg)
        c.roundRect(x, y + h - header_h, w, header_h, 3.5*mm, fill=1, stroke=0)
        c.rect(x, y + h - header_h, w, 2.5*mm, fill=1, stroke=0) # flatten bottom

        # Gold Accent Divider
        c.setFillColor(GOLD)
        c.rect(x, y + h - header_h - 0.7*mm, w, 0.7*mm, fill=1, stroke=0)

        # Title Text
        p_t = Paragraph(f"<b>{title_text}</b>", style_card_title)
        p_t.wrap(w - 8*mm, header_h)
        p_t.drawOn(c, x + 3.5*mm, y + h - header_h + 1.8*mm)

    # ══════════════════════════════════════════════════════════════════════════
    #  TOP HEADER BANNER
    # ══════════════════════════════════════════════════════════════════════════
    hb_x = 8 * mm
    hb_y = 354 * mm
    hb_w = 281 * mm
    hb_h = 59 * mm

    # Background Navy Container
    c.setFillColor(NAVY_DARK)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.roundRect(hb_x, hb_y, hb_w, hb_h, 4.5*mm, fill=1, stroke=1)

    # Top Gold Strip
    c.setFillColor(GOLD_BRIGHT)
    c.roundRect(hb_x, hb_y + hb_h - 2.5*mm, hb_w, 2.5*mm, 2*mm, fill=1, stroke=0)

    # GNDEC College Emblem
    emblem_path = os.path.join(FIG_DIR, "gndec_emblem.png")
    if os.path.exists(emblem_path):
        c.drawImage(emblem_path, hb_x + 3.5*mm, hb_y + 4.5*mm, width=32*mm, height=50*mm, preserveAspectRatio=True, mask='auto')

    # Central Institutional & Title Block
    cx = hb_x + 38 * mm
    cw = 168 * mm

    p_inst = Paragraph(
        "<font size='9.2' color='#F59E0B'><b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b></font><br/>"
        "<font size='11.5' color='#FFFFFF'><b>GURU NANAK DEV ENGINEERING COLLEGE, LUDHIANA</b></font><br/>"
        "<font size='7.8' color='#94A3B8'>MAJOR PROJECT (PRCS-103) • B.TECH (CSE) • BATCH 2023–2027 • NOVEMBER 2026</font>",
        ParagraphStyle('HInst', alignment=1, leading=11.5)
    )
    p_inst.wrap(cw, 22*mm)
    p_inst.drawOn(c, cx, hb_y + 36.8*mm)

    # Main Project Title (Clean, Bold, High Contrast)
    p_mtitle = Paragraph(
        "<font size='16.2' color='#FFFFFF'><b>POCKETLAW: TYPE YOUR PROBLEM, GET YOUR LEGAL RIGHTS</b></font>",
        ParagraphStyle('HTitle', alignment=1, leading=18)
    )
    p_mtitle.wrap(cw, 10*mm)
    p_mtitle.drawOn(c, cx, hb_y + 20.0*mm)

    # Subtitle
    p_sub = Paragraph(
        "<font size='8.3' color='#FEF3C7'><b>Hybrid AI-Powered Legal Assistance, Statutory Mapping (BNS/BNSS/BSA 2023) & Automated Legal Document Generation System</b></font>",
        ParagraphStyle('HSub', alignment=1, leading=10.5)
    )
    p_sub.wrap(cw, 10*mm)
    p_sub.drawOn(c, cx, hb_y + 7.5*mm)

    # Right Metadata Box (Submitted By & Guide)
    rx = hb_x + 209 * mm
    rw = 68.5 * mm
    c.setFillColor(colors.HexColor('#1E293B'))
    c.setStrokeColor(colors.HexColor('#334155'))
    c.setLineWidth(0.8)
    c.roundRect(rx, hb_y + 3.5*mm, rw, hb_h - 7*mm, 3*mm, fill=1, stroke=1)

    p_meta = Paragraph(
        "<font size='7.8' color='#F59E0B'><b>SUBMITTED BY:</b></font><br/>"
        "<font size='8.1' color='#FFFFFF'>• Khushpreet Kaur (2302591)</font><br/>"
        "<font size='8.1' color='#FFFFFF'>• Mohammad Shehzad (2302612)</font><br/>"
        "<font size='8.1' color='#FFFFFF'>• Neha Mehta (2302625)</font><br/>"
        "<font size='7.8' color='#F59E0B'><b>PROJECT GUIDE:</b></font><br/>"
        "<font size='8.4' color='#FFFFFF'><b>Dr. Hardeep Singh Kang</b></font><br/>"
        "<font size='7.2' color='#94A3B8'>Dept. of Computer Science & Engg.</font>",
        ParagraphStyle('HMeta', fontName='Helvetica', leading=9.2)
    )
    p_meta.wrap(rw - 4*mm, hb_h - 9*mm)
    p_meta.drawOn(c, rx + 2.5*mm, hb_y + 4.5*mm)

    # ══════════════════════════════════════════════════════════════════════════
    #  MAIN GRID (2 COLUMNS: x1 = 8mm, x2 = 151mm, w = 138mm)
    # ══════════════════════════════════════════════════════════════════════════
    col1_x = 8 * mm
    col2_x = 151 * mm
    col_w = 138 * mm

    # ──────────────────────────────────────────────────────────────────────────
    #  COLUMN 1
    # ──────────────────────────────────────────────────────────────────────────

    # --- Card 1.1: 1. Introduction & Problem Formulation ---
    c11_y = 272 * mm
    c11_h = 76 * mm
    draw_card_shell(col1_x, c11_y, col_w, c11_h, "1. Introduction & Problem Formulation")

    p_c11 = Paragraph(
        "<b>The Judicial Access Divide:</b> Over 50 Million litigations remain pending across Indian courts. "
        "Ordinary citizens facing everyday crises (cyber skimming, unlawful eviction, matrimonial disputes) are crippled by "
        "prohibitive advocate retainers (₹3,000–₹25,000) and intimidating archaic terminology.<br/><br/>"
        "<b>The BNS 2024 Transition Dilemma:</b> On 1 July 2024, the Republic of India repealed colonial-era penal codes "
        "(IPC 1860, CrPC 1973, Evidence Act 1872) and instituted the modern <i>Bharatiya Nyaya Sanhita (BNS)</i>, <i>BNSS</i>, and <i>BSA</i>. "
        "Citizens and police officers alike struggle with statutory renumbering and procedural cross-mappings.<br/><br/>"
        "<b>Limitations of Existing Portals:</b> Traditional databases (Indian Kanoon) offer complex 50-page raw judgments, "
        "commercial portals enforce referral paywalls, and general LLMs (ChatGPT) frequently hallucinate repealed IPC sections.",
        style_body
    )
    p_c11.wrap(col_w - 7*mm, c11_h - 11*mm)
    p_c11.drawOn(c, col1_x + 3.5*mm, c11_y + 2.5*mm)

    # --- Card 1.2: 1.3 Objectives (Exact Verbatim Bullets) ---
    c12_y = 198 * mm
    c12_h = 70 * mm
    draw_card_shell(col1_x, c12_y, col_w, c12_h, "1.3 Objectives (Official Approved Scope)", title_bg=NAVY_CARD, border_color=GOLD)

    # Intro line
    p_obj_in = Paragraph("<b>The project successfully executes the following 3 primary objectives:</b>", style_body_muted)
    p_obj_in.wrap(col_w - 7*mm, 5*mm)
    p_obj_in.drawOn(c, col1_x + 3.5*mm, c12_y + c12_h - 12.8*mm)

    objs_data = [
        ("1", "To develop an interface that understands the legal problem of the user and finds the relevant Indian laws, Acts, articles or sections for it.", 12.5*mm),
        ("2", "To give legal guidance, tell users about their legal rights, and provide the related emergency or authority contacts.", 12.5*mm),
        ("3", "To develop a document generation module that takes basic case details from the user and creates a properly formatted legal application that can be used in legal proceedings.", 15.5*mm)
    ]

    box_y = c12_y + c12_h - 15.0 * mm

    for num_str, obj_text, b_height in objs_data:
        box_y -= b_height

        # Micro-card container
        c.setFillColor(colors.HexColor('#F8FAFC'))
        c.setStrokeColor(colors.HexColor('#E2E8F0'))
        c.roundRect(col1_x + 3.5*mm, box_y, col_w - 7*mm, b_height - 1.5*mm, 2*mm, fill=1, stroke=1)

        # Numbered Gold Badge
        badge_cy = box_y + (b_height - 1.5*mm)/2
        c.setFillColor(GOLD)
        c.circle(col1_x + 7.5*mm, badge_cy, 2.8*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawCentredString(col1_x + 7.5*mm, badge_cy - 1.1*mm, num_str)

        # Verbatim Text
        p_ob = Paragraph(f"<b>{obj_text}</b>", style_obj)
        _, h_calc = p_ob.wrap(col_w - 18*mm, b_height)
        p_ob.drawOn(c, col1_x + 12.5*mm, badge_cy - h_calc/2 + 0.5*mm)

        box_y -= 0.5 * mm

    # Realization footer badge
    c.setFillColor(GOLD_LIGHT)
    c.roundRect(col1_x + 3.5*mm, c12_y + 2.5*mm, col_w - 7*mm, 5.0*mm, 1.5*mm, fill=1, stroke=0)
    p_rf = Paragraph("<font size='6.8' color='#B45309'><b>VERIFIED STATUS: 100% Realized in Code via Sparse VSM, Rights Engine & ReportLab Studio</b></font>", ParagraphStyle('ORF', alignment=1))
    p_rf.wrap(col_w - 8*mm, 4.5*mm)
    p_rf.drawOn(c, col1_x + 4*mm, c12_y + 3.0*mm)

    # --- Card 1.3: 3. System Architecture & Dual-Engine Workflow ---
    c13_y = 88 * mm
    c13_h = 106 * mm
    draw_card_shell(col1_x, c13_y, col_w, c13_h, "3. System Architecture & Dual-Engine Workflow")

    wf_img_path = os.path.join(FIG_DIR, "poster_workflow_diagram.png")
    if os.path.exists(wf_img_path):
        c.drawImage(wf_img_path, col1_x + 3.5*mm, c13_y + 23*mm, width=col_w - 7*mm, height=73*mm, preserveAspectRatio=True)

    p_wf_desc = Paragraph(
        "<b>Workflow Pipeline:</b> Natural language text or speech dictation is converted into a 15,000-D sparse vector. "
        "The Dual-Engine kernel scores cosine similarity against 2,290 Supreme Court chunks, maps colonial IPC sections to modern BNS 2023, "
        "and triggers ReportLab to compile court-ready vector PDFs stored in SQLite WAL.",
        style_body_muted
    )
    p_wf_desc.wrap(col_w - 7*mm, 20*mm)
    p_wf_desc.drawOn(c, col1_x + 3.5*mm, c13_y + 2.5*mm)

    # --- Card 1.4: 4. Tech Stack & Implementation ---
    c14_y = 20 * mm
    c14_h = 64 * mm
    draw_card_shell(col1_x, c14_y, col_w, c14_h, "4. Tech Stack & Algorithmic Core")

    # Grid of tech pills
    tech_pills = [
        ("React 18 SPA", "#0284C7", "#E0F2FE"),
        ("Python 3.14 / Flask", "#0F172A", "#F1F5F9"),
        ("Scikit-learn TF-IDF", "#B45309", "#FEF3C7"),
        ("SciPy CSR (99.08% Sparse)", "#15803D", "#DCFCE7"),
        ("Google Gemini API", "#7E22CE", "#F3E8FF"),
        ("ReportLab 3.6 PDF", "#BE123C", "#FFE4E6"),
        ("SQLite 3 WAL Mode", "#334155", "#F1F5F9"),
        ("Web Speech Voice API", "#0369A1", "#E0F2FE")
    ]

    px_start = col1_x + 3.5 * mm
    py_start = c14_y + c14_h - 14 * mm
    pill_w = 32 * mm
    pill_h = 5 * mm

    for i, (p_txt, b_col, bg_col) in enumerate(tech_pills):
        col_idx = i % 4
        row_idx = i // 4
        px = px_start + col_idx * (pill_w + 1.8*mm)
        py = py_start - row_idx * (pill_h + 1.8*mm)

        c.setFillColor(colors.HexColor(bg_col))
        c.setStrokeColor(colors.HexColor(b_col))
        c.setLineWidth(0.7)
        c.roundRect(px, py, pill_w, pill_h, 1.5*mm, fill=1, stroke=1)

        c.setFillColor(colors.HexColor(b_col))
        c.setFont('Helvetica-Bold', 6.8)
        c.drawCentredString(px + pill_w/2, py + 1.4*mm, p_txt)

    # Mathematical Algorithm Box
    p_alg = Paragraph(
        "<b>Algorithmic Formulation:</b><br/>"
        "• <b>Sublinear TF-IDF:</b> <i>w(t, d) = (1 + ln(tf)) · ln(1 + N/df)</i> (dampens repeated legal terms).<br/>"
        "• <b>Cosine Similarity:</b> <i>sim(q, d) = (q · d) / (||q|| ||d||) ≥ τ (0.05)</i> across 2,290 judicial chunks.<br/>"
        "• <b>Performance:</b> 41.6ms average query latency on CPU; 100% offline fallback without cloud APIs.",
        style_body
    )
    p_alg.wrap(col_w - 7*mm, 28*mm)
    p_alg.drawOn(c, col1_x + 3.5*mm, c14_y + 2.5*mm)

    # ──────────────────────────────────────────────────────────────────────────
    #  COLUMN 2
    # ──────────────────────────────────────────────────────────────────────────

    # --- Card 2.1: 5. Results & Empirical Benchmark ---
    c21_y = 230 * mm
    c21_h = 118 * mm
    draw_card_shell(col2_x, c21_y, col_w, c21_h, "5. Results & Empirical Retrieval Benchmark")

    # Embed Metrics Chart
    chart_path = os.path.join(FIG_DIR, "poster_metrics_chart.png")
    if os.path.exists(chart_path):
        c.drawImage(chart_path, col2_x + 3.5*mm, c21_y + 58*mm, width=col_w - 7*mm, height=50*mm, preserveAspectRatio=True)

    # Metric Cards Row
    m_boxes = [
        ("Precision@3", "90.0%", "#1E293B"),
        ("Precision@5", "84.0%", "#334155"),
        ("Mean Reciprocal Rank", "0.92 MRR", "#B45309"),
        ("Average Latency", "41.6 ms", "#0284C7"),
        ("CSR Matrix Sparsity", "99.08%", "#0F172A"),
        ("Automated Tests", "100% Pass", "#15803D")
    ]
    mb_w = 42 * mm
    mb_h = 10 * mm
    mb_xs = col2_x + 4 * mm
    mb_ys = c21_y + 34 * mm

    for idx, (m_title, m_val, m_col) in enumerate(m_boxes):
        c_i = idx % 3
        r_i = idx // 3
        bx = mb_xs + c_i * (mb_w + 2.5*mm)
        by = mb_ys - r_i * (mb_h + 2*mm)

        c.setFillColor(colors.HexColor('#F8FAFC'))
        c.setStrokeColor(colors.HexColor('#E2E8F0'))
        c.roundRect(bx, by, mb_w, mb_h, 2*mm, fill=1, stroke=1)

        c.setFillColor(colors.HexColor(m_col))
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(bx + mb_w/2, by + 4.8*mm, m_val)

        c.setFillColor(TEXT_MUTED)
        c.setFont('Helvetica', 6.8)
        c.drawCentredString(bx + mb_w/2, by + 1.6*mm, m_title)

    # Narrative on Benchmark
    p_c21_desc = Paragraph(
        "<b>Rigorous Evaluation:</b> Evaluated across 10 ground-truth Supreme Court benchmark queries "
        "(Cyber fraud, defective products, tenancy eviction, police custody, cheque bounce). "
        "The MRR of 0.92 verifies that relevant landmark precedents rank #1 or #2 for over 85% of cases, "
        "while SQLite WAL mode sustained 50 concurrent transactions with zero lock exceptions.",
        style_body_muted
    )
    p_c21_desc.wrap(col_w - 7*mm, 18*mm)
    p_c21_desc.drawOn(c, col2_x + 3.5*mm, c21_y + 2.5*mm)

    # --- Card 2.2: Live UI & Document Studio ---
    c22_y = 104 * mm
    c22_h = 122 * mm
    draw_card_shell(col2_x, c22_y, col_w, c22_h, "User Interface & Court-Ready Drafting Studio")

    # Embed Screenshots Side-by-Side
    ui1_path = os.path.join(FIG_DIR, "fig_5_1_home_consultation.png")
    ui2_path = os.path.join(FIG_DIR, "fig_5_3_documents_studio.png")

    img_w = 64 * mm
    img_h = 44 * mm

    if os.path.exists(ui1_path):
        c.drawImage(ui1_path, col2_x + 3.5*mm, c22_y + 67*mm, width=img_w, height=img_h, preserveAspectRatio=True)
        c.setFillColor(NAVY_DARK)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(col2_x + 3.5*mm + img_w/2, c22_y + 63.5*mm, "Home Consultation & BNS Section Matcher")

    if os.path.exists(ui2_path):
        c.drawImage(ui2_path, col2_x + 70.5*mm, c22_y + 67*mm, width=img_w, height=img_h, preserveAspectRatio=True)
        c.setFillColor(NAVY_DARK)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(col2_x + 70.5*mm + img_w/2, c22_y + 63.5*mm, "Court-Ready Document Drafting Studio")

    # UI Features Breakdown
    p_ui_desc = Paragraph(
        "<b>Core Interface Innovations:</b><br/>"
        "• <b>Multilingual Ingestion:</b> Supports voice dictation and typed queries in English, Hindi, and Punjabi.<br/>"
        "• <b>Actionable Survival Cards:</b> Outlines constitutional rights (Art 22, Zero FIR under Sec 173 BNSS), limitation deadlines, and national emergency contacts (1930 Cybercrime, 1091 Women Helpline).<br/>"
        "• <b>Dynamic Live Drafting Preview:</b> Live character-by-character form rendering coupled with server-side ReportLab compilation for formal First Information Reports, Sec 80 CPC Legal Notices, Affidavits, and E-Daakhil Consumer Complaints.",
        style_body
    )
    p_ui_desc.wrap(col_w - 7*mm, 58*mm)
    p_ui_desc.drawOn(c, col2_x + 3.5*mm, c22_y + 2.5*mm)

    # --- Card 2.3: 6. Conclusion & Future Scope ---
    c23_y = 20 * mm
    c23_h = 80 * mm
    draw_card_shell(col2_x, c23_y, col_w, c23_h, "6. Conclusion & Future Technological Roadmap")

    p_c23 = Paragraph(
        "<b>Key Project Contributions:</b><br/>"
        "• <b>Democratized Legal Access:</b> Delivered a functional, zero-cost legal diagnostic engine for citizens.<br/>"
        "• <b>Zero Cloud Dependency:</b> 100% offline-capable sparse retrieval running in &lt;150MB RAM.<br/>"
        "• <b>Modern BNS 2023 Synchronization:</b> Seamlessly bridges the 2024 criminal law transition.<br/>"
        "• <b>Court-Ready Vector Instruments:</b> Automated drafting conforming to statutory court specifications.<br/>"
        "<b>Future Scope & Technological Roadmap:</b><br/>"
        "1. <b>Indic Voice Interface:</b> Whisper ASR and Coqui TTS for illiterate citizens across rural districts.<br/>"
        "2. <b>Judicial E-Filing Gateways:</b> Direct integration with Supreme Court e-Courts and E-Daakhil APIs.<br/>"
        "3. <b>Blockchain Document Notarization:</b> Smart contract hashing for tamper-evident proof of notice delivery.<br/>"
        "4. <b>Fine-Tuned Legal LLM:</b> Domain-adaptive Legal-Llama for localized Indian High Court case law.",
        style_body
    )
    p_c23.wrap(col_w - 7*mm, c23_h - 10*mm)
    p_c23.drawOn(c, col2_x + 3.5*mm, c23_y + 2.5*mm)

    # ══════════════════════════════════════════════════════════════════════════
    #  BOTTOM FOOTER STRIP
    # ══════════════════════════════════════════════════════════════════════════
    fb_x = 8 * mm
    fb_y = 7 * mm
    fb_w = 281 * mm
    fb_h = 9 * mm

    c.setFillColor(NAVY_DARK)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(fb_x, fb_y, fb_w, fb_h, 2*mm, fill=1, stroke=1)

    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawString(fb_x + 4*mm, fb_y + 2.8*mm, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING, GNDEC LUDHIANA")

    c.setFillColor(GOLD_BRIGHT)
    c.drawCentredString(fb_x + fb_w/2, fb_y + 2.8*mm, "MAJOR PROJECT (PRCS-103) • BATCH: 2023–2027")

    c.setFillColor(WHITE)
    c.drawRightString(fb_x + fb_w - 4*mm, fb_y + 2.8*mm, "PROJECT GUIDE: DR. HARDEEP SINGH KANG | NOVEMBER 2026")

    # Finalize PDF
    c.showPage()
    c.save()
    print(f"Successfully generated PDF: {PDF_PATH}")

    # ══════════════════════════════════════════════════════════════════════════
    #  RENDER TO 300 DPI PNG VIA PYMUPDF (fitz)
    # ══════════════════════════════════════════════════════════════════════════
    print(f"Rendering 300 DPI raster preview to: {PNG_PATH} ...")
    doc = fitz.open(PDF_PATH)
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(PNG_PATH)
    doc.close()

    pdf_size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
    png_size_mb = os.path.getsize(PNG_PATH) / (1024 * 1024)
    print(f"Poster generation complete!")
    print(f"  - PDF: {pdf_size_mb:.2f} MB ({PDF_PATH})")
    print(f"  - PNG: {png_size_mb:.2f} MB ({PNG_PATH}) | Dimensions: {pix.width} x {pix.height} px")

if __name__ == "__main__":
    create_poster()

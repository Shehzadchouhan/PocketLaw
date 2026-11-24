"""
PocketLaw - Major Project Final Evaluation Presentation (.pptx) Generator
GNDEC Ludhiana - Department of Computer Science and Engineering
Major Project (PRCS-103) | 7th Semester (Batch: 2023-2027) | November 2026

Generates a widescreen 16:9 (13.333 in x 7.5 in) publication-quality presentation
strictly consistent with the GNDEC Final Project Report and Evaluation Guidelines.
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = r"C:\Users\Shehzad\OneDrive\Desktop\PROJECTS\PocketLaw\GNDEC_Major_Project_Report"
FIG_DIR = os.path.join(BASE_DIR, "figures")
OUTPUT_PPTX = os.path.join(BASE_DIR, "PocketLaw_Major_Project_Presentation.pptx")

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY = RGBColor(30, 41, 59)          # #1E293B (Deep Navy)
NAVY_LIGHT = RGBColor(51, 65, 85)    # #334155 (Slate Navy)
GOLD = RGBColor(180, 83, 9)          # #B45309 (Warm Amber / Gold)
GOLD_LIGHT = RGBColor(254, 243, 199) # #FEF3C7 (Soft Gold Tint)
GOLD_BORDER = RGBColor(245, 158, 11) # #F59E0B (Vibrant Gold Border)
WHITE = RGBColor(255, 255, 255)      # #FFFFFF (Crisp White)
BG_CARD = RGBColor(248, 250, 252)    # #F8FAFC (Soft Light Grey)
BORDER = RGBColor(226, 232, 240)     # #E2E8F0 (Subtle Divider / Border)
SLATE = RGBColor(71, 85, 105)        # #475569 (Secondary Text)
SLATE_DARK = RGBColor(30, 41, 59)    # #1E293B (Primary Text)
GREEN = RGBColor(21, 128, 61)        # #15803D (Pass Green)
GREEN_BG = RGBColor(240, 253, 244)   # #F0FDF4

FONT_HEADING = 'Segoe UI'
FONT_BODY = 'Segoe UI'

# ── Helpers ───────────────────────────────────────────────────────────────────

def create_base_slide(prs, chapter_tag, title_text, slide_num):
    """Creates a standardized slide with top banner, title, divider, footer, and page count."""
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 1. Top Accent Line (Gold)
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = GOLD
    top_bar.line.fill.background()

    # 2. Header Container
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.733), Inches(0.95))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Chapter Tag
    p_tag = tf.paragraphs[0]
    p_tag.text = chapter_tag.upper()
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(10.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = GOLD
    p_tag.space_after = Pt(2)

    # Slide Title
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

    # Header Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.15), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()

    # 3. Footer Bar
    f_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.02))
    f_line.fill.solid()
    f_line.fill.fore_color.rgb = BORDER
    f_line.line.fill.background()

    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(8.5), Inches(0.35))
    tf_f = footer_box.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    pf = tf_f.paragraphs[0]
    pf.text = "POCKETLAW: TYPE YOUR PROBLEM, GET YOUR LEGAL RIGHTS | Dept. of CSE, GNDEC Ludhiana"
    pf.font.name = FONT_BODY
    pf.font.size = Pt(9)
    pf.font.color.rgb = SLATE

    pager_box = slide.shapes.add_textbox(Inches(9.333), Inches(6.98), Inches(3.2), Inches(0.35))
    tf_p = pager_box.text_frame
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
    pp = tf_p.paragraphs[0]
    pp.alignment = PP_ALIGN.RIGHT
    pp.text = f"Slide {slide_num} of 10 | PRCS-103 | Nov 2026"
    pp.font.name = FONT_BODY
    pp.font.size = Pt(9)
    pp.font.bold = True
    pp.font.color.rgb = SLATE

    return slide

def add_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=BORDER):
    """Draws a rounded rectangular card shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_bullet_run(p, prefix, text, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10), font_name=FONT_BODY, space_after=Pt(4)):
    """Sets a bullet run with bold colored prefix and normal text."""
    p.text = ""
    r1 = p.add_run()
    r1.text = prefix + " "
    r1.font.bold = True
    r1.font.size = font_size
    r1.font.name = font_name
    r1.font.color.rgb = prefix_color
    
    r2 = p.add_run()
    r2.text = text
    r2.font.bold = False
    r2.font.size = font_size
    r2.font.name = font_name
    r2.font.color.rgb = text_color
    p.space_after = space_after

def add_speaker_notes(slide, notes_text):
    """Appends viva/defense speaker notes to the slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1: TITLE SLIDE
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Top Accent Gold Banner
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = GOLD
    top_bar.line.fill.background()

    # Department & College Banner
    banner_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.733), Inches(0.7))
    tf_b = banner_box.text_frame
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p1 = tf_b.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

    p2 = tf_b.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "GURU NANAK DEV ENGINEERING COLLEGE, LUDHIANA"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = GOLD

    # Emblem Center
    emblem_path = os.path.join(FIG_DIR, "gndec_emblem.png")
    if os.path.exists(emblem_path):
        slide.shapes.add_picture(emblem_path, Inches(5.966), Inches(1.15), width=Inches(1.4))

    # Badge: Evaluation Info
    badge_box = slide.shapes.add_textbox(Inches(2.0), Inches(2.72), Inches(9.333), Inches(0.35))
    tf_bd = badge_box.text_frame
    tf_bd.margin_left = tf_bd.margin_top = tf_bd.margin_right = tf_bd.margin_bottom = 0
    p_bd = tf_bd.paragraphs[0]
    p_bd.alignment = PP_ALIGN.CENTER
    p_bd.text = "MAJOR PROJECT (PRCS-103) • FINAL EVALUATION • 7TH SEMESTER (BATCH: 2023–2027)"
    p_bd.font.name = FONT_HEADING
    p_bd.font.size = Pt(11)
    p_bd.font.bold = True
    p_bd.font.color.rgb = GOLD

    # Project Title (Exact Verified Title)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(3.08), Inches(11.733), Inches(0.9))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.alignment = PP_ALIGN.CENTER
    p_t.text = "POCKETLAW: TYPE YOUR PROBLEM, GET YOUR LEGAL RIGHTS"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1.2), Inches(3.95), Inches(10.933), Inches(0.55))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.alignment = PP_ALIGN.CENTER
    p_s.text = "An Intelligent Legal Information Retrieval, Modern BNS 2023 Harmonization & Automated Court-Ready Document Drafting Platform"
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(13)
    p_s.font.color.rgb = SLATE

    # Left Card: Submitted By
    add_card(slide, Inches(1.2), Inches(4.75), Inches(5.2), Inches(2.05), bg_color=BG_CARD, border_color=BORDER)
    tb_subby = slide.shapes.add_textbox(Inches(1.45), Inches(4.88), Inches(4.7), Inches(1.8))
    tf_sb = tb_subby.text_frame
    tf_sb.margin_left = tf_sb.margin_top = tf_sb.margin_right = tf_sb.margin_bottom = 0
    
    psb_h = tf_sb.paragraphs[0]
    psb_h.text = "SUBMITTED BY:"
    psb_h.font.name = FONT_HEADING
    psb_h.font.size = Pt(11)
    psb_h.font.bold = True
    psb_h.font.color.rgb = GOLD
    psb_h.space_after = Pt(4)

    team = [
        "Khushpreet Kaur (2302591)",
        "Mohammad Shehzad (2302612)",
        "Neha Mehta (2302625)"
    ]
    for mem in team:
        pm = tf_sb.add_paragraph()
        pm.text = f"•  {mem}"
        pm.font.name = FONT_BODY
        pm.font.size = Pt(12)
        pm.font.bold = True
        pm.font.color.rgb = NAVY
        pm.space_after = Pt(2)
    
    pdeg = tf_sb.add_paragraph()
    pdeg.text = "B.Tech - Computer Science and Engineering"
    pdeg.font.name = FONT_BODY
    pdeg.font.size = Pt(10)
    pdeg.font.color.rgb = SLATE

    # Right Card: Submitted To
    add_card(slide, Inches(6.933), Inches(4.75), Inches(5.2), Inches(2.05), bg_color=BG_CARD, border_color=BORDER)
    tb_subto = slide.shapes.add_textbox(Inches(7.183), Inches(4.88), Inches(4.7), Inches(1.8))
    tf_st = tb_subto.text_frame
    tf_st.margin_left = tf_st.margin_top = tf_st.margin_right = tf_st.margin_bottom = 0

    pst_h = tf_st.paragraphs[0]
    pst_h.text = "SUBMITTED TO (PROJECT GUIDE):"
    pst_h.font.name = FONT_HEADING
    pst_h.font.size = Pt(11)
    pst_h.font.bold = True
    pst_h.font.color.rgb = GOLD
    pst_h.space_after = Pt(4)

    pg = tf_st.add_paragraph()
    pg.text = "Dr. Hardeep Singh Kang"
    pg.font.name = FONT_BODY
    pg.font.size = Pt(14)
    pg.font.bold = True
    pg.font.color.rgb = NAVY
    pg.space_after = Pt(2)

    pdes = tf_st.add_paragraph()
    pdes.text = "Project Guide, Department of CSE\nGNDEC, Ludhiana - 141006\nNovember, 2026"
    pdes.font.name = FONT_BODY
    pdes.font.size = Pt(11)
    pdes.font.color.rgb = SLATE

    add_speaker_notes(slide,
        "Respected members of the Evaluation Committee, our Project Guide Dr. Hardeep Singh Kang, and faculty members: "
        "Good morning. We—Khushpreet Kaur, Mohammad Shehzad, and Neha Mehta—welcome you to our Major Project Final Evaluation presentation "
        "for 'PocketLaw: Type Your Problem, Get Your Legal Rights'. In our presentation today, we will demonstrate how PocketLaw bridges India's "
        "deep judicial access divide through offline-capable AI information retrieval, modern BNS 2023 legal harmonization, and automated court-ready drafting."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2: 1. INTRODUCTION & PROBLEM FORMULATION
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_2(prs):
    slide = create_base_slide(prs, "Chapter 1: Background & Need Recognition", "1. Introduction & Problem Formulation", 2)

    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.4)
    h_pos = Inches(4.45)

    # Column 1: Project Overview & Need Recognition
    add_card(slide, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "Project Overview & Need"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    pts1 = [
        ("• Project Category:", "Application-Based & Institutional Software engineered for societal utility."),
        ("• The Judicial Crisis:", "Over 50 Million cases currently pending across Indian subordinate, High, and Supreme benches."),
        ("• The 'Golden Hours':", "Critical initial actions (prompt FIR under CrPC 154 / BNSS 173 or Legal Notice under CPC 80) dictate case success."),
        ("• Cognitive Barrier:", "Archaic legal terminology and fear of procedural intimidation dissuade citizens from seeking rightful remedies.")
    ]
    for prefix, desc in pts1:
        p = tf1.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10.5), space_after=Pt(6))

    # Column 2: Problem Formulation
    c2_x = Inches(0.8) + col_w + gap
    add_card(slide, c2_x, top_pos, col_w, h_pos)
    tb2 = slide.shapes.add_textbox(c2_x + Inches(0.2), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    p.text = "Problem Formulation"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    pts2 = [
        ("• Economic Inequality:", "Initial advocate retainers range from ₹3,000 to ₹25,000, excluding low-income and middle-class victims."),
        ("• Procedural Obscurity:", "Laypersons cannot determine whether an offense is cognizable, bailable, or time-barred by limitation statutes."),
        ("• BNS 2024 Dilemma:", "On 1 July 2024, India overhauled colonial laws (IPC, CrPC, Evidence Act) into BNS, BNSS, and BSA. Citizens struggle with section conversions."),
        ("• Unstructured Grievances:", "Victims write emotional statements lacking legal averments required for court admissibility.")
    ]
    for prefix, desc in pts2:
        p = tf2.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10.5), space_after=Pt(6))

    # Column 3: Existing System Limitations
    c3_x = c2_x + col_w + gap
    add_card(slide, c3_x, top_pos, col_w, h_pos)
    tb3 = slide.shapes.add_textbox(c3_x + Inches(0.2), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0

    p = tf3.paragraphs[0]
    p.text = "Existing System Limitations"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    pts3 = [
        ("• Traditional Law Portals:", "Indian Kanoon provides raw keyword queries over 50-page complex judgments unreadable by non-lawyers."),
        ("• Commercial Legal Tech:", "Vakilsearch / Cleartax enforce paywalls and prioritize monetized advocate referrals over instant free guidance."),
        ("• Commercial LLMs (ChatGPT):", "Prone to dangerous hallucinations, cite repealed colonial IPC sections, and leak private sensitive grievances to external clouds."),
        ("• Zero Drafting Automation:", "No existing system dynamically generates verified, jurisdictional vector PDF documents locally.")
    ]
    for prefix, desc in pts3:
        p = tf3.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10.5), space_after=Pt(6))

    # Bottom Highlight Callout
    banner = add_card(slide, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.72), bg_color=GOLD_LIGHT, border_color=GOLD_BORDER)
    tbb = slide.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.333), Inches(0.55))
    tfb = tbb.text_frame
    tfb.word_wrap = True
    tfb.margin_left = tfb.margin_top = tfb.margin_right = tfb.margin_bottom = 0
    pb = tfb.paragraphs[0]
    add_bullet_run(pb, "Key Project Takeaway:", "PocketLaw provides an instantaneous, privacy-preserving, and hallucination-free legal intelligence engine that translates everyday grievances into actionable constitutional rights and court-ready vector documents.", prefix_color=GOLD, text_color=NAVY, font_size=Pt(11))

    add_speaker_notes(slide,
        "Here in Chapter 1, we establish the core problem statement. Access to justice in India faces two gigantic hurdles: "
        "a staggering backlog of 50 million cases, and an economic barrier where lawyers charge thousands of rupees just for a preliminary consultation. "
        "Furthermore, on July 1st, 2024, India enacted the Bharatiya Nyaya Sanhita (BNS), replacing the 164-year-old IPC. "
        "Existing tools like Indian Kanoon are designed for advocates, while general AI like ChatGPT hallucinates and cites repealed statutes. "
        "PocketLaw solves this by providing instant, free, and accurate guidance grounded in real Supreme Court precedents."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3: 1.3 OBJECTIVES (EXACT 3 VERBATIM BULLETS)
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_3(prs):
    slide = create_base_slide(prs, "Chapter 1: Formal Project Scope", "1.3 Objectives", 3)

    # Intro line
    tb_intro = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.4))
    tf_in = tb_intro.text_frame
    tf_in.margin_left = tf_in.margin_top = tf_in.margin_right = tf_in.margin_bottom = 0
    pin = tf_in.paragraphs[0]
    pin.text = "The proposed Major Project was formulated and executed with the following three primary objectives:"
    pin.font.name = FONT_BODY
    pin.font.size = Pt(13)
    pin.font.bold = True
    pin.font.color.rgb = NAVY

    # 3 Distinct Objective Cards (Exact Verbatim Text)
    objs = [
        ("01",
         "To develop an interface that understands users' legal problems and identifies the relevant Indian laws, Acts, articles, or sections.",
         "Technical Realization & Evidence:",
         "Engineered an intuitive natural language input interface powered by a 15,000-dimensional sparse Vector Space Model (VSM) using sublinear TF-IDF weighting over 2,290 verified Supreme Court chunks, returning relevant statutes and precedents in 41.6 milliseconds."),
        
        ("02",
         "To provide legal guidance, legal rights, and relevant emergency or authority contacts.",
         "Technical Realization & Evidence:",
         "Constructed a diagnostic legal rights engine outlining constitutional safeguards (Article 22, Zero FIR under Sec 173 BNSS), step-by-step citizen survival protocols, and emergency tele-helpline routing (Cybercrime 1930, Women 1091, Tele-MANAS 14416)."),
        
        ("03",
         "To develop an automated document-generation module that collects basic case details and creates formatted legal applications for users to be used for legal proceedings.",
         "Technical Realization & Evidence:",
         "Implemented a dual-layer document studio featuring real-time client preview and server-side ReportLab compilation generating court-admissible vector PDFs for First Information Reports, Section 80 CPC Notices, Sworn Affidavits, and Consumer Complaints.")
    ]

    card_h = Inches(1.52)
    start_y = Inches(1.8)
    spacing = Inches(1.68)

    for i, (num, verbatim_text, impl_label, impl_desc) in enumerate(objs):
        y_pos = start_y + (i * spacing)
        
        # Background card
        add_card(slide, Inches(0.8), y_pos, Inches(11.733), card_h, bg_color=BG_CARD, border_color=BORDER)

        # Number Badge
        add_card(slide, Inches(1.05), y_pos + Inches(0.2), Inches(0.9), Inches(1.12), bg_color=NAVY, border_color=GOLD)
        tb_num = slide.shapes.add_textbox(Inches(1.05), y_pos + Inches(0.42), Inches(0.9), Inches(0.6))
        tfn = tb_num.text_frame
        tfn.margin_left = tfn.margin_top = tfn.margin_right = tfn.margin_bottom = 0
        pn = tfn.paragraphs[0]
        pn.alignment = PP_ALIGN.CENTER
        pn.text = num
        pn.font.name = FONT_HEADING
        pn.font.size = Pt(22)
        pn.font.bold = True
        pn.font.color.rgb = GOLD

        # Content Box
        tb_c = slide.shapes.add_textbox(Inches(2.2), y_pos + Inches(0.16), Inches(10.1), Inches(1.2))
        tfc = tb_c.text_frame
        tfc.word_wrap = True
        tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0

        # Verbatim Objective
        p_obj = tfc.paragraphs[0]
        p_obj.text = verbatim_text
        p_obj.font.name = FONT_HEADING
        p_obj.font.size = Pt(13)
        p_obj.font.bold = True
        p_obj.font.color.rgb = NAVY
        p_obj.space_after = Pt(4)

        # Implementation Realization
        p_imp = tfc.add_paragraph()
        add_bullet_run(p_imp, impl_label, impl_desc, prefix_color=GOLD, text_color=SLATE, font_size=Pt(10.5))

    add_speaker_notes(slide,
        "Slide 3 presents our three exact, approved project objectives verbatim, as documented in our midterm and final reports. "
        "Objective 1: Understanding user problems and finding relevant laws—realized through our sublinear TF-IDF vector space model with sub-50ms latency. "
        "Objective 2: Providing actionable citizen rights and emergency contacts—realized via our survival guidance engine and 1930/1091 helplines. "
        "Objective 3: Generating properly formatted legal applications—realized via our ReportLab vector PDF drafting studio producing FIRs, notices, and affidavits."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4: 1.7 PROPOSED SYSTEM & UNIQUE FEATURES
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_4(prs):
    slide = create_base_slide(prs, "Chapter 1: System Innovation", "1.7 Proposed System & Unique Features", 4)

    # Left: Block Diagram Image
    diagram_path = os.path.join(FIG_DIR, "fig_1_1_block_diagram.png")
    if os.path.exists(diagram_path):
        add_card(slide, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3), bg_color=WHITE, border_color=BORDER)
        slide.shapes.add_picture(diagram_path, Inches(0.9), Inches(1.5), width=Inches(5.4))
        
        # Caption below diagram
        tb_cap = slide.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(5.6), Inches(0.3))
        tfc = tb_cap.text_frame
        tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0
        pc = tfc.paragraphs[0]
        pc.alignment = PP_ALIGN.CENTER
        pc.text = "Figure 1.1: High-Level Architectural Block Diagram"
        pc.font.name = FONT_BODY
        pc.font.size = Pt(9.5)
        pc.font.italic = True
        pc.font.color.rgb = SLATE

    # Right: 4 Unique Feature Cards
    right_x = Inches(6.65)
    card_w = Inches(5.88)
    card_h = Inches(1.2)
    start_y = Inches(1.4)
    gap = Inches(0.16)

    features = [
        ("Hybrid AI Legal Engine (Dual-Engine RAG)",
         "Combines offline 15,000-D sparse TF-IDF retrieval (SciPy CSR) with Google Gemini synthesis under strict prompt grounding guardrails; guarantees 100% offline fallback."),
        
        ("Native IPC-to-BNS 2023 Statutory Mapping",
         "First legal platform to cross-map colonial provisions (IPC 1860, CrPC 1973, Evidence Act 1872) directly to Bharatiya Nyaya Sanhita (BNS) 2023, BNSS, and BSA 2023."),
        
        ("Court-Ready Vector PDF Drafting Studio",
         "Real-time client-side live preview + backend ReportLab compilation for formal FIRs (BNSS Sec 173), Sec 80 CPC Legal Notices, Affidavits with Notary jurats, and Consumer Complaints."),
        
        ("Actionable Survival Steps & Emergency Helplines",
         "Instant chronological checklists, statutory limitation alerts, and one-tap emergency contact routing (National Cyber Helpline 1930, Women Emergency 1091, Tele-MANAS 14416).")
    ]

    for i, (title, desc) in enumerate(features):
        cy = start_y + i * (card_h + gap)
        add_card(slide, right_x, cy, card_w, card_h, bg_color=BG_CARD, border_color=BORDER)
        
        tb = slide.shapes.add_textbox(right_x + Inches(0.2), cy + Inches(0.12), card_w - Inches(0.4), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = f"{i+1}. {title}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.space_after = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = SLATE

    add_speaker_notes(slide,
        "In Slide 4, Figure 1.1 illustrates PocketLaw's end-to-end architecture. "
        "The system has four standout innovations: "
        "First, our dual-engine RAG combines local sparse TF-IDF with Google Gemini—if the internet drops, our local extractive engine still works 100% offline. "
        "Second, we natively support the new criminal laws of 2024—for example, converting Section 420 of IPC automatically into Section 318(4) of BNS. "
        "Third, our document studio compiles vector PDFs complete with legal headers and verification clauses. "
        "Fourth, we empower citizens with actionable survival checklists and national helplines."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5: 2. REQUIREMENT ANALYSIS & SYSTEM SPECIFICATION
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_5(prs):
    slide = create_base_slide(prs, "Chapter 2: Analysis & Process Model", "2. Requirement Analysis and System Specification", 5)

    # Left Column: Feasibility & Core SRS
    col_w = Inches(5.6)
    add_card(slide, Inches(0.8), Inches(1.4), col_w, Inches(5.3), bg_color=BG_CARD, border_color=BORDER)
    
    tb_left = slide.shapes.add_textbox(Inches(1.0), Inches(1.52), col_w - Inches(0.4), Inches(5.0))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p = tf_l.paragraphs[0]
    p.text = "Feasibility Study & SRS Analysis"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    feas_items = [
        ("• Technical Feasibility:", "Open-source Python, Flask, React, and SQLite stack running entirely on commodity CPUs with <150MB memory footprint."),
        ("• Economical Feasibility:", "Zero licensing costs; operates without expensive enterprise vector DB subscriptions (Pinecone/Milvus)."),
        ("• Operational Feasibility:", "Designed for multilingual, non-technical Indian citizens without requiring prior legal training.")
    ]
    for prefix, desc in feas_items:
        p = tf_l.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=GOLD, text_color=SLATE, font_size=Pt(10.5), space_after=Pt(4))

    p_srs = tf_l.add_paragraph()
    p_srs.text = "Functional & Non-Functional Requirements"
    p_srs.font.name = FONT_HEADING
    p_srs.font.size = Pt(12)
    p_srs.font.bold = True
    p_srs.font.color.rgb = NAVY
    p_srs.space_before = Pt(6)
    p_srs.space_after = Pt(4)

    srs_items = [
        ("• FR-1 to FR-4 (Grievance Analysis):", "Multilingual text ingestion, BNS/precedent retrieval, rights extraction."),
        ("• FR-5 to FR-8 (Document Studio):", "Interactive forms, live preview, court-ready PDF generation for 4 instruments."),
        ("• FR-9 to FR-10 (Security & Persistence):", "PBKDF2-SHA256 password hashing, stateless JWT session tokens."),
        ("• Performance & Reliability:", "Sub-50ms CPU query latency, SQLite WAL mode, zero hallucination guardrails.")
    ]
    for prefix, desc in srs_items:
        p = tf_l.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10), space_after=Pt(3))

    # Right Column: Agile SDLC Sprints & Diagram
    right_x = Inches(6.65)
    r_w = Inches(5.88)
    add_card(slide, right_x, Inches(1.4), r_w, Inches(5.3), bg_color=WHITE, border_color=BORDER)

    # Embed SDLC Diagram
    sdlc_path = os.path.join(FIG_DIR, "fig_2_1_agile_sdlc.png")
    if os.path.exists(sdlc_path):
        slide.shapes.add_picture(sdlc_path, right_x + Inches(0.15), Inches(1.5), width=r_w - Inches(0.3))

    # Caption / Sprint Details
    tb_sdlc = slide.shapes.add_textbox(right_x + Inches(0.2), Inches(4.75), r_w - Inches(0.4), Inches(1.8))
    tfs = tb_sdlc.text_frame
    tfs.word_wrap = True
    tfs.margin_left = tfs.margin_top = tfs.margin_right = tfs.margin_bottom = 0

    ps = tfs.paragraphs[0]
    ps.text = "6 Iterative Agile Development Sprints:"
    ps.font.name = FONT_HEADING
    ps.font.size = Pt(11)
    ps.font.bold = True
    ps.font.color.rgb = NAVY
    ps.space_after = Pt(3)

    sprints = [
        ("• Sprint 1-2:", "Corpus curation (2,290 chunks), TF-IDF vectorizer & CSR sparse kernel."),
        ("• Sprint 3-4:", "ReportLab vector PDF engine, React SPA client & live drafting preview."),
        ("• Sprint 5-6:", "SQLite WAL database integration, JWT auth, load testing & academic IR evaluation.")
    ]
    for s_title, s_desc in sprints:
        p = tfs.add_paragraph()
        add_bullet_run(p, s_title, s_desc, prefix_color=GOLD, text_color=SLATE, font_size=Pt(9.5), space_after=Pt(2))

    add_speaker_notes(slide,
        "Chapter 2 covers our Requirement Analysis and Agile Development process. "
        "Our feasibility study proved that PocketLaw runs efficiently on standard hardware without any recurring subscription costs. "
        "We followed an Agile Scrum framework divided across 6 two-week sprints. "
        "Sprints 1 and 2 built the offline NLP kernel; Sprints 3 and 4 implemented the PDF drafting studio and React UI; "
        "while Sprints 5 and 6 focused on security, SQLite WAL mode, and academic evaluation."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6: 3. SYSTEM DESIGN
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_6(prs):
    slide = create_base_slide(prs, "Chapter 3: Architecture & Schemas", "3. System Design", 6)

    col_w = Inches(5.66)
    gap = Inches(0.4)

    # Left Column: System Architecture & DFDs
    add_card(slide, Inches(0.8), Inches(1.4), col_w, Inches(5.3), bg_color=WHITE, border_color=BORDER)
    
    # Title
    tb_at = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), col_w - Inches(0.4), Inches(0.4))
    tf_at = tb_at.text_frame
    tf_at.margin_left = tf_at.margin_top = tf_at.margin_right = tf_at.margin_bottom = 0
    p = tf_at.paragraphs[0]
    p.text = "Decoupled Multi-Tier System Architecture"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Architecture Image
    arch_path = os.path.join(FIG_DIR, "fig_3_1_detailed_architecture.png")
    if os.path.exists(arch_path):
        slide.shapes.add_picture(arch_path, Inches(0.95), Inches(1.95), width=col_w - Inches(0.3))

    # Notes
    tb_an = slide.shapes.add_textbox(Inches(1.0), Inches(5.45), col_w - Inches(0.4), Inches(1.15))
    tf_an = tb_an.text_frame
    tf_an.word_wrap = True
    tf_an.margin_left = tf_an.margin_top = tf_an.margin_right = tf_an.margin_bottom = 0
    p = tf_an.paragraphs[0]
    p.text = "Architectural Decomposition & DFDs:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = GOLD
    p.space_after = Pt(2)
    p2 = tf_an.add_paragraph()
    p2.text = "• Level 0 DFD: Context boundary between Citizen, Flask Gateway, and Persistence.\n• Level 1/2 DFD: Decomposes natural language parsing, cosine ranking, and PDF compilation."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = SLATE

    # Right Column: Relational E-R Schema
    right_x = Inches(0.8) + col_w + gap
    add_card(slide, right_x, Inches(1.4), col_w, Inches(5.3), bg_color=WHITE, border_color=BORDER)

    tb_et = slide.shapes.add_textbox(right_x + Inches(0.2), Inches(1.5), col_w - Inches(0.4), Inches(0.4))
    tf_et = tb_et.text_frame
    tf_et.margin_left = tf_et.margin_top = tf_et.margin_right = tf_et.margin_bottom = 0
    p = tf_et.paragraphs[0]
    p.text = "Relational E-R Database Schema (SQLite WAL)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # ER Diagram Image
    er_path = os.path.join(FIG_DIR, "fig_3_10_er_diagram.png")
    if os.path.exists(er_path):
        slide.shapes.add_picture(er_path, right_x + Inches(0.15), Inches(1.95), width=col_w - Inches(0.3))

    # ER Table notes
    tb_en = slide.shapes.add_textbox(right_x + Inches(0.2), Inches(5.45), col_w - Inches(0.4), Inches(1.15))
    tf_en = tb_en.text_frame
    tf_en.word_wrap = True
    tf_en.margin_left = tf_en.margin_top = tf_en.margin_right = tf_en.margin_bottom = 0
    p = tf_en.paragraphs[0]
    p.text = "5 Core Relational Entities & ACID Compliance:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = GOLD
    p.space_after = Pt(2)
    p2 = tf_en.add_paragraph()
    p2.text = "• users, chat_sessions, chat_messages, saved_documents, case_bookmarks.\n• PRAGMA journal_mode=WAL ensures concurrent readers and writers without database locking."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = SLATE

    add_speaker_notes(slide,
        "Chapter 3 covers our comprehensive System Design. "
        "On the left, Figure 3.1 details our multi-tier architecture: the React frontend connects via REST API to our Flask gateway, "
        "which routes requests to the TF-IDF retrieval kernel, Gemini grounded synthesis, and ReportLab PDF compiler. "
        "On the right, Figure 3.10 shows our E-R schema comprising five normalized tables. "
        "We configured SQLite in Write-Ahead Logging (WAL) mode, allowing concurrent read queries during document generation."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7: 4. IMPLEMENTATION AND TESTING
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_7(prs):
    slide = create_base_slide(prs, "Chapter 4: Implementation & Verification", "4. Implementation and Testing", 7)

    col_w = Inches(3.64)
    gap = Inches(0.4)
    top_pos = Inches(1.4)
    h_pos = Inches(5.3)

    # Column 1: Tech Stack
    add_card(slide, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "Production Tech Stack"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    techs = [
        ("• Presentation Layer:", "React 18 SPA, Glassmorphic Modular CSS, Lucide React, Web Speech Voice API."),
        ("• Application Gateway:", "Python 3.14, Flask 3.0 REST API, CORS middleware, Gunicorn."),
        ("• Scientific & NLP Core:", "Scikit-learn, SciPy Compressed Sparse Row (CSR), NumPy."),
        ("• AI Synthesis Engine:", "Google Gemini 1.5 Flash (Hybrid) + Local Deterministic Fallback."),
        ("• Document Engine:", "ReportLab 3.6 Flowable Vector PDF compiler."),
        ("• Database Subsystem:", "SQLite 3 with WAL Pragma, SQLAlchemy 2.0 ORM.")
    ]
    for prefix, desc in techs:
        p = tf1.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10), space_after=Pt(4))

    # Column 2: Mathematical Algorithms
    c2_x = Inches(0.8) + col_w + gap
    add_card(slide, c2_x, top_pos, col_w, h_pos)
    tb2 = slide.shapes.add_textbox(c2_x + Inches(0.2), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    p.text = "Mathematical Retrieval Kernel"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    alg_items = [
        ("• Sublinear TF-IDF Vectorization:\n", "w(t, d) = (1 + ln(tf)) * ln(1 + N/df)\nDampens repeated term distortion in long statutory provisions."),
        ("• 99.08% Sparse Matrix Efficiency:\n", "15,000-D sparse matrix across 2,290 chunks compressed into SciPy CSR format; operates in <150MB RAM."),
        ("• Cosine Similarity Ranking:\n", "sim(q, d) = (q · d) / (|q| * |d|)\nCalibrated threshold (tau = 0.05) filters irrelevant noise."),
        ("• Blazing Query Execution:\n", "Average query response latency of 41.6ms on standard commodity CPUs without cloud roundtrips.")
    ]
    for prefix, desc in alg_items:
        p = tf2.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=GOLD, text_color=SLATE, font_size=Pt(9.5), space_after=Pt(4))

    # Column 3: Automated Testing & Verification
    c3_x = c2_x + col_w + gap
    add_card(slide, c3_x, top_pos, col_w, h_pos)
    tb3 = slide.shapes.add_textbox(c3_x + Inches(0.2), top_pos + Inches(0.15), col_w - Inches(0.4), h_pos - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0

    p = tf3.paragraphs[0]
    p.text = "Automated Testing Suites"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    # Pass Badge
    add_card(slide, c3_x + Inches(0.2), top_pos + Inches(0.45), col_w - Inches(0.4), Inches(0.45), bg_color=GREEN_BG, border_color=GREEN)
    tb_pb = slide.shapes.add_textbox(c3_x + Inches(0.2), top_pos + Inches(0.48), col_w - Inches(0.4), Inches(0.4))
    tf_pb = tb_pb.text_frame
    tf_pb.margin_left = tf_pb.margin_top = tf_pb.margin_right = tf_pb.margin_bottom = 0
    ppb = tf_pb.paragraphs[0]
    ppb.alignment = PP_ALIGN.CENTER
    ppb.text = "100% PASS RATE (18/18 TEST SUITES)"
    ppb.font.bold = True
    ppb.font.size = Pt(10.5)
    ppb.font.color.rgb = GREEN

    # Test cases breakdown
    tb_tc = slide.shapes.add_textbox(c3_x + Inches(0.2), top_pos + Inches(1.0), col_w - Inches(0.4), h_pos - Inches(1.15))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True
    tf_tc.margin_left = tf_tc.margin_top = tf_tc.margin_right = tf_tc.margin_bottom = 0

    test_items = [
        ("• test_rag_pipeline_retrieval:", "Verified precision across 10 judicial queries."),
        ("• test_bns_statute_mapping:", "Confirmed 100% IPC to BNS cross-conversion."),
        ("• test_fir_pdf_generation:", "Validated BNSS Sec 173 ReportLab compilation."),
        ("• test_notice_pdf_generation:", "Verified Sec 80 CPC legal notice vectors."),
        ("• test_affidavit_pdf_generation:", "Checked sworn affidavit jurat averments."),
        ("• test_complaint_pdf_generation:", "Validated E-Daakhil consumer complaint format."),
        ("• test_auth_jwt_security:", "PBKDF2 hashing & JWT expiration tests."),
        ("• test_wal_concurrency:", "50 parallel simulated write transactions.")
    ]
    for prefix, desc in test_items:
        p = tf_tc.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(9), space_after=Pt(2))

    add_speaker_notes(slide,
        "Chapter 4 covers our implementation and test verification. "
        "Our backend runs on Python 3.14 with Flask and SciPy; our frontend is React 18. "
        "Our mathematical retrieval kernel utilizes sublinear TF-IDF, compressing 2,290 case chunks into a 99.08% sparse matrix "
        "that executes in just 41.6 milliseconds. "
        "Our automated test suite executed across 18 distinct unit and integration suites—covering RAG retrieval, PDF compilation, "
        "and SQLite concurrency—achieving a perfect 100% pass rate."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8: 5. RESULTS AND DISCUSSIONS
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_8(prs):
    slide = create_base_slide(prs, "Chapter 5: Empirical Evaluation", "5. Results and Discussions", 8)

    # Left: UI Screenshots / Visual Preview
    col_w = Inches(5.6)
    add_card(slide, Inches(0.8), Inches(1.4), col_w, Inches(5.3), bg_color=WHITE, border_color=BORDER)
    
    tb_uit = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), col_w - Inches(0.4), Inches(0.35))
    tf_uit = tb_uit.text_frame
    tf_uit.margin_left = tf_uit.margin_top = tf_uit.margin_right = tf_uit.margin_bottom = 0
    p = tf_uit.paragraphs[0]
    p.text = "Live Platform User Interface & Drafting Studio"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Home Consultation Image
    ui1_path = os.path.join(FIG_DIR, "fig_5_1_home_consultation.png")
    if os.path.exists(ui1_path):
        slide.shapes.add_picture(ui1_path, Inches(0.95), Inches(1.9), width=col_w - Inches(0.3))

    # Document Studio Image
    ui2_path = os.path.join(FIG_DIR, "fig_5_3_documents_studio.png")
    if os.path.exists(ui2_path):
        slide.shapes.add_picture(ui2_path, Inches(0.95), Inches(4.35), width=col_w - Inches(0.3))

    # Right: Information Retrieval Evaluation Metrics Table
    right_x = Inches(6.65)
    r_w = Inches(5.88)
    add_card(slide, right_x, Inches(1.4), r_w, Inches(5.3), bg_color=WHITE, border_color=BORDER)

    tb_irt = slide.shapes.add_textbox(right_x + Inches(0.2), Inches(1.5), r_w - Inches(0.4), Inches(0.35))
    tf_irt = tb_irt.text_frame
    tf_irt.margin_left = tf_irt.margin_top = tf_irt.margin_right = tf_irt.margin_bottom = 0
    p = tf_irt.paragraphs[0]
    p.text = "Information Retrieval (IR) Evaluation on Judicial Benchmark"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Table of 10 Queries
    rows = 7
    cols = 4
    table_shape = slide.shapes.add_table(rows, cols, right_x + Inches(0.2), Inches(1.95), r_w - Inches(0.4), Inches(2.7))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.28)

    headers = ["Evaluation Query Topic", "Prec@3", "Prec@5", "Latency"]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    data = [
        ["Online Cyber Fraud / UPI", "100%", "80%", "38.2 ms"],
        ["Defective Product / Refund", "100%", "100%", "41.5 ms"],
        ["Arbitrary Tenant Eviction", "66.7%", "80%", "43.1 ms"],
        ["Unlawful Police Custody", "100%", "100%", "39.8 ms"],
        ["Cheque Dishonour (NI Act)", "100%", "80%", "42.0 ms"],
        ["OVERALL BENCHMARK MEAN", "90.0%", "84.0%", "41.6 ms"]
    ]
    for r_idx, row_vals in enumerate(data):
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if r_idx == len(data) - 1:
                cell.fill.fore_color.rgb = GOLD_LIGHT
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = BG_CARD
            else:
                cell.fill.fore_color.rgb = WHITE
            
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9)
            if r_idx == len(data) - 1:
                p.font.bold = True
                p.font.color.rgb = GOLD if c_idx > 0 else NAVY
            else:
                p.font.color.rgb = NAVY if c_idx == 0 else SLATE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Key Evaluation Insights Box
    tb_ins = slide.shapes.add_textbox(right_x + Inches(0.2), Inches(4.75), r_w - Inches(0.4), Inches(1.8))
    tf_ins = tb_ins.text_frame
    tf_ins.word_wrap = True
    tf_ins.margin_left = tf_ins.margin_top = tf_ins.margin_right = tf_ins.margin_bottom = 0

    p = tf_ins.paragraphs[0]
    p.text = "Key Empirical Performance Highlights:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = GOLD
    p.space_after = Pt(2)

    insights = [
        ("• Mean Reciprocal Rank (MRR = 0.92):", "Confirms that the primary ground-truth Supreme Court precedent ranks #1 or #2 for >85% of queries."),
        ("• Sub-50ms CPU Execution:", "Average query response time of 41.6ms guarantees instantaneous feedback on mobile devices."),
        ("• Zero WAL Lock Contention:", "SQLite Write-Ahead Logging handled 50 concurrent write transactions with an average commit latency of 1.4ms.")
    ]
    for prefix, desc in insights:
        p = tf_ins.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(9.5), space_after=Pt(2))

    add_speaker_notes(slide,
        "Slide 8 presents our empirical results and live UI. "
        "On the left, you see the actual interface: Figure 5.1 shows the multilingual grievance matcher, and Figure 5.3 shows our document studio. "
        "On the right, we evaluated our system across 10 landmark Supreme Court benchmark queries. "
        "The evaluation yielded a Mean Precision@3 of 90.0%, a Mean Precision@5 of 84.0%, and a Mean Reciprocal Rank (MRR) of 0.92, "
        "with an instantaneous query latency of just 41.6 milliseconds on standard hardware."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9: 6. CONCLUSION AND FUTURE SCOPE
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_9(prs):
    slide = create_base_slide(prs, "Chapter 6: Synthesis & Roadmap", "6. Conclusion and Future Scope", 9)

    col_w = Inches(5.66)
    gap = Inches(0.4)
    top_pos = Inches(1.4)
    h_pos = Inches(5.3)

    # Column 1: Conclusion & Technological Contributions
    add_card(slide, Inches(0.8), top_pos, col_w, h_pos)
    tb1 = slide.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.18), col_w - Inches(0.4), h_pos - Inches(0.35))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "Key Project Contributions (Conclusion)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    contribs = [
        ("• Democratized Citizen Access:", "Delivered a production-ready, zero-cost legal intelligence platform for ordinary Indian citizens facing acute personal or financial crises."),
        ("• Offline-Capable Mathematical Core:", "Eliminated dependency on expensive proprietary vector databases via 15,000-D sparse SciPy CSR TF-IDF retrieval running in <150MB RAM."),
        ("• Modern BNS 2023 Synchronization:", "First academic system to bridge the 2024 criminal code transition, seamlessly mapping colonial IPC sections to modern Bharatiya enactments."),
        ("• Court-Ready Instrument Synthesis:", "Automated creation of legally structured vector PDFs (FIR, Notice, Affidavit, Complaint) meeting statutory court standards."),
        ("• Verified Academic Rigor:", "Attained 90.0% Precision@3, 0.92 MRR, and 100% automated test pass rate.")
    ]
    for prefix, desc in contribs:
        p = tf1.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=NAVY, text_color=SLATE, font_size=Pt(10), space_after=Pt(5))

    # Column 2: Future Scope & Roadmap
    right_x = Inches(0.8) + col_w + gap
    add_card(slide, right_x, top_pos, col_w, h_pos)
    tb2 = slide.shapes.add_textbox(right_x + Inches(0.2), top_pos + Inches(0.18), col_w - Inches(0.4), h_pos - Inches(0.35))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    p.text = "Future Scope & Technological Roadmap"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    future_items = [
        ("• 1. Indic Vernacular Voice Interface:\n", "Integrate offline Whisper ASR and Coqui TTS to enable voice-based consultation in Punjabi, Hindi, and regional dialects for illiterate citizens."),
        ("• 2. Judicial E-Filing Gateway APIs:\n", "Connect directly with the Supreme Court's e-Courts portal and national E-Daakhil API for 1-click filing of complaints and notices."),
        ("• 3. Blockchain Document Notarization:\n", "Incorporate decentralized smart contract hashing (Ethereum/Polygon) to provide tamper-evident cryptographic proof of notice delivery."),
        ("• 4. Fine-Tuned Open-Weights Legal LLM:\n", "Domain-adaptive fine-tuning of Legal-Llama on Indian High Court case law for fully private on-premise inference.")
    ]
    for prefix, desc in future_items:
        p = tf2.add_paragraph()
        add_bullet_run(p, prefix, desc, prefix_color=GOLD, text_color=SLATE, font_size=Pt(10), space_after=Pt(6))

    add_speaker_notes(slide,
        "In Chapter 6, we conclude our project. "
        "PocketLaw successfully proves that modern NLP and full-stack software engineering can democratize legal rights in India. "
        "We achieved offline capability, zero hallucinations, modern BNS 2023 synchronization, and automated document compilation. "
        "Looking forward, we have charted a concrete four-point roadmap: "
        "adding Indic voice interfaces for rural citizens, integrating directly with e-Courts and E-Daakhil APIs, "
        "implementing blockchain notarization, and fine-tuning an open-source Indian legal language model."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10: REFERENCES & THANK YOU / Q&A
# ══════════════════════════════════════════════════════════════════════════════
def build_slide_10(prs):
    slide = create_base_slide(prs, "Scholarly Citations & Defense", "References & Thank You / Q&A", 10)

    col_w = Inches(5.66)
    gap = Inches(0.4)
    top_pos = Inches(1.4)
    h_pos = Inches(5.3)

    # Left: Key Academic References
    add_card(slide, Inches(0.8), top_pos, col_w, h_pos)
    tb_ref = slide.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.18), col_w - Inches(0.4), h_pos - Inches(0.35))
    tf_r = tb_ref.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p = tf_r.paragraphs[0]
    p.text = "Key Academic & Statutory References"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    refs = [
        ("[1] P. Lewis et al.,", "\"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, 2020."),
        ("[2] Ministry of Law & Justice,", "\"The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023),\" The Gazette of India, Extraordinary, Dec. 2023. Effective 1 July 2024."),
        ("[3] Supreme Court of India,", "Lalita Kumari v. Govt. of U.P., (2014) 2 SCC 1. Mandatory registration of First Information Reports under CrPC / BNSS 173."),
        ("[4] Supreme Court of India,", "Arnesh Kumar v. State of Bihar, (2014) 8 SCC 273. Landmark procedural safeguards governing arrest procedures."),
        ("[5] G. Salton et al.,", "\"A vector space model for automatic indexing,\" Communications of the ACM, vol. 18, no. 11, pp. 613-620, 1975."),
        ("[6] C. D. Manning et al.,", "Introduction to Information Retrieval. Cambridge, UK: Cambridge University Press, 2008.")
    ]
    for auth, cit in refs:
        p = tf_r.add_paragraph()
        add_bullet_run(p, auth, cit, prefix_color=NAVY, text_color=SLATE, font_size=Pt(9), space_after=Pt(3))

    # Right: Thank You & Defense Invitation
    right_x = Inches(0.8) + col_w + gap
    add_card(slide, right_x, top_pos, col_w, h_pos, bg_color=NAVY, border_color=GOLD)

    # Thank you box
    tb_ty = slide.shapes.add_textbox(right_x + Inches(0.4), top_pos + Inches(0.3), col_w - Inches(0.8), Inches(4.7))
    tfty = tb_ty.text_frame
    tfty.word_wrap = True
    tfty.margin_left = tfty.margin_top = tfty.margin_right = tfty.margin_bottom = 0

    pty = tfty.paragraphs[0]
    pty.alignment = PP_ALIGN.CENTER
    pty.text = "THANK YOU!"
    pty.font.name = FONT_HEADING
    pty.font.size = Pt(32)
    pty.font.bold = True
    pty.font.color.rgb = GOLD
    pty.space_after = Pt(4)

    pq = tfty.add_paragraph()
    pq.alignment = PP_ALIGN.CENTER
    pq.text = "We welcome questions, suggestions, and feedback\nfrom the Evaluation Committee."
    pq.font.name = FONT_BODY
    pq.font.size = Pt(13)
    pq.font.bold = True
    pq.font.color.rgb = WHITE
    pq.space_after = Pt(16)

    # Candidate details
    pcd = tfty.add_paragraph()
    pcd.alignment = PP_ALIGN.CENTER
    pcd.text = "PROJECT CANDIDATES:"
    pcd.font.name = FONT_HEADING
    pcd.font.size = Pt(11)
    pcd.font.bold = True
    pcd.font.color.rgb = GOLD
    pcd.space_after = Pt(3)

    candidates = [
        "Khushpreet Kaur (2302591)",
        "Mohammad Shehzad (2302612)",
        "Neha Mehta (2302625)"
    ]
    for c in candidates:
        pc = tfty.add_paragraph()
        pc.alignment = PP_ALIGN.CENTER
        pc.text = c
        pc.font.name = FONT_BODY
        pc.font.size = Pt(11.5)
        pc.font.color.rgb = WHITE
        pc.space_after = Pt(1)

    # Guide
    pgu = tfty.add_paragraph()
    pgu.alignment = PP_ALIGN.CENTER
    pgu.text = "\nPROJECT GUIDE:"
    pgu.font.name = FONT_HEADING
    pgu.font.size = Pt(11)
    pgu.font.bold = True
    pgu.font.color.rgb = GOLD
    pgu.space_after = Pt(2)

    pgun = tfty.add_paragraph()
    pgun.alignment = PP_ALIGN.CENTER
    pgun.text = "Dr. Hardeep Singh Kang"
    pgun.font.name = FONT_BODY
    pgun.font.size = Pt(12)
    pgun.font.bold = True
    pgun.font.color.rgb = WHITE

    pgud = tfty.add_paragraph()
    pgud.alignment = PP_ALIGN.CENTER
    pgud.text = "Department of Computer Science and Engineering\nGuru Nanak Dev Engineering College, Ludhiana"
    pgud.font.name = FONT_BODY
    pgud.font.size = Pt(10)
    pgud.font.color.rgb = BORDER

    add_speaker_notes(slide,
        "We express our deepest gratitude to our project guide Dr. Hardeep Singh Kang for his invaluable mentorship throughout this work, "
        "as well as our Principal Dr. Sehijpal Singh and the faculty of the Department of Computer Science & Engineering. "
        "We now warmly welcome questions, evaluations, and suggestions from the committee. Thank you very much."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("Building PocketLaw Major Project Presentation (.pptx)")
    print("GNDEC Ludhiana - Department of Computer Science & Engineering")
    print("=" * 65)

    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333) # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    print("\n[Slide 1/10] Building Title Slide...")
    build_slide_1(prs)

    print("[Slide 2/10] Building 1. Introduction & Problem Formulation...")
    build_slide_2(prs)

    print("[Slide 3/10] Building 1.3 Objectives (Exact Verbatim Bullets)...")
    build_slide_3(prs)

    print("[Slide 4/10] Building 1.7 Proposed System & Unique Features...")
    build_slide_4(prs)

    print("[Slide 5/10] Building 2. Requirement Analysis and System Specification...")
    build_slide_5(prs)

    print("[Slide 6/10] Building 3. System Design...")
    build_slide_6(prs)

    print("[Slide 7/10] Building 4. Implementation and Testing...")
    build_slide_7(prs)

    print("[Slide 8/10] Building 5. Results and Discussions...")
    build_slide_8(prs)

    print("[Slide 9/10] Building 6. Conclusion and Future Scope...")
    build_slide_9(prs)

    print("[Slide 10/10] Building References & Thank You / Q&A...")
    build_slide_10(prs)

    print(f"\nSaving presentation to: {OUTPUT_PPTX} ...")
    prs.save(OUTPUT_PPTX)

    size_mb = os.path.getsize(OUTPUT_PPTX) / (1024 * 1024)
    print(f"File saved successfully! Size: {size_mb:.2f} MB")
    print(f"Total Slides: {len(prs.slides)}")
    print("=" * 65)

if __name__ == "__main__":
    main()

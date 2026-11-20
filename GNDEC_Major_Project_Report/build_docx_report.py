"""
PocketLaw - Major Project Final Report Complete DOCX Generator
Builds the complete Microsoft Word (.docx) document strictly following GNDEC CSE specifications.
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
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")
DOCX_PATH = os.path.join(OUTPUT_DIR, "PocketLaw_GNDEC_Final_Report.docx")

# ── XML & Table Formatting Helpers ───────────────────────────────────────────

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_table_row_properties(row, is_header=False):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement('w:cantSplit')
    trPr.append(cantSplit)
    if is_header:
        tblHeader = OxmlElement('w:tblHeader')
        trPr.append(tblHeader)

def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), val)
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tblBorders.append(b)
    b_inv = OxmlElement('w:insideV')
    b_inv.set(qn('w:val'), 'none')
    tblBorders.append(b_inv)
    tblPr.append(tblBorders)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_number_to_footer(footer):
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def setup_gndec_section_geometry(section):
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(3.5)
    section.top_margin = Cm(2.5)
    section.right_margin = Cm(1.25)
    section.bottom_margin = Cm(1.25)

# ── Heading & Text Insertion Helpers ──────────────────────────────────────────

def add_chapter_heading(doc, num_str, title_str):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_with_next = True
    r1 = p.add_run(f"CHAPTER {num_str}\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(16)
    r1.font.bold = True
    r2 = p.add_run(title_str.upper())
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(16)
    r2.font.bold = True

def add_section_heading(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{num_str} {title_str}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

def add_subsection_heading(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{num_str} {title_str}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0  # Strict GNDEC Double Spacing
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_bullet_item(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = 'Times New Roman'
    r_bullet.font.size = Pt(12)
    r_bullet.font.bold = True
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(12)
    return p

def add_numbered_item(doc, num_str, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r_num = p.add_run(f"{num_str}. ")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(12)
    return p

def add_table_with_caption(doc, caption_text, headers, rows_data, col_widths=None):
    # Mandatory GNDEC Rule: Table caption at TOP
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11)
    r_cap.font.bold = True

    tbl = doc.add_table(rows=len(rows_data)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="CBD5E0", sz="4")

    # Header Row
    set_table_row_properties(tbl.rows[0], is_header=True)
    for idx, h_text in enumerate(headers):
        cell = tbl.cell(0, idx)
        set_cell_shading(cell, "E8EEF5")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True

    # Data Rows
    for r_idx, r_data in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        set_table_row_properties(row)
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F7FAFC")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(val))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)
    p_sp.paragraph_format.space_after = Pt(0)
    p_sp.paragraph_format.line_spacing = 1.0

def add_figure_with_caption(doc, fig_filename, caption_text, width=Inches(6.2)):
    fig_path = os.path.join(FIG_DIR, fig_filename)
    if os.path.exists(fig_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.line_spacing = 1.0
        p_img.add_run().add_picture(fig_path, width=width)

    # Mandatory GNDEC Rule: Figure caption at BOTTOM
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    p_cap.paragraph_format.line_spacing = 1.0
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11)
    r_cap.font.bold = True

def add_algorithm_box(doc, alg_num, title, require_text, ensure_text, steps):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.0
    p_cap.paragraph_format.keep_with_next = True
    r = p_cap.add_run(f"Algorithm {alg_num}: {title}")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="A0AEC0", sz="6")
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "FAFAFA")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    p0 = cell.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.0
    p0.paragraph_format.space_after = Pt(2)
    r_req = p0.add_run(f"Input: {require_text}\n")
    r_req.font.name = 'Consolas'
    r_req.font.size = Pt(9.5)
    r_req.font.bold = True
    r_ens = p0.add_run(f"Output: {ensure_text}\n")
    r_ens.font.name = 'Consolas'
    r_ens.font.size = Pt(9.5)
    r_ens.font.bold = True

    for idx, s in enumerate(steps):
        p_s = cell.add_paragraph()
        p_s.paragraph_format.line_spacing = 1.0
        p_s.paragraph_format.space_after = Pt(1)
        r_idx = p_s.add_run(f"{idx+1:2d}: ")
        r_idx.font.name = 'Consolas'
        r_idx.font.size = Pt(9)
        r_idx.font.bold = True
        r_st = p_s.add_run(s)
        r_st.font.name = 'Consolas'
        r_st.font.size = Pt(9)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)
    p_sp.paragraph_format.line_spacing = 1.0

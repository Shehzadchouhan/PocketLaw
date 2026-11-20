"""
PocketLaw - Master Document Builder Orchestrator
Executes the complete generation of PocketLaw_GNDEC_Final_Report.docx.
"""

import os
import sys
import docx

OUTPUT_DIR = r"C:\Users\Shehzad\OneDrive\Desktop\PROJECTS\PocketLaw\GNDEC_Major_Project_Report"
sys.path.insert(0, OUTPUT_DIR)

from build_docx_report import DOCX_PATH
from content_frontmatter import build_frontmatter
from content_chap1 import build_chapter1
from content_chap2 import build_chapter2
from content_chap3 import build_chapter3
from content_chap4 import build_chapter4
from content_chap5 import build_chapter5
from content_chap6_appendix import build_chapter6_and_appendix

def main():
    print("=" * 65)
    print("Building PocketLaw Major Project Final Report (.docx)")
    print("GNDEC Ludhiana - Department of Computer Science & Engineering")
    print("=" * 65)

    doc = docx.Document()

    # 1. Front Matter (Section 1 & 2)
    print("\n[1/7] Building Front Matter (Title Pages, Certificate, Abstract, TOC, Lists)...")
    build_frontmatter(doc)

    # 2. Chapter 1
    print("[2/7] Building Chapter 1: Introduction...")
    build_chapter1(doc)

    # 3. Chapter 2
    print("[3/7] Building Chapter 2: Requirement Analysis & System Specification...")
    build_chapter2(doc)

    # 4. Chapter 3
    print("[4/7] Building Chapter 3: System Design (Architecture, DFDs, UML, E-R, Schemas)...")
    build_chapter3(doc)

    # 5. Chapter 4
    print("[5/7] Building Chapter 4: Implementation and Testing (Tech Stack, Algorithms, Tests)...")
    build_chapter4(doc)

    # 6. Chapter 5
    print("[6/7] Building Chapter 5: Results and Discussions (Screens, Diagnostics, Benchmarks)...")
    build_chapter5(doc)

    # 7. Chapter 6 & Appendices
    print("[7/7] Building Chapter 6, References, Appendix A, and Annexures I-III...")
    build_chapter6_and_appendix(doc)

    # Save
    print(f"\nSaving document to: {DOCX_PATH} ...")
    doc.save(DOCX_PATH)
    file_size_mb = os.path.getsize(DOCX_PATH) / (1024 * 1024)
    print(f"File saved successfully! Size: {file_size_mb:.2f} MB")

    # Metrics Inspection
    print("\n" + "=" * 65)
    print("DOCUMENT METRICS VERIFICATION")
    print("=" * 65)
    
    # Reload and inspect
    doc_inspect = docx.Document(DOCX_PATH)
    total_sections = len(doc_inspect.sections)
    total_paragraphs = len(doc_inspect.paragraphs)
    total_tables = len(doc_inspect.tables)

    total_words = 0
    for p in doc_inspect.paragraphs:
        total_words += len(p.text.split())
    for t in doc_inspect.tables:
        for row in t.rows:
            for cell in row.cells:
                total_words += len(cell.text.split())

    # Count figures
    fig_count = 0
    for p in doc_inspect.paragraphs:
        if "Figure " in p.text and ("Figure 1." in p.text or "Figure 2." in p.text or "Figure 3." in p.text or "Figure 5." in p.text):
            fig_count += 1

    # Approximate page count based on typical Word metrics (double spaced ~250 words/page)
    # Plus tables and figures (16 figures = ~16 pages, 15 tables = ~12 pages)
    est_body_pages = total_words / 230
    est_total_pages = int(est_body_pages + 15)

    print(f"Total Sections:           {total_sections}")
    print(f"Total Paragraphs:         {total_paragraphs}")
    print(f"Total Tables:             {total_tables}")
    print(f"Embedded Figures:         {fig_count}")
    print(f"Total Word Count:         {total_words:,} words")
    print(f"Estimated Page Count:     {est_total_pages}+ pages (Double-Spaced A4)")
    print("=" * 65)

if __name__ == "__main__":
    main()

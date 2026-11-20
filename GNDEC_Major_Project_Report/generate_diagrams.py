"""
PocketLaw - Diagram Generator for GNDEC Major Project Report
Generates publication-quality 300 DPI diagram images with pure white backgrounds
for inclusion in the Word (.docx) document.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

FIG_DIR = r"C:\Users\Shehzad\OneDrive\Desktop\PROJECTS\PocketLaw\GNDEC_Major_Project_Report\figures"
os.makedirs(FIG_DIR, exist_ok=True)

def setup_canvas(width=10, height=6):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    return fig, ax

def save_and_close(fig, filename):
    filepath = os.path.join(FIG_DIR, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Saved: {filename}")

# ── 1. GNDEC College Emblem ───────────────────────────────────────────────────
def make_gndec_emblem():
    fig, ax = plt.subplots(figsize=(4, 4), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

    c1 = plt.Circle((0, 0), 2.2, color='#A91D22', fill=False, lw=4)
    c2 = plt.Circle((0, 0), 2.05, color='#1A365D', fill=False, lw=1.5)
    c3 = plt.Circle((0, 0), 1.5, color='#A91D22', fill=False, lw=3)
    ax.add_patch(c1); ax.add_patch(c2); ax.add_patch(c3)

    # Bridge symbol representation
    ax.plot([-1.2, 1.2], [-0.2, -0.2], color='#1A365D', lw=4)
    xs = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    ys = [0.6 if i%2 else -0.2 for i in range(len(xs))]
    ax.plot(xs, ys, color='#1A365D', lw=2.5)

    ax.text(0, 0.9, "1956", fontsize=14, fontweight='bold', ha='center', va='center', color='#A91D22')
    ax.text(0, 1.75, "GURU NANAK DEV ENGG. COLLEGE", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(0, -1.75, "WORK IS WORSHIP", fontsize=9, fontweight='bold', ha='center', va='center', color='#1A365D')
    ax.text(0, -2.0, "LUDHIANA", fontsize=8, fontweight='bold', ha='center', va='center', color='#A91D22')

    save_and_close(fig, "gndec_emblem.png")

# ── 2. Fig 1.1: High-Level Architecture Block Diagram ─────────────────────────
def make_fig_1_1():
    fig, ax = setup_canvas(10, 6.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    # 4 Layers
    layers = [
        ("Tier 1: Client Presentation Layer", 5.6, 1.1, '#EBF8FF', '#2B6CB0', "React 18 Single Page Application (SPA)\nGlassmorphic UI, Speech Web Audio API, Reactive Drafting Forms"),
        ("Tier 2: API Gateway & Security Layer", 4.1, 1.1, '#F0FFF4', '#2F855A', "Flask RESTful API Gateway (Port 5001)\nJWT Authentication (HMAC-SHA256), PBKDF2 Password Hashing, CORS, Route Guard"),
        ("Tier 3: Legal Intelligence & RAG Processing Core", 2.4, 1.3, '#FAF5FF', '#6B46C1', "Scikit-Learn Sparse TF-IDF Vector Space Model (15,000 N-Gram Features)\n2,290 Supreme Court Chunks x Cosine Kernel (tau=0.05) | Hybrid Gemini & Offline Synthesizer"),
        ("Tier 4: Relational Persistence & Document Generation Layer", 0.7, 1.3, '#FFF5F5', '#C53030', "SQLite 3 Database (WAL Mode) via SQLAlchemy ORM (5 Normalized Tables)\nReportLab 5.0.1 Court-Ready Vector PDF Compiler (FIR, Notice, Affidavit, Complaint)")
    ]

    for title, y, h, bg, border, desc in layers:
        rect = patches.FancyBboxPatch((0.8, y), 8.4, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, lw=2)
        ax.add_patch(rect)
        ax.text(5.0, y + h - 0.28, title, fontsize=10.5, fontweight='bold', ha='center', va='center', color=border)
        ax.text(5.0, y + (h - 0.35)/2, desc, fontsize=9, ha='center', va='center', color='#2D3748', multialignment='center')

    # Connecting arrows
    for y_top in [5.6, 4.1, 2.4]:
        ax.annotate('', xy=(5.0, y_top - 0.1), xytext=(5.0, y_top + 0.1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color='#4A5568', lw=2))

    save_and_close(fig, "fig_1_1_block_diagram.png")

# ── 3. Fig 2.1: Agile SDLC Sprints ───────────────────────────────────────────
def make_fig_2_1():
    fig, ax = setup_canvas(10, 5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    sprints = [
        (1.0, 3.2, "Sprint 1:\nRequirements &\nCorpus Curation"),
        (4.0, 3.2, "Sprint 2:\nVector Space Model\n& RAG Calibration"),
        (7.0, 3.2, "Sprint 3:\nHybrid Synthesis &\nDocument Engine"),
        (7.0, 1.0, "Sprint 4:\nSQLite WAL Persistence\n& API Gateway"),
        (4.0, 1.0, "Sprint 5:\nReact 18 SPA &\nGlassmorphic UI"),
        (1.0, 1.0, "Sprint 6:\nRegression Testing &\nAcademic Evaluation")
    ]

    for x, y, label in sprints:
        rect = patches.FancyBboxPatch((x, y), 2.0, 1.1, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=2)
        ax.add_patch(rect)
        ax.text(x + 1.0, y + 0.55, label, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1A365D', multialignment='center')

    # Arrows
    ax.annotate('', xy=(3.9, 3.75), xytext=(3.1, 3.75), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    ax.annotate('', xy=(6.9, 3.75), xytext=(6.1, 3.75), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    ax.annotate('', xy=(8.0, 2.2), xytext=(8.0, 3.1), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    ax.annotate('', xy=(6.1, 1.55), xytext=(6.9, 1.55), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    ax.annotate('', xy=(3.1, 1.55), xytext=(3.9, 1.55), arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2))
    # Feedback loop
    ax.annotate('', xy=(1.5, 3.1), xytext=(1.5, 2.2), arrowprops=dict(arrowstyle="->", linestyle='dashed', color='#718096', lw=1.5))

    save_and_close(fig, "fig_2_1_agile_sdlc.png")

# ── 4. Fig 3.1: Detailed Component-Level System Architecture ──────────────────
def make_fig_3_1():
    fig, ax = setup_canvas(10.5, 7)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)

    # Client
    ax.add_patch(patches.FancyBboxPatch((3.5, 6.6), 4.0, 1.0, boxstyle="round,pad=0.1", facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=2))
    ax.text(5.5, 7.1, "React 18 Client Application (SPA)\nReact Router v6, Axios, Lucide Icons, Chart.js", fontsize=9, fontweight='bold', ha='center', va='center')

    # Gateway
    ax.add_patch(patches.FancyBboxPatch((3.5, 4.8), 4.0, 1.0, boxstyle="round,pad=0.1", facecolor='#F0FFF4', edgecolor='#2F855A', lw=2))
    ax.text(5.5, 5.3, "Flask REST API Gateway (Port 5001)\nCORS, JWT Bearer Auth, Request Dispatcher", fontsize=9, fontweight='bold', ha='center', va='center')

    # Intelligence Left
    ax.add_patch(patches.FancyBboxPatch((0.5, 2.6), 4.0, 1.3, boxstyle="round,pad=0.1", facecolor='#FAF5FF', edgecolor='#6B46C1', lw=2))
    ax.text(2.5, 3.25, "TF-IDF Vector RAG Engine\n15,000 N-Gram Vocabulary\nCosine Kernel (tau=0.05) | 2,290 Chunks", fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Intelligence Right
    ax.add_patch(patches.FancyBboxPatch((6.5, 2.6), 4.0, 1.3, boxstyle="round,pad=0.1", facecolor='#FEFCBF', edgecolor='#B7791F', lw=2))
    ax.text(8.5, 3.25, "Hybrid Synthesis Engine\nGoogle Gemini Grounded LLM\n100% Offline Extractive Fallback", fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Persistence Bottom Left
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.4), 4.0, 1.3, boxstyle="round,pad=0.1", facecolor='#FFF5F5', edgecolor='#C53030', lw=2))
    ax.text(2.5, 1.05, "SQLite 3 Relational Database\nWAL Mode (Write-Ahead Logging)\nSQLAlchemy ORM (5 Normalized Tables)", fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Document Engine Bottom Right
    ax.add_patch(patches.FancyBboxPatch((6.5, 0.4), 4.0, 1.3, boxstyle="round,pad=0.1", facecolor='#E6FFFA', edgecolor='#2C7A7B', lw=2))
    ax.text(8.5, 1.05, "ReportLab Vector PDF Engine\nOfficial Judicial Headers & Typography\nNotary Jurat / Oath Commissioner Blocks", fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Connectors
    ax.annotate('', xy=(5.5, 5.9), xytext=(5.5, 6.5), arrowprops=dict(arrowstyle="<->", lw=2, color='#2B6CB0'))
    ax.annotate('', xy=(2.5, 4.0), xytext=(4.5, 4.7), arrowprops=dict(arrowstyle="->", lw=1.8, color='#4A5568'))
    ax.annotate('', xy=(8.5, 4.0), xytext=(6.5, 4.7), arrowprops=dict(arrowstyle="->", lw=1.8, color='#4A5568'))
    ax.annotate('', xy=(6.4, 3.25), xytext=(4.6, 3.25), arrowprops=dict(arrowstyle="->", lw=2, color='#6B46C1'))
    ax.annotate('', xy=(2.5, 1.8), xytext=(2.5, 2.5), arrowprops=dict(arrowstyle="<->", lw=1.8, color='#C53030'))
    ax.annotate('', xy=(8.5, 1.8), xytext=(8.5, 2.5), arrowprops=dict(arrowstyle="->", lw=1.8, color='#2C7A7B'))

    save_and_close(fig, "fig_3_1_detailed_architecture.png")

# ── 5. Fig 3.2: DFD Level 0 (Context Diagram) ─────────────────────────────────
def make_fig_3_2():
    fig, ax = setup_canvas(10, 4)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)

    # User
    ax.add_patch(patches.Rectangle((0.6, 1.3), 2.2, 1.4, facecolor='#EDF2F7', edgecolor='#2D3748', lw=2))
    ax.text(1.7, 2.0, "Aggrieved Citizen /\nLitigant", fontsize=9.5, fontweight='bold', ha='center', va='center')

    # PocketLaw System
    ax.add_patch(plt.Circle((5.0, 2.0), 1.3, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=2.5))
    ax.text(5.0, 2.0, "PocketLaw System\n(Process 0.0)", fontsize=10, fontweight='bold', ha='center', va='center')

    # Court
    ax.add_patch(patches.Rectangle((7.2, 1.3), 2.2, 1.4, facecolor='#EDF2F7', edgecolor='#2D3748', lw=2))
    ax.text(8.3, 2.0, "Police Station /\nDistrict Court /\nConsumer Forum", fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Flows
    ax.annotate('Grievance / Form Data', xy=(3.6, 2.3), xytext=(2.9, 2.3), arrowprops=dict(arrowstyle="->", lw=1.8, color='#2B6CB0'), fontsize=8, ha='center', va='bottom')
    ax.annotate('Legal Advisory / Precedents', xy=(2.9, 1.7), xytext=(3.6, 1.7), arrowprops=dict(arrowstyle="->", lw=1.8, color='#2B6CB0'), fontsize=8, ha='center', va='top')
    ax.annotate('Court-Ready Vector PDFs', xy=(7.1, 2.0), xytext=(6.4, 2.0), arrowprops=dict(arrowstyle="->", lw=1.8, color='#2F855A'), fontsize=8, ha='center', va='bottom')

    save_and_close(fig, "fig_3_2_dfd_level_0.png")

# ── 6. Fig 3.3: DFD Level 1 (Functional Decomposition) ────────────────────────
def make_fig_3_3():
    fig, ax = setup_canvas(10, 6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # User
    ax.add_patch(patches.Rectangle((0.5, 2.3), 1.8, 1.4, facecolor='#EDF2F7', edgecolor='#2D3748', lw=2))
    ax.text(1.4, 3.0, "User / Citizen", fontsize=9, fontweight='bold', ha='center', va='center')

    # 3 Processes
    procs = [
        (4.2, 4.4, "1.0\nAuthenticate\nUser"),
        (4.2, 2.5, "2.0\nConsultation\n& RAG"),
        (4.2, 0.6, "3.0\nDraft Legal\nDocument")
    ]
    for x, y, label in procs:
        ax.add_patch(plt.Circle((x, y + 0.5), 0.75, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=2))
        ax.text(x, y + 0.5, label, fontsize=8, fontweight='bold', ha='center', va='center')

    # 3 Data Stores
    stores = [
        (7.0, 4.6, "D1: Users Relational Table"),
        (7.0, 2.7, "D2: Supreme Court Knowledge Base"),
        (7.0, 0.8, "D3: Saved Documents Table")
    ]
    for x, y, label in stores:
        ax.add_patch(patches.Rectangle((x, y), 2.5, 0.6, facecolor='#FAF5FF', edgecolor='#6B46C1', lw=1.8))
        ax.text(x + 1.25, y + 0.3, label, fontsize=8, fontweight='bold', ha='center', va='center')

    # Flows
    ax.annotate('Credentials', xy=(3.4, 4.8), xytext=(2.4, 3.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'), fontsize=7.5)
    ax.annotate('Grievance', xy=(3.4, 3.0), xytext=(2.4, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'), fontsize=7.5)
    ax.annotate('Draft Form', xy=(3.4, 1.2), xytext=(2.4, 2.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4A5568'), fontsize=7.5)

    ax.annotate('Verify/Token', xy=(6.9, 4.9), xytext=(5.1, 4.9), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#6B46C1'), fontsize=7.5)
    ax.annotate('2,290 Chunks', xy=(5.1, 3.0), xytext=(6.9, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#6B46C1'), fontsize=7.5)
    ax.annotate('Persist Draft', xy=(6.9, 1.1), xytext=(5.1, 1.1), arrowprops=dict(arrowstyle="->", lw=1.5, color='#6B46C1'), fontsize=7.5)

    save_and_close(fig, "fig_3_3_dfd_level_1.png")

# ── 7. Fig 3.4: DFD Level 2 (RAG & Consultation) ──────────────────────────────
def make_fig_3_4():
    fig, ax = setup_canvas(10.5, 4.5)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)

    steps = [
        (1.0, "2.1\nNormalize\nVernacular"),
        (3.2, "2.2\nTF-IDF Vector\nTransform"),
        (5.4, "2.3\nCosine Score\nEvaluation"),
        (7.6, "2.4\nThreshold Filter\n(tau >= 0.05)"),
        (9.8, "2.5\nHybrid Legal\nSynthesis")
    ]
    for x, label in steps:
        ax.add_patch(plt.Circle((x, 3.2), 0.7, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=2))
        ax.text(x, 3.2, label, fontsize=7.5, fontweight='bold', ha='center', va='center')

    # Connecting arrows
    for i in range(len(steps)-1):
        x1 = steps[i][0] + 0.75
        x2 = steps[i+1][0] - 0.75
        ax.annotate('', xy=(x2, 3.2), xytext=(x1, 3.2), arrowprops=dict(arrowstyle="->", lw=1.8, color='#2B6CB0'))

    # Sub-stores
    sub_stores = [
        (1.0, "D2.1: Hindi/Vernacular\nDictionary Map"),
        (3.2, "D2.2: 15,000 N-Gram\nVocabulary Model"),
        (5.4, "D2.3: 2,290 Chunks\nCSR Matrix"),
        (9.8, "D2.4: BNS 2023 /\nStatutory Rules")
    ]
    for x, label in sub_stores:
        ax.add_patch(patches.Rectangle((x - 0.9, 0.8), 1.8, 1.0, facecolor='#FAF5FF', edgecolor='#6B46C1', lw=1.5))
        ax.text(x, 1.3, label, fontsize=7, fontweight='bold', ha='center', va='center')
        ax.annotate('', xy=(x, 2.45), xytext=(x, 1.85), arrowprops=dict(arrowstyle="->", lw=1.4, color='#6B46C1'))

    save_and_close(fig, "fig_3_4_dfd_level_2.png")

# ── 8. Fig 3.5: UML Use Case Diagram ──────────────────────────────────────────
def make_fig_3_5():
    fig, ax = setup_canvas(10, 6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    # Boundary
    ax.add_patch(patches.Rectangle((2.8, 0.4), 6.8, 6.2, facecolor='#F7FAFC', edgecolor='#A0AEC0', lw=1.5, linestyle='--'))
    ax.text(6.2, 6.35, "PocketLaw System Boundary", fontsize=10, fontweight='bold', ha='center', va='center', color='#4A5568')

    # Actors
    ax.text(1.2, 5.0, "O\n/|\\\n/ \\", fontsize=16, ha='center', va='center')
    ax.text(1.2, 4.0, "Unregistered\nCitizen", fontsize=8.5, fontweight='bold', ha='center', va='center')

    ax.text(1.2, 2.0, "O\n/|\\\n/ \\", fontsize=16, ha='center', va='center')
    ax.text(1.2, 1.0, "Registered\nLitigant", fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Use Cases
    ucs = [
        (6.2, 5.4, "Submit Natural Language Grievance"),
        (6.2, 4.6, "Search Supreme Court Precedents"),
        (6.2, 3.8, "Browse Modern Statutes (BNS 2023)"),
        (6.2, 3.0, "Generate Live Document Preview"),
        (6.2, 2.2, "Download Court-Ready Vector PDF"),
        (6.2, 1.4, "Bookmark Judicial Precedents"),
        (6.2, 0.6, "Manage Profile & Saved Drafts")
    ]
    for x, y, label in ucs:
        ax.add_patch(patches.FancyBboxPatch((x - 2.5, y - 0.28), 5.0, 0.56, boxstyle="round,pad=0.08,rounding_size=0.28",
                                            facecolor='white', edgecolor='#2B6CB0', lw=1.5))
        ax.text(x, y, label, fontsize=8.5, ha='center', va='center', color='#1A202C')

    # Association lines
    for i in range(5):
        ax.plot([1.7, 3.7], [4.5, ucs[i][1]], color='#4A5568', lw=1.2)
    for i in [0, 3, 4, 5, 6]:
        ax.plot([1.7, 3.7], [1.5, ucs[i][1]], color='#4A5568', lw=1.2)

    save_and_close(fig, "fig_3_5_uml_use_case.png")

# ── 9. Fig 3.6: UML Class Diagram ─────────────────────────────────────────────
def make_fig_3_6():
    fig, ax = setup_canvas(10, 6.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    classes = [
        (3.5, 4.5, 3.0, 2.2, "User", [
            "+ id: Integer [PK]",
            "+ user_id: String [UQ, IDX]",
            "+ email: String [UQ, IDX]",
            "+ password_hash: String",
            "+ role: String",
            "+ to_dict(): Dict"
        ]),
        (0.5, 1.2, 2.8, 2.2, "ChatSession", [
            "+ id: Integer [PK]",
            "+ session_id: String [UQ]",
            "+ user_id: String [FK]",
            "+ title: String",
            "+ to_dict(): Dict"
        ]),
        (3.6, 1.2, 2.8, 2.2, "SavedDocument", [
            "+ id: Integer [PK]",
            "+ doc_id: String [UQ]",
            "+ user_id: String [FK]",
            "+ doc_type: String",
            "+ to_dict(): Dict"
        ]),
        (6.7, 1.2, 2.8, 2.2, "CaseBookmark", [
            "+ id: Integer [PK]",
            "+ user_id: String [FK]",
            "+ case_id: Integer",
            "+ summary: Text",
            "+ to_dict(): Dict"
        ])
    ]

    for x, y, w, h, name, attrs in classes:
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor='white', edgecolor='#2B6CB0', lw=2))
        ax.plot([x, x + w], [y + h - 0.45, y + h - 0.45], color='#2B6CB0', lw=1.5)
        ax.text(x + w/2, y + h - 0.22, name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#1A365D')
        for idx, attr in enumerate(attrs):
            ax.text(x + 0.15, y + h - 0.7 - idx * 0.26, attr, fontsize=7.5, va='center', color='#2D3748')

    # Association lines
    ax.annotate('', xy=(1.9, 3.4), xytext=(3.5, 4.8), arrowprops=dict(arrowstyle="->", lw=1.6, color='#2B6CB0'))
    ax.annotate('', xy=(5.0, 3.4), xytext=(5.0, 4.5), arrowprops=dict(arrowstyle="->", lw=1.6, color='#2B6CB0'))
    ax.annotate('', xy=(8.1, 3.4), xytext=(6.5, 4.8), arrowprops=dict(arrowstyle="->", lw=1.6, color='#2B6CB0'))
    ax.text(2.6, 4.2, "1..*", fontsize=7.5, color='#4A5568')
    ax.text(5.1, 3.9, "1..*", fontsize=7.5, color='#4A5568')
    ax.text(7.4, 4.2, "1..*", fontsize=7.5, color='#4A5568')

    save_and_close(fig, "fig_3_6_uml_class.png")

# ── 10. Fig 3.7: UML Sequence Diagram ─────────────────────────────────────────
def make_fig_3_7():
    fig, ax = setup_canvas(10, 6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    cols = [(1.2, "Client / SPA"), (3.6, "API Gateway"), (6.0, "RAG Engine"), (8.4, "SQLite WAL DB")]

    for x, name in cols:
        ax.add_patch(patches.Rectangle((x - 0.9, 5.2), 1.8, 0.6, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5))
        ax.text(x, 5.5, name, fontsize=8.5, fontweight='bold', ha='center', va='center')
        ax.plot([x, x], [0.6, 5.2], linestyle='--', color='#CBD5E0', lw=1.5)

    # Messages
    msgs = [
        (1.2, 3.6, 4.6, "1: POST /api/chat {msg, lang}", True),
        (3.6, 6.0, 3.9, "2: rag_retrieve(query, top_k=5)", True),
        (6.0, 3.6, 3.2, "3: Ranked Precedent Chunks (Score >= 0.05)", False),
        (3.6, 8.4, 2.5, "4: INSERT INTO chat_messages", True),
        (8.4, 3.6, 1.8, "5: Transaction Commit OK", False),
        (3.6, 1.2, 1.1, "6: JSON Response 200 {analysis, prediction}", False)
    ]
    for x1, x2, y, text, is_call in msgs:
        style = "->" if is_call else "-->"
        ax.annotate(text, xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", linestyle='solid' if is_call else 'dashed', lw=1.5, color='#2B6CB0'),
                    fontsize=7.5, ha='center', va='bottom')

    save_and_close(fig, "fig_3_7_uml_sequence.png")

# ── 11. Fig 3.8: UML Activity Diagram ─────────────────────────────────────────
def make_fig_3_8():
    fig, ax = setup_canvas(10, 6.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    # Start
    ax.add_patch(plt.Circle((5.0, 6.6), 0.18, color='black'))

    steps = [
        (5.0, 5.8, "Normalize Vernacular Query Terms"),
        (5.0, 4.9, "Compute Cosine Similarity on 2,290 Chunks"),
        (5.0, 3.8, "GEMINI_API_KEY Configured? (Decision)"),
        (2.5, 2.5, "Offline Extractive Synthesis\nfrom Knowledge Base"),
        (7.5, 2.5, "Call Gemini Grounded API\n(8-Second Timeout)"),
        (5.0, 1.1, "Synthesize Categorized Legal Cards"),
    ]

    for idx, (x, y, label) in enumerate(steps):
        if idx == 2:
            # Diamond
            ax.plot([x, x+1.2, x, x-1.2, x], [y+0.35, y, y-0.35, y, y+0.35], color='#D69E2E', lw=2)
            ax.text(x, y, "GEMINI_API_KEY\nConfigured?", fontsize=7.5, fontweight='bold', ha='center', va='center')
        else:
            ax.add_patch(patches.FancyBboxPatch((x - 1.5, y - 0.28), 3.0, 0.56, boxstyle="round,pad=0.08",
                                                facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5))
            ax.text(x, y, label, fontsize=8, fontweight='bold', ha='center', va='center')

    # End
    ax.add_patch(plt.Circle((5.0, 0.4), 0.2, color='white', ec='black', lw=2))
    ax.add_patch(plt.Circle((5.0, 0.4), 0.12, color='black'))

    # Connectors
    ax.annotate('', xy=(5.0, 6.1), xytext=(5.0, 6.4), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 5.2), xytext=(5.0, 5.5), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 4.18), xytext=(5.0, 4.6), arrowprops=dict(arrowstyle="->", lw=1.5))

    ax.annotate('No', xy=(2.5, 2.8), xytext=(3.8, 3.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#C53030'), fontsize=8)
    ax.annotate('Yes', xy=(7.5, 2.8), xytext=(6.2, 3.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2F855A'), fontsize=8)

    ax.annotate('', xy=(4.0, 1.2), xytext=(2.5, 2.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(6.0, 1.2), xytext=(7.5, 2.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 0.62), xytext=(5.0, 0.8), arrowprops=dict(arrowstyle="->", lw=1.5))

    save_and_close(fig, "fig_3_8_uml_activity.png")

# ── 12. Fig 3.9: UML Deployment Diagram ───────────────────────────────────────
def make_fig_3_9():
    fig, ax = setup_canvas(10, 5.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Client Node
    ax.add_patch(patches.Rectangle((0.8, 0.8), 3.8, 4.4, facecolor='white', edgecolor='#4A5568', lw=2))
    ax.text(2.7, 4.9, "<<Device: Client Machine>>\nModern Web Browser", fontsize=8.5, fontweight='bold', ha='center', va='center')
    ax.add_patch(patches.Rectangle((1.2, 3.2), 3.0, 0.8, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5))
    ax.text(2.7, 3.6, "React 18 SPA (Build Artifacts)", fontsize=7.5, ha='center', va='center')
    ax.add_patch(patches.Rectangle((1.2, 2.0), 3.0, 0.8, facecolor='#EBF8FF', edgecolor='#2B6CB0', lw=1.5))
    ax.text(2.7, 2.4, "Axios HTTP Interceptors", fontsize=7.5, ha='center', va='center')

    # Server Node
    ax.add_patch(patches.Rectangle((5.4, 0.8), 3.8, 4.4, facecolor='white', edgecolor='#4A5568', lw=2))
    ax.text(7.3, 4.9, "<<Device: Application Host>>\nPython 3.14 / Flask Gateway", fontsize=8.5, fontweight='bold', ha='center', va='center')
    ax.add_patch(patches.Rectangle((5.8, 3.2), 3.0, 0.8, facecolor='#F0FFF4', edgecolor='#2F855A', lw=1.5))
    ax.text(7.3, 3.6, "Flask REST API (Port 5001)", fontsize=7.5, ha='center', va='center')
    ax.add_patch(patches.Rectangle((5.8, 2.0), 3.0, 0.8, facecolor='#FAF5FF', edgecolor='#6B46C1', lw=1.5))
    ax.text(7.3, 2.4, "SQLite 3 WAL (data/pocketlaw.db)", fontsize=7.5, ha='center', va='center')

    # Network connection
    ax.annotate('HTTP / JSON (TCP 3000 / 5001)', xy=(5.4, 2.8), xytext=(4.6, 2.8),
                arrowprops=dict(arrowstyle="<->", lw=2, color='#2B6CB0'), fontsize=8, ha='center', va='bottom')

    save_and_close(fig, "fig_3_9_uml_deployment.png")

# ── 13. Fig 3.10: Entity-Relationship (E-R) Diagram ───────────────────────────
def make_fig_3_10():
    fig, ax = setup_canvas(10, 6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Entities
    ents = [
        (4.0, 4.5, "USER"),
        (8.0, 4.5, "CHAT_SESSION"),
        (8.0, 1.2, "CHAT_MESSAGE"),
        (4.0, 1.2, "SAVED_DOCUMENT"),
        (0.6, 4.5, "CASE_BOOKMARK")
    ]
    for x, y, name in ents:
        ax.add_patch(patches.Rectangle((x, y), 1.8, 0.9, facecolor='white', edgecolor='#2B6CB0', lw=2))
        ax.text(x + 0.9, y + 0.45, name, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1A365D')

    # Relationship diamonds
    ax.plot([6.4, 6.9, 6.4, 5.9, 6.4], [5.25, 4.95, 4.65, 4.95, 5.25], color='#D69E2E', lw=1.8)
    ax.text(6.4, 4.95, "Initiates", fontsize=7, ha='center', va='center')

    ax.plot([8.9, 9.4, 8.9, 8.4, 8.9], [3.3, 3.0, 2.7, 3.0, 3.3], color='#D69E2E', lw=1.8)
    ax.text(8.9, 3.0, "Contains", fontsize=7, ha='center', va='center')

    ax.plot([4.9, 5.4, 4.9, 4.4, 4.9], [3.3, 3.0, 2.7, 3.0, 3.3], color='#D69E2E', lw=1.8)
    ax.text(4.9, 3.0, "Drafts", fontsize=7, ha='center', va='center')

    ax.plot([3.1, 3.6, 3.1, 2.6, 3.1], [5.25, 4.95, 4.65, 4.95, 5.25], color='#D69E2E', lw=1.8)
    ax.text(3.1, 4.95, "Pins", fontsize=7, ha='center', va='center')

    # Connecting lines
    ax.plot([5.8, 5.9], [4.95, 4.95], color='#4A5568', lw=1.5)
    ax.plot([6.9, 8.0], [4.95, 4.95], color='#4A5568', lw=1.5)
    ax.text(5.85, 5.1, "1", fontsize=8)
    ax.text(7.9, 5.1, "N", fontsize=8)

    ax.plot([8.9, 8.9], [4.5, 3.3], color='#4A5568', lw=1.5)
    ax.plot([8.9, 8.9], [2.7, 2.1], color='#4A5568', lw=1.5)
    ax.text(9.05, 4.3, "1", fontsize=8)
    ax.text(9.05, 2.2, "N", fontsize=8)

    ax.plot([4.9, 4.9], [4.5, 3.3], color='#4A5568', lw=1.5)
    ax.plot([4.9, 4.9], [2.7, 2.1], color='#4A5568', lw=1.5)
    ax.text(5.05, 4.3, "1", fontsize=8)
    ax.text(5.05, 2.2, "N", fontsize=8)

    ax.plot([4.0, 3.6], [4.95, 4.95], color='#4A5568', lw=1.5)
    ax.plot([2.6, 2.4], [4.95, 4.95], color='#4A5568', lw=1.5)
    ax.text(3.9, 5.1, "1", fontsize=8)
    ax.text(2.45, 5.1, "N", fontsize=8)

    save_and_close(fig, "fig_3_10_er_diagram.png")

# ── 14. Fig 5.1: Home Consultation UI Mockup ──────────────────────────────────
def make_fig_5_1():
    fig, ax = setup_canvas(10, 6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Browser Frame
    ax.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 5.6, facecolor='white', edgecolor='#CBD5E0', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 5.3), 9.6, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1))
    ax.text(0.5, 5.55, "● ● ●  PocketLaw AI Legal Intelligence -- http://localhost:3000", fontsize=7.5, color='#718096')

    # Header
    ax.text(5.0, 4.9, "⚖️ PocketLaw: Type Your Problem, Get Your Legal Rights", fontsize=11, fontweight='bold', ha='center', color='#1A365D')
    ax.text(5.0, 4.55, "Grounded on 2,290 Supreme Court Precedents & Modern Indian Criminal Codes (BNS 2023)", fontsize=7.5, ha='center', color='#4A5568')

    # Input Box
    ax.add_patch(patches.Rectangle((0.8, 3.2), 8.4, 0.9, facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5))
    ax.text(1.0, 3.65, "Someone cheated me online by sending a fake UPI payment link and deducted Rs. 45,000...", fontsize=8, color='#2D3748')

    # Predictor Bar
    ax.add_patch(patches.Rectangle((0.8, 2.45), 8.4, 0.55, facecolor='#EBF8FF', edgecolor='#3182CE', lw=1))
    ax.text(5.0, 2.7, "Predicted Duration: 2-6 Months  |  Risk Level: Low-Medium  |  Historical Success Rate: 62% Favourable", fontsize=8, fontweight='bold', ha='center', color='#2B6CB0')

    # 4 Cards
    cards = [
        (0.8, 0.5, 2.0, 1.7, "Applicable Modern Laws", ["Sec 318 BNS 2023 (Cheating)", "Sec 66D IT Act (Impersonation)", "Sec 173 BNSS (Zero FIR)"], '#EBF8FF', '#3182CE'),
        (2.9, 0.5, 2.0, 1.7, "Your Citizen Rights", ["Right to freeze bank account", "Right to register Zero FIR", "Free signed copy of FIR"], '#FAF5FF', '#805AD5'),
        (5.0, 0.5, 2.0, 1.7, "Immediate Action Steps", ["Call Cyber Helpline 1930", "File at cybercrime.gov.in", "Notify Bank Branch Mgr"], '#F0FFF4', '#38A169'),
        (7.1, 0.5, 2.1, 1.7, "Emergency Helplines", ["Cyber Helpline: 1930", "Consumer Helpline: 1915", "Police Emergency: 112"], '#FFFAF0', '#DD6B20')
    ]
    for x, y, w, h, title, items, bg, border in cards:
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=1.5))
        ax.text(x + w/2, y + h - 0.22, title, fontsize=7.5, fontweight='bold', ha='center', color=border)
        for idx, item in enumerate(items):
            ax.text(x + 0.1, y + h - 0.55 - idx*0.35, f"• {item}", fontsize=6.5, color='#2D3748')

    save_and_close(fig, "fig_5_1_home_consultation.png")

# ── 15. Fig 5.2: Analytics Dashboard UI Mockup ────────────────────────────────
def make_fig_5_2():
    fig, ax = setup_canvas(10, 5.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Frame
    ax.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 5.1, facecolor='white', edgecolor='#CBD5E0', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 4.8), 9.6, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1))
    ax.text(0.5, 5.05, "● ● ●  PocketLaw Analytics Dashboard -- http://localhost:3000/dashboard", fontsize=7.5, color='#718096')

    # 4 Metric Cards
    m_cards = [
        (0.6, 3.6, 2.0, 0.9, "148", "Indexed Cases"),
        (2.9, 3.6, 2.0, 0.9, "2,290", "RAG Chunks"),
        (5.2, 3.6, 2.0, 0.9, "24.3%", "Overall Success"),
        (7.5, 3.6, 2.0, 0.9, "Connected", "SQLite WAL Engine")
    ]
    for x, y, w, h, val, lbl in m_cards:
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.2))
        ax.text(x + w/2, y + 0.55, val, fontsize=12, fontweight='bold', ha='center', color='#2B6CB0')
        ax.text(x + w/2, y + 0.2, lbl, fontsize=7.5, ha='center', color='#718096')

    # Donut 1
    ax.text(2.8, 3.1, "Case Type Distribution", fontsize=8.5, fontweight='bold', ha='center', color='#2D3748')
    d1 = plt.Circle((2.8, 1.8), 0.9, color='#3182CE', fill=True)
    d1_in = plt.Circle((2.8, 1.8), 0.55, color='white', fill=True)
    ax.add_patch(d1); ax.add_patch(d1_in)
    ax.text(2.8, 0.5, "Criminal (36.5%), Property (27.7%)\nConsumer (25.0%), Civil (5.4%)", fontsize=7, ha='center', color='#4A5568')

    # Donut 2
    ax.text(7.2, 3.1, "Judicial Outcome Ratios", fontsize=8.5, fontweight='bold', ha='center', color='#2D3748')
    d2 = plt.Circle((7.2, 1.8), 0.9, color='#E53E3E', fill=True)
    d2_in = plt.Circle((7.2, 1.8), 0.55, color='white', fill=True)
    ax.add_patch(d2); ax.add_patch(d2_in)
    ax.text(7.2, 0.5, "Dismissed (71.6%), Allowed (24.3%)\nPartially Allowed (4.1%)", fontsize=7, ha='center', color='#4A5568')

    save_and_close(fig, "fig_5_2_dashboard.png")

# ── 16. Fig 5.3: Document Drafting Studio UI Mockup ───────────────────────────
def make_fig_5_3():
    fig, ax = setup_canvas(10, 5.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Frame
    ax.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 5.1, facecolor='white', edgecolor='#CBD5E0', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 4.8), 9.6, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1))
    ax.text(0.5, 5.05, "● ● ●  PocketLaw Document Drafting Studio -- http://localhost:3000/documents", fontsize=7.5, color='#718096')

    # Tab bar
    ax.add_patch(patches.Rectangle((0.5, 4.1), 2.2, 0.5, facecolor='#3182CE', edgecolor='#3182CE'))
    ax.text(1.6, 4.35, "First Information Report (FIR)", fontsize=7.5, fontweight='bold', color='white', ha='center')
    ax.add_patch(patches.Rectangle((2.8, 4.1), 1.8, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0'))
    ax.text(3.7, 4.35, "Legal Notice (Sec 80)", fontsize=7.5, color='#4A5568', ha='center')
    ax.add_patch(patches.Rectangle((4.7, 4.1), 1.8, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0'))
    ax.text(5.6, 4.35, "Sworn Affidavit", fontsize=7.5, color='#4A5568', ha='center')
    ax.add_patch(patches.Rectangle((6.6, 4.1), 1.8, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0'))
    ax.text(7.5, 4.35, "Consumer Complaint", fontsize=7.5, color='#4A5568', ha='center')

    # Left Form Pane
    ax.add_patch(patches.Rectangle((0.5, 0.5), 4.3, 3.4, facecolor='#F7FAFC', edgecolor='#CBD5E0', lw=1.5))
    ax.text(0.7, 3.6, "Complainant Name: [ Rajesh Kumar ]", fontsize=7, color='#2D3748')
    ax.text(0.7, 3.1, "Police Station: [ Division No. 5, Ludhiana ]", fontsize=7, color='#2D3748')
    ax.text(0.7, 2.6, "Offence: [ Online Financial Phishing Fraud ]", fontsize=7, color='#2D3748')
    ax.text(0.7, 2.1, "Statement of Facts: [ Rs. 75,000 debited... ]", fontsize=7, color='#2D3748')
    ax.add_patch(patches.Rectangle((0.7, 0.8), 3.9, 0.5, facecolor='#38A169', edgecolor='#2F855A'))
    ax.text(2.65, 1.05, "⬇️ Download Official Vector PDF", fontsize=8, fontweight='bold', color='white', ha='center')

    # Right Live Preview Pane
    ax.add_patch(patches.Rectangle((5.2, 0.5), 4.3, 3.4, facecolor='white', edgecolor='#CBD5E0', lw=1.5))
    ax.text(7.35, 3.6, "FORM NO. 1 - FIRST INFORMATION REPORT", fontsize=7, fontweight='bold', ha='center', color='#1A365D')
    ax.text(7.35, 3.3, "Under Section 173, BNSS 2023 / Sec 154 CrPC", fontsize=6.5, ha='center', color='#4A5568')
    ax.plot([5.5, 9.2], [3.15, 3.15], color='#CBD5E0', lw=1)
    ax.text(5.5, 2.8, "TO: SHO, Police Station: Division No. 5, Ludhiana", fontsize=6, color='#2D3748')
    ax.text(5.5, 2.4, "1. Complainant: Rajesh Kumar, Age: 34 yrs", fontsize=6, color='#2D3748')
    ax.text(5.5, 2.0, "2. Offence: Online Financial Fraud (BNS Sec 318)", fontsize=6, color='#2D3748')
    ax.text(5.5, 1.6, "3. Relief: Register FIR & Freeze Beneficiary Acct", fontsize=6, color='#2D3748')
    ax.text(5.5, 1.0, "[NOTARY JURAT / VERIFICATION BLOCK ATTESTED]", fontsize=6, color='#718096')

    save_and_close(fig, "fig_5_3_documents_studio.png")

# ── 17. Fig 5.4: Modern Statutes Catalog UI Mockup ────────────────────────────
def make_fig_5_4():
    fig, ax = setup_canvas(10, 5.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)

    # Frame
    ax.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 5.1, facecolor='white', edgecolor='#CBD5E0', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 4.8), 9.6, 0.5, facecolor='#EDF2F7', edgecolor='#CBD5E0', lw=1))
    ax.text(0.5, 5.05, "● ● ●  PocketLaw Modern Criminal Statutes Browser -- http://localhost:3000/laws", fontsize=7.5, color='#718096')

    # Header
    ax.text(5.0, 4.4, "⚖️ Modern Indian Criminal Jurisprudence & Statutory Cross-Mapper", fontsize=10, fontweight='bold', ha='center', color='#1A365D')
    ax.text(5.0, 4.1, "Enacted 1 July 2024: Reconciling Colonial Enactments (IPC, CrPC, Evidence Act) with Modern Successors", fontsize=7.5, ha='center', color='#4A5568')

    # Table Mockup
    y_starts = [3.5, 2.9, 2.3, 1.7, 1.1]
    headers = [("Colonial Code", 0.6, 2.0), ("Modern Statute (2023)", 2.8, 2.2), ("Key Section Mapping", 5.2, 2.5), ("Citizen Procedural Impact", 7.9, 1.8)]
    for title, x, w in headers:
        ax.add_patch(patches.Rectangle((x, 3.5), w, 0.45, facecolor='#2B6CB0', edgecolor='#2B6CB0'))
        ax.text(x + w/2, 3.72, title, fontsize=7.5, fontweight='bold', color='white', ha='center')

    rows = [
        ("IPC 1860", "BNS 2023", "Sec 420 -> Sec 318 (Cheating)\nSec 302 -> Sec 103 (Murder)", "Modern wording covers online & digital scams."),
        ("CrPC 1973", "BNSS 2023", "Sec 154 -> Sec 173 (FIR)\nSec 41A -> Sec 35 (Notice)", "Mandatory Zero FIR at any police station."),
        ("Evidence Act 1872", "BSA 2023", "Sec 65B -> Sec 61 & 63", "Electronic chats & server logs are primary proof.")
    ]
    for idx, (col, mod, secs, impact) in enumerate(rows):
        y = 2.7 - idx * 0.75
        for x, w, val in [(0.6, 2.0, col), (2.8, 2.2, mod), (5.2, 2.5, secs), (7.9, 1.8, impact)]:
            ax.add_patch(patches.Rectangle((x, y), w, 0.65, facecolor='#F7FAFC' if idx%2==0 else 'white', edgecolor='#CBD5E0'))
            ax.text(x + w/2, y + 0.32, val, fontsize=6.5, ha='center', va='center', color='#2D3748')

    save_and_close(fig, "fig_5_4_statutes_catalog.png")

if __name__ == "__main__":
    print("Generating all 17 diagram images...")
    make_gndec_emblem()
    make_fig_1_1()
    make_fig_2_1()
    make_fig_3_1()
    make_fig_3_2()
    make_fig_3_3()
    make_fig_3_4()
    make_fig_3_5()
    make_fig_3_6()
    make_fig_3_7()
    make_fig_3_8()
    make_fig_3_9()
    make_fig_3_10()
    make_fig_5_1()
    make_fig_5_2()
    make_fig_5_3()
    make_fig_5_4()
    print("All diagrams generated successfully!")

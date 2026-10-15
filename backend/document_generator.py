"""
PocketLaw - Court-Ready Legal Document Generation Engine
Generates formal, court-admissible drafts for:
1. First Information Report (CrPC Sec 154 / BNSS Sec 173)
2. Formal Legal Notice (Section 80 CPC / Standard Legal Practice)
3. Sworn Affidavit with Notary Jurat & Verification
4. Consumer Complaint (Consumer Protection Act, 2019 / E-Daakhil Format)

Provides formatted plain text (for UI live preview & DB storage)
and high-resolution, court-ready PDF generation via ReportLab.
"""

import io
import re
import html
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT


# ══════════════════════════════════════════════════════════════════════════════
#  1. TEXT FORMATTERS (Court-Ready & Formatted for UI Live Preview)
# ══════════════════════════════════════════════════════════════════════════════

def format_fir_text(d):
    dt = datetime.now().strftime("%d-%m-%Y")
    tm = datetime.now().strftime("%H:%M hrs")
    district = d.get("district", "Ludhiana").strip() or "Ludhiana"
    state = d.get("state", "Punjab").strip() or "Punjab"
    station = d.get("station", "[Police Station]").strip() or "[Police Station]"
    default_evidence = "1. Transaction slips / Bank statements\n2. Chat / SMS screenshots\n3. Call logs\n4. Any other documentary proof"
    evidence_val = d.get('evidence', default_evidence)

    return f"""================================================================================
          FORM NO. 1 - FIRST INFORMATION REPORT (INFORMAL DRAFT)
       Under Section 154, Code of Criminal Procedure, 1973 (CrPC)
        / Section 173, Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
================================================================================

TO:
The Station House Officer (SHO),
Police Station: {station},
District: {district}, State: {state}.

DATE & TIME: {dt} at {tm}
SUBJECT    : Complaint / Request for Registration of FIR regarding {d.get('crime_type', 'Cognizable Offence')}

--------------------------------------------------------------------------------
1. DETAILS OF THE COMPLAINANT / INFORMANT:
--------------------------------------------------------------------------------
   (a) Full Name            : {d.get('name', '[Complainant Full Name]')}
   (b) Father's/Spouse Name : {d.get('guardian', '[Father/Husband Name]')}
   (c) Age / Gender         : {d.get('age', '__')} years
   (d) Permanent Address    : {d.get('address', '[Residential Address]')}
   (e) Contact Number       : {d.get('phone', '[Contact Number]')}
   (f) Email Address        : {d.get('email', 'N/A')}

--------------------------------------------------------------------------------
2. PARTICULARS OF THE OCCURRENCE / OFFENCE:
--------------------------------------------------------------------------------
   (a) Nature of Offence    : {d.get('crime_type', 'Cognizable Offence')}
   (b) Date of Incident     : {d.get('date', '[Date of Incident]')}
   (c) Time of Incident     : {d.get('time', '[Time of Incident]')}
   (d) Place of Incident    : {d.get('place', '[Exact Location / Online Portal]')}
   (e) Distance & Direction : Within the territorial jurisdiction of PS {station}

--------------------------------------------------------------------------------
3. SUSPECT / ACCUSED DETAILS:
--------------------------------------------------------------------------------
   Name & Description       : {d.get('accused', 'Unknown person(s) / Under investigation')}
   Contact / Identifier     : {d.get('accused_details', 'Phone, UPI ID, IP Address or identity details as available')}

--------------------------------------------------------------------------------
4. DETAILED STATEMENT OF FACTS (CHRONOLOGICAL):
--------------------------------------------------------------------------------
{d.get('description', '[State all facts chronologically and clearly]')}

--------------------------------------------------------------------------------
5. DETAILS OF EVIDENCE ENCLOSED:
--------------------------------------------------------------------------------
{evidence_val}

--------------------------------------------------------------------------------
6. WITNESS PARTICULARS (IF ANY):
--------------------------------------------------------------------------------
{d.get('witnesses', 'Nil / Available upon police summons')}

--------------------------------------------------------------------------------
7. PRAYER / RELIEF SOUGHT:
--------------------------------------------------------------------------------
In light of the above facts, it is respectfully prayed that:
(a) A First Information Report (FIR) may kindly be registered under appropriate
    sections of the Indian Penal Code / Bharatiya Nyaya Sanhita, 2023, and IT Act;
(b) Necessary investigation be initiated expeditiously;
(c) Action may kindly be taken to secure evidence, trace the accused, and recover
    the victim's losses ({d.get('relief', 'Investigation and recovery of stolen property/funds')});
(d) A free copy of the FIR be provided to the complainant under Section 154(2) CrPC.

VERIFICATION:
I, the undersigned complainant, do hereby state on solemn affirmation that the
contents of this complaint are true and correct to the best of my knowledge,
information, and belief, and nothing material has been concealed therein.


Place: {district}
Date : {dt}

                                               _______________________________
                                               SIGNATURE / THUMB IMPRESSION
                                               Name: {d.get('name', '[Complainant Name]')}
                                               Phone: {d.get('phone', '')}

================================================================================
                            FOR POLICE OFFICE USE ONLY
================================================================================
FIR Registration No.  : ___________________________
Date & Time of Entry  : ___________________________
General Diary (GD) Ref: ___________________________
Assigned I.O. Name/No.: ___________________________
Statutory Sections    : ___________________________

Disclaimer: Generated by PocketLaw Legal Intelligence.
Must be reviewed and verified by an Advocate prior to official police submission.
================================================================================
""".strip()


def format_notice_text(d):
    dt = datetime.now().strftime("%d %B %Y")
    days = d.get("days", "15").strip() or "15"

    return f"""================================================================================
                               FORMAL LEGAL NOTICE
               (Issued Under Substantive Law & Section 80 CPC Principles)
================================================================================

DISPATCH MODE: By Registered Speed Post with A.D. / WhatsApp / Electronic Mail

DATE: {dt}

FROM:
{d.get('sender_name', '[Your Full Name]')}
{d.get('sender_address', '[Your Full Residential / Business Address]')}
City: {d.get('sender_city', '[City]')}
Phone: {d.get('sender_phone', '[Phone Number]')} | Email: {d.get('sender_email', '[Email Address]')}

TO (RECIPIENT / OPPOSITE PARTY):
{d.get('recipient_name', '[Recipient Individual / Entity / Organization]')}
{d.get('recipient_address', '[Recipient Complete Registered Office / Address]')}

SUBJECT: LEGAL NOTICE REGARDING {d.get('subject', '[Subject Matter / Dispute]')}.

Sir / Madam,

Under instructions and on behalf of my client / from the sender named above,
I hereby serve upon you this FORMAL LEGAL NOTICE on the following terms:

1. BACKGROUND & RELATIONSHIP:
   That you, the Addressee, entered into a binding transaction/agreement with the
   Sender wherein {d.get('subject', 'a lawful obligation was created')}.

2. CHRONOLOGY OF FACTS & CAUSE OF ACTION:
{d.get('facts', '[Detailed statement of facts describing what occurred, dates, financial amounts, and breach committed]')}

3. STATUTORY / LEGAL BASIS:
   That your acts and omissions constitute a direct breach of obligations under
   {d.get('law', 'the Indian Contract Act, Transfer of Property Act, and Consumer Protection Act')},
   infringing upon the legitimate legal rights of the sender and causing grave
   financial injury, mental agony, and distress.

4. SPECIFIC DEMAND & REMEDY:
   You are hereby called upon to comply with the following demands:
{d.get('demand', '[State exact demands, e.g., refund of money with interest, delivery of possession, replacement of product]')}

5. STATUTORY NOTICE PERIOD:
   You are hereby given a period of {days} (FIFTEEN) DAYS from the date of receipt
   of this notice to comply with the aforesaid demands in full.

6. CONSEQUENCE OF DEFAULT:
   PLEASE TAKE NOTE that in the event of your failure, neglect, or refusal to comply
   with the demands within the stipulated period of {days} days, the sender shall have
   no option but to initiate appropriate Civil and/or Criminal legal proceedings
   against you in the competent Court of Law at your sole risk, cost, and consequence,
   holding you liable for all legal expenses and damages.

A copy of this Legal Notice is retained in records for future production before the Court.


Yours faithfully,


____________________________________
{d.get('sender_name', '[Sender Name]')}
Date: {dt}

================================================================================
NOTE: Keep postal speed post receipt and delivery acknowledgment tracking report.
Generated by PocketLaw AI Legal Intelligence.
================================================================================
""".strip()


def format_affidavit_text(d):
    dt = datetime.now().strftime("%d %B %Y")
    city = d.get("city", "Ludhiana").strip() or "Ludhiana"

    return f"""================================================================================
                       SWORN AFFIDAVIT
        (To be executed on appropriate Non-Judicial Stamp Paper)
================================================================================

IN THE COURT OF / BEFORE THE COMPETENT AUTHORITY:
{d.get('court', 'District & Sessions Court / Executive Magistrate / Notary Public, ' + city)}
Case / Misc. Ref. No.: {d.get('case_ref', 'N/A')}

AFFIDAVIT OF:
I, {d.get('name', '[Full Name of Deponent]')},
Son / Daughter / Wife of: {d.get('guardian', '[Father/Husband Name]')},
Aged about: {d.get('age', '__')} years,
Occupation: {d.get('occupation', '[Occupation / Service / Business]')},
Residing at: {d.get('address', '[Complete Residential Address]')}, {city},

do hereby solemnly affirm, declare, and state on oath as under:

1. That I am the Deponent in this matter, a citizen of India, and fully competent
   and conversant with the facts stated herein.

2. PURPOSE OF AFFIDAVIT:
   That this Affidavit is solemnly affirmed for the purpose of:
   "{d.get('purpose', '[Purpose of affidavit - e.g., Address verification, Name change, Court statement]')}".

3. STATEMENT OF FACTS:
{d.get('statement', '[Set out all facts in numbered sequential order clearly and specifically]')}

4. That the facts stated above are true to my personal knowledge, belief, and records,
   and I have not concealed, misstated, or suppressed any material fact.


                                                      __________________________
                                                      DEPONENT (SIGNATURE)
                                                      Name: {d.get('name', '[Name]')}

--------------------------------------------------------------------------------
                                 VERIFICATION
--------------------------------------------------------------------------------
I, the above-named Deponent, do hereby verify and declare at {city} on this
{dt}, that the contents of paragraphs 1 to 4 of this Affidavit are true and
correct to my personal knowledge and belief. No part of it is false and nothing
material has been concealed or suppressed therefrom.


                                                      __________________________
                                                      DEPONENT (SIGNATURE)

--------------------------------------------------------------------------------
                       ATTESTATION (BEFORE NOTARY PUBLIC)
--------------------------------------------------------------------------------
Solemnly sworn and affirmed before me by the Deponent who is identified by:
Shri / Smt.: ________________________________________ (Advocate / Identifer)
at {city} on this {dt}.

The contents of this affidavit were read over and explained to the deponent in
the vernacular language, and the deponent appeared to understand the same.


[NOTARY PUBLIC / OATH COMMISSIONER SEAL]       __________________________________
                                              SIGNATURE OF ATTESTING AUTHORITY
                                              Regn No.: ________________________
                                              Commission Expires on: ___________

================================================================================
Generated by PocketLaw AI Legal Assistance Platform.
Must be printed on stamp paper and executed before an authorized Notary Public.
================================================================================
""".strip()


def format_complaint_text(d):
    dt = datetime.now().strftime("%d %B %Y")
    district = d.get("district", "Ludhiana").strip() or "Ludhiana"
    state = d.get("state", "Punjab").strip() or "Punjab"
    amount = d.get("amount", "0").strip() or "0"
    default_relief = f"Refund the entire amount of Rs. {amount}/- along with interest @ 18% p.a."
    relief_val = d.get('relief', default_relief)
    default_docs = "1. Copy of Tax Invoice / Purchase Receipt\n2. Warranty Card\n3. Email communications & Proof of notice served\n4. Photographs / Screenshots of defective product"
    docs_val = d.get('documents', default_docs)

    return f"""================================================================================
                   FORMAL CONSUMER COMPLAINT
      Filed under Section 35 of the Consumer Protection Act, 2019
       (Suitable for submission before District CDRC / E-Daakhil Portal)
================================================================================

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
AT: {district}, {state}

CONSUMER COMPLAINT NO.: _________ OF 2026

IN THE MATTER OF:

COMPLAINANT:
{d.get('name', '[Complainant Full Name]')}
Resident of: {d.get('address', '[Complete Residential Address]')},
District: {district}, State: {state}.
Phone: {d.get('phone', '[Phone Number]')} | Email: {d.get('email', '[Email Address]')}
                                                                  ...COMPLAINANT
                                     VERSUS

OPPOSITE PARTY (OP):
{d.get('company', '[Company / Seller / Service Provider Name]')}
Registered Address: {d.get('company_address', '[Complete Corporate / Store Address]')},
Authorized Officer / Manager.
                                                                  ...OPPOSITE PARTY

--------------------------------------------------------------------------------
COMPLAINT UNDER SECTION 35, CONSUMER PROTECTION ACT, 2019 FOR DEFICIENCY IN
SERVICE, DEFECT IN GOODS, AND UNFAIR TRADE PRACTICES.
--------------------------------------------------------------------------------

MOST RESPECTFULLY SHOWETH:

1. JURISDICTION:
   (a) Pecuniary Jurisdiction: The total consideration paid by the Complainant is
       Rs. {amount}/- which falls well within the statutory limit of Rs. 50 Lakhs
       prescribed for the District Consumer Commission under CPA 2019.
   (b) Territorial Jurisdiction: The cause of action arose within the territorial
       limits of this Hon'ble Commission where the transaction took place.

2. PARTICULARS OF TRANSACTION:
   - Product / Service Purchased : {d.get('product', '[Product/Service Name]')}
   - Date of Purchase            : {d.get('purchase_date', '[Date of Purchase]')}
   - Invoice / Order Number      : {d.get('invoice', '[Invoice/Order Ref]')}
   - Total Amount Paid           : Rs. {amount}/- (Rupees {amount} only)

3. STATEMENT OF FACTS & DEFICIENCY IN SERVICE:
{d.get('facts', '[Detailed statement describing the defects, failure of Opposite Party to repair/replace, and breach of consumer guarantee]')}

4. LEGAL GROUNDS & UNFAIR TRADE PRACTICE:
   (a) That the OP supplied goods suffering from latent defects as defined under
       Section 2(10) of the Consumer Protection Act, 2019.
   (b) That the refusal to refund or rectify constitutes acute "Deficiency in Service"
       under Section 2(11) and an "Unfair Trade Practice" under Section 2(47).
   (c) That despite repeated requests and written representations, the OP failed
       to redress the legitimate grievance of the Complainant.

5. PRAYER / RELIEF SOUGHT:
   It is therefore most respectfully prayed that this Hon'ble Commission may be
   pleased to direct the Opposite Party to:
   (a) {relief_val};
   (b) Pay a sum of Rs. 25,000/- as compensation for mental agony, harassment, and
       hardship suffered by the Complainant;
   (c) Pay Rs. 10,000/- towards litigation costs incurred by the Complainant;
   (d) Grant any other or further relief as this Hon'ble Commission may deem fit.

6. LIST OF ENCLOSURES / EVIDENCE:
{docs_val}

--------------------------------------------------------------------------------
                                 VERIFICATION
--------------------------------------------------------------------------------
I, {d.get('name', '[Complainant Name]')}, do hereby solemnly verify that the
contents of paragraphs 1 to 6 of this Complaint are true and correct to the best
of my personal knowledge and belief, based on records, and nothing material has
been concealed therefrom.

Verified at: {district}
Date       : {dt}

                                               _________________________________
                                               COMPLAINANT (IN PERSON)
                                               Name: {d.get('name', '[Name]')}
                                               Phone: {d.get('phone', '')}

================================================================================
Filing Note: Can also be filed online FREE of hassle on edaakhil.nic.in
National Consumer Helpline: 1915 / 1800-11-4000
Generated by PocketLaw AI Legal Assistance Platform.
================================================================================
""".strip()


# ══════════════════════════════════════════════════════════════════════════════
#  2. REPORTLAB PDF RENDERER (Professional, Court-Ready Layout)
# ══════════════════════════════════════════════════════════════════════════════

def build_pdf_stream(title_text, subtitle_text, raw_formatted_text, metadata=None):
    """
    Constructs an elegant, professional legal document PDF in memory using ReportLab.
    Features:
    - Standard A4 court margins
    - Clean header banner with decorative borders
    - Structured typography and proper line breaking
    - Verification & Signature blocks
    - Security / Disclaimer footer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=44,
        rightMargin=44,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    header_style = ParagraphStyle(
        "CourtHeader",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F1E3D")
    )
    sub_style = ParagraphStyle(
        "CourtSubHeader",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#78350F")  # Warm gold/amber accent
    )
    body_style = ParagraphStyle(
        "CourtBody",
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1A1A1A")
    )
    bold_style = ParagraphStyle(
        "CourtBold",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0F1E3D")
    )
    section_head_style = ParagraphStyle(
        "CourtSection",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0F1E3D"),
        spaceBefore=8,
        spaceAfter=4
    )
    footer_style = ParagraphStyle(
        "CourtFooter",
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6B7280")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("JUSTICE & LEGAL AID DOCUMENTATION", sub_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(html.escape(title_text.upper()), header_style))
    if subtitle_text:
        story.append(Spacer(1, 3))
        story.append(Paragraph(html.escape(subtitle_text), sub_style))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F1E3D"), spaceAfter=10))

    # 2. Body Text Parsing & Formatting
    lines = raw_formatted_text.split("\n")
    skip_header = True

    for line in lines:
        s = line.strip()

        # Skip raw ASCII equal/dash dividers in text since we use flowables
        if re.match(r"^[=\-_]{10,}$", s):
            continue

        # Skip redundant title repeat from plain text
        if ("FIRST INFORMATION REPORT" in s or "FORMAL LEGAL NOTICE" in s or
            "SWORN AFFIDAVIT" in s or "FORMAL CONSUMER COMPLAINT" in s or
            "LEGAL CONSULTATION" in s) and skip_header:
            continue
        if skip_header and ("Under Section" in s or "Issued Under" in s or "Code of Criminal" in s or "Issued via" in s):
            continue

        skip_header = False

        if not s:
            story.append(Spacer(1, 4))
            continue

        # Section Headings (e.g. "1. DETAILS OF THE COMPLAINANT:", "VERIFICATION", etc.)
        if (re.match(r"^[0-9]+\.\s+[A-Z\s]+:?$", s) or
            s.startswith("TO:") or s.startswith("FROM:") or
            s in ("VERIFICATION:", "VERIFICATION", "JURISDICTION:", "PRAYER / RELIEF SOUGHT:",
                  "PARTICULARS OF OCCURRENCE:", "ATTESTATION (BEFORE NOTARY PUBLIC)",
                  "FOR POLICE OFFICE USE ONLY", "MOST RESPECTFULLY SHOWETH:", "IN THE MATTER OF:",
                  "CASE REFERENCE & CONSULTATION PARTICULARS:")):
            story.append(Spacer(1, 4))
            story.append(Paragraph(html.escape(s), section_head_style))
            continue

        # Bold field labels (e.g., "(a) Full Name : Rajesh Kumar")
        if re.match(r"^\s*(\([a-z0-9]+\)|[A-Za-z\s]+)\s*:\s*.+", s) and len(s) < 120:
            parts = s.split(":", 1)
            lbl = parts[0].strip()
            val = parts[1].strip()
            story.append(Paragraph(f"<b>{html.escape(lbl)} :</b> {html.escape(val)}", body_style))
            continue

        # Signatures and right aligned markers
        if "SIGNATURE" in s or "DEPONENT" in s or "COMPLAINANT (" in s or "Yours faithfully" in s:
            story.append(Spacer(1, 8))
            story.append(Paragraph(html.escape(s), bold_style))
            continue

        # Regular paragraph
        story.append(Paragraph(html.escape(s), body_style))

    # 3. Footer Bar
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#9CA3AF"), spaceBefore=6, spaceAfter=6))
    dt_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    footer_text = (
        f"Generated via PocketLaw AI Legal Intelligence on {dt_str} | "
        "Strictly for review and reference. Verification by an Advocate is advised."
    )
    story.append(Paragraph(html.escape(footer_text), footer_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_document_pdf(doc_type, data):
    """
    Main dispatch method: takes doc_type and form input dict,
    and returns (rendered_text, pdf_bytes_io).
    """
    dt = doc_type.lower().strip()
    if dt == "fir":
        rendered_text = format_fir_text(data)
        title = "FIRST INFORMATION REPORT"
        sub = "Under Section 154 CrPC, 1973 / Section 173 BNSS, 2023"
    elif dt == "notice":
        rendered_text = format_notice_text(data)
        title = "FORMAL LEGAL NOTICE"
        sub = "Served Under Substantive Civil Law & Section 80 CPC Principles"
    elif dt == "affidavit":
        rendered_text = format_affidavit_text(data)
        title = "SWORN AFFIDAVIT"
        sub = "For Execution Before Notary Public / Oath Commissioner"
    elif dt == "complaint":
        rendered_text = format_complaint_text(data)
        title = "FORMAL CONSUMER COMPLAINT"
        sub = "Under Section 35 of the Consumer Protection Act, 2019"
    else:
        rendered_text = format_notice_text(data)
        title = "LEGAL DOCUMENT"
        sub = "PocketLaw Legal Documentation"

    pdf_stream = build_pdf_stream(title, sub, rendered_text, metadata=data)
    return rendered_text, pdf_stream


def generate_consultation_pdf(data):
    """
    Generates a formal, printable PDF consultation report for a specific
    legal grievance and AI consultation response from chat history.
    """
    q = data.get("question") or data.get("message") or "Legal Consultation"
    ans = data.get("response") or data.get("ai_response") or data.get("response_preview") or "No legal opinion recorded."
    cat = (data.get("category") or "General Legal Matter").capitalize()
    user_name = data.get("user_name") or "Verified Citizen"
    raw_ts = data.get("timestamp")
    
    try:
        if raw_ts:
            dt = datetime.fromisoformat(str(raw_ts)).strftime("%d-%m-%Y %H:%M hrs")
        else:
            dt = datetime.now().strftime("%d-%m-%Y %H:%M hrs")
    except Exception:
        dt = datetime.now().strftime("%d-%m-%Y %H:%M hrs")

    consultation_text = f"""================================================================================
                    LEGAL CONSULTATION & CASE ADVISORY REPORT
                   Issued via PocketLaw AI Legal Intelligence
================================================================================

CASE REFERENCE & CONSULTATION PARTICULARS:
(a) Consultation Date : {dt}
(b) Legal Category    : {cat}
(c) Applicant / User  : {user_name}
(d) Regulatory Scope  : Indian Statutory Law & Landmark Supreme Court Precedents

--------------------------------------------------------------------------------
1. STATEMENT OF CITIZEN GRIEVANCE / INQUIRY:
--------------------------------------------------------------------------------
{q}

--------------------------------------------------------------------------------
2. AI LEGAL OPINION & STATUTORY GUIDANCE:
--------------------------------------------------------------------------------
{ans}

--------------------------------------------------------------------------------
3. JURISDICTION & PROCEDURAL NOTICE:
--------------------------------------------------------------------------------
This legal consultation was generated utilizing the PocketLaw RAG knowledge base
of 148 landmark Supreme Court of India judgments and modernized statutory provisions
under the Bharatiya Nyaya Sanhita (BNS) 2023, Bharatiya Nagarik Suraksha Sanhita
(BNSS) 2023, and specialized Central & State enactments.

--------------------------------------------------------------------------------
4. VERIFICATION & ADVISORY NOTICE:
--------------------------------------------------------------------------------
This document is an informational legal consultation summary generated for initial
case assessment and reference. It is recommended to present this consultation record
along with supporting evidence when engaging an enrolled Advocate for formal court
representation or filing before statutory commissions.

Date  : {dt}
Portal: PocketLaw AI Legal Intelligence System
"""
    return build_pdf_stream("LEGAL CONSULTATION REPORT", f"Reference: {cat} · {dt}", consultation_text, metadata=data)


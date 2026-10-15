import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import { dlFIR, dlNotice, dlAffidavit, dlComplaint, saveDocAPI } from "../services/api";

const TABS = [
  { id: "fir", l: "FIR Draft", ic: "fa-file-lines", d: "Report a crime to the police (CrPC 154 / BNSS 173)" },
  { id: "notice", l: "Legal Notice", ic: "fa-envelope-open-text", d: "Formal warning before taking legal action (Sec 80 CPC)" },
  { id: "affidavit", l: "Affidavit", ic: "fa-stamp", d: "Sworn statement of facts for courts & offices (Notary Verified)" },
  { id: "complaint", l: "Consumer Complaint", ic: "fa-cart-shopping", d: "Complaint to the Consumer Commission (CPA 2019)" },
];

function F({ label, id, type = "text", ph, v, chg, rows, opts, req, span }) {
  return (
    <div className="fg" style={span ? { gridColumn: "span 2" } : {}}>
      <label>{label}{req && <span style={{ color: "var(--err)", marginLeft: 2 }}>*</span>}</label>
      {opts ? <select value={v} onChange={e => chg(e.target.value)} className="sel">{opts.map(o => <option key={o}>{o}</option>)}</select>
        : rows ? <textarea rows={rows} placeholder={ph} value={v} onChange={e => chg(e.target.value)} />
          : <input type={type} placeholder={ph} value={v} onChange={e => chg(e.target.value)} />}
    </div>
  );
}

// ── Client-Side Real-Time Formatters (Instant Live Preview) ──────────────────

function buildFIRText(d) {
  const dt = new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "2-digit", year: "numeric" });
  return `================================================================================
          FORM NO. 1 - FIRST INFORMATION REPORT (INFORMAL DRAFT)
       Under Section 154, Code of Criminal Procedure, 1973 (CrPC)
        / Section 173, Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
================================================================================

TO:
The Station House Officer (SHO),
Police Station: ${d.station || "[Police Station]"},
District: ${d.district || "Ludhiana"}, State: ${d.state || "Punjab"}.

DATE       : ${dt}
SUBJECT    : Complaint / Request for Registration of FIR regarding ${d.crime_type || "Cognizable Offence"}

1. DETAILS OF THE COMPLAINANT / INFORMANT:
   (a) Full Name            : ${d.name || "[Complainant Full Name]"}
   (b) Father's/Spouse Name : ${d.guardian || "[Father/Husband Name]"}
   (c) Age                  : ${d.age || "__"} years
   (d) Permanent Address    : ${d.address || "[Residential Address]"}
   (e) Contact Number       : ${d.phone || "[Contact Number]"}
   (f) Email Address        : ${d.email || "N/A"}

2. PARTICULARS OF THE OCCURRENCE / OFFENCE:
   (a) Nature of Offence    : ${d.crime_type || "Cognizable Offence"}
   (b) Date of Incident     : ${d.date || "[Date of Incident]"}
   (c) Time of Incident     : ${d.time || "[Time of Incident]"}
   (d) Place of Incident    : ${d.place || "[Exact Location / Online Portal]"}
   (e) Jurisdiction         : Within the territorial limits of PS ${d.station || "[Police Station]"}

3. DETAILED STATEMENT OF FACTS (CHRONOLOGICAL):
${d.description || "[Describe facts chronologically with dates, transaction IDs, and events]"}

4. EVIDENCE ENCLOSED:
${d.evidence || "1. Relevant transaction screenshots & bank slips\n2. Call logs and message history\n3. Proof of identity"}

5. WITNESS PARTICULARS:
${d.witnesses || "Nil / Available upon police summons"}

6. PRAYER / RELIEF SOUGHT:
In light of the above facts, it is respectfully prayed that:
(a) A First Information Report (FIR) be registered under appropriate BNS 2023 / IT Act sections;
(b) Speedy investigation be initiated to recover losses (${d.relief || "Investigation and recovery"});
(c) A free copy of the registered FIR be provided to the complainant under Section 173(2) BNSS.

VERIFICATION:
I, the undersigned complainant, do hereby declare on solemn affirmation that the contents
of this complaint are true and correct to the best of my knowledge and belief.

Place: ${d.district || "Ludhiana"}
Date : ${dt}

                                               _______________________________
                                               SIGNATURE OF COMPLAINANT
                                               Name: ${d.name || "[Name]"}`;
}

function buildNoticeText(d) {
  const dt = new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
  return `================================================================================
                               FORMAL LEGAL NOTICE
               (Issued Under Substantive Law & Section 80 CPC Principles)
================================================================================

DISPATCH MODE: By Registered Speed Post with A.D. / WhatsApp / Electronic Mail
DATE: ${dt}

FROM:
${d.sender_name || "[Your Full Name]"}
${d.sender_address || "[Your Full Address]"}, ${d.sender_city || "Ludhiana"}
Phone: ${d.sender_phone || "[Phone]"} | Email: ${d.sender_email || "[Email]"}

TO (RECIPIENT / OPPOSITE PARTY):
${d.recipient_name || "[Recipient Individual / Entity Name]"}
${d.recipient_address || "[Recipient Address]"}

SUBJECT: LEGAL NOTICE REGARDING ${d.subject || "[Subject Matter / Dispute]"}.

Sir / Madam,

Under instructions and on behalf of my client / from the sender named above, I serve upon you this FORMAL LEGAL NOTICE:

1. BACKGROUND & RELATIONSHIP:
   That you entered into a transaction/obligation with the Sender regarding ${d.subject || "a lawful obligation"}.

2. STATEMENT OF FACTS & CAUSE OF ACTION:
${d.facts || "[Detailed statement of facts describing what occurred, dates, financial amounts, and breach committed]"}

3. STATUTORY / LEGAL BASIS:
   That your acts and omissions constitute a breach under ${d.law || "applicable Indian Laws (Contract Act / Consumer Protection Act)"},
   causing grave financial loss, injury, and mental harassment to the sender.

4. SPECIFIC DEMAND & REMEDY:
${d.demand || "[State exact demands, e.g. refund with interest, replacement of goods, compliance]"}

5. STATUTORY NOTICE PERIOD:
   You are hereby called upon to comply with the aforesaid demands in full within ${d.days || "15"} DAYS of receipt of this notice.

6. CONSEQUENCE OF DEFAULT:
   Take note that if you fail to comply within ${d.days || "15"} days, legal civil and/or criminal proceedings
   will be instituted against you in the competent Court of Law at your sole risk, cost, and consequences.

Yours faithfully,

____________________________________
${d.sender_name || "[Sender Name]"}`;
}

function buildAffidavitText(d) {
  const dt = new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
  return `================================================================================
                       SWORN AFFIDAVIT
        (To be executed on appropriate Non-Judicial Stamp Paper)
================================================================================

IN THE COURT OF / BEFORE: ${d.court || "District Court / Notary Public, " + (d.city || "Ludhiana")}
Case / Misc. Ref. No.   : ${d.case_ref || "N/A"}

AFFIDAVIT OF:
I, ${d.name || "[Full Name of Deponent]"},
Son / Daughter / Wife of: ${d.guardian || "[Father/Husband Name]"},
Aged about: ${d.age || "__"} years, Occupation: ${d.occupation || "[Occupation]"},
Residing at: ${d.address || "[Address]"}, ${d.city || "Ludhiana"},

do hereby solemnly affirm, declare, and state on oath as under:

1. That I am the Deponent in this matter, a citizen of India, and fully conversant with the facts stated herein.
2. PURPOSE OF AFFIDAVIT:
   That this Affidavit is affirmed for the purpose of: "${d.purpose || "[Purpose of affidavit]"}".
3. STATEMENT OF FACTS:
${d.statement || "[State all facts in numbered sequential paragraphs clearly and specifically]"}
4. That the facts stated above are true to my personal knowledge, and I have not concealed any material fact.

                                                      __________________________
                                                      DEPONENT (SIGNATURE)

VERIFICATION:
Verified at ${d.city || "Ludhiana"} on this ${dt}, that contents of paragraphs 1 to 4 above
are true and correct to my personal knowledge. Nothing material has been concealed therefrom.

                                                      __________________________
                                                      DEPONENT (SIGNATURE)

ATTESTATION (BEFORE NOTARY PUBLIC / OATH COMMISSIONER):
Sworn before me by the Deponent at ${d.city || "Ludhiana"} on ${dt}.
[NOTARY STAMP & SEAL]                                  __________________________
                                                      ATTESTING AUTHORITY`;
}

function buildComplaintText(d) {
  const dt = new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
  return `================================================================================
                   FORMAL CONSUMER COMPLAINT
      Filed under Section 35 of the Consumer Protection Act, 2019
       (Suitable for submission before District CDRC / E-Daakhil Portal)
================================================================================

BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
AT: ${d.district || "Ludhiana"}, ${d.state || "Punjab"}

COMPLAINANT:
${d.name || "[Complainant Full Name]"}
Address: ${d.address || "[Address]"}, ${d.district || "Ludhiana"}, ${d.state || "Punjab"}.
Phone: ${d.phone || ""} | Email: ${d.email || ""}
                                                                  ...COMPLAINANT
                                     VERSUS

OPPOSITE PARTY (OP):
${d.company || "[Company / Seller Name]"}
Address: ${d.company_address || "[Company Address]"}
                                                                  ...OPPOSITE PARTY

1. JURISDICTION:
   (a) Pecuniary: Consideration paid is Rs. ${d.amount || "0"}/- (within statutory limit of Rs. 50 Lakhs for District Commission).
   (b) Territorial: Transaction took place within the territorial jurisdiction of this Hon'ble Commission.

2. TRANSACTION DETAILS:
   - Product/Service: ${d.product || "[Product Name]"}
   - Purchase Date  : ${d.purchase_date || "[Date]"}
   - Invoice / Order: ${d.invoice || "[Invoice No.]"}
   - Amount Paid    : Rs. ${d.amount || "0"}/-

3. STATEMENT OF DEFICIENCY / FACTS:
${d.facts || "[Describe the defect, deficiency in service, and failure of seller/company to rectify]"}

4. RELIEF SOUGHT:
   (a) ${d.relief || `Full refund of Rs. ${d.amount || "0"}/- along with interest @ 18% p.a.`};
   (b) Compensation of Rs. 25,000/- towards mental agony and harassment;
   (c) Litigation expenses of Rs. 10,000/-.

5. ENCLOSURES:
${d.documents || "1. Tax Invoice / Receipt\n2. Warranty Card\n3. Email correspondence"}

VERIFICATION:
I, ${d.name || "[Complainant Name]"}, do verify that paragraphs 1 to 5 are true to my knowledge and records.

Place: ${d.district || "Ludhiana"}
Date : ${dt}

                                               _________________________________
                                               COMPLAINANT (IN PERSON)`;
}

// ── Live Document Preview & Actions Component ────────────────────────────────

function LivePreviewPanel({ tab, title, text, data, onDownload }) {
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    toast.success("Draft copied to clipboard!");
  };

  const handlePrint = () => {
    const w = window.open("", "_blank");
    if (!w) {
      toast.error("Popup blocked. Please allow popups to print.");
      return;
    }
    w.document.write(`<html><head><title>${title}</title><style>body{font-family:monospace;font-size:12px;line-height:1.5;padding:30px;color:#111;white-space:pre-wrap;}</style></head><body>${text.replace(/</g, "&lt;")}</body></html>`);
    w.document.close();
    w.focus();
    w.print();
  };

  const handleSaveDraft = async () => {
    const token = localStorage.getItem("jl_token");
    if (!token) {
      toast.error("Sign in to save drafts to your account");
      return;
    }
    try {
      toast.loading("Saving draft to your account...");
      await saveDocAPI({
        doc_type: tab,
        title: `${title} - ${data.name || data.sender_name || "Draft"}`,
        form_payload: data,
        rendered_content: text
      });
      toast.dismiss();
      toast.success("Draft saved successfully to your account!");
    } catch (e) {
      toast.dismiss();
      toast.error("Failed to save draft");
    }
  };

  return (
    <div style={{ marginTop: 24, borderTop: "1px solid var(--border)", paddingTop: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12, flexWrap: "wrap", gap: 10 }}>
        <div>
          <span className="tag tok"><i className="fas fa-eye" /> Live Document Preview</span>
          <span style={{ fontSize: 12, color: "var(--dim)", marginLeft: 8 }}>Updates in real-time as you fill the form</span>
        </div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <button className="btn btn-sm btn-o" onClick={handleCopy} title="Copy draft text to clipboard">
            <i className="fas fa-copy" /> Copy
          </button>
          <button className="btn btn-sm btn-o" onClick={handlePrint} title="Print formatted document">
            <i className="fas fa-print" /> Print
          </button>
          <button className="btn btn-sm btn-o" onClick={handleSaveDraft} title="Save draft to account">
            <i className="fas fa-bookmark" /> Save Draft
          </button>
          <button className="btn btn-sm btn-g" onClick={onDownload} title="Download official court-ready PDF">
            <i className="fas fa-file-pdf" /> Download PDF
          </button>
        </div>
      </div>
      <div style={{ background: "var(--panel2)", border: "1px solid var(--border)", borderRadius: 10, padding: 18, maxHeight: 420, overflowY: "auto" }}>
        <pre style={{ whiteSpace: "pre-wrap", fontFamily: "var(--mono, monospace)", fontSize: 12, lineHeight: 1.6, color: "var(--ink)", margin: 0 }}>
          {text}
        </pre>
      </div>
    </div>
  );
}

// ── Form Components ──────────────────────────────────────────────────────────

function FIRForm() {
  const [d, setD] = useState({ name: "", age: "", guardian: "", address: "", phone: "", email: "", station: "", district: "Ludhiana", state: "Punjab", crime_type: "Online Fraud", date: "", time: "", place: "", witnesses: "", description: "", evidence: "", relief: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  
  const dl = async () => {
    if (!d.name) { toast.error("Enter your name"); return; }
    toast.loading("Generating Court-Ready PDF...");
    await dlFIR(d);
    toast.dismiss();
    toast.success("FIR Draft PDF downloaded!");
  };

  const previewText = buildFIRText(d);

  return (
    <div>
      <div className="ibox">Fill details to generate an official court-ready FIR draft under Section 154 CrPC / Section 173 BNSS.</div>
      <div className="g2">
        <F label="Full Name" ph="Rajesh Kumar" v={d.name} chg={s("name")} req />
        <F label="Age" type="number" ph="35" v={d.age} chg={s("age")} />
        <F label="Father/Husband Name" ph="Mohan Kumar" v={d.guardian} chg={s("guardian")} />
        <F label="Phone" ph="+91 98765 43210" v={d.phone} chg={s("phone")} />
        <F label="Full Address" ph="123 MG Road, Ludhiana" v={d.address} chg={s("address")} span />
        <F label="Email" type="email" ph="you@email.com" v={d.email} chg={s("email")} />
        <F label="Crime Type" opts={["Online Fraud", "UPI Fraud", "Theft", "Assault", "Harassment", "Domestic Violence", "Property Dispute", "Cheating", "Cyber Crime", "Extortion"]} v={d.crime_type} chg={s("crime_type")} />
        <F label="Police Station" ph="Sadar PS" v={d.station} chg={s("station")} />
        <F label="District" ph="Ludhiana" v={d.district} chg={s("district")} />
        <F label="State" ph="Punjab" v={d.state} chg={s("state")} />
        <F label="Date of Incident" type="date" v={d.date} chg={s("date")} />
        <F label="Time of Incident" type="time" v={d.time} chg={s("time")} />
        <F label="Place of Incident" ph="Exact location / Online URL" v={d.place} chg={s("place")} span />
        <F label="Detailed Description" ph="Describe what happened in detail, chronologically..." rows={4} v={d.description} chg={s("description")} req span />
        <F label="Evidence Available" ph="Screenshots, transaction IDs, bank statements, CCTV..." rows={2} v={d.evidence} chg={s("evidence")} span />
        <F label="Witnesses (if any)" ph="Name, Phone" v={d.witnesses} chg={s("witnesses")} />
        <F label="Relief Sought" ph="Investigation, arrest, recovery of money..." v={d.relief} chg={s("relief")} />
      </div>
      <div style={{ marginTop: 20 }}>
        <button className="btn btn-g" onClick={dl}><i className="fas fa-file-pdf" /> Download FIR Draft (PDF)</button>
      </div>
      <LivePreviewPanel tab="fir" title="FIR Draft" text={previewText} data={d} onDownload={dl} />
    </div>
  );
}

function NoticeForm() {
  const [d, setD] = useState({ sender_name: "", sender_phone: "", sender_address: "", sender_email: "", sender_city: "Ludhiana", recipient_name: "", recipient_address: "", subject: "", days: "15", law: "", facts: "", demand: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  
  const dl = async () => {
    if (!d.sender_name) { toast.error("Enter your name"); return; }
    toast.loading("Generating Legal Notice PDF...");
    await dlNotice(d);
    toast.dismiss();
    toast.success("Legal Notice PDF downloaded!");
  };

  const previewText = buildNoticeText(d);

  return (
    <div>
      <div className="ibox">Formal Legal Notice under Section 80 CPC style. Send via Registered Speed Post + Email.</div>
      <div className="form-sec">FROM (Your Details)</div>
      <div className="g2">
        <F label="Your Full Name" ph="Rajesh Kumar" v={d.sender_name} chg={s("sender_name")} req />
        <F label="Phone" ph="+91 98765 43210" v={d.sender_phone} chg={s("sender_phone")} />
        <F label="Email" type="email" ph="you@email.com" v={d.sender_email} chg={s("sender_email")} />
        <F label="City" ph="Ludhiana" v={d.sender_city} chg={s("sender_city")} />
        <F label="Full Address" ph="Complete address" v={d.sender_address} chg={s("sender_address")} span />
      </div>
      <hr className="dvd" />
      <div className="form-sec">TO (Recipient)</div>
      <div className="g2">
        <F label="Recipient Name/Company" ph="Company / Landlord Name" v={d.recipient_name} chg={s("recipient_name")} req />
        <F label="Response Days" type="number" ph="15" v={d.days} chg={s("days")} />
        <F label="Recipient Address" ph="Complete address" v={d.recipient_address} chg={s("recipient_address")} span />
        <F label="Subject/Matter" ph="Security Deposit / Product Defect" v={d.subject} chg={s("subject")} req />
        <F label="Applicable Law" ph="Consumer Protection Act / Transfer of Property Act" v={d.law} chg={s("law")} />
        <F label="Facts of Dispute" ph="Background, what happened, dates, amounts involved..." rows={4} v={d.facts} chg={s("facts")} req span />
        <F label="Your Demand" ph="Refund of ₹50,000 / Replacement / Reinstatement..." rows={2} v={d.demand} chg={s("demand")} req span />
      </div>
      <div style={{ marginTop: 20 }}>
        <button className="btn btn-g" onClick={dl}><i className="fas fa-file-pdf" /> Download Legal Notice (PDF)</button>
      </div>
      <LivePreviewPanel tab="notice" title="Legal Notice" text={previewText} data={d} onDownload={dl} />
    </div>
  );
}

function AffidavitForm() {
  const [d, setD] = useState({ name: "", age: "", guardian: "", occupation: "", address: "", city: "Ludhiana", court: "", case_ref: "", purpose: "", statement: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  
  const dl = async () => {
    if (!d.name) { toast.error("Enter your name"); return; }
    toast.loading("Generating Affidavit PDF...");
    await dlAffidavit(d);
    toast.dismiss();
    toast.success("Affidavit PDF downloaded!");
  };

  const previewText = buildAffidavitText(d);

  return (
    <div>
      <div className="ibox">Sworn Affidavit with formal Deponent Verification and Notary Public / Oath Commissioner jurat.</div>
      <div className="g2">
        <F label="Full Name" ph="Rajesh Kumar" v={d.name} chg={s("name")} req />
        <F label="Age" type="number" ph="35" v={d.age} chg={s("age")} />
        <F label="Father/Husband Name" ph="Mohan Kumar" v={d.guardian} chg={s("guardian")} />
        <F label="Occupation" ph="Service / Business / Retired" v={d.occupation} chg={s("occupation")} />
        <F label="Full Address" ph="Complete residential address" v={d.address} chg={s("address")} span />
        <F label="City" ph="Ludhiana" v={d.city} chg={s("city")} />
        <F label="Court/Authority" ph="District Court, Ludhiana" v={d.court} chg={s("court")} />
        <F label="Case Number (if any)" ph="CS/123/2025 or N/A" v={d.case_ref} chg={s("case_ref")} />
        <F label="Purpose of Affidavit" ph="Identity / Address Proof / Name Change / Court Submission" v={d.purpose} chg={s("purpose")} req span />
        <F label="Statement of Facts" ph="I solemnly declare that..." rows={5} v={d.statement} chg={s("statement")} req span />
      </div>
      <div style={{ marginTop: 20 }}>
        <button className="btn btn-g" onClick={dl}><i className="fas fa-file-pdf" /> Download Affidavit (PDF)</button>
      </div>
      <LivePreviewPanel tab="affidavit" title="Sworn Affidavit" text={previewText} data={d} onDownload={dl} />
    </div>
  );
}

function ComplaintForm() {
  const [d, setD] = useState({ name: "", address: "", phone: "", email: "", district: "Ludhiana", state: "Punjab", company: "", company_address: "", purchase_date: "", amount: "", product: "", invoice: "", facts: "", relief: "", documents: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  
  const dl = async () => {
    if (!d.name) { toast.error("Enter your name"); return; }
    toast.loading("Generating Complaint PDF...");
    await dlComplaint(d);
    toast.dismiss();
    toast.success("Consumer Complaint PDF downloaded!");
  };

  const previewText = buildComplaintText(d);

  return (
    <div>
      <div className="ibox"><strong>File FREE at edaakhil.nic.in</strong> — Consumer Helpline: 1800-11-4000 (Toll Free)<br />District: up to ₹50L | State: up to ₹2Cr | National: above ₹2Cr</div>
      <div className="form-sec">Complainant</div>
      <div className="g2">
        <F label="Your Full Name" ph="Rajesh Kumar" v={d.name} chg={s("name")} req />
        <F label="Phone" ph="+91 98765 43210" v={d.phone} chg={s("phone")} />
        <F label="Email" type="email" ph="you@email.com" v={d.email} chg={s("email")} />
        <F label="District" ph="Ludhiana" v={d.district} chg={s("district")} />
        <F label="State" ph="Punjab" v={d.state} chg={s("state")} />
        <F label="Your Address" ph="Complete address" v={d.address} chg={s("address")} span />
      </div>
      <hr className="dvd" />
      <div className="form-sec">Opposite Party (Company/Seller)</div>
      <div className="g2">
        <F label="Company/Seller Name" ph="Amazon / ABC Pvt Ltd" v={d.company} chg={s("company")} req />
        <F label="Company Address" ph="Company address" v={d.company_address} chg={s("company_address")} />
      </div>
      <hr className="dvd" />
      <div className="g2">
        <F label="Purchase Date" type="date" v={d.purchase_date} chg={s("purchase_date")} />
        <F label="Amount Paid (₹)" type="number" ph="5000" v={d.amount} chg={s("amount")} />
        <F label="Product/Service" ph="Mobile / Washing Machine / Insurance" v={d.product} chg={s("product")} req />
        <F label="Invoice/Order No." ph="INV-001 / Order #12345" v={d.invoice} chg={s("invoice")} />
        <F label="Facts of Complaint" ph="Describe defect/deficiency in detail..." rows={4} v={d.facts} chg={s("facts")} req span />
        <F label="Relief Sought" ph="Full refund of ₹5000 / Replacement / Compensation..." rows={2} v={d.relief} chg={s("relief")} req span />
        <F label="Documents Enclosed" ph="1. Invoice 2. Warranty 3. Company emails..." rows={2} v={d.documents} chg={s("documents")} span />
      </div>
      <div style={{ marginTop: 20 }}>
        <button className="btn btn-g" onClick={dl}><i className="fas fa-file-pdf" /> Download Consumer Complaint (PDF)</button>
      </div>
      <LivePreviewPanel tab="complaint" title="Consumer Complaint" text={previewText} data={d} onDownload={dl} />
    </div>
  );
}

export default function DocumentsPage() {
  const [sp] = useSearchParams();
  const [tab, setTab] = useState(sp.get("tab") || "fir");
  useEffect(() => { const t = sp.get("tab"); if (t) setTab(t); }, [sp]);
  
  const forms = { fir: <FIRForm />, notice: <NoticeForm />, affidavit: <AffidavitForm />, complaint: <ComplaintForm /> };
  const cur = TABS.find(t => t.id === tab) || TABS[0];
  
  return (
    <div className="page">
      <div className="shdr">
        <div className="stag"><i className="fas fa-file-signature" /> Automated Legal Document Drafting</div>
        <h2 className="stit">Draft a <em>legal document</em> in minutes</h2>
        <p className="ssub">Pick a document, fill in a simple form, review the real-time live preview, and download a court-ready PDF template.</p>
      </div>
      <div className="doc-picker">
        {TABS.map(t => (
          <button key={t.id} className={`doc-card${tab === t.id ? " act" : ""}`} onClick={() => setTab(t.id)}>
            <span className="di"><i className={`fas ${t.ic}`} /></span>
            <b>{t.l}</b>
            <small>{t.d}</small>
          </button>
        ))}
      </div>
      <div className="card" style={{ padding: 28 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 18 }}>
          <span className="di" style={{ width: 40, height: 40, borderRadius: 11, background: "var(--accent-soft)", color: "var(--accent)", display: "flex", alignItems: "center", justifyContent: "center" }}><i className={`fas ${cur.ic}`} /></span>
          <div>
            <div style={{ fontFamily: "var(--serif)", fontSize: 21, fontWeight: 600 }}>{cur.l}</div>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>{cur.d}</div>
          </div>
        </div>
        {forms[tab]}
      </div>
      <p style={{ textAlign: "center", fontSize: 12.5, color: "var(--muted)", marginTop: 20 }}>
        <i className="fas fa-circle-info" /> Generated documents are reference templates formatted for Indian courts and authorities. Please review them (ideally with a lawyer) before filing.
      </p>
    </div>
  );
}

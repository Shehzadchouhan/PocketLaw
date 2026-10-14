import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import { dlFIR, dlNotice, dlAffidavit, dlComplaint } from "../services/api";

const TABS = [
  { id: "fir", l: "FIR Draft", ic: "fa-file-lines", d: "Report a crime to the police (CrPC 154)" },
  { id: "notice", l: "Legal Notice", ic: "fa-envelope-open-text", d: "Formal warning before taking legal action" },
  { id: "affidavit", l: "Affidavit", ic: "fa-stamp", d: "Sworn statement of facts for courts & offices" },
  { id: "complaint", l: "Consumer Complaint", ic: "fa-cart-shopping", d: "Complaint to the Consumer Commission" },
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

function FIRForm() {
  const [d, setD] = useState({ name: "", age: "", guardian: "", address: "", phone: "", email: "", station: "", district: "Ludhiana", state: "Punjab", crime_type: "Online Fraud", date: "", time: "", place: "", witnesses: "", description: "", evidence: "", relief: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  const dl = async () => { if (!d.name) { toast.error("Enter your name"); return; } toast.loading("Generating FIR..."); await dlFIR(d); toast.dismiss(); toast.success("FIR Draft downloaded!"); };
  return (
    <div>
      <div className="ibox">Fill details and download. Review with a lawyer before submitting to police.</div>
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
        <F label="Place of Incident" ph="Exact location" v={d.place} chg={s("place")} span />
        <F label="Detailed Description" ph="Describe what happened in detail, chronologically..." rows={4} v={d.description} chg={s("description")} req span />
        <F label="Evidence Available" ph="Screenshots, transaction IDs, bank statements, CCTV..." rows={2} v={d.evidence} chg={s("evidence")} span />
        <F label="Witnesses (if any)" ph="Name, Phone" v={d.witnesses} chg={s("witnesses")} />
        <F label="Relief Sought" ph="Investigation, arrest, recovery of money..." v={d.relief} chg={s("relief")} />
      </div>
      <button className="btn btn-g" style={{ marginTop: 20 }} onClick={dl}><i className="fas fa-download" /> Download FIR Draft (.txt)</button>
    </div>
  );
}

function NoticeForm() {
  const [d, setD] = useState({ sender_name: "", sender_phone: "", sender_address: "", sender_email: "", sender_city: "Ludhiana", recipient_name: "", recipient_address: "", subject: "", days: "15", law: "", facts: "", demand: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  const dl = async () => { if (!d.sender_name) { toast.error("Enter your name"); return; } toast.loading("Generating Notice..."); await dlNotice(d); toast.dismiss(); toast.success("Legal Notice downloaded!"); };
  return (
    <div>
      <div className="ibox">Send via Registered Post + WhatsApp + Email. Keep delivery proof for court.</div>
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
      <button className="btn btn-g" style={{ marginTop: 20 }} onClick={dl}><i className="fas fa-download" /> Download Legal Notice (.txt)</button>
    </div>
  );
}

function AffidavitForm() {
  const [d, setD] = useState({ name: "", age: "", guardian: "", occupation: "", address: "", city: "Ludhiana", court: "", case_ref: "", purpose: "", statement: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  const dl = async () => { if (!d.name) { toast.error("Enter your name"); return; } toast.loading("Generating..."); await dlAffidavit(d); toast.dismiss(); toast.success("Affidavit downloaded!"); };
  return (
    <div>
      <div className="ibox">Must be executed before a Notary/Oath Commissioner on stamp paper. This is a template only.</div>
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
      <button className="btn btn-g" style={{ marginTop: 20 }} onClick={dl}><i className="fas fa-download" /> Download Affidavit (.txt)</button>
    </div>
  );
}

function ComplaintForm() {
  const [d, setD] = useState({ name: "", address: "", phone: "", email: "", district: "Ludhiana", state: "Punjab", company: "", company_address: "", purchase_date: "", amount: "", product: "", invoice: "", facts: "", relief: "", documents: "" });
  const s = k => v => setD(p => ({ ...p, [k]: v }));
  const dl = async () => { if (!d.name) { toast.error("Enter your name"); return; } toast.loading("Generating..."); await dlComplaint(d); toast.dismiss(); toast.success("Complaint downloaded!"); };
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
      <button className="btn btn-g" style={{ marginTop: 20 }} onClick={dl}><i className="fas fa-download" /> Download Consumer Complaint (.txt)</button>
      <p style={{ fontSize: 11, color: "var(--ok)", marginTop: 10 }}><i className="fas fa-check-circle" /> Also file FREE at: edaakhil.nic.in</p>
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
        <p className="ssub">Pick a document, fill in a simple form, and download a properly formatted template you can review and use.</p>
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
        <i className="fas fa-circle-info" /> Generated documents are reference templates. Please review them (ideally with a lawyer) before use.
      </p>
    </div>
  );
}

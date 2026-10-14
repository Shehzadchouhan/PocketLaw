import React, { useState, useEffect } from "react";
import { searchAPI, caseAPI } from "../services/api";

function Modal({ c, onClose }) {
  if (!c) return null;
  return (
    <div className="ovrl" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="mbox">
        <button className="mcls" onClick={onClose}><i className="fas fa-times" /></button>
        <h3 style={{ fontFamily: "var(--serif)", fontSize: 22, color: "var(--gold-l)", marginBottom: 12 }}>{c.case_type} · {c.year}</h3>
        <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
          <span className={`tag t${c.case_type}`}>{c.case_type}</span>
          <span className={`tag ${c.outcome === "Allowed" ? "tok" : c.outcome === "Dismissed" ? "terr" : "twarn"}`}>{c.outcome}</span>
        </div>
        <div className="ibox"><strong>File:</strong> {c.filename}</div>
        <div className="ibox"><strong>Summary:</strong><br />{c.summary || "Supreme Court judgment."}</div>
        {c.full_text && <div className="ibox" style={{ fontFamily: "monospace", fontSize: 12 }}><strong>Text Extract:</strong><br />{c.full_text.substring(0, 600)}...</div>}
      </div>
    </div>
  );
}

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [cat, setCat] = useState("");
  const [out, setOut] = useState("");
  const [res, setRes] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [sel, setSel] = useState(null);
  const [page, setPage] = useState(1);

  const doSearch = async (pg = 1) => {
    setLoading(true); setPage(pg);
    try {
      const data = await searchAPI({ q, category: cat, outcome: out, page: pg, per_page: 20 });
      setRes(data.results); setTotal(data.total);
    } catch { setRes([]); }
    setLoading(false);
  };

  const loadCase = async (c) => {
    try { const full = await caseAPI(c.id); setSel(full); } catch { setSel(c); }
  };

  useEffect(() => { doSearch(1); }, []);

  return (
    <div className="page">
      <div className="shdr">
        <div className="stag"><i className="fas fa-gavel" /> Case Search</div>
        <h2 className="stit">Browse <em>Supreme Court judgments</em></h2>
        <p className="ssub">Filter real judgments by category and outcome to see how courts have decided similar matters.</p>
      </div>
      <div style={{ display: "flex", gap: 12, marginBottom: 24, flexWrap: "wrap" }}>
        <input style={{ flex: 1, minWidth: 200 }} placeholder="Search keyword..." value={q} onChange={e => setQ(e.target.value)} onKeyDown={e => e.key === "Enter" && doSearch(1)} />
        <select className="sel" style={{ minWidth: 140 }} value={cat} onChange={e => setCat(e.target.value)}>
          <option value="">All Categories</option>
          {["Criminal", "Consumer", "Property", "Family", "Labour", "Civil", "Constitutional"].map(c => <option key={c}>{c}</option>)}
        </select>
        <select className="sel" style={{ minWidth: 140 }} value={out} onChange={e => setOut(e.target.value)}>
          <option value="">All Outcomes</option>
          {["Allowed", "Dismissed", "Partially Allowed"].map(o => <option key={o}>{o}</option>)}
        </select>
        <button className="btn btn-g" onClick={() => doSearch(1)}><i className="fas fa-search" /> Search</button>
        <button className="btn btn-o" onClick={() => { setQ(""); setCat(""); setOut(""); doSearch(1); }}>Clear</button>
      </div>
      <p style={{ color: "var(--dim)", fontSize: 13, marginBottom: 16 }}>{loading ? "Searching..." : `${total} cases found`}</p>
      {loading ? <div style={{ textAlign: "center", padding: 60 }}><div className="ldr"><span /><span /><span /></div></div> : (
        <div className="ga">
          {res.map(c => (
            <div key={c.id} className="card" style={{ cursor: "pointer" }} onClick={() => loadCase(c)}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span className={`tag t${c.case_type}`}>{c.case_type}</span>
                <span style={{ fontSize: 12, color: "var(--dim)" }}>{c.year || "N/A"}</span>
              </div>
              <div style={{ marginBottom: 8 }}><span className={`tag ${c.outcome === "Allowed" ? "tok" : c.outcome === "Dismissed" ? "terr" : "twarn"}`} style={{ fontSize: 10 }}>{c.outcome}</span></div>
              <p style={{ fontSize: 12.5, color: "var(--dim)", lineHeight: 1.6, display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}>{c.summary || "SC Judgment."}</p>
              <p style={{ fontSize: 10, color: "var(--dim)", marginTop: 8, fontFamily: "monospace", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.filename?.substring(0, 50)}...</p>
            </div>
          ))}
        </div>
      )}
      {total > 20 && <div style={{ display: "flex", justifyContent: "center", gap: 8, marginTop: 28 }}>
        {page > 1 && <button className="btn btn-o" onClick={() => doSearch(page - 1)}>← Prev</button>}
        <span style={{ padding: "10px 16px", color: "var(--dim)" }}>Page {page}</span>
        {page * 20 < total && <button className="btn btn-o" onClick={() => doSearch(page + 1)}>Next →</button>}
      </div>}
      {sel && <Modal c={sel} onClose={() => setSel(null)} />}
    </div>
  );
}

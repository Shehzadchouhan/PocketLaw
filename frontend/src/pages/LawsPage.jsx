import React, { useState, useEffect } from "react";
import { lawsAPI } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function LawsPage() {
  const [laws, setLaws] = useState({});
  const [loading, setLoading] = useState(true);
  const [sel, setSel] = useState(null);
  const [selName, setSelName] = useState("");
  const [filter, setFilter] = useState("");
  const nav = useNavigate();

  useEffect(() => { lawsAPI().then(d => { setLaws(d); setLoading(false); }).catch(() => setLoading(false)); }, []);

  const filtered = Object.entries(laws).filter(([n, l]) => !filter || n.toLowerCase().includes(filter.toLowerCase()) || l.cat?.toLowerCase().includes(filter.toLowerCase()));

  const catColors = { Criminal: "var(--err)", Consumer: "var(--info)", Constitutional: "#FFB060", Family: "#D080D0", Labour: "var(--ok)", Property: "var(--gold)", Cyber: "#60D0FF", Motor: "var(--warn)" };

  return (
    <div className="page">
      <div className="shdr">
        <div className="stag"><i className="fas fa-book-open" /> Indian Laws Explorer</div>
        <h2 className="stit">Key <em>Indian laws</em>, simply explained</h2>
        <p className="ssub">Tap any Act to see its key sections, then jump to related cases.</p>
      </div>
      <div style={{ maxWidth: 400, margin: "0 auto 32px" }}>
        <input placeholder="Filter laws..." value={filter} onChange={e => setFilter(e.target.value)} />
      </div>
      {loading ? <div style={{ textAlign: "center", padding: 60 }}><div className="ldr"><span /><span /><span /></div></div> : (
        <div className="gl">
          {filtered.map(([name, law]) => (
            <div key={name} className="card" style={{ cursor: "pointer", borderLeft: `3px solid ${catColors[law.cat] || "var(--gold)"}` }} onClick={() => { setSel(law); setSelName(name); }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <h3 style={{ fontFamily: "var(--serif)", fontSize: 18, color: "var(--gold-l)" }}>{name}</h3>
                <span className={`tag t${law.cat}`} style={{ flexShrink: 0, marginLeft: 8 }}>{law.cat}</span>
              </div>
              <p style={{ fontSize: 12.5, color: "var(--dim)", lineHeight: 1.6 }}>{law.desc}</p>
              <p style={{ fontSize: 11, color: "var(--gold)", marginTop: 10 }}>› {law.sections?.length} key sections · Click to explore</p>
            </div>
          ))}
        </div>
      )}

      {sel && (
        <div className="ovrl" onClick={e => e.target === e.currentTarget && setSel(null)}>
          <div className="mbox">
            <button className="mcls" onClick={() => setSel(null)}><i className="fas fa-times" /></button>
            <h3 style={{ fontFamily: "var(--serif)", fontSize: 24, color: "var(--gold-l)", marginBottom: 6 }}>{selName}</h3>
            <p style={{ fontSize: 12, color: "var(--dim)", marginBottom: 14 }}>{sel.full}</p>
            <span className={`tag t${sel.cat}`} style={{ marginBottom: 16, display: "inline-block" }}>{sel.cat}</span>
            <div className="ibox">{sel.desc}</div>
            <div style={{ marginTop: 16 }}>
              <p style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 1.5, color: "var(--gold)", marginBottom: 10 }}>Key Sections</p>
              {sel.sections?.map((s, i) => (
                <div key={i} style={{ display: "flex", gap: 10, padding: "6px 0", borderBottom: "1px solid var(--border)" }}>
                  <span style={{ color: "var(--gold)" }}>›</span>
                  <span style={{ fontSize: 13 }}>{s}</span>
                </div>
              ))}
            </div>
            <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
              <button className="btn btn-g" onClick={() => { nav(`/search?category=${sel.cat}`); setSel(null); }}><i className="fas fa-search" /> Search Cases</button>
              <button className="btn btn-o" onClick={() => { nav(`/rag?q=${encodeURIComponent(selName)}`); setSel(null); }}><i className="fas fa-database" /> Deep Search</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

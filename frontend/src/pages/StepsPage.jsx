import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { chatAPI } from "../services/api";

const EXAMPLES = [
  "Landlord not returning security deposit",
  "Online UPI fraud happened to me",
  "Salary not paid for 3 months",
  "Defective product company refusing refund",
];

// Suggest a document template based on the matched problem
function docFor(title = "") {
  const t = title.toLowerCase();
  if (/consumer|product|refund|builder|rera/.test(t)) return ["complaint", "Consumer complaint"];
  if (/fraud|cyber|theft|accident|harass|violence|assault|crime/.test(t)) return ["fir", "FIR draft"];
  return ["notice", "Legal notice"];
}

export default function StepsPage({ lang = "en" }) {
  const loc = useLocation();
  const nav = useNavigate();
  const [query, setQuery] = useState(loc.state?.query || "");
  const [data, setData] = useState(loc.state?.data || null);
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState({});

  useEffect(() => { setDone({}); }, [data]);

  const run = async (q = query) => {
    if (!q.trim() || loading) return;
    setQuery(q);
    setLoading(true);
    try {
      const res = await chatAPI(q, "rag", lang);
      setData(res);
    } catch {
      toast.error("Can't reach the PocketLaw server");
    }
    setLoading(false);
  };

  const a = data?.analysis;
  const steps = a?.steps || [];
  const count = steps.filter((_, i) => done[i]).length;
  const pct = steps.length ? Math.round((count / steps.length) * 100) : 0;
  const [docTab, docLabel] = docFor(a?.title);

  return (
    <div className="page">
      <div className="shdr">
        <div className="stag"><i className="fas fa-list-check" /> Interactive Legal Survival Steps</div>
        <h2 className="stit">Know exactly <em>what to do next</em></h2>
        <p className="ssub">Describe your situation and get a practical checklist — immediate actions, your rights, the laws involved and who to contact.</p>
      </div>

      {/* Problem input */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <input style={{ flex: 1, minWidth: 220 }} placeholder="Describe your problem, e.g. my employer hasn't paid my salary…" value={query}
            onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === "Enter" && run()} />
          <button className="btn btn-g" onClick={() => run()} disabled={loading}>
            {loading ? <><span className="ldr"><span /><span /><span /></span> Building…</> : <><i className="fas fa-wand-magic-sparkles" /> Get my steps</>}
          </button>
        </div>
        {!data && (
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 14 }}>
            {EXAMPLES.map(e => <button key={e} className="chip" onClick={() => run(e)}>{e}</button>)}
          </div>
        )}
      </div>

      {!a && !loading && (
        <div className="card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <div style={{ width: 64, height: 64, borderRadius: 18, background: "var(--accent-soft)", color: "var(--accent)", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 26, marginBottom: 14 }}>
            <i className="fas fa-route" />
          </div>
          <h3 style={{ fontFamily: "var(--serif)", fontSize: 22, marginBottom: 6 }}>Your checklist will appear here</h3>
          <p style={{ color: "var(--muted)", maxWidth: 440, margin: "0 auto" }}>Type your problem above or pick an example. You can tick off each step as you complete it.</p>
        </div>
      )}

      {a && (
        <div className="steps-layout">
          {/* Checklist */}
          <div className="card">
            <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 18, flexWrap: "wrap" }}>
              <div className="res-ico">{a.icon}</div>
              <div style={{ flex: 1, minWidth: 180 }}>
                <div style={{ fontFamily: "var(--serif)", fontSize: 22, fontWeight: 600, lineHeight: 1.2 }}>{a.title}</div>
                <div style={{ fontSize: 13, color: "var(--muted)" }}>{query && <>For: "{query}"</>}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontFamily: "var(--serif)", fontSize: 26, fontWeight: 600, color: pct === 100 ? "var(--ok)" : "var(--ink)" }}>{count}/{steps.length}</div>
                <div style={{ fontSize: 12, color: "var(--muted)" }}>steps done</div>
              </div>
            </div>
            <div className="pbar" style={{ marginBottom: 20 }}><div className="pfill" style={{ width: `${pct}%`, background: pct === 100 ? "var(--ok)" : "var(--accent)" }} /></div>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {steps.map((s, i) => (
                <button key={i} className={`check-item${done[i] ? " done" : ""}`} onClick={() => setDone(d => ({ ...d, [i]: !d[i] }))}>
                  <span className="box">{done[i] && <i className="fas fa-check" />}</span>
                  <span>
                    <span className="sn">{i === 0 ? "Do this first" : `Step ${i + 1}`}</span>
                    <span className="txt">{s}</span>
                  </span>
                </button>
              ))}
            </div>

            {pct === 100 && (
              <div className="ibox ok" style={{ marginTop: 18, marginBottom: 0 }}>
                <i className="fas fa-circle-check" /> Great work — you've completed every step. If the issue isn't resolved, consider free legal aid (NALSA 15100) or a lawyer.
              </div>
            )}

            <hr className="dvd" />
            <div className="res-h"><i className="fas fa-shield-halved" />Your legal rights</div>
            <ul className="blist ok">{(a.rights || []).map((r, i) => <li key={i}>{r}</li>)}</ul>
          </div>

          {/* Side panel */}
          <div className="side-sticky">
            <div className="card">
              <div className="res-h"><i className="fas fa-phone" />Who to contact</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {(a.helplines || []).map((h, i) => <div key={i} className="help-chip"><i className="fas fa-phone" />{h}</div>)}
                <div className="help-chip" style={{ background: "var(--surface2)", color: "var(--ink2)" }}><i className="fas fa-hands-holding" />Free legal aid (NALSA): 15100</div>
              </div>
            </div>

            <div className="card">
              <div className="res-h"><i className="fas fa-scale-balanced" />Laws involved</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {(a.laws || []).map((l, i) => <div key={i} className="law-item"><i className="fas fa-book" /><span>{l}</span></div>)}
              </div>
            </div>

            <div className="card" style={{ background: "var(--ink)", borderColor: "var(--ink)", color: "var(--bg)" }}>
              <div style={{ fontFamily: "var(--serif)", fontSize: 18, fontWeight: 600, marginBottom: 4, color: "var(--bg)" }}>Need a document?</div>
              <p style={{ fontSize: 13.5, opacity: .8, marginBottom: 14 }}>Generate a ready-to-edit {docLabel.toLowerCase()} for this situation.</p>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <button className="btn btn-g btn-sm" onClick={() => nav(`/documents?tab=${docTab}`)}><i className="fas fa-file-signature" /> {docLabel}</button>
                <button className="btn btn-sm" style={{ background: "rgba(255,255,255,.12)", color: "var(--bg)" }} onClick={() => nav("/documents")}>All templates</button>
              </div>
            </div>
          </div>
        </div>
      )}

      <p style={{ textAlign: "center", fontSize: 12.5, color: "var(--muted)", marginTop: 28 }}>
        <i className="fas fa-circle-info" /> These steps are general guidance, not legal advice. For serious matters, consult a lawyer.
      </p>
    </div>
  );
}

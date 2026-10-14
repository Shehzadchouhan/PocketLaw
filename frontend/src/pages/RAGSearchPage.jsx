import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { ragAPI, webSearchAPI } from "../services/api";
import toast from "react-hot-toast";

export default function RAGSearchPage() {
  const [sp] = useSearchParams();
  const [query, setQuery] = useState(sp.get("q") || "");
  const [category, setCategory] = useState("");
  const [results, setResults] = useState(null);
  const [webResults, setWebResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [webLoading, setWebLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("rag");

  useEffect(() => { if (sp.get("q")) doSearch(sp.get("q")); }, []);

  const doSearch = async (q = query) => {
    if (!q.trim()) return;
    setLoading(true);
    try {
      const data = await ragAPI(q, category);
      setResults(data);
      toast.success(`Found ${data.total} relevant chunks`);
    } catch { toast.error("Backend not connected"); }
    setLoading(false);
  };

  const doWebSearch = async () => {
    if (!query.trim()) return;
    setWebLoading(true);
    try {
      const data = await webSearchAPI(query);
      setWebResults(data.results || []);
      toast.success(`${data.results?.length || 0} web results`);
    } catch { toast.error("Web search failed"); }
    setWebLoading(false);
  };

  return (
    <div className="page">
      <div className="shdr">
        <div className="stag"><i className="fas fa-database" /> Deep Search</div>
        <h2 className="stit">Search inside <em>Supreme Court judgments</em></h2>
        <p className="ssub">PocketLaw's retrieval engine scans thousands of passages from real judgments to find the text most relevant to your question.</p>
      </div>

      {/* Architecture diagram */}
      <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 16, padding: 24, marginBottom: 32, display: "flex", gap: 0, alignItems: "center", justifyContent: "center", flexWrap: "wrap" }}>
        {[
          { icon: "👤", label: "User Query", sub: "Natural language" },
          { arrow: true },
          { icon: "🔢", label: "TF-IDF Vectorizer", sub: "15,000 features" },
          { arrow: true },
          { icon: "🗄️", label: "Vector Index", sub: "2,290 chunks" },
          { arrow: true },
          { icon: "📊", label: "Cosine Similarity", sub: "Top-K retrieval" },
          { arrow: true },
          { icon: "🤖", label: "RAG Answer", sub: "Extractive QA" },
        ].map((step, i) => step.arrow ? (
          <div key={i} style={{ fontSize: 20, color: "var(--gold)", margin: "0 8px" }}>→</div>
        ) : (
          <div key={i} style={{ textAlign: "center", padding: "8px 16px" }}>
            <div style={{ fontSize: 28, marginBottom: 4 }}>{step.icon}</div>
            <div style={{ fontSize: 12, fontWeight: 600, color: "var(--text)" }}>{step.label}</div>
            <div style={{ fontSize: 10, color: "var(--dim)" }}>{step.sub}</div>
          </div>
        ))}
      </div>

      {/* Search form */}
      <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 16, padding: 24, marginBottom: 24 }}>
        <div className="g2" style={{ marginBottom: 16 }}>
          <div className="fg">
            <label>Your Query</label>
            <input placeholder="e.g. consumer refund rights, property dispute Section 138..." value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === "Enter" && doSearch()} />
          </div>
          <div className="fg">
            <label>Filter by Category (optional)</label>
            <select value={category} onChange={e => setCategory(e.target.value)} className="sel">
              <option value="">All Categories</option>
              <option>Criminal</option><option>Consumer</option><option>Property</option>
              <option>Family</option><option>Labour</option><option>Civil</option><option>Constitutional</option>
            </select>
          </div>
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <button className="btn btn-g" onClick={() => doSearch()} disabled={loading}>
            {loading ? <><div className="ldr" style={{ transform: "scale(.7)" }}><span /><span /><span /></div> Searching...</> : <><i className="fas fa-search" /> Search judgments</>}
          </button>
          <button className="btn btn-info" onClick={doWebSearch} disabled={webLoading}>
            {webLoading ? "Searching web..." : <><i className="fas fa-globe" /> Also Search Web</>}
          </button>
          <button className="btn btn-o" onClick={() => { setQuery(""); setResults(null); setWebResults([]); }}>Clear</button>
        </div>

        {/* Sample queries */}
        <div style={{ marginTop: 16 }}>
          <p style={{ fontSize: 13, color: "var(--muted)", marginBottom: 8 }}>Try these queries:</p>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {["cheque bounce Section 138", "motor accident compensation MACT", "consumer deficiency of service", "property encroachment trespass", "bail conditions criminal appeal", "domestic violence protection order"].map(q => (
              <button key={q} onClick={() => { setQuery(q); doSearch(q); }} className="chip">{q}</button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {(results || webResults.length > 0) && (
        <>
          <div className="tabs">
            <button className={`tab${activeTab === "rag" ? " act" : ""}`} onClick={() => setActiveTab("rag")}>📚 PDF RAG Results {results ? `(${results.total})` : ""}</button>
            <button className={`tab${activeTab === "web" ? " act" : ""}`} onClick={() => setActiveTab("web")}>🌐 Web Results {webResults.length > 0 ? `(${webResults.length})` : ""}</button>
          </div>

          {activeTab === "rag" && results && (
            <div>
              {/* Answer */}
              <div className="card" style={{ marginBottom: 20 }}>
                <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 1.5, color: "var(--ok)", marginBottom: 12, fontWeight: 600 }}>🤖 RAG Answer (Extracted from SC Judgments)</div>
                <div style={{ background: "var(--ok-soft)", border: "1px solid transparent", borderRadius: 10, padding: "14px 18px", fontSize: 13.5, lineHeight: 1.8, color: "var(--text)" }}>
                  {results.answer || "No specific matching text found. Try different keywords."}
                </div>
                <div style={{ marginTop: 12, display: "flex", gap: 10 }}>
                  <span style={{ fontSize: 11, color: "var(--dim)" }}>Query: <strong style={{ color: "var(--text)" }}>{results.query}</strong></span>
                  <span className="tag tok" style={{ fontSize: 10 }}>{results.total} chunks found</span>
                </div>
              </div>

              {/* Source chunks */}
              <h3 style={{ fontFamily: "var(--serif)", fontSize: 22, marginBottom: 16 }}>Source passages from judgments</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {results.chunks.map((chunk, i) => (
                  <div key={i} className="card" style={{ borderLeft: `3px solid ${chunk.score > 0.1 ? "var(--ok)" : "var(--border)"}` }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                        <span className={`tag t${chunk.case_type}`}>{chunk.case_type}</span>
                        <span style={{ fontSize: 12, color: "var(--dim)" }}>{chunk.year || "N/A"}</span>
                        <span className={`tag ${chunk.outcome === "Allowed" ? "tok" : chunk.outcome === "Dismissed" ? "terr" : "twarn"}`} style={{ fontSize: 10 }}>{chunk.outcome}</span>
                      </div>
                      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                        <span style={{ fontSize: 11, padding: "3px 10px", background: "var(--ok-soft)", border: "1px solid transparent", color: "var(--ok)", borderRadius: 20 }}>
                          Relevance: {(chunk.score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    <p style={{ fontSize: 13, color: "var(--text)", lineHeight: 1.7, marginBottom: 10 }}>{chunk.text}</p>
                    <p style={{ fontSize: 10.5, color: "var(--dim)", fontFamily: "monospace" }}>Source: {chunk.source?.substring(0, 60)}...</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "web" && (
            <div>
              {webResults.length === 0 ? (
                <div style={{ textAlign: "center", color: "var(--dim)", padding: 40 }}>
                  <p>Click "Also Search Web" button to get live web results</p>
                </div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                  {webResults.map((r, i) => (
                    <div key={i} className="card" style={{ borderLeft: "3px solid var(--info)" }}>
                      <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                        <span style={{ fontSize: 20, flexShrink: 0 }}>🌐</span>
                        <div>
                          {r.url && <a href={r.url} target="_blank" rel="noopener noreferrer" style={{ color: "var(--info)", textDecoration: "none", fontSize: 13, fontWeight: 500, display: "block", marginBottom: 6 }}>{r.url}</a>}
                          <p style={{ fontSize: 13, color: "var(--text)", lineHeight: 1.7 }}>{r.snippet}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

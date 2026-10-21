import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getChatsAPI, clearChatsAPI, dlConsultation } from "../services/api";
import toast from "react-hot-toast";
import { translate } from "../i18n";

export default function ChatHistoryPage({ lang = "en" }) {
  const t = (text) => translate(lang, text);
  const [chats, setChats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [catFilter, setCatFilter] = useState("");
  const [exportingId, setExportingId] = useState(null);
  const nav = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("jl_token");
    if (!token) { nav("/login"); return; }
    loadChats();
  }, []);

  const loadChats = async () => {
    try {
      const data = await getChatsAPI();
      setChats(data);
    } catch (err) {
      if (err?.response?.status === 401) nav("/login");
      else toast.error("Failed to load chat history");
    }
    setLoading(false);
  };

  const handleClear = async () => {
    if (!window.confirm("Clear all chat history?")) return;
    try {
      await clearChatsAPI();
      setChats({ messages: [], sessions: [] });
      toast.success("Chat history cleared");
    } catch (err) {
      toast.error("Failed to clear");
    }
  };

  const handleRevisit = (question) => {
    if (!question) return;
    nav(`/?q=${encodeURIComponent(question)}`);
  };

  const handleExportPDF = async (msg) => {
    try {
      setExportingId(msg.id);
      toast.loading("Generating consultation PDF...", { id: `pdf-${msg.id}` });
      await dlConsultation({
        question: msg.message,
        message: msg.message,
        response: msg.response_preview || msg.ai_response,
        category: msg.category || "General Legal Matter",
        timestamp: msg.timestamp,
        user_name: user?.name || user?.email || "Verified Citizen"
      });
      toast.success("Consultation PDF downloaded", { id: `pdf-${msg.id}` });
    } catch (err) {
      toast.error("Failed to generate PDF report", { id: `pdf-${msg.id}` });
    } finally {
      setExportingId(null);
    }
  };

  const user = JSON.parse(localStorage.getItem("jl_user") || "{}");

  if (loading) {
    return (
      <div className="page" style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "60vh" }}>
        <span className="ldr"><span/><span/><span/></span>
      </div>
    );
  }

  const messages = chats?.messages || [];

  const filteredMessages = messages.filter(m => {
    const matchesSearch = !searchTerm || 
      (m.message && m.message.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (m.response_preview && m.response_preview.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCat = !catFilter || (m.category && m.category.toLowerCase() === catFilter.toLowerCase());
    return matchesSearch && matchesCat;
  });

  return (
    <div className="page" style={{ maxWidth: 840, margin: "0 auto" }}>
      <div className="shdr" style={{ marginBottom: 36 }}>
        <div className="stag"><i className="fas fa-clock-rotate-left" /> {t("Your consultations")}</div>
        <h1 className="stit">{t("Chat History")}</h1>
        <p style={{ color: "var(--dim)", marginTop: 12, fontSize: 14 }}>
          {messages.length} {t("legal consultations saved")} · {user?.name || user?.email || "User"}
        </p>
      </div>

      {messages.length === 0 ? (
        <div className="card" style={{ padding: 48, textAlign: "center" }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>💬</div>
          <h3 style={{ fontFamily: "var(--serif)", marginBottom: 8 }}>{t("No conversations yet")}</h3>
          <p style={{ color: "var(--dim)", fontSize: 14, marginBottom: 24 }}>
            {t("Questions you ask on the Law Matcher will appear here with instant revisit and PDF export options")}
          </p>
          <button className="btn btn-g" onClick={() => nav("/")}><i className="fas fa-magnifying-glass" /> Type your problem</button>
        </div>
      ) : (
        <>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
            <div style={{ display: "flex", gap: 8, flex: 1, minWidth: 260 }}>
              <input
                style={{ flex: 1, fontSize: 13 }}
                placeholder={t("Search consultations...")}
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
              {searchTerm && (
                <button className="btn btn-o btn-sm" onClick={() => setSearchTerm("")}>
                  {t("Clear")}
                </button>
              )}
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button className="btn btn-danger btn-sm" onClick={handleClear} title="Clear all consultation history">
                <i className="fas fa-trash" /> {t("Clear all")}
              </button>
            </div>
          </div>

          {filteredMessages.length === 0 ? (
            <div className="card" style={{ padding: 32, textAlign: "center", color: "var(--dim)" }}>
              {t("No conversations matching")} "{searchTerm}"
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {[...filteredMessages].reverse().map((msg) => (
                <div key={msg.id} className="card" style={{ padding: 22 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12, flexWrap: "wrap", gap: 8 }}>
                    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <span className="tag" style={{ background: "var(--accent-soft)", color: "var(--accent-d)", fontWeight: 600 }}>
                        {msg.category || "General Legal"}
                      </span>
                      <span className="tag" style={{ fontSize: 11 }}>
                        <i className="fas fa-robot" style={{ marginRight: 4 }} />
                        {t(msg.mode || "both")}
                      </span>
                    </div>
                    <span style={{ fontSize: 11.5, color: "var(--dim)" }}>
                      <i className="fas fa-clock" style={{ marginRight: 4 }} />
                      {new Date(msg.timestamp).toLocaleDateString({ hi: "hi-IN", pa: "pa-IN" }[lang] || "en-IN", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>

                  {/* Clickable Query Section */}
                  <div
                    onClick={() => handleRevisit(msg.message)}
                    style={{
                      cursor: "pointer",
                      padding: "10px 14px",
                      background: "var(--bg)",
                      borderRadius: 8,
                      border: "1px solid var(--border)",
                      marginBottom: 12,
                      transition: "all 0.15s ease"
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = "var(--gold)";
                      e.currentTarget.style.background = "var(--bg-card)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = "var(--border)";
                      e.currentTarget.style.background = "var(--bg)";
                    }}
                    title="Click to revisit and re-run this query in Law Matcher"
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                      <strong style={{ fontSize: 12, color: "var(--gold)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                        <i className="fas fa-user" style={{ marginRight: 5 }} /> {t("Your Query")}
                      </strong>
                      <span style={{ fontSize: 11, color: "var(--gold)", display: "flex", alignItems: "center", gap: 4 }}>
                        <i className="fas fa-rotate-left" /> {t("Revisit")} ↗
                      </span>
                    </div>
                    <p style={{ fontSize: 13.5, margin: 0, lineHeight: 1.5, fontWeight: 500, color: "var(--ink)" }}>
                      {msg.message}
                    </p>
                  </div>

                  {/* AI Legal Opinion Preview */}
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
                      <strong style={{ fontSize: 12, color: "var(--accent)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                        <i className="fas fa-scale-balanced" style={{ marginRight: 5 }} /> {t("AI Legal Guidance")}
                      </strong>
                    </div>
                    <p style={{ fontSize: 13, margin: 0, lineHeight: 1.55, color: "var(--dim)", whiteSpace: "pre-line" }}>
                      {msg.response_preview || "Legal analysis and statutory guidance recorded."}
                    </p>
                  </div>

                  {/* Card Action Buttons: Revisit Query & Export PDF */}
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap", borderTop: "1px solid var(--border)", paddingTop: 12, justifyContent: "flex-end" }}>
                    <button
                      className="btn btn-g btn-sm"
                      onClick={() => handleRevisit(msg.message)}
                      title="Revisit and re-run this inquiry in the Law Matcher"
                    >
                      <i className="fas fa-rotate-left" /> {t("Revisit Query")}
                    </button>
                    <button
                      className="btn btn-o btn-sm"
                      onClick={() => handleExportPDF(msg)}
                      disabled={exportingId === msg.id}
                      title="Export this consultation as a court-style PDF document"
                    >
                      <i className="fas fa-file-pdf" style={{ color: "var(--gold)" }} />
                      {exportingId === msg.id ? ` ${t("Generating PDF...")}` : ` ${t("Export PDF")}`}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

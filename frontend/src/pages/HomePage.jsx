import React, { useState, useRef, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { chatAPI, saveChatAPI } from "../services/api";

const QUICK = [
  "Landlord not returning security deposit",
  "Online UPI fraud happened to me",
  "Workplace sexual harassment",
  "Road accident driver fled",
  "Defective product company refusing refund",
  "Wrongful termination from job",
  "Builder not delivering flat - RERA",
  "Divorce and child custody issue"
];

const LANG = {
  en: {
    pill: "AI Law Matcher",
    t1: "Type your problem.",
    t2: "Get your legal rights.",
    sub: "Describe what happened in simple words. PocketLaw finds the Indian laws that apply, explains your rights and shows you what to do next.",
    ph: "e.g. My landlord is not returning my security deposit…",
    how: [["Describe", "Tell us your problem in everyday language — no legal terms needed."], ["Match laws", "AI finds relevant Acts, sections and similar Supreme Court cases."], ["Take action", "Follow survival steps and generate legal documents."]],
    welcome: "Hi! I'm PocketLaw 👋\n\nTell me your legal problem in simple words — for example, \"my employer hasn't paid my salary for 3 months\".\n\nI'll match it to the relevant Indian laws, explain your rights, and give you step-by-step guidance."
  },
  hi: {
    pill: "AI कानून मैचर",
    t1: "अपनी समस्या लिखें।",
    t2: "अपने कानूनी अधिकार जानें।",
    sub: "आसान शब्दों में बताएं कि क्या हुआ। PocketLaw लागू भारतीय कानून खोजता है, आपके अधिकार समझाता है और आगे के कदम बताता है।",
    ph: "जैसे: मकान मालिक मेरी सिक्योरिटी डिपॉज़िट वापस नहीं कर रहा…",
    how: [["बताएं", "अपनी समस्या रोज़मर्रा की भाषा में बताएं।"], ["कानून मिलाएं", "AI संबंधित अधिनियम, धाराएं और समान मामले खोजता है।"], ["कार्रवाई करें", "कदमों का पालन करें और कानूनी दस्तावेज़ बनाएं।"]],
    welcome: "नमस्ते! मैं PocketLaw हूँ 👋\n\nअपनी कानूनी समस्या आसान शब्दों में बताएं। मैं संबंधित भारतीय कानून, आपके अधिकार और चरण-दर-चरण मार्गदर्शन दूँगा।"
  },
  pa: {
    pill: "AI ਕਾਨੂੰਨ ਮੈਚਰ",
    t1: "ਆਪਣੀ ਸਮੱਸਿਆ ਲਿਖੋ।",
    t2: "ਆਪਣੇ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ ਜਾਣੋ।",
    sub: "ਸੌਖੇ ਸ਼ਬਦਾਂ ਵਿੱਚ ਦੱਸੋ ਕਿ ਕੀ ਹੋਇਆ। PocketLaw ਲਾਗੂ ਭਾਰਤੀ ਕਾਨੂੰਨ ਲੱਭਦਾ ਹੈ, ਤੁਹਾਡੇ ਅਧਿਕਾਰ ਸਮਝਾਉਂਦਾ ਹੈ ਅਤੇ ਅਗਲੇ ਕਦਮ ਦੱਸਦਾ ਹੈ।",
    ph: "ਜਿਵੇਂ: ਮਕਾਨ ਮਾਲਕ ਮੇਰੀ ਸਕਿਓਰਿਟੀ ਡਿਪਾਜ਼ਿਟ ਵਾਪਸ ਨਹੀਂ ਕਰ ਰਿਹਾ…",
    how: [["ਦੱਸੋ", "ਆਪਣੀ ਸਮੱਸਿਆ ਆਮ ਭਾਸ਼ਾ ਵਿੱਚ ਦੱਸੋ।"], ["ਕਾਨੂੰਨ ਮਿਲਾਓ", "AI ਸੰਬੰਧਿਤ ਐਕਟ, ਧਾਰਾਵਾਂ ਅਤੇ ਮਿਲਦੇ ਕੇਸ ਲੱਭਦਾ ਹੈ।"], ["ਕਾਰਵਾਈ ਕਰੋ", "ਕਦਮਾਂ ਦੀ ਪਾਲਣਾ ਕਰੋ ਅਤੇ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼ ਬਣਾਓ।"]],
    welcome: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ PocketLaw ਹਾਂ 👋\n\nਆਪਣੀ ਕਾਨੂੰਨੀ ਸਮੱਸਿਆ ਸੌਖੇ ਸ਼ਬਦਾਂ ਵਿੱਚ ਦੱਸੋ। ਮੈਂ ਸੰਬੰਧਿਤ ਕਾਨੂੰਨ, ਤੁਹਾਡੇ ਅਧਿਕਾਰ ਅਤੇ ਕਦਮ-ਦਰ-ਕਦਮ ਮਾਰਗਦਰਸ਼ਨ ਦਿਆਂਗਾ।"
  },
  ur: {
    pill: "AI قانون میچر",
    t1: "اپنا مسئلہ لکھیں۔",
    t2: "اپنے قانونی حقوق جانیں۔",
    sub: "آسان الفاظ میں بتائیں کہ کیا ہوا۔ PocketLaw متعلقہ بھارتی قوانین تلاش کرتا ہے، آپ کے حقوق سمجھاتا ہے اور اگلے اقدامات بتاتا ہے۔",
    ph: "مثلاً: مالک مکان میری سیکیورٹی ڈپازٹ واپس نہیں کر رہا…",
    how: [["بتائیں", "اپنا مسئلہ روزمرہ زبان میں بتائیں۔"], ["قانون ملائیں", "AI متعلقہ ایکٹ، دفعات اور ملتے جلتے مقدمات تلاش کرتا ہے۔"], ["عمل کریں", "اقدامات پر عمل کریں اور قانونی دستاویزات بنائیں۔"]],
    welcome: "السلام علیکم! میں PocketLaw ہوں 👋\n\nاپنا قانونی مسئلہ آسان الفاظ میں بتائیں۔ میں متعلقہ قوانین، آپ کے حقوق اور مرحلہ وار رہنمائی دوں گا۔"
  },
  hx: {
    pill: "AI Law Matcher",
    t1: "Apni problem likhiye.",
    t2: "Apne legal rights jaaniye.",
    sub: "Simple words mein batayiye kya hua. PocketLaw lagoo Indian laws dhoondhta hai, aapke rights samjhata hai aur next steps batata hai.",
    ph: "Jaise: Landlord meri security deposit wapas nahi kar raha…",
    how: [["Batayiye", "Apni problem roz ki bhasha mein batayiye."], ["Laws match", "AI relevant Acts, sections aur similar cases dhoondhta hai."], ["Action lijiye", "Survival steps follow kariye aur documents banaiye."]],
    welcome: "Namaste! Main PocketLaw hoon 👋\n\nApni legal problem simple words mein batayiye. Main relevant laws, aapke rights aur step-by-step guidance dunga."
  }
};

const UI = {
  en: { aiLabel: "AI Law Matcher result", ragSec: "From Supreme Court judgments", webSec: "Live web results", lawSec: "Matched laws & sections", rgtSec: "Your legal rights", stpSec: "Survival steps", prdSec: "Case insight", simSec: "Similar Supreme Court judgments", hlpSec: "Helplines & contacts", actSec: "What you can do next", noRag: "No specific matching text found in the judgment database.", hide: "Hide", show: "Show", srcChunks: "source passages", webResults: "web results", cases: "cases", successRate: "Success rate", duration: "Duration", riskLevel: "Risk level", scCases: "SC cases", readAloud: "Read aloud", deepRag: "Deep search", firDraft: "FIR draft", legalNotice: "Legal notice", complaint: "Consumer complaint", openSteps: "Open survival checklist", analysisComplete: "Here's what I found for:", chunks: "passages", scCasesFull: "SC cases", searching: "Matching laws for your problem…", offline: "⚠️ Can't reach the PocketLaw server. Start the backend:\n\ncd backend\npython app.py", modes: ["Judgments only", "Web only", "Judgments + Web"], online: "Online", messages: "messages" },
  hi: { aiLabel: "AI कानून मैचर परिणाम", ragSec: "सर्वोच्च न्यायालय निर्णयों से", webSec: "लाइव वेब परिणाम", lawSec: "मिलते कानून और धाराएं", rgtSec: "आपके कानूनी अधिकार", stpSec: "सर्वाइवल कदम", prdSec: "केस जानकारी", simSec: "समान सर्वोच्च न्यायालय निर्णय", hlpSec: "हेल्पलाइन और संपर्क", actSec: "आगे आप क्या कर सकते हैं", noRag: "निर्णय डेटाबेस में कोई विशिष्ट मिलान पाठ नहीं मिला।", hide: "छुपाएं", show: "दिखाएं", srcChunks: "स्रोत अंश", webResults: "वेब परिणाम", cases: "मामले", successRate: "सफलता दर", duration: "अवधि", riskLevel: "जोखिम स्तर", scCases: "SC मामले", readAloud: "ज़ोर से पढ़ें", deepRag: "गहन खोज", firDraft: "FIR ड्राफ्ट", legalNotice: "कानूनी नोटिस", complaint: "उपभोक्ता शिकायत", openSteps: "सर्वाइवल चेकलिस्ट खोलें", analysisComplete: "इसके लिए परिणाम:", chunks: "अंश", scCasesFull: "SC मामले", searching: "आपकी समस्या के लिए कानून खोजे जा रहे हैं…", modes: ["केवल निर्णय", "केवल वेब", "निर्णय + वेब"], online: "ऑनलाइन", messages: "संदेश" },
  pa: { aiLabel: "AI ਕਾਨੂੰਨ ਮੈਚਰ ਨਤੀਜਾ", ragSec: "ਸੁਪਰੀਮ ਕੋਰਟ ਦੇ ਫ਼ੈਸਲਿਆਂ ਤੋਂ", webSec: "ਲਾਈਵ ਵੈੱਬ ਨਤੀਜੇ", lawSec: "ਮਿਲਦੇ ਕਾਨੂੰਨ ਅਤੇ ਧਾਰਾਵਾਂ", rgtSec: "ਤੁਹਾਡੇ ਕਾਨੂੰਨੀ ਅਧਿਕਾਰ", stpSec: "ਸਰਵਾਈਵਲ ਕਦਮ", prdSec: "ਕੇਸ ਜਾਣਕਾਰੀ", simSec: "ਮਿਲਦੇ ਸੁਪਰੀਮ ਕੋਰਟ ਫ਼ੈਸਲੇ", hlpSec: "ਹੈਲਪਲਾਈਨ ਅਤੇ ਸੰਪਰਕ", actSec: "ਅੱਗੇ ਤੁਸੀਂ ਕੀ ਕਰ ਸਕਦੇ ਹੋ", noRag: "ਫ਼ੈਸਲਾ ਡੇਟਾਬੇਸ ਵਿੱਚ ਕੋਈ ਖ਼ਾਸ ਮੇਲ ਨਹੀਂ ਮਿਲਿਆ।", hide: "ਲੁਕਾਓ", show: "ਦਿਖਾਓ", srcChunks: "ਸਰੋਤ ਅੰਸ਼", webResults: "ਵੈੱਬ ਨਤੀਜੇ", cases: "ਕੇਸ", successRate: "ਸਫਲਤਾ ਦਰ", duration: "ਮਿਆਦ", riskLevel: "ਜੋਖਮ ਪੱਧਰ", scCases: "SC ਕੇਸ", readAloud: "ਉੱਚੀ ਪੜ੍ਹੋ", deepRag: "ਡੂੰਘੀ ਖੋਜ", firDraft: "FIR ਡਰਾਫਟ", legalNotice: "ਕਾਨੂੰਨੀ ਨੋਟਿਸ", complaint: "ਖਪਤਕਾਰ ਸ਼ਿਕਾਇਤ", openSteps: "ਸਰਵਾਈਵਲ ਚੈੱਕਲਿਸਟ ਖੋਲ੍ਹੋ", analysisComplete: "ਇਸ ਲਈ ਨਤੀਜਾ:", chunks: "ਅੰਸ਼", scCasesFull: "SC ਕੇਸ", searching: "ਤੁਹਾਡੀ ਸਮੱਸਿਆ ਲਈ ਕਾਨੂੰਨ ਲੱਭੇ ਜਾ ਰਹੇ ਹਨ…", modes: ["ਸਿਰਫ਼ ਫ਼ੈਸਲੇ", "ਸਿਰਫ਼ ਵੈੱਬ", "ਫ਼ੈਸਲੇ + ਵੈੱਬ"], online: "ਆਨਲਾਈਨ", messages: "ਸੁਨੇਹੇ" },
  ur: { aiLabel: "AI قانون میچر نتیجہ", ragSec: "سپریم کورٹ کے فیصلوں سے", webSec: "لائیو ویب نتائج", lawSec: "متعلقہ قوانین اور دفعات", rgtSec: "آپ کے قانونی حقوق", stpSec: "سروائیول اقدامات", prdSec: "کیس کی معلومات", simSec: "ملتے جلتے سپریم کورٹ فیصلے", hlpSec: "ہیلپ لائنز اور رابطے", actSec: "آگے آپ کیا کر سکتے ہیں", noRag: "فیصلوں کے ڈیٹابیس میں کوئی مخصوص متن نہیں ملا۔", hide: "چھپائیں", show: "دکھائیں", srcChunks: "ماخذ حصے", webResults: "ویب نتائج", cases: "مقدمات", successRate: "کامیابی کی شرح", duration: "مدت", riskLevel: "خطرے کی سطح", scCases: "SC مقدمات", readAloud: "بلند آواز سے پڑھیں", deepRag: "گہری تلاش", firDraft: "FIR مسودہ", legalNotice: "قانونی نوٹس", complaint: "صارف شکایت", openSteps: "سروائیول چیک لسٹ کھولیں", analysisComplete: "اس کے لیے نتیجہ:", chunks: "حصے", scCasesFull: "SC مقدمات", searching: "آپ کے مسئلے کے لیے قوانین تلاش کیے جا رہے ہیں…", modes: ["صرف فیصلے", "صرف ویب", "فیصلے + ویب"], online: "آن لائن", messages: "پیغامات" },
  hx: { aiLabel: "AI Law Matcher result", ragSec: "Supreme Court judgments se", webSec: "Live web results", lawSec: "Matched laws aur sections", rgtSec: "Aapke qanooni haq", stpSec: "Survival steps", prdSec: "Case insight", simSec: "Similar Supreme Court decisions", hlpSec: "Helplines aur contacts", actSec: "Aage aap kya kar sakte hain", noRag: "Judgment database mein koi specific matching text nahi mila.", hide: "Chhupayein", show: "Dikhayein", srcChunks: "source passages", webResults: "web results", cases: "cases", successRate: "Safalta dar", duration: "Avadhi", riskLevel: "Jokhim", scCases: "SC cases", readAloud: "Zor se padhein", deepRag: "Deep search", firDraft: "FIR draft", legalNotice: "Qanooni notice", complaint: "Consumer complaint", openSteps: "Survival checklist kholein", analysisComplete: "Iske liye result:", chunks: "passages", scCasesFull: "SC cases", searching: "Aapki problem ke liye laws dhoondh rahe hain…", modes: ["Sirf judgments", "Sirf web", "Judgments + Web"], online: "Online", messages: "messages" }
};

const tr = (lang) => (k) => (UI[lang] && UI[lang][k]) || UI.en[k];

function SourceChip({ chunk }) {
  return (
    <div className="src">
      <div className="src-meta">
        <span>{chunk.year || "N/A"} · {chunk.case_type} · {chunk.outcome}</span>
        <span className="tag tok">Score {(chunk.score || 0).toFixed(3)}</span>
      </div>
      <p>{chunk.text.substring(0, 180)}…</p>
    </div>
  );
}

function WebResult({ r }) {
  return (
    <div className="src">
      {r.url && <a href={r.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: 12.5, color: "var(--info)", textDecoration: "none", display: "block", marginBottom: 3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}><i className="fas fa-globe" /> {r.url.substring(0, 70)}…</a>}
      <p>{r.snippet}</p>
    </div>
  );
}

function AnalysisCard({ data, query, lang = "en" }) {
  const nav = useNavigate();
  const t = tr(lang);
  const { analysis, prediction, rag_results, web_results, similar_cases, meta } = data;
  const informational = meta?.informational || ["law_definition", "legal_case"].includes(data.detected_problem);
  const showCaseResearch = !informational;
  const pc = prediction.success_rate >= 70 ? "var(--ok)" : prediction.success_rate >= 50 ? "var(--accent)" : "var(--err)";
  const [showRag, setShowRag] = useState(false);
  const [showWeb, setShowWeb] = useState(false);
  const [showSim, setShowSim] = useState(false);

  return (
    <div className="res">
      <div className="res-head">
        <div className="res-ico">{analysis.icon}</div>
        <div style={{ flex: 1, minWidth: 160 }}>
          <div className="res-title">{analysis.title}</div>
          <div className="res-sub">{t("aiLabel")}</div>
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          <span className="tag tok"><i className="fas fa-database" /> RAG</span>
          {web_results?.length > 0 && <span className="tag" style={{ background: "var(--info-soft)", color: "var(--info)" }}><i className="fas fa-globe" /> Web</span>}
        </div>
      </div>

      {data.gemini_answer && <div className="res-ai">{data.gemini_answer.replace(/\*\*/g, "")}</div>}

      {/* Laws */}
      <div className="res-sec">
        <div className="res-h"><i className="fas fa-scale-balanced" />{t("lawSec")}</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(230px,1fr))", gap: 8 }}>
          {analysis.laws.map((l, i) => <div key={i} className="law-item"><i className="fas fa-book" /><span>{l}</span></div>)}
        </div>
      </div>

      {/* Rights + Steps */}
      <div className="res-grid">
        <div className="res-sec">
          <div className="res-h"><i className="fas fa-shield-halved" />{t("rgtSec")}</div>
          <ul className="blist ok">{analysis.rights.map((r, i) => <li key={i}>{r}</li>)}</ul>
        </div>
        <div className="res-sec">
          <div className="res-h"><i className="fas fa-list-check" />{t("stpSec")}</div>
          <div className="steps-mini">
            {analysis.steps.map((s, i) => (
              <div key={i} className="step-row"><span className="step-n">{i + 1}</span><span>{s}</span></div>
            ))}
          </div>
        </div>
      </div>

      {/* Helplines */}
      <div className="res-sec">
        <div className="res-h"><i className="fas fa-phone" />{t("hlpSec")}</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {analysis.helplines.map((h, i) => <span key={i} className="chip chip-ok"><i className="fas fa-phone" style={{ fontSize: 11 }} />{h}</span>)}
        </div>
      </div>

      {/* Case insight */}
      {showCaseResearch && (
        <div className="res-sec">
          <div className="res-h"><i className="fas fa-chart-line" />{t("prdSec")}</div>
          <div className="pred">
            {[[t("successRate"), `${prediction.success_rate}%`, pc, prediction.success_rate], [t("duration"), prediction.duration, "var(--ink)", null], [t("riskLevel"), prediction.risk_level, "var(--ink)", null], [t("scCases"), meta.total_cases, "var(--ink)", null]].map(([l, v, c, bar]) => (
              <div key={l} className="k">
                <div className="l">{l}</div>
                <div className="v" style={{ color: c }}>{v}</div>
                {bar != null && <div className="pbar"><div className="pfill" style={{ width: `${bar}%`, background: c }} /></div>}
              </div>
            ))}
          </div>

          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 14 }}>
            <button className="toggle" onClick={() => setShowRag(!showRag)}><i className={`fas fa-chevron-${showRag ? "up" : "down"}`} />{showRag ? t("hide") : t("show")} {rag_results.total_retrieved} {t("srcChunks")}</button>
            <button className="toggle" onClick={() => setShowSim(!showSim)}><i className={`fas fa-chevron-${showSim ? "up" : "down"}`} />{showSim ? t("hide") : t("show")} {similar_cases.length} {t("cases")}</button>
            {web_results?.length > 0 && <button className="toggle" onClick={() => setShowWeb(!showWeb)}><i className={`fas fa-chevron-${showWeb ? "up" : "down"}`} />{showWeb ? t("hide") : t("show")} {web_results.length} {t("webResults")}</button>}
          </div>

          {showRag && (
            <div style={{ marginTop: 10 }}>
              <div className="ibox ok" style={{ fontSize: 13.5, marginBottom: 6 }}><b>{t("ragSec")}:</b> {rag_results.answer || t("noRag")}</div>
              {rag_results.source_chunks.map((c, i) => <SourceChip key={i} chunk={c} />)}
            </div>
          )}
          {showSim && (
            <div style={{ marginTop: 10 }}>
              <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{t("simSec")}</div>
              {similar_cases.map((c, i) => (
                <div key={i} className="src">
                  <div className="src-meta">
                    <span>{c.year} · {c.type}</span>
                    <span className={`tag ${c.outcome === "Allowed" ? "tok" : c.outcome === "Dismissed" ? "terr" : "twarn"}`}>{c.outcome}</span>
                  </div>
                  <p>{c.summary}</p>
                </div>
              ))}
            </div>
          )}
          {showWeb && web_results?.length > 0 && (
            <div style={{ marginTop: 10 }}>
              <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{t("webSec")}</div>
              {web_results.map((r, i) => <WebResult key={i} r={r} />)}
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="res-sec">
        <div className="res-h"><i className="fas fa-bolt" />{t("actSec")}</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <button className="btn btn-g btn-sm" onClick={() => nav("/steps", { state: { data, query } })}><i className="fas fa-list-check" /> {t("openSteps")}</button>
          <button className="btn btn-o btn-sm" onClick={() => nav("/documents?tab=fir")}><i className="fas fa-file-lines" /> {t("firDraft")}</button>
          <button className="btn btn-o btn-sm" onClick={() => nav("/documents?tab=notice")}><i className="fas fa-envelope" /> {t("legalNotice")}</button>
          <button className="btn btn-o btn-sm" onClick={() => nav("/documents?tab=complaint")}><i className="fas fa-gavel" /> {t("complaint")}</button>
          <button className="btn btn-info btn-sm" onClick={() => {
            if ("speechSynthesis" in window) {
              const u2 = new SpeechSynthesisUtterance(`${analysis.title}. Success rate ${prediction.success_rate} percent. ${analysis.steps[0]}`);
              u2.rate = 0.9; window.speechSynthesis.speak(u2);
            }
          }}><i className="fas fa-volume-high" /> {t("readAloud")}</button>
          <button className="btn btn-info btn-sm" onClick={() => nav(`/rag?q=${encodeURIComponent(analysis.title)}`)}><i className="fas fa-database" /> {t("deepRag")}</button>
        </div>
        <p className="res-foot">
          RAG: {meta.rag_chunks} {t("chunks")} · {meta.total_cases} {t("scCasesFull")} · {new Date(meta.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}

export default function HomePage({ lang = "en" }) {
  const lc = LANG[lang] || LANG.en;
  const t = tr(lang);
  const [msgs, setMsgs] = useState([{ id: 0, type: "ai", welcome: true }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showQ, setShowQ] = useState(true);
  const [listening, setListening] = useState(false);
  const [mode, setMode] = useState("both");
  const msgsRef = useRef(null);
  const recRef = useRef(null);
  const taRef = useRef(null);

  useEffect(() => { if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight; }, [msgs, loading]);

  const send = async (txt) => {
    const msg = txt || input.trim();
    if (!msg || loading) return;
    setInput(""); setShowQ(false);
    if (taRef.current) taRef.current.style.height = "auto";
    setMsgs(m => [...m, { id: Date.now(), type: "user", text: msg }]);
    setLoading(true);
    try {
      const data = await chatAPI(msg, mode, lang);
      setMsgs(m => [...m, { id: Date.now() + 1, type: "ai", query: msg, data }]);
      // Save to chat history for signed-in users (guests skip silently)
      if (localStorage.getItem("jl_token")) { try { await saveChatAPI(msg, data, mode); } catch {} }
    } catch {
      setMsgs(m => [...m, { id: Date.now() + 1, type: "ai", text: t("offline") }]);
    }
    setLoading(false);
  };

  const startVoice = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert("Voice input is not supported in this browser"); return; }
    const r = new SR();
    r.lang = { en: "en-IN", hi: "hi-IN", pa: "pa-IN", ur: "ur-PK", hx: "en-IN" }[lang] || "en-IN";
    let finalText = "";
    r.onstart = () => setListening(true);
    r.onresult = e => { finalText = Array.from(e.results).map(x => x[0].transcript).join(""); setInput(finalText); };
    r.onend = () => { setListening(false); if (finalText.trim()) send(finalText.trim()); };
    r.start(); recRef.current = r;
  };

  const modeIcons = ["fa-landmark", "fa-globe", "fa-layer-group"];

  return (
    <div className="container" style={{ paddingBottom: 64 }}>
      {/* Hero */}
      <section className="hero">
        <div className="hero-script">PocketLaw</div>
        <h1>{lc.t1}<em>{lc.t2}</em></h1>
        <div className="hero-rule" />
        <p>{lc.sub}</p>
        <div className="hero-pill"><b>AI</b> {lc.pill} · Indian law in plain language</div>
      </section>

      <div className="matcher">
        {/* Mode selector */}
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 16 }}>
          <div className="seg">
            {["rag", "web", "both"].map((m, i) => (
              <button key={m} className={mode === m ? "act" : ""} onClick={() => setMode(m)}>
                <i className={`fas ${modeIcons[i]}`} /> {t("modes")[i]}
              </button>
            ))}
          </div>
        </div>

        {/* Chatbox */}
        <div className="chatbox">
          <div className="chat-head">
            <div className="chat-av"><i className="fas fa-scale-balanced" /></div>
            <div>
              <div className="chat-title">PocketLaw · AI Law Matcher</div>
              <div className="chat-status">{t("online")} · {t("modes")[["rag", "web", "both"].indexOf(mode)]} · {msgs.length - 1} {t("messages")}</div>
            </div>
          </div>

          <div ref={msgsRef} className="chat-msgs">
            {msgs.map(msg => (
              <div key={msg.id} className={`msg ${msg.type}`}>
                <div className="msg-av">{msg.type === "user" ? <i className="fas fa-user" /> : <i className="fas fa-scale-balanced" />}</div>
                <div className={`bubble${msg.data ? " wide" : ""}`}>
                  {msg.welcome && <p style={{ whiteSpace: "pre-line" }}>{lc.welcome}</p>}
                  {msg.text && <p style={{ whiteSpace: "pre-line" }}>{msg.text}</p>}
                  {msg.data && (
                    <>
                      <p>{t("analysisComplete")} <b>"{msg.query}"</b></p>
                      <AnalysisCard data={msg.data} query={msg.query} lang={lang} />
                    </>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="msg">
                <div className="msg-av"><i className="fas fa-scale-balanced" /></div>
                <div className="bubble" style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div className="ldr"><span /><span /><span /></div>
                  <span style={{ fontSize: 13.5, color: "var(--muted)" }}>{t("searching")}</span>
                </div>
              </div>
            )}
          </div>

          {showQ && (
            <div className="chat-quick">
              {QUICK.map(p => <button key={p} className="chip" onClick={() => send(p)}>{p}</button>)}
            </div>
          )}

          <div className="chat-input">
            <div className="field">
              <textarea ref={taRef} value={input} onChange={e => setInput(e.target.value)} placeholder={lc.ph} rows={1}
                onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
                onInput={e => { e.target.style.height = "auto"; e.target.style.height = Math.min(e.target.scrollHeight, 140) + "px"; }}
              />
              <button className={`mic${listening ? " on" : ""}`} onClick={listening ? () => recRef.current?.stop() : startVoice} title="Voice input" aria-label="Voice input">
                <i className={`fas fa-microphone${listening ? "-slash" : ""}`} />
              </button>
            </div>
            <button className="btn btn-g send" onClick={() => send()} disabled={loading} aria-label="Send">
              <i className="fas fa-paper-plane" />
            </button>
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="how">
        {lc.how.map(([h, p], i) => (
          <div key={h} className="how-step">
            <div className="how-num">{i + 1}</div>
            <div><h4>{h}</h4><p>{p}</p></div>
          </div>
        ))}
      </div>

      {/* Modules */}
      <div className="modules">
        {[
          ["/steps", "fa-list-check", "Legal Survival Steps", "A step-by-step checklist: immediate actions, evidence to collect, your rights and who to contact."],
          ["/documents", "fa-file-signature", "Document Drafting", "Fill a simple form and download a legal notice, FIR draft, affidavit or consumer complaint."],
          ["/laws", "fa-book-open", "Indian Laws Explorer", "Browse key Indian Acts and sections explained in simple language."],
        ].map(([to, ic, h, p]) => (
          <Link key={to} to={to} className="module">
            <div className="mi"><i className={`fas ${ic}`} /></div>
            <h4>{h}</h4>
            <p>{p}</p>
            <span className="go">Open <i className="fas fa-arrow-right" /></span>
          </Link>
        ))}
      </div>

      {listening && (
        <div className="listen">
          <p style={{ fontSize: 14, color: "var(--muted)" }}>Listening… speak now</p>
          <div className="wave">{[0, .1, .2, .3, .4].map(d => <div key={d} style={{ animationDelay: `${d}s` }} />)}</div>
          <p style={{ fontSize: 13.5, color: "var(--ink)" }}>{input || "Describe your legal problem"}</p>
          <button className="btn btn-sm btn-danger" style={{ marginTop: 10 }} onClick={() => recRef.current?.stop()}>Stop</button>
        </div>
      )}
    </div>
  );
}

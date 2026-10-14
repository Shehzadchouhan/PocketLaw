import React, { useState, useEffect, useRef, createContext, useContext } from "react";
import { BrowserRouter as Router, Routes, Route, NavLink, Link, useNavigate, useLocation } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import HomePage from "./pages/HomePage";
import DashboardPage from "./pages/DashboardPage";
import SearchPage from "./pages/SearchPage";
import LawsPage from "./pages/LawsPage";
import DocumentsPage from "./pages/DocumentsPage";
import RAGSearchPage from "./pages/RAGSearchPage";
import StepsPage from "./pages/StepsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ChatHistoryPage from "./pages/ChatHistoryPage";
import ProfilePage from "./pages/ProfilePage";
import "./App.css";

// ── Auth Context ──
export const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

const MAIN_LINKS = [
  ["/", "fa-magnifying-glass", "Type Your Problem"],
  ["/steps", "fa-list-check", "Survival Steps"],
  ["/documents", "fa-file-signature", "Documents"],
  ["/laws", "fa-book-open", "Laws"],
];

const MORE_LINKS = [
  ["/search", "fa-gavel", "Case Search", "Browse Supreme Court judgments"],
  ["/rag", "fa-database", "Deep Search", "Search inside judgment texts"],
  ["/dashboard", "fa-chart-simple", "Analytics", "Case statistics & charts"],
];

// Closes a dropdown when clicking outside of it
function useOutside(ref, onOut) {
  useEffect(() => {
    const fn = (e) => { if (ref.current && !ref.current.contains(e.target)) onOut(); };
    document.addEventListener("mousedown", fn);
    return () => document.removeEventListener("mousedown", fn);
  }, [ref, onOut]);
}

function Header({ theme, toggleTheme, lang, setLang }) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();
  const moreRef = useRef(null);
  const userRef = useRef(null);
  useOutside(moreRef, () => setMoreOpen(false));
  useOutside(userRef, () => setUserOpen(false));

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 8);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);

  // Close menus on navigation
  useEffect(() => { setMenuOpen(false); setMoreOpen(false); setUserOpen(false); }, [loc.pathname]);

  const handleLogout = () => { logout(); nav("/login"); };
  const linkClass = ({ isActive }) => (isActive ? "act" : "");
  const moreActive = MORE_LINKS.some(([to]) => loc.pathname === to);

  return (
    <header className={`hdr${scrolled ? " scrolled" : ""}`}>
      <div className="hdr-in">
        <Link to="/" className="brand">
          <div className="brand-mark"><i className="fas fa-scale-balanced" /></div>
          <div>
            <div className="brand-name">Pocket<span>Law</span></div>
            <div className="brand-tag">Type Your Problem, Get Your Legal Rights</div>
          </div>
        </Link>

        <ul className={`nav-links${menuOpen ? " open" : ""}`}>
          {MAIN_LINKS.map(([to, ic, lbl]) => (
            <li key={to}>
              <NavLink to={to} end={to === "/"} className={linkClass}>
                <i className={`fas ${ic}`} /> {lbl}
              </NavLink>
            </li>
          ))}
          <li className="nav-more" ref={moreRef}>
            <button className="nav-more-btn" onClick={() => setMoreOpen(o => !o)} style={moreActive ? { color: "var(--ink)", background: "var(--accent-soft)" } : {}}>
              More <i className={`fas fa-chevron-${moreOpen ? "up" : "down"}`} style={{ fontSize: 10 }} />
            </button>
            <div className={`nav-drop${moreOpen ? " open" : ""}`}>
              {MORE_LINKS.map(([to, ic, lbl, sub]) => (
                <NavLink key={to} to={to} className={linkClass}>
                  <i className={`fas ${ic}`} />
                  <span>{lbl}<small>{sub}</small></span>
                </NavLink>
              ))}
            </div>
          </li>
        </ul>

        <div className="nav-right">
          <select className="lang-sel" value={lang} onChange={(e) => setLang(e.target.value)} aria-label="Language">
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="pa">ਪੰਜਾਬੀ</option>
            <option value="ur">اردو</option>
            <option value="hx">Hinglish</option>
          </select>
          <button className="icon-btn" onClick={toggleTheme} title="Toggle theme" aria-label="Toggle theme">
            <i className={`fas fa-${theme === "dark" ? "sun" : "moon"}`} />
          </button>

          {user ? (
            <div className="nav-more" ref={userRef}>
              <button className="user-chip" onClick={() => setUserOpen(o => !o)}>
                {user?.avatar_url
                  ? <img src={user.avatar_url} alt="" style={{ width: 30, height: 30, borderRadius: 9, objectFit: "cover" }} />
                  : <div className="user-initial">{(user.name || user.email || "U").charAt(0).toUpperCase()}</div>}
                <span className="nm">{(user.name || user.email || "").split(" ")[0].slice(0, 14)}</span>
                <i className="fas fa-chevron-down" style={{ fontSize: 10, color: "var(--muted)" }} />
              </button>
              <div className={`nav-drop user-drop${userOpen ? " open" : ""}`}>
                <NavLink to="/profile"><i className="fas fa-user" /><span>Profile</span></NavLink>
                <NavLink to="/chats"><i className="fas fa-clock-rotate-left" /><span>Chat History</span></NavLink>
                <a href="#logout" onClick={(e) => { e.preventDefault(); handleLogout(); }}><i className="fas fa-arrow-right-from-bracket" /><span>Logout</span></a>
              </div>
            </div>
          ) : (
            <button className="btn btn-navy btn-sm" onClick={() => nav("/login")}>
              <i className="fas fa-user" /> <span className="lbl">Login</span>
            </button>
          )}

          <button className="icon-btn menu-toggle" onClick={() => setMenuOpen(o => !o)} aria-label="Menu">
            <i className={`fas fa-${menuOpen ? "xmark" : "bars"}`} />
          </button>
        </div>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="ftr">
      <div className="ftr-in">
        <div>
          <Link to="/" className="brand" style={{ marginBottom: 12 }}>
            <div className="brand-mark"><i className="fas fa-scale-balanced" /></div>
            <div className="brand-name">Pocket<span>Law</span></div>
          </Link>
          <p style={{ marginTop: 12, maxWidth: 360 }}>
            Type your problem in simple words and get the Indian laws, your legal rights and clear next steps — all in one place.
          </p>
        </div>
        <div>
          <h4>Core features</h4>
          <ul>
            <li><Link to="/">AI Law Matcher</Link></li>
            <li><Link to="/steps">Legal Survival Steps</Link></li>
            <li><Link to="/documents">Legal Document Drafting</Link></li>
            <li><Link to="/laws">Indian Laws Explorer</Link></li>
          </ul>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><Link to="/search">Case Search</Link></li>
            <li><Link to="/rag">Deep Search</Link></li>
            <li><Link to="/dashboard">Analytics</Link></li>
            <li><a href="https://nalsa.gov.in" target="_blank" rel="noopener noreferrer">Free Legal Aid (NALSA)</a></li>
          </ul>
        </div>
      </div>
      <div className="ftr-bottom">
        <span>© {new Date().getFullYear()} PocketLaw · Type Your Problem, Get Your Legal Rights</span>
        <span><i className="fas fa-circle-info" /> General legal information only — not a substitute for professional legal advice.</span>
      </div>
    </footer>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState(() => { try { return localStorage.getItem("pl_theme_v3") || "light"; } catch { return "light"; } });
  const [lang, setLang] = useState(() => { try { return localStorage.getItem("pl_lang") || "en"; } catch { return "en"; } });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("pl_theme_v3", theme); } catch {}
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute("lang", lang === "hx" ? "en" : lang);
    try { localStorage.setItem("pl_lang", lang); } catch {}
  }, [lang]);

  const toggleTheme = () => setTheme(t => (t === "dark" ? "light" : "dark"));

  useEffect(() => {
    const stored = localStorage.getItem("jl_user");
    if (stored) {
      try { setUser(JSON.parse(stored)); } catch {}
    }
  }, []);

  const login = (userData, token) => {
    localStorage.setItem("jl_user", JSON.stringify(userData));
    localStorage.setItem("jl_token", token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("jl_user");
    localStorage.removeItem("jl_token");
    setUser(null);
  };

  const authValue = { user, login, logout };

  return (
    <AuthContext.Provider value={authValue}>
      <Router>
        <div className="app-container">
          <Header theme={theme} toggleTheme={toggleTheme} lang={lang} setLang={setLang} />

          <main>
            <Routes>
              <Route path="/" element={<HomePage lang={lang} />} />
              <Route path="/steps" element={<StepsPage lang={lang} />} />
              <Route path="/dashboard" element={<DashboardPage theme={theme} />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/rag" element={<RAGSearchPage />} />
              <Route path="/laws" element={<LawsPage />} />
              <Route path="/documents" element={<DocumentsPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/chats" element={<ChatHistoryPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>

          <Footer />

          <Toaster
            position="bottom-right"
            toastOptions={{
              style: {
                background: "var(--surface)",
                border: "1px solid var(--line)",
                color: "var(--ink)",
                fontFamily: "var(--sans)",
                fontSize: 14,
                boxShadow: "var(--shadow-lg)",
              },
              duration: 3000,
            }}
          />
        </div>
      </Router>
    </AuthContext.Provider>
  );
}

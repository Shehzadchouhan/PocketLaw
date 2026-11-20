import axios from "axios";

// ── Smart Base URL Resolution ──
export const isLocalhost = () => {
  if (typeof window === "undefined") return true;
  if (process.env.NODE_ENV === "development") return true;
  const host = (window.location.hostname || "").toLowerCase();
  const protocol = window.location.protocol || "";
  const port = window.location.port || "";

  // 1. File protocol (file:///.../index.html opened locally) or missing host
  if (protocol === "file:" || !host) return true;

  // 2. Loopback / local development addresses
  if (
    host === "localhost" ||
    host === "127.0.0.1" ||
    host === "0.0.0.0" ||
    host === "[::1]" ||
    host === "::1"
  ) {
    return true;
  }

  // 3. Common local development ports
  if (["3000", "5000", "5001", "5173", "8000", "8080"].includes(port)) {
    return true;
  }

  // 4. Local private network IPs (e.g. 192.168.x.x, 10.x.x.x, 172.16-31.x.x) or .local
  if (
    host.endsWith(".local") ||
    host.endsWith(".lan") ||
    host.endsWith(".internal") ||
    /^192\.168\./.test(host) ||
    /^10\./.test(host) ||
    /^172\.(1[6-9]|2[0-9]|3[0-1])\./.test(host)
  ) {
    return true;
  }

  return false;
};

export const getBaseUrl = () => {
  if (typeof window !== "undefined") {
    // 1. Manual runtime override saved in browser
    const stored = localStorage.getItem("pl_backend_url");
    if (stored) return stored.replace(/\/+$/, "");

    // 2. Localhost development fallback (always target local Flask backend on 5001)
    if (isLocalhost()) {
      return process.env.REACT_APP_API_URL || "http://127.0.0.1:5001";
    }

    // 3. Explicit environment variable set at build/deploy time for production
    if (process.env.REACT_APP_API_URL) {
      return process.env.REACT_APP_API_URL.replace(/\/+$/, "");
    }

    // 4. On live production deployments with relative reverse proxy
    return "";
  }
  return process.env.REACT_APP_API_URL || "http://127.0.0.1:5001";
};

export const BASE = getBaseUrl();

// Timeout increased to 75s to gracefully tolerate cloud free-tier cold starts (Render/Koyeb)
const api = axios.create({
  baseURL: BASE,
  timeout: 75000,
  headers: { "Content-Type": "application/json" }
});

// Dynamic BaseURL resolution & JWT token injection
api.interceptors.request.use((config) => {
  if (!config.baseURL) {
    config.baseURL = getBaseUrl();
  }
  const token = localStorage.getItem("jl_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Handle 401 globally & auto-retry once on cloud cold-starts / timeouts
api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const config = err?.config;
    // Handle 401 Unauthorized
    if (err?.response?.status === 401) {
      localStorage.removeItem("jl_token");
      localStorage.removeItem("jl_user");
      return Promise.reject(err);
    }

    // Auto-retry once on network timeouts or 502/503/504 errors (typical for sleeping free-tier containers)
    if (config && !config.__isRetry) {
      const isColdStartOrTimeout =
        !err.response ||
        err.code === "ECONNABORTED" ||
        [502, 503, 504].includes(err.response?.status);

      if (isColdStartOrTimeout) {
        config.__isRetry = true;
        // Wait 3.5 seconds before retrying to give sleeping container time to finish booting
        await new Promise((res) => setTimeout(res, 3500));
        return api(config);
      }
    }

    return Promise.reject(err);
  }
);

// ── Silent Pre-Warming Ping (Wakes sleeping cloud container on page load) ──
export const pingServer = async () => {
  try {
    const res = await api.get("/api/health", { timeout: 15000 });
    return res.data;
  } catch {
    return null;
  }
};

// ── Runtime Backend Configuration ──
export const setCustomBackendUrl = (url) => {
  if (url) {
    localStorage.setItem("pl_backend_url", url.trim());
  } else {
    localStorage.removeItem("pl_backend_url");
  }
  window.location.reload();
};

// ── RAG / Legal APIs ──
export const chatAPI = (message, mode = "both", lang = "en") => api.post("/api/chat", { message, mode, lang }).then(r => r.data);
export const statsAPI = () => api.get("/api/stats").then(r => r.data);
export const searchAPI = (params) => api.get("/api/search", { params }).then(r => r.data);
export const caseAPI = (id) => api.get(`/api/case/${id}`).then(r => r.data);
export const lawsAPI = () => api.get("/api/laws").then(r => r.data);
export const ragAPI = (q, cat) => api.get("/api/rag", { params: { q, category: cat || "" } }).then(r => r.data);
export const webSearchAPI = (q) => api.get("/api/websearch", { params: { q } }).then(r => r.data);
export const ragEvalAPI = () => api.get("/api/rag/eval").then(r => r.data);

const dl = async (url, data, fname) => {
  const res = await api.post(url, data, { responseType: "blob" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(res.data); a.download = fname; a.click();
  URL.revokeObjectURL(a.href);
};
export const previewDocAPI = (d) => api.post("/api/documents/preview", d).then(r => r.data);
export const dlFIR = (d) => dl("/api/download/fir", d, `FIR_Draft_${Date.now()}.pdf`);
export const dlNotice = (d) => dl("/api/download/notice", d, `Legal_Notice_${Date.now()}.pdf`);
export const dlAffidavit = (d) => dl("/api/download/affidavit", d, `Affidavit_${Date.now()}.pdf`);
export const dlComplaint = (d) => dl("/api/download/complaint", d, `Consumer_Complaint_${Date.now()}.pdf`);
export const dlConsultation = (d) => dl("/api/download/consultation", d, `Legal_Consultation_${Date.now()}.pdf`);

// ── Auth APIs ──
export const registerAPI = (email, password, name) =>
  api.post("/api/auth/register", { email, password, name }).then(r => r.data);
export const loginAPI = (email, password) =>
  api.post("/api/auth/login", { email, password }).then(r => r.data);
export const logoutAPI = () =>
  api.post("/api/auth/logout").then(r => r.data);
export const meAPI = () =>
  api.get("/api/auth/me").then(r => r.data);
export const changePasswordAPI = (current_password, new_password) =>
  api.post("/api/auth/change-password", { current_password, new_password }).then(r => r.data);

// ── Profile APIs ──
export const getProfileAPI = () => api.get("/api/profile").then(r => r.data);
export const updateProfileAPI = (payload) => api.put("/api/profile", payload).then(r => r.data);

// ── Chat History APIs ──
export const getChatsAPI = () =>
  api.get("/api/chats").then(r => r.data);
export const saveChatAPI = (message, response, mode) =>
  api.post("/api/chats/save", { message, response, mode }).then(r => r.data);
export const clearChatsAPI = () =>
  api.post("/api/chats/clear").then(r => r.data);

// ── Document Persistence APIs ──
export const saveDocAPI = (payload) =>
  api.post("/api/documents/save", payload).then(r => r.data);
export const getDocsAPI = (type) =>
  api.get("/api/documents", { params: { type } }).then(r => r.data);
export const deleteDocAPI = (docId) =>
  api.delete(`/api/documents/${docId}`).then(r => r.data);

// ── Case Bookmarks APIs ──
export const getBookmarksAPI = () =>
  api.get("/api/bookmarks").then(r => r.data);
export const addBookmarkAPI = (payload) =>
  api.post("/api/bookmarks", payload).then(r => r.data);
export const removeBookmarkAPI = (caseId) =>
  api.delete(`/api/bookmarks/${caseId}`).then(r => r.data);

// ── Database Diagnostics API ──
export const dbStatsAPI = () =>
  api.get("/api/db/stats").then(r => r.data);

export default api;


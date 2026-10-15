import axios from "axios";
const BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5001";
const api = axios.create({ baseURL: BASE, timeout: 20000, headers: { "Content-Type": "application/json" } });

// Add JWT token to all requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jl_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Handle 401 globally
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      localStorage.removeItem("jl_token");
      localStorage.removeItem("jl_user");
    }
    return Promise.reject(err);
  }
);

// Ensure Authorization header uses Bearer format (override broken interceptor if present)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jl_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

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


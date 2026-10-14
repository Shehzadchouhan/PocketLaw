import axios from "axios";
const BASE = process.env.REACT_APP_API_URL || "";
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

const dl = async (url, data, fname) => {
  const res = await api.post(url, data, { responseType: "blob" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(res.data); a.download = fname; a.click();
  URL.revokeObjectURL(a.href);
};
export const dlFIR = (d) => dl("/api/download/fir", d, `FIR_Draft_${Date.now()}.txt`);
export const dlNotice = (d) => dl("/api/download/notice", d, `Legal_Notice_${Date.now()}.txt`);
export const dlAffidavit = (d) => dl("/api/download/affidavit", d, `Affidavit_${Date.now()}.txt`);
export const dlComplaint = (d) => dl("/api/download/complaint", d, `Consumer_Complaint_${Date.now()}.txt`);

// ── Auth APIs ──
export const registerAPI = (email, password, name) =>
  api.post("/api/auth/register", { email, password, name }).then(r => r.data);
export const loginAPI = (email, password) =>
  api.post("/api/auth/login", { email, password }).then(r => r.data);
export const logoutAPI = () =>
  api.post("/api/auth/logout").then(r => r.data);
export const meAPI = () =>
  api.get("/api/auth/me").then(r => r.data);

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

export default api;


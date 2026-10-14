import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../App";
import { loginAPI } from "../services/api";
import toast from "react-hot-toast";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) { toast.error("Please fill all fields"); return; }
    setLoading(true);
    try {
      const data = await loginAPI(email, password);
      login(data.user, data.token);
      toast.success("Login successful!");
      nav("/");
    } catch (err) {
      toast.error(err?.response?.data?.error || "Login failed");
    }
    setLoading(false);
  };

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <div className="shdr" style={{ marginBottom: 36 }}>
          <div className="stag"><i className="fas fa-lock" /> PocketLaw account</div>
          <h1 className="stit">Welcome Back</h1>
          <p className="ssub">Sign in to save your conversations. You can also use PocketLaw as a guest.</p>
        </div>

        <form onSubmit={handleSubmit} className="card" style={{ padding: 32 }}>
          <div className="fg" style={{ marginBottom: 18 }}>
            <label>Email Address</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="your@email.com" required />
          </div>
          <div className="fg" style={{ marginBottom: 24 }}>
            <label>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" required minLength={6} />
          </div>
          <button className="btn btn-g" style={{ width: "100%", justifyContent: "center", padding: 14, fontSize: 15 }} disabled={loading}>
            {loading ? <span className="ldr"><span/><span/><span/></span> : "Sign in"}
          </button>
          <p style={{ textAlign: "center", marginTop: 18, fontSize: 13, color: "var(--dim)" }}>
            Don't have an account? <Link to="/register" style={{ color: "var(--gold)" }}>Create one</Link>
          </p>
        </form>
      </div>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../App";
import { getProfileAPI, updateProfileAPI, changePasswordAPI, getDocsAPI, getBookmarksAPI, getChatsAPI } from "../services/api";
import toast from "react-hot-toast";

export default function ProfilePage() {
  const nav = useNavigate();
  const { user, login, logout } = useAuth();
  const [profile, setProfile] = useState({ email: "", name: "", bio: "", avatar_url: "" });
  const [saving, setSaving] = useState(false);
  const [unauth, setUnauth] = useState(false);
  
  // Activity stats
  const [counts, setCounts] = useState({ chats: 0, docs: 0, bookmarks: 0 });

  // Change password form
  const [pwForm, setPwForm] = useState({ current_password: "", new_password: "", confirm_password: "" });
  const [changingPw, setChangingPw] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("jl_token");
    if (!token) { setUnauth(true); return; }
    fetchProfile();
    fetchActivity();
    // eslint-disable-next-line
  }, []);

  const fetchActivity = async () => {
    try {
      const [c, d, b] = await Promise.allSettled([
        getChatsAPI(),
        getDocsAPI(),
        getBookmarksAPI()
      ]);
      setCounts({
        chats: c.status === "fulfilled" && c.value?.messages ? c.value.messages.length : 0,
        docs: d.status === "fulfilled" && d.value?.documents ? d.value.documents.length : 0,
        bookmarks: b.status === "fulfilled" && b.value?.bookmarks ? b.value.bookmarks.length : 0
      });
    } catch {
      // Non-fatal
    }
  };

  const fetchProfile = async () => {
    try {
      const res = await getProfileAPI();
      if (res && res.profile) setProfile(res.profile);
    } catch (err) {
      console.error(err);
      if (err?.response?.status === 401) {
        logout();
        setUnauth(true);
        toast.error("Your session expired. Please login again.");
      } else {
        toast.error("Failed to load profile");
      }
    }
  };

  const onSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await updateProfileAPI({ name: profile.name, bio: profile.bio, avatar_url: profile.avatar_url });
      toast.success(res.message || "Profile updated");
      // Update stored user name in localStorage and context
      const storedUser = JSON.parse(localStorage.getItem("jl_user") || "{}");
      const updatedUser = { ...storedUser, name: profile.name };
      localStorage.setItem("jl_user", JSON.stringify(updatedUser));
      login(updatedUser, localStorage.getItem("jl_token"));
    } catch (err) {
      console.error(err);
      toast.error("Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  const onChangePassword = async (e) => {
    e.preventDefault();
    if (!pwForm.current_password || !pwForm.new_password) {
      toast.error("Please fill in current and new password");
      return;
    }
    if (pwForm.new_password.length < 6) {
      toast.error("New password must be at least 6 characters");
      return;
    }
    if (pwForm.new_password !== pwForm.confirm_password) {
      toast.error("New passwords do not match");
      return;
    }
    setChangingPw(true);
    try {
      const res = await changePasswordAPI(pwForm.current_password, pwForm.new_password);
      toast.success(res.message || "Password changed successfully");
      setPwForm({ current_password: "", new_password: "", confirm_password: "" });
    } catch (err) {
      toast.error(err?.response?.data?.message || "Failed to change password");
    } finally {
      setChangingPw(false);
    }
  };

  if (unauth) {
    return (
      <div className="auth-wrap">
        <div className="card auth-card" style={{ textAlign: "center", padding: 32 }}>
          <div style={{ width: 56, height: 56, borderRadius: 16, background: "var(--accent-soft)", color: "var(--accent)", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 22, marginBottom: 14 }}><i className="fas fa-user" /></div>
          <h2 style={{ fontFamily: "var(--serif)", fontSize: 26 }}>Profile</h2>
          <p style={{ marginTop: 8, color: "var(--muted)" }}>You are not logged in. Please login or register to view and edit your profile.</p>
          <div style={{ display: 'flex', gap: 8, marginTop: 18, justifyContent: "center" }}>
            <button className="btn btn-g" onClick={() => nav('/login')}>Login</button>
            <button className="btn btn-o" onClick={() => nav('/register')}>Register</button>
          </div>
        </div>
      </div>
    );
  }

  const initial = (profile.name || profile.email || "U").charAt(0).toUpperCase();

  return (
    <div className="page" style={{ maxWidth: 720 }}>
      <div className="shdr" style={{ textAlign: "left", marginBottom: 28 }}>
        <div className="stag"><i className="fas fa-user" /> Account</div>
        <h1 className="stit">Your profile</h1>
      </div>

      {/* Activity Overview */}
      <div className="card" style={{ padding: 20, marginBottom: 20 }}>
        <h3 style={{ fontSize: 11, letterSpacing: 1.5, textTransform: "uppercase", color: "var(--ink2)", fontWeight: 700, marginBottom: 14 }}>
          Activity Overview
        </h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 12 }}>
          <div className="kbox">
            <div className="knum" style={{ color: "var(--gold)" }}>{counts.chats}</div>
            <div className="klbl">Legal Queries Asked</div>
          </div>
          <div className="kbox">
            <div className="knum" style={{ color: "var(--ok)" }}>{counts.docs}</div>
            <div className="klbl">Drafted Documents</div>
          </div>
          <div className="kbox">
            <div className="knum" style={{ color: "var(--accent)" }}>{counts.bookmarks}</div>
            <div className="klbl">Bookmarked Precedents</div>
          </div>
          <div className="kbox">
            <div className="knum" style={{ color: "var(--ok)" }}>Active</div>
            <div className="klbl">Account Status</div>
          </div>
        </div>
      </div>

      <form onSubmit={onSave} className="card" style={{ padding: 28 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 24 }}>
          {profile.avatar_url
            ? <img src={profile.avatar_url} alt="" style={{ width: 64, height: 64, borderRadius: 18, objectFit: "cover" }} />
            : <div className="user-initial" style={{ width: 64, height: 64, borderRadius: 18, fontSize: 24 }}>{initial}</div>}
          <div>
            <div style={{ fontFamily: "var(--serif)", fontSize: 21, fontWeight: 600 }}>{profile.name || "Your name"}</div>
            <div style={{ fontSize: 13.5, color: "var(--muted)" }}>{profile.email}</div>
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div className="fg">
            <label>Email (read-only)</label>
            <input type="email" value={profile.email} readOnly />
          </div>
          <div className="fg">
            <label>Name</label>
            <input value={profile.name} onChange={e => setProfile(p => ({ ...p, name: e.target.value }))} required />
          </div>
          <div className="fg">
            <label>Bio</label>
            <textarea value={profile.bio} onChange={e => setProfile(p => ({ ...p, bio: e.target.value }))} rows={4} />
          </div>
          <div className="fg">
            <label>Avatar URL</label>
            <input value={profile.avatar_url} onChange={e => setProfile(p => ({ ...p, avatar_url: e.target.value }))} placeholder="https://…" />
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8, marginTop: 22 }}>
          <button className="btn btn-g" type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save changes'}</button>
          <button className="btn btn-o" type="button" onClick={() => nav('/chats')}><i className="fas fa-clock-rotate-left" /> Chat history</button>
        </div>
      </form>

      {/* Security & Password Card */}
      <form onSubmit={onChangePassword} className="card" style={{ padding: 28, marginTop: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 18 }}>
          <span className="di" style={{ width: 40, height: 40, borderRadius: 11, background: "var(--accent-soft)", color: "var(--accent)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <i className="fas fa-lock" />
          </span>
          <div>
            <div style={{ fontFamily: "var(--serif)", fontSize: 18, fontWeight: 600 }}>Security & Password</div>
            <div style={{ fontSize: 13, color: "var(--muted)" }}>Update your account login password</div>
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div className="fg">
            <label>Current Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={pwForm.current_password}
              onChange={e => setPwForm(p => ({ ...p, current_password: e.target.value }))}
              required
            />
          </div>
          <div className="g2">
            <div className="fg">
              <label>New Password</label>
              <input
                type="password"
                placeholder="At least 6 characters"
                value={pwForm.new_password}
                onChange={e => setPwForm(p => ({ ...p, new_password: e.target.value }))}
                required
              />
            </div>
            <div className="fg">
              <label>Confirm New Password</label>
              <input
                type="password"
                placeholder="Repeat new password"
                value={pwForm.confirm_password}
                onChange={e => setPwForm(p => ({ ...p, confirm_password: e.target.value }))}
                required
              />
            </div>
          </div>
        </div>
        <div style={{ marginTop: 20 }}>
          <button className="btn btn-g" type="submit" disabled={changingPw}>
            {changingPw ? "Updating..." : "Update Password"}
          </button>
        </div>
      </form>
    </div>
  );
}

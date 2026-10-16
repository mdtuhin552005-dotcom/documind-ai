from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import aiosqlite
from pathlib import Path
import os

router = APIRouter(prefix="/admin", tags=["admin"])
from app.core.config import settings

def get_db_path(request: Request | None = None) -> Path:
    if request and hasattr(request.app.state, "database"):
        return request.app.state.database.database_path
    if request and hasattr(request.app.state, "settings"):
        return request.app.state.settings.database_path
    # Check if /var/data exists (Render mount)
    render_db = Path("/var/data/documind.sqlite3")
    if render_db.exists():
        return render_db
    local_sqlite = Path("data/documind.sqlite3")
    if local_sqlite.exists():
        return local_sqlite
    local_db = Path("data/documind.db")
    if local_db.exists():
        return local_db
    return settings.database_path

import time
import secrets

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ACTIVE_ADMIN_SESSIONS: dict[str, float] = {}  # token -> expire_timestamp (5 min TTL)


def is_authenticated(request: Request) -> bool:
    token = request.cookies.get("admin_token")
    if not token:
        return False
    exp = ACTIVE_ADMIN_SESSIONS.get(token)
    if not exp or time.time() > exp:
        ACTIVE_ADMIN_SESSIONS.pop(token, None)
        return False
    return True


def check_admin(request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=307, headers={"Location": "/admin/login"})


ADMIN_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', 'Segoe UI', Roboto, sans-serif;
  background: #07090e;
  color: #f1f5f9;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* Desktop Sidebar */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 240px;
  height: 100vh;
  background: #0d111c;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  padding: 24px 0 16px;
  display: flex;
  flex-direction: column;
  z-index: 50;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.sidebar .logo {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sidebar .logo h2 {
  font-size: 18px;
  background: linear-gradient(135deg, #f5d0fe 0%, #c084fc 50%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: -0.4px;
}
.sidebar .logo small {
  color: #c084fc;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  display: block;
}
.sidebar-close-btn {
  display: none;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #94a3b8;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  place-items: center;
  line-height: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.15s ease;
}
.nav-link:hover {
  background: rgba(124, 58, 237, 0.10);
  color: #e9d5ff;
}
.nav-link.active {
  background: rgba(124, 58, 237, 0.18);
  color: #c084fc;
  border-right: 3px solid #a855f7;
  font-weight: 700;
}
.nav-link .icon {
  font-size: 16px;
  width: 22px;
  display: inline-grid;
  place-items: center;
}

/* Mobile Topbar for Android/iOS */
.mobile-topbar {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: rgba(13, 17, 28, 0.95);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 40;
}
.mobile-topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.mobile-menu-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #f1f5f9;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  font-size: 18px;
  display: grid;
  place-items: center;
  cursor: pointer;
}
.mobile-topbar-title {
  font-size: 15px;
  font-weight: 800;
  background: linear-gradient(135deg, #f5d0fe 0%, #c084fc 50%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.mobile-topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Drawer Backdrop for Mobile */
.sidebar-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  z-index: 45;
  opacity: 0;
  transition: opacity 0.25s ease;
}

/* Main Content Area */
.main {
  margin-left: 240px;
  padding: 32px 36px 60px;
  max-width: 1400px;
  min-height: 100vh;
}
.page-title {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}
.page-sub {
  color: #a855f7;
  font-size: 13.5px;
  margin-bottom: 24px;
  font-weight: 600;
  opacity: 0.9;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}
.stat-card {
  background: #0e1320;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
  transition: transform 0.18s ease;
}
.stat-card .label {
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 6px;
  font-weight: 700;
}
.stat-card .value {
  font-size: 30px;
  font-weight: 800;
  color: #c084fc;
  line-height: 1.1;
}
.stat-card .icon {
  font-size: 24px;
  margin-bottom: 10px;
}

/* Cards & Tables */
.card {
  background: #0e1320;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}
.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.card-header h3 {
  font-size: 15px;
  font-weight: 700;
  color: #ffffff;
}

/* Responsive Table Wrapper */
.table-wrap {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 520px;
}
th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: #c084fc;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: #090e18;
  font-weight: 700;
  white-space: nowrap;
}
td {
  padding: 12px 16px;
  font-size: 13px;
  color: #e2e8f0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
tr:last-child td {
  border-bottom: none;
}
tr:hover td {
  background: rgba(124, 58, 237, 0.06);
}

/* Badges */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.badge-blue { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }
.badge-green { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }
.badge-red { background: rgba(244, 63, 94, 0.12); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.25); }
.badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 15px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  text-decoration: none;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-primary {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35);
}
.btn-primary:hover {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  transform: translateY(-1px);
}
.btn-danger {
  background: #e11d48;
  color: #ffffff;
}
.btn-danger:hover {
  background: #f43f5e;
}
.btn-warning {
  background: #d97706;
  color: #ffffff;
}
.btn-warning:hover {
  background: #f59e0b;
}

.empty { padding: 40px; text-align: center; color: #64748b; font-size: 14px; }
.alert { padding: 14px 20px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
.alert-success { background: rgba(124, 58, 237, 0.15); border: 1px solid #7c3aed; color: #e9d5ff; }
.alert-error { background: rgba(225, 29, 72, 0.15); border: 1px solid #e11d48; color: #fca5a5; }
.truncate { max-width: 240px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Mobile & Android Optimizations */
@media (max-width: 850px) {
  .mobile-topbar {
    display: flex;
  }
  .sidebar {
    transform: translateX(-100%);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.85);
  }
  .sidebar.is-open {
    transform: translateX(0);
  }
  .sidebar-backdrop.is-open {
    display: block;
    opacity: 1;
  }
  .sidebar-close-btn {
    display: grid;
  }
  .main {
    margin-left: 0;
    padding: 16px 14px 40px;
    margin-top: 56px;
    width: 100%;
  }
  .page-title {
    font-size: 20px;
  }
  .page-sub {
    font-size: 12px;
    margin-bottom: 16px;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 18px;
  }
  .stat-card {
    padding: 12px 14px;
    border-radius: 12px;
  }
  .stat-card .icon {
    font-size: 20px;
    margin-bottom: 4px;
  }
  .stat-card .label {
    font-size: 10px;
  }
  .stat-card .value {
    font-size: 22px;
  }
  .card {
    border-radius: 12px;
    margin-bottom: 16px;
  }
  .card-header {
    padding: 12px 14px;
  }
  .card-header h3 {
    font-size: 14px;
  }
  th, td {
    padding: 10px 12px;
    font-size: 12px;
  }
  .truncate {
    max-width: 140px;
  }
  .btn {
    padding: 6px 12px;
    font-size: 11.5px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .truncate {
    max-width: 110px;
  }
}
"""

SIDEBAR = """
<div class="sidebar-backdrop" onclick="toggleSidebar(false)"></div>
<div class="sidebar">
  <div class="logo">
    <div>
      <h2>⚡ DocuMind AI</h2>
      <small>Enterprise Admin</small>
    </div>
    <button class="sidebar-close-btn" onclick="toggleSidebar(false)" aria-label="Close menu">✕</button>
  </div>
  <a href="/admin" class="nav-link {d}"><span class="icon">📊</span> Dashboard</a>
  <a href="/admin/users" class="nav-link {u}"><span class="icon">👤</span> Users</a>
  <a href="/admin/documents" class="nav-link {doc}"><span class="icon">📄</span> Documents</a>
  <a href="/admin/conversations" class="nav-link {c}"><span class="icon">💬</span> Conversations</a>
  <a href="/admin/activity" class="nav-link {act}"><span class="icon">📜</span> Activity Logs</a>
  <a href="/admin/analytics" class="nav-link {ana}"><span class="icon">⚡</span> Query Analytics</a>
  <a href="/admin/settings" class="nav-link {cfg}"><span class="icon">⚙️</span> Settings</a>
  <a href="/admin/sessions" class="nav-link {s}"><span class="icon">🔑</span> Sessions</a>
  <a href="/" class="nav-link" style="margin-top:auto;padding-bottom:18px"><span class="icon">🏠</span> Back to App</a>
</div>
<div class="mobile-topbar">
  <div class="mobile-topbar-left">
    <button class="mobile-menu-btn" onclick="toggleSidebar(true)" aria-label="Open menu">☰</button>
    <span class="mobile-topbar-title">⚡ DocuMind Admin</span>
  </div>
  <div class="mobile-topbar-actions">
    <a href="/" class="btn btn-primary" style="padding:4px 10px;font-size:11px">App</a>
    <a href="/admin/logout" class="btn btn-danger" style="padding:4px 8px;font-size:11px">🚪</a>
  </div>
</div>
"""


def page(title, body, active="d"):
    sidebar = SIDEBAR.format(
        d="active" if active=="d" else "",
        u="active" if active=="u" else "",
        doc="active" if active=="doc" else "",
        c="active" if active=="c" else "",
        act="active" if active=="act" else "",
        ana="active" if active=="ana" else "",
        cfg="active" if active=="cfg" else "",
        s="active" if active=="s" else "",
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#07090e">
<title>{title} — DocuMind Admin</title>
<style>{ADMIN_CSS}</style>
<script>
function toggleSidebar(open) {{
  const sb = document.querySelector('.sidebar');
  const bd = document.querySelector('.sidebar-backdrop');
  if (sb && bd) {{
    if (open) {{
      sb.classList.add('is-open');
      bd.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }} else {{
      sb.classList.remove('is-open');
      bd.classList.remove('is-open');
      document.body.style.overflow = '';
    }}
  }}
}}
</script>
</head>
<body>
{sidebar}
<div class="main">
  <div class="page-title">{title}</div>
  {body}
</div>
</body>
</html>"""


# ── Login ────────────────────────────────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
async def login_page(error: str = ""):
    err = f'<div class="alert alert-error">Wrong password!</div>' if error else ""
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Login</title>
<style>
{ADMIN_CSS}
.login-wrap{{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:16px}}
.login-box{{background:#0e1320;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:36px 24px;width:100%;max-width:380px;box-shadow:0 8px 32px rgba(0,0,0,0.5)}}
h2{{color:#c084fc;font-size:22px;margin-bottom:6px;font-weight:800}} p{{color:#94a3b8;font-size:13px;margin-bottom:24px}}
input{{width:100%;padding:12px 14px;background:#07090e;border:1px solid rgba(255,255,255,0.12);border-radius:8px;
       color:#f1f5f9;font-size:14px;margin-bottom:16px;outline:none}}
input:focus{{border-color:#a855f7}} button{{width:100%;padding:12px;background:linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
color:white;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}}
button:hover{{background:linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)}}
</style></head><body>
<div class="login-wrap"><div class="login-box">
{err}
<h2>🔐 Admin Login</h2><p>DocuMind AI Admin Panel</p>
<form method="post" action="/admin/login">
<input type="password" name="password" placeholder="Admin Password" autofocus>
<button type="submit">Login</button>
</form></div></div></body></html>"""
    return HTMLResponse(html)


@router.post("/login")
async def login_submit(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        token = secrets.token_urlsafe(32)
        ACTIVE_ADMIN_SESSIONS[token] = time.time() + 300
        try:
            db_path = get_db_path(request)
            async with aiosqlite.connect(db_path) as conn:
                await conn.execute(
                    "INSERT INTO activity_logs (action, details, ip_address, created_at) VALUES (?, ?, ?, datetime('now'))",
                    ("ADMIN_LOGIN", "Master Admin authenticated", request.client.host if request.client else None)
                )
                await conn.commit()
        except Exception:
            pass
        resp = RedirectResponse("/admin", status_code=302)
        resp.set_cookie("admin_token", token, httponly=True, max_age=300, samesite="lax")
        resp.delete_cookie("admin_auth")
        return resp
    return RedirectResponse("/admin/login?error=1", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    token = request.cookies.get("admin_token")
    if token:
        ACTIVE_ADMIN_SESSIONS.pop(token, None)
    resp = RedirectResponse("/admin/login", status_code=302)
    resp.delete_cookie("admin_token")
    resp.delete_cookie("admin_auth")
    return resp


# ── Dashboard ────────────────────────────────────────────────────────────────
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        stats = {}
        for tbl in ("users", "documents", "conversations", "conversation_messages", "sessions", "activity_logs", "query_analytics"):
            try:
                c = await conn.execute(f"SELECT COUNT(*) FROM {tbl}")
                stats[tbl] = (await c.fetchone())[0]
            except Exception:
                stats[tbl] = 0

    body = f"""
<div class="page-sub">Enterprise system overview &amp; live telemetry</div>
<div class="stats-grid">
  <div class="stat-card"><div class="icon">👤</div><div class="label">Users</div><div class="value">{stats['users']}</div></div>
  <div class="stat-card"><div class="icon">📄</div><div class="label">Documents</div><div class="value">{stats['documents']}</div></div>
  <div class="stat-card"><div class="icon">💬</div><div class="label">Conversations</div><div class="value">{stats['conversations']}</div></div>
  <div class="stat-card"><div class="icon">💌</div><div class="label">Messages</div><div class="value">{stats['conversation_messages']}</div></div>
  <div class="stat-card"><div class="icon">📜</div><div class="label">Activity Logs</div><div class="value">{stats['activity_logs']}</div></div>
  <div class="stat-card"><div class="icon">⚡</div><div class="label">Queries Analyzed</div><div class="value">{stats['query_analytics']}</div></div>
  <div class="stat-card"><div class="icon">🔑</div><div class="label">Active Sessions</div><div class="value">{stats['sessions']}</div></div>
</div>
<div class="card">
  <div class="card-header"><h3>Quick Management</h3></div>
  <div style="padding:20px;display:flex;gap:12px;flex-wrap:wrap">
    <a href="/admin/users" class="btn btn-primary">👤 Manage Users</a>
    <a href="/admin/activity" class="btn btn-primary">📜 Audit Activity</a>
    <a href="/admin/analytics" class="btn btn-primary">⚡ Query Analytics</a>
    <a href="/admin/settings" class="btn btn-primary">⚙️ System Settings</a>
    <form method="post" action="/admin/sessions/clear" style="display:inline">
      <button class="btn btn-warning" onclick="return confirm('Logout all users?')">🔑 Clear All Sessions</button>
    </form>
    <a href="/admin/logout" class="btn btn-danger">🚪 Logout</a>
  </div>
</div>"""
    return HTMLResponse(page("Dashboard", body, "d"))


# ── Users ─────────────────────────────────────────────────────────────────────
@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute("SELECT id, email, full_name, created_at FROM users ORDER BY created_at DESC")
        users = await cur.fetchall()

    alert = f'<div class="alert alert-success">{msg}</div>' if msg else ""
    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#818cf8">{r['id'][:8]}...</code></td>
      <td>{r['email']}</td>
      <td>{r['full_name']}</td>
      <td>{r['created_at'][:16]}</td>
      <td><form method="post" action="/admin/users/{r['id']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Delete this user?')" style="padding:4px 12px;font-size:12px">Delete</button>
      </form></td>
    </tr>""" for r in users) or f'<tr><td colspan="5" class="empty">No users yet.</td></tr>'

    body = f"""{alert}
<div class="page-sub">{len(users)} total users</div>
<div class="card">
  <div class="card-header"><h3>All Users</h3><span class="badge badge-blue">{len(users)}</span></div>
  <div class="table-wrap"><table><thead><tr><th>ID</th><th>Email</th><th>Name</th><th>Created</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</div>"""
    return HTMLResponse(page("Users", body, "u"))


@router.post("/users/{user_id}/delete")
async def delete_user(user_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
        await conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        await conn.commit()
    return RedirectResponse("/admin/users?msg=User+deleted", status_code=302)


# ── Documents ────────────────────────────────────────────────────────────────
@router.get("/documents", response_class=HTMLResponse)
async def documents_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            """
            SELECT d.id, d.filename, d.title, d.page_count, d.created_at, d.is_deleted, d.deleted_at, u.email
            FROM documents d
            LEFT JOIN users u ON u.id=d.user_id
            ORDER BY d.created_at DESC
            """
        )
        docs = await cur.fetchall()

    alert = f'<div class="alert alert-success">{msg}</div>' if msg else ""
    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#34d399">{r['id'][:8]}...</code></td>
      <td class="truncate" title="{r['filename']}">{r['filename']}</td>
      <td class="truncate" title="{r['title']}">{r['title']}</td>
      <td style="text-align:center">{r['page_count']}</td>
      <td>{r['email'] or '<span style="color:#64748b">Anonymous</span>'}</td>
      <td>{r['created_at'][:10]}</td>
      <td>{'<span class="badge badge-red" title="Deleted by user: ' + (r['deleted_at'] or '') + '">Deleted by User</span>' if r['is_deleted'] else '<span class="badge badge-green">Active</span>'}</td>
      <td><form method="post" action="/admin/documents/{r['id']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Permanently remove this document record from database?')" style="padding:4px 10px;font-size:11px">Purge</button>
      </form></td>
    </tr>""" for r in docs) or '<tr><td colspan="8" class="empty">No documents in database.</td></tr>'

    body = f"""{alert}
<div class="page-sub">{len(docs)} documents stored (including retained user-deleted archives)</div>
<div class="card">
  <div class="card-header"><h3>Document Vault</h3><span class="badge badge-green">{len(docs)} total</span></div>
  <div class="table-wrap"><table><thead><tr><th>ID</th><th>Filename</th><th>Title</th><th>Pages</th><th>Owner</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</div>"""
    return HTMLResponse(page("Documents", body, "doc"))


@router.post("/documents/{doc_id}/delete")
async def delete_document(doc_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute("DELETE FROM conversation_messages WHERE conversation_id IN (SELECT id FROM conversations WHERE document_id=?)", (doc_id,))
        await conn.execute("DELETE FROM conversations WHERE document_id=?", (doc_id,))
        await conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        await conn.commit()
    return RedirectResponse("/admin/documents?msg=Document+purged+from+database", status_code=302)


# ── Conversations ────────────────────────────────────────────────────────────
@router.get("/conversations", response_class=HTMLResponse)
async def conversations_page(request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            """
            SELECT c.id, c.title, c.updated_at, c.is_deleted, c.deleted_at, u.email,
                   (SELECT COUNT(*) FROM conversation_messages WHERE conversation_id=c.id) as msg_count
            FROM conversations c
            LEFT JOIN users u ON u.id=c.user_id
            ORDER BY c.updated_at DESC
            LIMIT 100
            """
        )
        convs = await cur.fetchall()

    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#34d399">{r['id'][:8]}...</code></td>
      <td class="truncate" title="{r['title']}">{r['title']}</td>
      <td>{r['email'] or '<span style="color:#64748b">Anonymous</span>'}</td>
      <td style="text-align:center"><span class="badge badge-blue">{r['msg_count']} msgs</span></td>
      <td>{r['updated_at'][:16]}</td>
      <td>{'<span class="badge badge-red" title="Deleted by user: ' + (r['deleted_at'] or '') + '">Deleted by User</span>' if r['is_deleted'] else '<span class="badge badge-green">Active</span>'}</td>
      <td><form method="post" action="/admin/conversations/{r['id']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Purge conversation?')" style="padding:4px 10px;font-size:11px">Purge</button>
      </form></td>
    </tr>""" for r in convs) or '<tr><td colspan="7" class="empty">No conversations in database.</td></tr>'

    body = f"""
<div class="page-sub">Last 100 conversations (including retained archives)</div>
<div class="card">
  <div class="card-header"><h3>Conversation History</h3><span class="badge badge-blue">{len(convs)}</span></div>
  <div class="table-wrap"><table><thead><tr><th>ID</th><th>Title</th><th>User</th><th>Messages</th><th>Updated</th><th>Status</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</div>"""
    return HTMLResponse(page("Conversations", body, "c"))


@router.post("/conversations/{conv_id}/delete")
async def delete_conversation(conv_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute("DELETE FROM conversation_messages WHERE conversation_id=?", (conv_id,))
        await conn.execute("DELETE FROM conversations WHERE id=?", (conv_id,))
        await conn.commit()
    return RedirectResponse("/admin/conversations?msg=Deleted", status_code=302)


# ── Sessions ────────────────────────────────────────────────────────────────
@router.get("/sessions", response_class=HTMLResponse)
async def sessions_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            "SELECT s.token, s.created_at, s.expires_at, u.email FROM sessions s JOIN users u ON u.id=s.user_id ORDER BY s.created_at DESC"
        )
        sessions = await cur.fetchall()

    alert = f'<div class="alert alert-success">{msg}</div>' if msg else ""
    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#818cf8">{r['token'][:12]}...</code></td>
      <td>{r['email']}</td>
      <td>{r['created_at'][:16]}</td>
      <td>{r['expires_at'][:16]}</td>
      <td><form method="post" action="/admin/sessions/{r['token']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Logout?')" style="padding:4px 12px;font-size:12px">Revoke</button>
      </form></td>
    </tr>""" for r in sessions) or f'<tr><td colspan="5" class="empty">No active sessions.</td></tr>'

    body = f"""{alert}
<div class="page-sub">{len(sessions)} active sessions</div>
<div class="card">
  <div class="card-header">
    <h3>Active Sessions</h3>
    <form method="post" action="/admin/sessions/clear">
      <button class="btn btn-warning" onclick="return confirm('Logout ALL users?')">Clear All</button>
    </form>
  </div>
  <div class="table-wrap"><table><thead><tr><th>Token</th><th>User</th><th>Created</th><th>Expires</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</div>"""
    return HTMLResponse(page("Sessions", body, "s"))


@router.post("/sessions/clear")
async def clear_sessions(request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute("DELETE FROM sessions")
        await conn.commit()
    return RedirectResponse("/admin/sessions?msg=All+sessions+cleared", status_code=302)


@router.post("/sessions/{token}/delete")
async def delete_session(token: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        await conn.commit()
    return RedirectResponse("/admin/sessions?msg=Session+revoked", status_code=302)


# ── Activity Logs ────────────────────────────────────────────────────────────
@router.get("/activity", response_class=HTMLResponse)
async def activity_page(request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            """
            SELECT a.id, a.action, a.details, a.ip_address, a.created_at, u.email
            FROM activity_logs a
            LEFT JOIN users u ON u.id = a.user_id
            ORDER BY a.id DESC
            LIMIT 100
            """
        )
        logs = await cur.fetchall()

    rows = "".join(f"""<tr>
      <td><span class="badge badge-green">{r['action']}</span></td>
      <td>{r['details'] or '-'}</td>
      <td>{r['email'] or '<span style="color:#64748b">Anonymous / Admin</span>'}</td>
      <td><code>{r['ip_address'] or '-'}</code></td>
      <td>{r['created_at'][:19] if r['created_at'] else '-'}</td>
    </tr>""" for r in logs) or '<tr><td colspan="5" class="empty">No activity logs recorded yet.</td></tr>'

    body = f"""
<div class="page-sub">Latest 100 system audit &amp; security events</div>
<div class="card">
  <div class="card-header"><h3>Audit Trail</h3></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Action</th><th>Details</th><th>User</th><th>IP Address</th><th>Timestamp</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div>"""
    return HTMLResponse(page("Activity Logs", body, "act"))


# ── Query Analytics ──────────────────────────────────────────────────────────
@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            """
            SELECT q.id, q.query_text, q.response_time_ms, q.retrieved_chunks, q.created_at,
                   d.filename, u.email
            FROM query_analytics q
            LEFT JOIN documents d ON d.id = q.document_id
            LEFT JOIN users u ON u.id = q.user_id
            ORDER BY q.id DESC
            LIMIT 100
            """
        )
        queries = await cur.fetchall()

    rows = "".join(f"""<tr>
      <td class="truncate" title="{r['query_text']}">{r['query_text']}</td>
      <td>{r['filename'] or '<span style="color:#64748b">Direct</span>'}</td>
      <td>{r['email'] or '-'}</td>
      <td><span class="badge badge-blue">{r['response_time_ms']} ms</span></td>
      <td>{r['retrieved_chunks']} chunks</td>
      <td>{r['created_at'][:19] if r['created_at'] else '-'}</td>
    </tr>""" for r in queries) or '<tr><td colspan="6" class="empty">No query analytics logged yet. Ask questions in chat to populate.</td></tr>'

    body = f"""
<div class="page-sub">Latest 100 user questions &amp; RAG retrieval performance telemetry</div>
<div class="card">
  <div class="card-header"><h3>Query Telemetry</h3></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Question</th><th>Document</th><th>User</th><th>Latency</th><th>Chunks</th><th>Timestamp</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div>"""
    return HTMLResponse(page("Query Analytics", body, "ana"))


# ── System Settings ──────────────────────────────────────────────────────────
@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute("SELECT key, value, description, updated_at FROM system_settings ORDER BY key")
        settings_rows = await cur.fetchall()

    alert = f'<div class="alert alert-success">{msg}</div>' if msg else ""
    rows = "".join(f"""<tr>
      <td><code>{r['key']}</code></td>
      <td><strong>{r['value']}</strong></td>
      <td style="color:#94a3b8">{r['description'] or '-'}</td>
      <td>{r['updated_at'][:19] if r['updated_at'] else '-'}</td>
      <td>
        <form method="post" action="/admin/settings/update" style="display:flex;gap:6px">
          <input type="hidden" name="key" value="{r['key']}">
          <input type="text" name="value" value="{r['value']}" style="width:120px;padding:4px 8px;font-size:12px;background:#090e0c;border:1px solid #1c362a;border-radius:6px;color:#fff;margin:0">
          <button type="submit" class="btn btn-primary" style="padding:4px 10px;font-size:11px">Save</button>
        </form>
      </td>
    </tr>""" for r in settings_rows) or '<tr><td colspan="5" class="empty">No settings configured.</td></tr>'

    body = f"""{alert}
<div class="page-sub">Enterprise system configuration &amp; active parameters</div>
<div class="card">
  <div class="card-header"><h3>Global Application Settings</h3></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Key</th><th>Current Value</th><th>Description</th><th>Last Updated</th><th>Update</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div>"""
    return HTMLResponse(page("System Settings", body, "cfg"))


@router.post("/settings/update")
async def update_setting(request: Request, key: str = Form(...), value: str = Form(...)):
    check_admin(request)
    async with aiosqlite.connect(get_db_path(request)) as conn:
        await conn.execute(
            "UPDATE system_settings SET value = ?, updated_at = datetime('now') WHERE key = ?",
            (value.strip(), key.strip())
        )
        await conn.commit()
    return RedirectResponse("/admin/settings?msg=Setting+updated+successfully", status_code=302)



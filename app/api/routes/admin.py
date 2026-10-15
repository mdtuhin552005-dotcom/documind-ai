from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import aiosqlite
from pathlib import Path
import os

router = APIRouter(prefix="/admin", tags=["admin"])

DB_PATH = Path("data/documind.db")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def check_admin(request: Request):
    if request.cookies.get("admin_auth") != ADMIN_PASSWORD:
        raise HTTPException(status_code=302, headers={"Location": "/admin/login"})


ADMIN_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; }
.sidebar { position: fixed; left: 0; top: 0; width: 220px; height: 100vh; background: #1a1d2e; border-right: 1px solid #2d3748; padding: 24px 0; }
.sidebar .logo { padding: 0 20px 24px; border-bottom: 1px solid #2d3748; margin-bottom: 16px; }
.sidebar .logo h2 { font-size: 18px; color: #818cf8; font-weight: 700; }
.sidebar .logo small { color: #64748b; font-size: 11px; }
.nav-link { display: flex; align-items: center; gap: 10px; padding: 10px 20px; color: #94a3b8; text-decoration: none; font-size: 14px; transition: all .2s; }
.nav-link:hover, .nav-link.active { background: #252840; color: #818cf8; border-right: 3px solid #818cf8; }
.nav-link .icon { font-size: 16px; width: 20px; }
.main { margin-left: 220px; padding: 32px; }
.page-title { font-size: 24px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; }
.page-sub { color: #64748b; font-size: 14px; margin-bottom: 28px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }
.stat-card { background: #1a1d2e; border: 1px solid #2d3748; border-radius: 12px; padding: 20px; }
.stat-card .label { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 8px; }
.stat-card .value { font-size: 32px; font-weight: 700; color: #818cf8; }
.stat-card .icon { font-size: 28px; margin-bottom: 12px; }
.card { background: #1a1d2e; border: 1px solid #2d3748; border-radius: 12px; overflow: hidden; margin-bottom: 24px; }
.card-header { padding: 16px 20px; border-bottom: 1px solid #2d3748; display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { font-size: 15px; font-weight: 600; color: #f1f5f9; }
.badge { padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 600; }
.badge-blue { background: #1e3a5f; color: #60a5fa; }
.badge-green { background: #14532d; color: #4ade80; }
.badge-red { background: #450a0a; color: #f87171; }
table { width: 100%; border-collapse: collapse; }
th { padding: 12px 16px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .5px; color: #64748b; border-bottom: 1px solid #2d3748; }
td { padding: 12px 16px; font-size: 13px; color: #cbd5e1; border-bottom: 1px solid #1e293b; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #252840; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; border: none; text-decoration: none; transition: all .2s; }
.btn-danger { background: #7f1d1d; color: #fca5a5; }
.btn-danger:hover { background: #991b1b; }
.btn-primary { background: #3730a3; color: #a5b4fc; }
.btn-primary:hover { background: #4338ca; }
.btn-warning { background: #78350f; color: #fcd34d; }
.btn-warning:hover { background: #92400e; }
.empty { padding: 40px; text-align: center; color: #475569; font-size: 14px; }
.alert { padding: 14px 20px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
.alert-success { background: #14532d44; border: 1px solid #16a34a; color: #4ade80; }
.alert-error { background: #450a0a44; border: 1px solid #dc2626; color: #f87171; }
.truncate { max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.chip { display: inline-block; padding: 2px 8px; border-radius: 99px; font-size: 11px; }
.chip-user { background: #1e3a5f44; color: #60a5fa; }
.chip-assistant { background: #14532d44; color: #4ade80; }
"""

SIDEBAR = """
<div class="sidebar">
  <div class="logo"><h2>⚡ DocuMind</h2><small>Admin Panel</small></div>
  <a href="/admin" class="nav-link {d}"><span class="icon">📊</span> Dashboard</a>
  <a href="/admin/users" class="nav-link {u}"><span class="icon">👤</span> Users</a>
  <a href="/admin/documents" class="nav-link {doc}"><span class="icon">📄</span> Documents</a>
  <a href="/admin/conversations" class="nav-link {c}"><span class="icon">💬</span> Conversations</a>
  <a href="/admin/sessions" class="nav-link {s}"><span class="icon">🔑</span> Sessions</a>
  <a href="/" class="nav-link" style="margin-top:auto;position:absolute;bottom:20px;left:0;right:0"><span class="icon">🏠</span> Back to App</a>
</div>
"""


def page(title, body, active="d"):
    sidebar = SIDEBAR.format(d="active" if active=="d" else "", u="active" if active=="u" else "",
                              doc="active" if active=="doc" else "", c="active" if active=="c" else "",
                              s="active" if active=="s" else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — DocuMind Admin</title>
<style>{ADMIN_CSS}</style></head>
<body>{sidebar}
<div class="main">
<div class="page-title">{title}</div>
{body}
</div></body></html>"""


# ── Login ────────────────────────────────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
async def login_page(error: str = ""):
    err = f'<div class="alert alert-error">Wrong password!</div>' if error else ""
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Admin Login</title>
<style>
{ADMIN_CSS}
.login-wrap{{display:flex;align-items:center;justify-content:center;min-height:100vh}}
.login-box{{background:#1a1d2e;border:1px solid #2d3748;border-radius:16px;padding:40px;width:360px}}
h2{{color:#818cf8;font-size:22px;margin-bottom:6px}} p{{color:#64748b;font-size:13px;margin-bottom:24px}}
input{{width:100%;padding:10px 14px;background:#0f1117;border:1px solid #374151;border-radius:8px;
       color:#f1f5f9;font-size:14px;margin-bottom:16px;outline:none}}
input:focus{{border-color:#818cf8}} button{{width:100%;padding:12px;background:#4f46e5;
color:white;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}}
button:hover{{background:#4338ca}}
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
async def login_submit(password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        resp = RedirectResponse("/admin", status_code=302)
        resp.set_cookie("admin_auth", ADMIN_PASSWORD, httponly=True, max_age=86400)
        return resp
    return RedirectResponse("/admin/login?error=1", status_code=302)


@router.get("/logout")
async def logout():
    resp = RedirectResponse("/admin/login", status_code=302)
    resp.delete_cookie("admin_auth")
    return resp


# ── Dashboard ────────────────────────────────────────────────────────────────
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        stats = {}
        for tbl in ("users", "documents", "conversations", "conversation_messages", "sessions"):
            c = await conn.execute(f"SELECT COUNT(*) FROM {tbl}")
            stats[tbl] = (await c.fetchone())[0]

    body = f"""
<div class="page-sub">System overview</div>
<div class="stats-grid">
  <div class="stat-card"><div class="icon">👤</div><div class="label">Users</div><div class="value">{stats['users']}</div></div>
  <div class="stat-card"><div class="icon">📄</div><div class="label">Documents</div><div class="value">{stats['documents']}</div></div>
  <div class="stat-card"><div class="icon">💬</div><div class="label">Conversations</div><div class="value">{stats['conversations']}</div></div>
  <div class="stat-card"><div class="icon">💌</div><div class="label">Messages</div><div class="value">{stats['conversation_messages']}</div></div>
  <div class="stat-card"><div class="icon">🔑</div><div class="label">Active Sessions</div><div class="value">{stats['sessions']}</div></div>
</div>
<div class="card">
  <div class="card-header"><h3>Quick Actions</h3></div>
  <div style="padding:20px;display:flex;gap:12px;flex-wrap:wrap">
    <a href="/admin/users" class="btn btn-primary">👤 Manage Users</a>
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
    async with aiosqlite.connect(DB_PATH) as conn:
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
  <table><thead><tr><th>ID</th><th>Email</th><th>Name</th><th>Created</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>"""
    return HTMLResponse(page("Users", body, "u"))


@router.post("/users/{user_id}/delete")
async def delete_user(user_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
        await conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        await conn.commit()
    return RedirectResponse("/admin/users?msg=User+deleted", status_code=302)


# ── Documents ────────────────────────────────────────────────────────────────
@router.get("/documents", response_class=HTMLResponse)
async def documents_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            "SELECT d.id, d.filename, d.title, d.page_count, d.created_at, u.email FROM documents d LEFT JOIN users u ON u.id=d.user_id ORDER BY d.created_at DESC"
        )
        docs = await cur.fetchall()

    alert = f'<div class="alert alert-success">{msg}</div>' if msg else ""
    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#818cf8">{r['id'][:8]}...</code></td>
      <td class="truncate">{r['filename']}</td>
      <td class="truncate">{r['title']}</td>
      <td style="text-align:center">{r['page_count']}</td>
      <td style="color:#64748b">{(r['email'] or 'N/A')}</td>
      <td>{r['created_at'][:10]}</td>
      <td><form method="post" action="/admin/documents/{r['id']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Delete?')" style="padding:4px 12px;font-size:12px">Delete</button>
      </form></td>
    </tr>""" for r in docs) or f'<tr><td colspan="7" class="empty">No documents.</td></tr>'

    body = f"""{alert}
<div class="page-sub">{len(docs)} documents uploaded</div>
<div class="card">
  <div class="card-header"><h3>All Documents</h3><span class="badge badge-green">{len(docs)}</span></div>
  <table><thead><tr><th>ID</th><th>Filename</th><th>Title</th><th>Pages</th><th>Owner</th><th>Date</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>"""
    return HTMLResponse(page("Documents", body, "doc"))


@router.post("/documents/{doc_id}/delete")
async def delete_document(doc_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM conversation_messages WHERE conversation_id IN (SELECT id FROM conversations WHERE document_id=?)", (doc_id,))
        await conn.execute("DELETE FROM conversations WHERE document_id=?", (doc_id,))
        await conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        await conn.commit()
    return RedirectResponse("/admin/documents?msg=Document+deleted", status_code=302)


# ── Conversations ────────────────────────────────────────────────────────────
@router.get("/conversations", response_class=HTMLResponse)
async def conversations_page(request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.execute(
            "SELECT c.id, c.title, c.updated_at, u.email, (SELECT COUNT(*) FROM conversation_messages WHERE conversation_id=c.id) as msg_count FROM conversations c LEFT JOIN users u ON u.id=c.user_id ORDER BY c.updated_at DESC LIMIT 50"
        )
        convs = await cur.fetchall()

    rows = "".join(f"""<tr>
      <td><code style="font-size:11px;color:#818cf8">{r['id'][:8]}...</code></td>
      <td class="truncate">{r['title']}</td>
      <td>{r['email'] or 'N/A'}</td>
      <td style="text-align:center">{r['msg_count']}</td>
      <td>{r['updated_at'][:16]}</td>
      <td><form method="post" action="/admin/conversations/{r['id']}/delete" style="display:inline">
        <button class="btn btn-danger" onclick="return confirm('Delete?')" style="padding:4px 12px;font-size:12px">Delete</button>
      </form></td>
    </tr>""" for r in convs) or f'<tr><td colspan="6" class="empty">No conversations.</td></tr>'

    body = f"""
<div class="page-sub">Last 50 conversations</div>
<div class="card">
  <div class="card-header"><h3>All Conversations</h3><span class="badge badge-blue">{len(convs)}</span></div>
  <table><thead><tr><th>ID</th><th>Title</th><th>User</th><th>Messages</th><th>Updated</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>"""
    return HTMLResponse(page("Conversations", body, "c"))


@router.post("/conversations/{conv_id}/delete")
async def delete_conversation(conv_id: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM conversation_messages WHERE conversation_id=?", (conv_id,))
        await conn.execute("DELETE FROM conversations WHERE id=?", (conv_id,))
        await conn.commit()
    return RedirectResponse("/admin/conversations?msg=Deleted", status_code=302)


# ── Sessions ────────────────────────────────────────────────────────────────
@router.get("/sessions", response_class=HTMLResponse)
async def sessions_page(request: Request, msg: str = ""):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
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
  <table><thead><tr><th>Token</th><th>User</th><th>Created</th><th>Expires</th><th>Action</th></tr></thead>
  <tbody>{rows}</tbody></table>
</div>"""
    return HTMLResponse(page("Sessions", body, "s"))


@router.post("/sessions/clear")
async def clear_sessions(request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM sessions")
        await conn.commit()
    return RedirectResponse("/admin/sessions?msg=All+sessions+cleared", status_code=302)


@router.post("/sessions/{token}/delete")
async def delete_session(token: str, request: Request):
    check_admin(request)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        await conn.commit()
    return RedirectResponse("/admin/sessions?msg=Session+revoked", status_code=302)


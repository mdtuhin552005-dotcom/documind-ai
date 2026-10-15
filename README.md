# DocuMind AI

DocuMind AI lets you upload a PDF, ask questions about it, and receive answers grounded in its contents.

## Features

- Responsive 3D glassmorphic document workspace with drag-and-drop PDF upload and interactive hover tilts.
- Email & Password accounts plus Google Identity Services sign-in with server-verified Google ID tokens.
- Private, per-account PDF libraries and chat history. Existing unowned data is assigned to the earliest existing account, or the first account created after upgrade.
- Daily Ethical Wisdom & AI Principles (জ্ঞান ও নীতিবাক্য): Dynamic bilingual ethical quotes banner & ticker promoting truthfulness, intellectual integrity, and responsible AI.
- Document-scoped vector search using ChromaDB and Gemini embeddings.
- Instant Smart Executive Summary generator and key takeaways extractor.
- Document search & real-time filter in the workspace library.
- Export chat conversations to Markdown (`.md`) format.
- Interactive Message Tools: One-click answer copying and Web Speech Text-to-Speech (TTS 🔊) read aloud.
- Document metadata insights (page count, chunk metrics).
- Answers with grounded page references and safe Markdown rendering.
- Saved conversations with searchable recent-chat titles, transcripts, and citations in SQLite.
- SQLite document & user catalog, persistent Chroma storage, and stored source PDFs.
- Upload limits, PDF validation, structured API errors, and application logging.

## Requirements

- Python 3.11 or newer.
- A Gemini API key with access to the configured chat and embedding models.

## Run locally

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Gemini API key as `GEMINI_API_KEY` in `.env`. To enable real Google sign-in, create a Web OAuth client in Google Cloud Console, add your local and deployed app origins as authorized JavaScript origins, and set its client ID as `GOOGLE_CLIENT_ID`. Google Identity Services sends a signed ID token, so this app does not need the OAuth client secret. Never put that secret in the app or frontend. If a client secret was shared, rotate it in Google Cloud Console. Then run:

```powershell
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. FastAPI's interactive API documentation is available at <http://127.0.0.1:8000/docs>.

The first upload indexes a PDF with the Gemini embedding model. Chat and indexing return a clear `503` response when `GEMINI_API_KEY` is not configured.
Conversations and their transcripts are stored in the same persistent `DATA_DIR` SQLite database as the document catalog. Removing a PDF also removes its saved conversations.

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | — | Required Google Gemini API key. |
| `GOOGLE_CLIENT_ID` | — | Google OAuth Web client ID used to verify Google Identity Services sign-ins. |
| `CHAT_MODEL` | `gemini-3.1-flash-lite` | Gemini chat model. |
| `EMBEDDING_MODEL` | `models/gemini-embedding-001` | Gemini embedding model. |
| `DATA_DIR` | `./data` | Persistent directory for SQLite, ChromaDB, and uploaded PDFs. |
| `MAX_UPLOAD_MB` | `15` | Maximum PDF upload size in MiB. |
| `MAX_PDF_PAGES` | `500` | Maximum pages accepted in a PDF. |
| `CHUNK_SIZE` | `1100` | Maximum chunk length in characters. |
| `CHUNK_OVERLAP` | `180` | Overlap between chunks from the same page. |
| `RETRIEVAL_K` | `5` | Number of relevant passages used per answer. |
| `ALLOWED_ORIGINS` | — | Optional comma-separated CORS origins; same-origin use needs none. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

## Run tests

```powershell
pip install pytest
pytest
```

## Deploy to Render

The included `render.yaml` provisions a single-worker web service and a persistent disk mounted at `/var/data`. Set `GEMINI_API_KEY` and `GOOGLE_CLIENT_ID` in Render, and add the deployed Render origin to the OAuth client's authorized JavaScript origins. A persistent disk requires a paid Render service; without one, local SQLite, uploaded files, and the vector index are ephemeral. Keep one worker while using the local ChromaDB store and do not attach the same disk to multiple service instances.

For Docker, build with `docker build -t documind-ai .` and run with `GEMINI_API_KEY` set and a persistent volume mounted at `/var/data`.

## Project structure

```text
.
├── app/
│   ├── api/routes/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── services/
│   │   ├── chat.py
│   │   └── documents.py
│   ├── static/
│   │   ├── app.js
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   ├── test_auth.py
│   ├── test_chat.py
│   ├── test_conversations.py
│   └── test_documents.py
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── render.yaml
└── requirements.txt
```

# SignalStack API

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/profile/resume` | Extract a PDF, DOCX, or TXT resume |
| PUT | `/profiles/{profile_id}` | Persist an extracted profile |
| GET | `/profiles/{profile_id}` | Read a persisted profile |
| POST | `/briefing` | Retrieve ranked source documents for a profile |
| POST | `/rag/ask` | Return a grounded answer and source citations |
| POST | `/ingest/refresh` | Fetch public GitHub and arXiv examples for topics |

All generated answer content is accompanied by the retrieved source records.
The local service uses a dependency-free hashed-token cosine baseline so it can
run without credentials; the interface is intentionally compatible with a
future BM25 + vector store implementation.

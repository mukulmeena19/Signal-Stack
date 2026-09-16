# SignalStack

> Technical signal, not noise.

SignalStack is a local-first technical intelligence workspace. It combines
resume context, optional public GitHub context, research papers, releases,
engineering stories, and open-source activity into an explainable feed.

## What’s in this MVP

- Profile onboarding with PDF, DOCX, and TXT resume analysis
- Editable inferred skills, projects, and topics before saving
- Personalized **For You** briefing with profile-fit scores
- Broad **Tech Feed** with source filters and search
- **Research** cards with problem, method, limitations, and practical value
- **GitHub Radar** for relevant repositories and public activity
- **Real Problems, Real Solutions** engineering case studies
- Save and “Not relevant” feedback controls
- **Ask SignalStack** grounded in retrieved local source documents
- Responsive dark-mode-first interface with Lucide icons
- FastAPI service with local SQLite persistence and retrieval tests

## Run locally

Start the frontend:

```powershell
npm install
npm run dev -- -H 127.0.0.1 -p 5173
```

Start the API in a second terminal:

```powershell
python -m pip install -r backend/requirements.txt
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173).

## Docker Compose

```powershell
docker compose up --build
```

The compose stack includes the Next.js app, FastAPI service, and PostgreSQL
with pgvector. Redis is intentionally not included because no worker queue is
implemented in this local MVP.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/profile/resume` | Extract a PDF, DOCX, or TXT resume |
| PUT | `/profiles/{profile_id}` | Persist a profile |
| GET | `/profiles/{profile_id}` | Read a profile |
| POST | `/briefing` | Retrieve ranked source documents |
| POST | `/rag/ask` | Return a grounded answer with citations |
| POST | `/ingest/refresh` | Fetch public GitHub and arXiv examples |

## Verification

```powershell
cd backend
python -m unittest discover -s tests
```

The backend retrieval suite currently includes tests for document retrieval,
source-backed answers, and recommendation explanations.

## Honest MVP boundary

The local service uses SQLite and a dependency-free hashed-token retrieval
baseline so it runs without credentials. Production upgrades are PostgreSQL +
pgvector persistence, Sentence Transformers embeddings, BM25 hybrid ranking,
owner-scoped authentication, scheduled workers, encrypted resume storage, and
an optional grounded LLM provider.

See [docs/architecture.md](docs/architecture.md) and
[docs/api.md](docs/api.md) for the current architecture and API contract.

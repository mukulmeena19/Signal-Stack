# SignalStack

### Technical signal, not noise.

SignalStack is a local-first technical intelligence workspace for engineers,
researchers, open-source contributors, and technical builders. It brings
research papers, GitHub activity, releases, engineering stories, and
source-backed recommendations into one focused interface.

The product is built around a simple promise: a useful technical update should
tell you what happened, why it matters to your work, what to do next, and which
source supports it.

## Why SignalStack

Most technology feeds optimize for popularity, recency, or engagement. That
creates noise and hides the smaller updates that matter to a specific developer:
a breaking release, a new retrieval technique, a repository worth studying, or
an engineering team solving the same problem.

SignalStack starts with technical context instead. A resume, optional public
GitHub username, and explicit interests create a visible, editable profile. The
feed then explains the relationship between that profile and each
recommendation.

## Product surfaces

### For You

A personalized briefing ranked around profile fit, source quality, freshness,
and user feedback. Every recommendation includes:

- profile-match score;
- source type, timestamp, and technology tags;
- a “Why you’re seeing this” explanation;
- a recommended next action;
- an original source citation;
- Save and Not relevant controls.

### Tech Feed

A broader technical feed with filters for GitHub, research, engineering, and
release signals. Search narrows the feed to a technology, problem, or
implementation pattern.

### Research

Research cards are structured around the parts that help a practitioner decide
whether a paper is worth their time:

~~~text
problem → method → limitations → practical value → source
~~~

### GitHub Radar

Relevant repositories, releases, languages, stars, and recent public activity.
Matches are tied back to the profile rather than shown as a generic trending
list.

### Real Problems, Real Solutions

Engineering case studies are organized as:

~~~text
problem → approach → stack → trade-offs → outcome → source → relevance
~~~

This makes the section useful as an implementation-pattern library, not just a
collection of blog links.

### Ask SignalStack

Users can ask a technical question from the workspace. The FastAPI service
retrieves matching technical documents and returns a grounded answer with the
retrieved source links. When evidence is insufficient, the service says so
instead of manufacturing certainty.

## Current MVP capabilities

| Capability | Current local implementation |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, responsive dark UI |
| UI behavior | Multi-view workspace, filters, search, reasoning modal, feedback, saved state |
| Icons and forms | Lucide React, React Hook Form, Zod validation |
| Resume parsing | PDF with pypdf; DOCX with python-docx; TXT with UTF-8 extraction |
| Profile inference | Technical skills, project signals, and topic candidates |
| GitHub context | Optional username capture and public API enrichment route |
| Source ingestion | Public GitHub and arXiv adapter examples in FastAPI |
| Persistence | Local SQLite profile and normalized-document store |
| Retrieval | Dependency-free hashed-token similarity baseline |
| Grounded Q&A | FastAPI retrieval endpoint returning answer text and citations |
| Infrastructure | Docker Compose with web, API, and PostgreSQL + pgvector |
| Tests | Backend retrieval, grounded-answer, and explanation tests |

The dashboard ships with curated normalized example signals so it remains useful
immediately after onboarding. Resume analysis and Ask SignalStack are wired to
the local FastAPI service. The ingestion service can refresh live public
GitHub and arXiv examples through /ingest/refresh.

## Architecture

~~~text
┌──────────────────────────────────────────────────────────┐
│ Next.js workspace                                        │
│ onboarding · For You · Tech Feed · Research · Radar      │
│ solutions · saved feedback · grounded question flow      │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼───────────────────────────────┐
│ FastAPI service                                          │
│ resume extraction · profile inference · ingestion         │
│ retrieval · ranking · source-backed answers               │
└───────────────┬──────────────────────────┬───────────────┘
                │                          │
┌───────────────▼───────────────┐  ┌──────▼────────────────┐
│ SQLite local store             │  │ Public source adapters │
│ profiles · documents           │  │ GitHub · arXiv         │
└───────────────────────────────┘  └────────────────────────┘
~~~

### Personalization flow

~~~text
resume / GitHub / interests
            ↓
skills · projects · topics · profile context
            ↓
normalized source documents
            ↓
keyword and similarity retrieval
            ↓
source-quality and profile-overlap ranking
            ↓
explanation + next action + citation
~~~

The retrieval module has a stable interface so the local baseline can be
replaced with a production hybrid stack:

~~~text
BM25 exact retrieval + pgvector similarity
                    ↓
metadata filters + freshness + source credibility
                    ↓
feedback-aware reranking
~~~

## Repository layout

~~~text
.
├── app/                    # Next.js app router UI
│   ├── page.tsx            # SignalStack workspace and onboarding
│   ├── globals.css         # Dark theme, responsive layout, components
│   └── api/github/         # Public GitHub enrichment route
├── backend/
│   ├── app/main.py         # FastAPI routes and resume extraction
│   ├── app/corpus.py       # Curated normalized source documents
│   ├── app/ingestion.py    # GitHub and arXiv adapters
│   ├── app/rag.py          # Query construction and grounded answers
│   ├── app/retrieval.py    # Local retrieval baseline
│   ├── app/ranking.py      # Source-weighted recommendation ranking
│   ├── app/store.py        # SQLite persistence
│   └── tests/              # Backend retrieval tests
├── docs/                   # Architecture and API documentation
├── public/favicon.svg      # SignalStack favicon
├── docker-compose.yml      # Local web/API/PostgreSQL stack
├── .env.example            # Environment variable template
└── package.json            # Frontend scripts and dependencies
~~~

## Tech stack

### Frontend

- Next.js 15
- React 19
- TypeScript
- Lucide React
- React Hook Form
- Zod
- CSS theme tokens for the local responsive UI

### Backend

- Python
- FastAPI
- Pydantic-compatible request shapes
- SQLite local persistence
- pypdf and python-docx resume extraction
- GitHub public API and arXiv ingestion examples

### Retrieval and infrastructure

- Local hashed-token similarity baseline
- PostgreSQL + pgvector service in Docker Compose for the upgrade path
- Docker and Docker Compose
- Environment-variable configuration

## Run locally

Install frontend dependencies from the repository root:

~~~powershell
npm install
~~~

Start the frontend:

~~~powershell
npm run dev -- -H 127.0.0.1 -p 5173
~~~

Start the API in a second terminal:

~~~powershell
python -m pip install -r backend/requirements.txt
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

Open http://127.0.0.1:5173.

### Try the product

1. Enter interests such as AI agents, Python, RAG, and vector search.
2. Optionally attach a PDF, DOCX, or TXT resume.
3. Optionally enter a public GitHub username.
4. Select Preview my signal profile.
5. Review the inferred skills, project signals, and topics.
6. Select Looks right — build my briefing.
7. Explore the workspace views and open recommendation reasoning.
8. Open Ask SignalStack to try a source-backed question.

Profile state is stored in browser local storage for this local MVP. Use the
profile control in the sidebar to delete it from the current browser.

## Docker Compose

~~~powershell
docker compose up --build
~~~

Services:

| Service | Local port | Purpose |
|---|---:|---|
| web | 3000 | Next.js production server |
| profile-api | 8000 | FastAPI profile, ingestion, and retrieval service |
| postgres | 5432 | PostgreSQL + pgvector upgrade path |

Redis is intentionally excluded because there is no active worker or queue
implementation in this MVP.

## API reference

Base URL: http://127.0.0.1:8000

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Check service health |
| POST | /profile/resume | Extract and analyze a PDF, DOCX, or TXT resume |
| PUT | /profiles/{profile_id} | Persist profile skills, projects, and topics |
| GET | /profiles/{profile_id} | Read a persisted local profile |
| POST | /briefing | Retrieve ranked signals for a profile |
| POST | /rag/ask | Return a grounded answer and retrieved citations |
| POST | /ingest/refresh | Refresh public GitHub and arXiv examples |

Example grounded question:

~~~powershell
curl.exe -X POST http://127.0.0.1:8000/rag/ask `
  -H "Content-Type: application/json" `
  -d '{"question":"How should I evaluate a technical RAG pipeline?","profile":{"topics":["RAG","vector search"],"skills":["Python"]}}'
~~~

## Testing and verification

Run the backend tests:

~~~powershell
cd backend
python -m unittest discover -s tests
~~~

The current suite covers:

- retrieval of a relevant agent-workflow document;
- source-backed grounded answers;
- explanation presence on briefing recommendations.

The local frontend route was verified with a successful HTTP 200 response. The
Next.js app compiled and type-checked successfully during development.

## Privacy and source integrity

- Resume analysis is sent only to the local FastAPI service during local use.
- Profile state is stored locally in the browser for the MVP.
- Public GitHub context is optional.
- Source URLs are preserved in returned citations.
- The Q&A path reports insufficient evidence instead of inventing a source.
- Community and generated claims should not be treated as primary evidence.

## Honest MVP boundary

This repository is a functional local MVP, not a production SaaS deployment.
The following pieces are intentionally documented as upgrade paths:

- owner-scoped authentication and secure password storage;
- encrypted object storage for uploaded resumes;
- PostgreSQL-backed application persistence;
- Sentence Transformers embeddings in pgvector;
- BM25 + vector hybrid retrieval at scale;
- scheduled background ingestion workers;
- production LLM provider abstraction and observability;
- Precision@K, Recall@K, MRR, nDCG, latency, and source-coverage dashboards.

## Production roadmap

1. Add local email/password auth with owner-scoped access control.
2. Move profile and source persistence to PostgreSQL + pgvector.
3. Replace the local retrieval baseline with BM25 + Sentence Transformers.
4. Add scheduled ingestion, retries, deduplication clusters, and health metrics.
5. Add ranking evaluation against benchmark users and expected documents.
6. Add grounded LLM summaries with citation validation.
7. Add secure resume storage, deletion workflows, and observability.

## Resume-ready project description

> Built SignalStack, a local-first technical intelligence workspace with a
> Next.js and TypeScript frontend and FastAPI backend. Implemented resume-aware
> profile inference, explainable source ranking, GitHub/arXiv ingestion
> examples, structured research and engineering-solution views, and grounded
> technical Q&A with retrieved citations. Added responsive dark-mode UI,
> Docker Compose infrastructure, local persistence, and backend retrieval tests.

## License

This project is a personal local MVP. Add a license before distributing or
deploying it publicly.

# SignalStack local architecture

SignalStack is a local-first MVP with a Next.js 15 client and a FastAPI service.

```text
Next.js workspace
  ├─ onboarding + local profile state
  ├─ For You / Tech Feed / Research / GitHub Radar / Solutions views
  └─ Ask SignalStack client
          │ HTTP
          ▼
FastAPI profile + retrieval service
  ├─ PDF / TXT resume extraction (DOCX when python-docx is installed)
  ├─ public GitHub + arXiv refresh adapters
  ├─ local SQLite profile/document persistence
  └─ hashed-token retrieval baseline + source-backed answer API
```

The service keeps a stable document shape so the local retrieval interface can
be replaced with Sentence Transformers + PostgreSQL/pgvector without changing
the feed contract. The current MVP intentionally does not claim production
auth, hosted storage, background workers, or model-provider credentials.

## Data flow

1. A user enters technical interests and optionally uploads a resume.
2. The service extracts skills, project signals, and topic candidates.
3. The user reviews the inferred profile before it is stored in local browser
   storage and can remove it from the sidebar profile control.
4. Briefing cards are ranked from normalized source documents and show the
   matched reason, next action, and canonical source link.
5. Ask SignalStack retrieves matching documents and returns the answer with
   citations. Insufficient evidence is stated explicitly by the API.

## Production upgrade path

- Replace the SQLite store with PostgreSQL and `pgvector`.
- Add Sentence Transformers embeddings alongside BM25 exact retrieval.
- Add owner-scoped auth and encrypted object storage for resumes.
- Move ingestion to a real scheduled worker implementation.
- Add ranking telemetry for Precision@K, Recall@K, MRR, nDCG, latency, and
  source coverage against the benchmark corpus.

# SignalStack

Status: first build scaffold started.

## Current MVP

The current build includes a Next.js user interface and a FastAPI profile service.

- Resume upload accepts PDF and TXT files and extracts readable text with `pypdf`.
- The profile service finds declared technical skills, project signals, and topic candidates.
- A public GitHub username is enriched through GitHub's public API, returning repository count and languages.
- The ranking API produces GitHub, research, and engineering recommendations from profile topics, with a confidence score and an explicit reason for every signal.
- The RAG API retrieves the most relevant technical documents for a user question and returns a grounded answer together with the source links it used.
- Profiles and ingested documents persist locally in SQLite for the MVP; Docker Compose provides the PostgreSQL + pgvector upgrade path.
- `POST /ingest/refresh` retrieves public GitHub repository results and arXiv papers for up to three technical topics and stores them for later briefing and RAG retrieval.
- The dashboard lets users filter signals, save items, and inspect the explanation behind a recommendation.

### Run locally

Start the website:

```bash
npm install
npm run dev -- -H 127.0.0.1 -p 5173
```

Start the profile service in a separate terminal:

```bash
python -m pip install -r backend/requirements.txt
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

For the production-shaped local stack, use Docker Compose. It defines the web app, FastAPI service, PostgreSQL with pgvector, and Redis:

```bash
docker compose up --build
```

### RAG design

The MVP has a working retrieval-augmented answer path:

```text
Resume / GitHub / chosen interests
        ↓
Profile skills, project text, and topics
        ↓
Retrieve matching technical documents
        ↓
Rank by retrieval similarity + source credibility
        ↓
Grounded answer with explicit source links
```

For local development, retrieval uses a dependency-free hashed-token cosine
baseline. It keeps the app runnable without an embedding API key. The document
shape and retrieval interface are designed to be replaced by production
embeddings stored in PostgreSQL + pgvector; that is the deployment path for
semantic matching at scale.

Run the backend tests:

```bash
cd backend
python -m unittest discover -s tests
```

### API operations

```text
POST /profile/resume      Analyze a PDF/TXT resume
PUT  /profiles/{id}       Persist a user's extracted skills, projects, and topics
GET  /profiles/{id}       Read a persisted profile
POST /ingest/refresh      Fetch current public GitHub and arXiv source documents
POST /briefing            Retrieve a relevance-ranked technical briefing
POST /rag/ask             Ask a grounded question and receive source citations
```

The ingestion endpoint intentionally reports provider failures per source rather
than failing the whole request. GitHub's public API is rate-limited when no user
token is configured; a production deployment should use a server-side GitHub
token and add scheduled workers, retry policies, and source-specific terms of
use handling.

> A deeply personalized, tech-only intelligence feed for people who want to know what matters in technology — not what is merely popular.

SignalStack brings together technical research, GitHub activity, release notes, engineering blogs, trusted tech reporting, and approved developer-community signals. It filters that information into a high-confidence feed based on each user's technical interests, tools, and areas of work.

Every item answers two questions:

1. **What happened?**
2. **Why does it matter to me?**

The product does not try to be a teacher, a career coach, or a general-news app. It is a better technology-news website: personal, evidence-backed, and designed to reduce noise.

---

## The problem

Technology changes too quickly for anyone to follow manually. Important updates are spread across GitHub, research papers, company blogs, release notes, technical publications, developer communities, and social platforms.

Existing feeds mostly rank content by popularity. Popularity is not relevance. A small GitHub project, an IEEE paper, or a breaking release note may matter far more to one person than a viral headline.

SignalStack exists to make the useful signal easy to find.

---

## Product principles

- **Tech only.** No general news, politics, lifestyle content, or generic career content.
- **Personal relevance beats popularity.** A low-profile but highly relevant paper should outrank a broad trending story.
- **Evidence before hype.** Prefer original sources, clearly label source type, and link every claim to its source.
- **Explain every recommendation.** Users should always see why an item appeared in their feed.
- **Fewer, better updates.** A short, trustworthy briefing is more valuable than an endless stream.
- **User control is mandatory.** Users can change interests, mute topics, follow sources, and mark results as irrelevant at any time.
- **No black-box certainty.** The system makes its inferred interests visible and correctable.

---

## Who it is for

- Software engineers and developers
- AI, ML, data, cloud, and cybersecurity practitioners
- Technical founders and product builders
- Researchers and students following technical fields
- Open-source contributors
- Anyone who wants a high-signal view of a specific area of technology

Users do not need a GitHub account. They can begin by selecting topics, technologies, companies, and interests. Optional integrations can improve personalization.

---

## What users see

### Your Briefing

A daily or weekly collection of the highest-confidence updates for the user. It should be small, scannable, and useful.

Each card includes:

- title and short summary;
- source and publication date;
- content type: release, paper, GitHub project, engineering story, security notice, or reported news;
- a clear **Why you're seeing this** explanation;
- original-source links;
- save, share, follow, and `Not relevant` actions.

### Research

Relevant technical papers from permitted research sources, including arXiv and publisher/index sources such as IEEE where access and licensing allow it. Each paper card explains:

- the problem it addresses;
- the core method;
- results and limitations;
- whether it appears research-only or practical today;
- related code, repositories, or implementation links when available.

### GitHub Radar

Relevant repositories, releases, security advisories, changelogs, and rapidly developing open-source projects.

Useful signals include:

- releases from followed repositories;
- meaningful dependency or breaking changes;
- new projects related to followed technology or problems;
- security-relevant updates;
- high-quality repositories connected to papers or engineering stories.

### Real Problems, Real Solutions

This is a core feature, not an optional blog section. It turns real technical work into structured, useful cards:

```text
The real-world problem
↓
Who solved it
↓
Their technical approach
↓
Technologies used
↓
Outcome and trade-offs
↓
Original sources
↓
Why it may matter to this user
```

Sources can include engineering blogs, technical postmortems, open-source README files, conference talks, public architecture write-ups, research papers, and product engineering announcements.

### Similar Work

Surfaces repositories, papers, products, or technical write-ups that overlap with a user's interests. The relationship must be explicit:

- **Inspiration** — similar problem, different approach
- **Useful building block** — likely reusable code, tool, or pattern
- **Related research** — promising idea or method
- **Alternative** — different technology solving the same need
- **Competitor/overlap** — similar technical product or capability

### Technology Watchlists

Users can follow technologies, companies, repositories, topics, or technical concepts, for example:

```text
React · Python · PostgreSQL · Kubernetes · AI agents · observability
OpenAI · Vercel · Cloudflare · OWASP · Apache Kafka
```

They can also explicitly hide things they do not want, such as crypto, consumer gadgets, or startup-funding coverage.

### Catch-up Timeline

When a user returns after days or weeks away, SignalStack summarizes meaningful developments in their selected areas rather than showing every missed item.

---

## Personalization and accuracy

Accuracy is the product. It cannot be reduced to keyword matching or a single AI prompt.

### 1. Build an editable interest map

At onboarding, users choose topics and technologies. Optional connections and user-provided context can improve this map, but every inference must be visible and editable.

```text
Topics:        AI agents, frontend engineering, application security
Technologies:  TypeScript, React, Python, PostgreSQL
Following:     GitHub, OWASP, Vercel
Preferences:   practical releases, research, engineering case studies
Muted:         crypto, generic startup coverage
```

The map changes over time from explicit feedback such as `More like this`, `Not relevant`, `I no longer use this`, and `Follow this technology`.

### 2. Normalize every source item

Each item is converted into a consistent internal record:

```text
What happened:        A durable-workflow feature was released
Content type:         Official release
Technologies:         Python, agent orchestration
Problems addressed:   retries, state persistence, reliability
Audience:             Teams building multi-step AI applications
Maturity:             Experimental / production-ready / unclear
Evidence:             Original release notes and documentation
```

### 3. Retrieve broadly, rank carefully

Semantic search finds conceptually related material; exact keyword and technology matching catches precise dependencies. Both are necessary.

```text
Final relevance score =
  semantic similarity
+ topic and technology overlap
+ user feedback affinity
+ freshness and importance
+ source credibility
+ novelty
- duplicate/noise penalty
- low-confidence penalty
```

### 4. Verify and deduplicate

- Prefer primary sources over commentary.
- Group multiple stories that report the same underlying event.
- Preserve original links and cite evidence in summaries.
- Do not present community claims as verified facts.
- Apply different confidence thresholds to research, releases, security information, and reporting.

### 5. Explain the match

Every recommendation needs a human-readable reason, for example:

> Shown because you follow PostgreSQL and vector search. This official update adds a capability relevant to semantic retrieval workloads.

If the explanation is weak, the item should not be shown prominently.

### 6. Learn from feedback, not only clicks

Clicks are weak signals. Stronger signals include saving, following, dismissing, muting, and explicit corrections. Feedback must be easy to give and easy to undo.

---

## Sources

### Initial source categories

1. **Primary technical sources**
   - official company engineering blogs and documentation
   - official product and release notes
   - GitHub repositories, releases, and security advisories
   - public research archives and permitted publisher/index metadata

2. **Trusted technical reporting**
   - selected technology publications and newsletters
   - technical podcasts or talks with structured metadata where permitted

3. **Developer-community signals**
   - approved APIs and public feeds from communities such as Hacker News, Reddit, Dev.to, or social platforms
   - these are supporting signals, never the sole evidence for a factual claim

### Access and licensing rules

- Use official APIs, RSS/Atom feeds, licenses, and user-authorized integrations where available.
- Do not bypass paywalls, scrape restricted services, or store copyrighted full text without permission.
- For sources such as Google Scholar, IEEE, X/Twitter, or LinkedIn, use permitted access methods, public metadata, and links to original content according to their terms.
- Store source attribution, canonical URL, publication date, and access rights with every item.

---

## Technical architecture

```text
                         ┌─────────────────────────────┐
                         │       Next.js web app        │
                         │ feed · search · settings     │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │ API + PostgreSQL + pgvector  │
                         │ users · items · feedback     │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │       Job queue/scheduler     │
                         └──────────────┬──────────────┘
                                        │
       ┌────────────────────────────────┼────────────────────────────────┐
       ▼                                ▼                                ▼
┌───────────────┐              ┌────────────────┐              ┌────────────────┐
│ Source adapters│              │ AI enrichment  │              │ Ranking engine │
│ API/RSS/GitHub │              │ classify/embed │              │ match/rerank   │
└───────────────┘              └────────────────┘              └────────────────┘
       │                                │                                │
       └────────────────────────────────┴────────────────────────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │ normalized, deduped items     │
                         └─────────────────────────────┘
```

### Recommended stack

| Layer | Choice | Responsibility |
|---|---|---|
| Web application | Next.js + TypeScript | Dashboard, onboarding, authentication flows, API routes, SEO pages |
| UI | Tailwind CSS + shadcn/ui | Accessible, responsive interface |
| API backend | FastAPI + Python | Feed APIs, ranking endpoints, item detail endpoints, user feedback endpoints |
| Database | PostgreSQL | Users, preferences, sources, items, saved collections, feedback |
| Vector search | pgvector | Meaning-based retrieval and similarity matching |
| Background workers | Python workers | Source ingestion, paper parsing, enrichment, scheduled jobs |
| Queue | Redis + a Python task queue | Reliable retries, rate limiting, and long-running work |
| Object storage | S3-compatible storage | Permitted snapshots, images, and generated assets |
| AI services | LLM + embedding provider | Structured extraction, summaries, similarity vectors, explanations |
| Observability | Error monitoring + metrics + tracing | Reliability, queue health, source failures, ranking evaluation |
| Deployment | Docker + Vercel/Railway | Containerized local dev, web deployment, and worker deployment |

### Why the system is split

The website must stay fast for users. Fetching feeds, respecting source rate limits, parsing papers, running enrichment, and calculating relevance happen in background workers. The web app reads completed, ranked results from the database.

### Resume-ready confirmed stack

This is the stack I would treat as the confirmed project stack for your resume:

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- FastAPI
- Python
- PostgreSQL
- pgvector
- Redis
- Docker
- GitHub APIs
- RSS/Atom feeds
- LLM and embedding APIs

That matches your current resume well because you already show Next.js, TypeScript, Python, FastAPI, PostgreSQL, Docker, and modern AI/project work.

---

## Core data model

```text
User
  └─ InterestProfile
      ├─ followed topics / technologies / companies / repositories
      ├─ muted topics
      ├─ explicit preferences
      └─ inferred interests with confidence and provenance

Source
  └─ SourceItem
      ├─ canonical URL, source type, access status, publication date
      ├─ normalized content and extracted entities
      ├─ embeddings and duplicate cluster
      └─ evidence links and confidence signals

User + SourceItem
  └─ Recommendation
      ├─ relevance score and rank
      ├─ why-this-matters explanation
      ├─ delivery state
      └─ user feedback
```

---

## MVP

The first release must prove that a smaller, personalized technical feed is genuinely better than generic news.

### Include

- account creation and simple onboarding;
- topic, technology, and source selection;
- personal feed with source links;
- `Why you're seeing this` on every card;
- save and `Not relevant` feedback;
- RSS/Atom and official engineering/blog sources;
- GitHub public repository/release ingestion;
- arXiv or another permitted open research source;
- basic deduplication, source labels, and daily digest;
- a first version of Real Problems, Real Solutions.

### Deliberately defer

- every possible research publisher;
- unrestricted social-platform ingestion;
- complicated profile integrations;
- team collaboration and enterprise controls;
- native mobile apps;
- broad alerts for low-confidence content;
- automated claims that a project is a direct competitor.

---

## Development roadmap

### Phase 1 — Useful personal feed

- Ship onboarding, watchlists, sources, basic ranking, and web feed.
- Start with high-quality primary sources.
- Instrument feedback and feed-quality metrics from day one.

### Phase 2 — Intelligence layer

- Add semantic matching and structured AI enrichment.
- Improve deduplication and original-source clustering.
- Introduce paper summaries, GitHub Radar, and solution cards.

### Phase 3 — Trust and depth

- Add confidence labels, richer evidence views, and user controls.
- Connect papers to code, releases, and case studies.
- Add catch-up timelines and high-confidence alerts.

### Phase 4 — Paid product and teams

- Add Pro watchlists, deep analysis, custom alerts, and private collections.
- Add shared team watchlists, shared collections, and team digests only after the individual product is trusted.

---

## Business model

### Free

- Basic personalized briefing
- Limited tracked technologies/topics
- Saved items
- Access to original sources

### Pro

- Unlimited watchlists
- Research and GitHub intelligence
- Deep solution analysis
- Advanced filters and custom alerts
- Weekly catch-up/intelligence report
- Private collections and exports

### Team (later)

- Shared watchlists and collections
- Team-specific source tracking
- Shared digests
- Admin, access, and billing controls

The paid value is not more articles. It is better relevance, less time spent filtering, and deeper technical context.

---

## Measuring success

The north-star question is:

> Was this item worth interrupting the user for?

Track:

- relevance rate: saved/followed items versus dismissed items;
- explanation quality: how often users agree with `Why you're seeing this`;
- duplicate rate;
- source freshness and ingestion health;
- return rate for daily/weekly briefings;
- time-to-useful-first-feed after onboarding;
- qualitative feedback from early users.

Do **not** optimize primarily for scroll time, page views, or sensational clicks.

---

## Safety, privacy, and trust

- Collect only the information needed for personalization.
- Make connected accounts optional and revokeable.
- Encrypt tokens and follow least-privilege access.
- Explain what data influences recommendations.
- Never expose one user's interests, integrations, or saved items to another user.
- Respect source terms, attribution, licenses, rate limits, and robots policies.
- Clearly separate original facts from model-generated summaries or inferences.

---

## Landing-page message

### Headline

**Tech news that understands what matters to you.**

### Supporting copy

Follow research, GitHub, releases, engineering stories, and trusted technical news in one personalized feed. See what changed, why it matters, and how other people solved real technology problems.

### Three promises

1. **Follow your technical world** — Choose the technologies, problems, projects, companies, and fields you care about.
2. **See the useful signal** — Get evidence-backed updates, not a flood of links.
3. **Learn from real implementations** — Discover how engineers, researchers, and open-source builders solved real problems.

---

## Project status

This repository is the starting point for SignalStack. The immediate goal is an MVP that users can trust: a highly relevant, tech-only feed built from a small number of strong sources, transparent explanations, and continuous feedback.

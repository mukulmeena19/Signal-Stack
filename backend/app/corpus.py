"""Curated source documents used by the local RAG demonstration.

In production this module is replaced by ingestion workers that write the same
document shape to PostgreSQL + pgvector. Keeping a stable schema here makes the
retrieval and ranking paths testable without external API credentials.
"""

DOCUMENTS = [
    {
        "id": "github-agent-checkpoints",
        "title": "Reliable checkpoints for long-running agent workflows",
        "source": "GitHub",
        "source_type": "github",
        "kind": "Try this",
        "url": "https://github.com/",
        "tags": ["ai agents", "python", "workflow", "reliability"],
        "content": "Open-source agent workflow systems can persist task state, resume interrupted work, and retry failed steps. Checkpoints make long-running Python agent workflows more reliable and easier to debug.",
        "action": "Compare checkpoint state, retry rules, and observability against the workflow orchestration your project needs.",
    },
    {
        "id": "research-retrieval-eval",
        "title": "Evaluation-driven retrieval for technical RAG",
        "source": "Research",
        "source_type": "research",
        "kind": "Learn this",
        "url": "https://arxiv.org/",
        "tags": ["rag", "vector search", "llm", "evaluation"],
        "content": "Technical retrieval systems should measure evidence quality before generation. Retrieval evaluation can detect missing context, irrelevant chunks, and unsupported answers before an LLM produces a response.",
        "action": "Use retrieval precision, evidence coverage, and grounded-answer checks to create an offline relevance benchmark.",
    },
    {
        "id": "engineering-dedup",
        "title": "Keeping a high-volume engineering feed fresh and deduplicated",
        "source": "Engineering blog",
        "source_type": "engineering",
        "kind": "Real-world solution",
        "url": "https://martinfowler.com/",
        "tags": ["python", "web apps", "postgresql", "ingestion"],
        "content": "Feed systems avoid duplicates with normalized canonical URLs, content fingerprints, source-specific rules, and freshness windows. A review queue handles low-confidence matches instead of silently deleting them.",
        "action": "Start with canonical URLs plus text fingerprints, then record every merge decision for later ranking feedback.",
    },
    {
        "id": "release-vector-filtering",
        "title": "Hybrid search improves technical-document retrieval",
        "source": "Release notes",
        "source_type": "release",
        "kind": "Try this",
        "url": "https://github.com/pgvector/pgvector",
        "tags": ["vector search", "postgresql", "rag", "search"],
        "content": "Hybrid retrieval combines keyword matching with vector similarity. Keywords keep exact technology names precise while embeddings surface conceptually related papers, repositories, and engineering posts.",
        "action": "Use hybrid retrieval with metadata filters for source type, publication date, and credibility instead of vector similarity alone.",
    },
]

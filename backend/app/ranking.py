from datetime import datetime, timezone

SOURCE_WEIGHTS = {"github": 0.92, "research": 0.96, "engineering": 0.9, "release": 0.88}

SEED_SIGNALS = [
    {"id": "github-agent-checkpoints", "title": "Reliable checkpoints for long-running agent workflows", "source": "GitHub", "source_type": "github", "kind": "Try this", "tags": ["ai agents", "python", "workflow"], "summary": "An open-source release adds recoverable state and retry patterns for multi-step agent tasks.", "action": "Compare its state model with the workflow orchestration your project needs."},
    {"id": "research-retrieval-eval", "title": "Evaluation-driven retrieval for technical RAG", "source": "Research", "source_type": "research", "kind": "Learn this", "tags": ["rag", "vector search", "llm"], "summary": "A paper evaluates retrieval quality before generation to reduce irrelevant technical answers.", "action": "Use its evaluation framing to create an offline relevance benchmark."},
    {"id": "engineering-dedup", "title": "Keeping a high-volume engineering feed fresh and deduplicated", "source": "Engineering blog", "source_type": "engineering", "kind": "Real-world solution", "tags": ["python", "web apps", "postgresql"], "summary": "A team combines source-specific fingerprints, freshness windows, and review rules to remove duplicates.", "action": "Review the trade-offs before choosing the initial ingestion architecture."},
]


def rank_signals(topics: list[str]) -> list[dict]:
    normalized_topics = {topic.lower() for topic in topics}
    ranked = []
    for signal in SEED_SIGNALS:
        matched = [tag for tag in signal["tags"] if tag in normalized_topics]
        relevance = len(matched) / max(len(signal["tags"]), 1)
        confidence = round((0.55 * relevance + 0.45 * SOURCE_WEIGHTS[signal["source_type"]]) * 100)
        if matched:
            ranked.append({
                **signal,
                "confidence": confidence,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "why": f"Matched your profile through: {', '.join(matched)}.",
            })
    return sorted(ranked, key=lambda item: item["confidence"], reverse=True)

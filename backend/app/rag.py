from .corpus import DOCUMENTS
from .retrieval import retrieve

SOURCE_WEIGHTS = {"github": 0.92, "research": 0.96, "engineering": 0.90, "release": 0.88}


def build_query(profile: dict, question: str = "") -> str:
    skills = profile.get("skills", [])
    projects = profile.get("projects", [])
    topics = profile.get("topics", [])
    return " ".join([question, *map(str, skills), *map(str, projects), *map(str, topics)])


def grounded_answer(question: str, matches: list[dict]) -> str:
    if not matches:
        return "No sufficiently relevant source was retrieved. Add more profile detail or broaden the source set."
    titles = "; ".join(match["title"] for match in matches[:2])
    if question.strip():
        return f"Based on the retrieved technical sources, the strongest evidence is: {titles}. Review the cited sources before making an implementation decision."
    return f"Your briefing was built from the most relevant retrieved sources: {titles}."


def retrieve_briefing(profile: dict, limit: int = 8) -> dict:
    query = build_query(profile)
    matches = retrieve(query, DOCUMENTS, limit)
    signals = []
    normalized = {str(topic).lower() for topic in profile.get("topics", []) + profile.get("skills", [])}
    for match in matches:
        overlap = [tag for tag in match["tags"] if tag.lower() in normalized]
        relevance = match["retrieval_score"]
        credibility = SOURCE_WEIGHTS[match["source_type"]]
        confidence = round(min(99, (0.68 * relevance + 0.32 * credibility) * 100))
        signals.append({
            **match,
            "confidence": confidence,
            "why": f"Retrieved because it overlaps with {', '.join(overlap) if overlap else 'your profile context'}.",
        })
    return {"query": query, "signals": signals, "answer": grounded_answer("", matches)}


def answer_question(profile: dict, question: str) -> dict:
    query = build_query(profile, question)
    matches = retrieve(query, DOCUMENTS, 4)
    return {
        "answer": grounded_answer(question, matches),
        "sources": [{"id": item["id"], "title": item["title"], "source": item["source"], "url": item["url"], "score": item["retrieval_score"]} for item in matches],
    }

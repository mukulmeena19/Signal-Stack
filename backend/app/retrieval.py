"""Dependency-free retrieval baseline for local development.

It uses hashed token vectors and cosine similarity. The interface deliberately
matches an embedding store so it can be swapped for pgvector + production
embeddings without changing the API or ranking layer.
"""

from collections import Counter
from hashlib import blake2b
import math
import re

DIMENSIONS = 512
STOP_WORDS = {"a", "an", "and", "are", "for", "from", "how", "in", "is", "of", "on", "or", "the", "this", "to", "with", "what", "using"}


def tokenize(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9+#.]{2,}", text.lower()) if word not in STOP_WORDS]


def vectorize(text: str) -> Counter[int]:
    vector: Counter[int] = Counter()
    for token in tokenize(text):
        index = int.from_bytes(blake2b(token.encode(), digest_size=4).digest(), "big") % DIMENSIONS
        vector[index] += 1
    return vector


def cosine(left: Counter[int], right: Counter[int]) -> float:
    numerator = sum(weight * right.get(index, 0) for index, weight in left.items())
    if not numerator:
        return 0.0
    left_length = math.sqrt(sum(weight * weight for weight in left.values()))
    right_length = math.sqrt(sum(weight * weight for weight in right.values()))
    return numerator / (left_length * right_length) if left_length and right_length else 0.0


def retrieve(query: str, documents: list[dict], limit: int = 5) -> list[dict]:
    query_vector = vectorize(query)
    matches = []
    for document in documents:
        searchable = " ".join([document["title"], document["content"], *document.get("tags", [])])
        score = cosine(query_vector, vectorize(searchable))
        if score > 0:
            matches.append({**document, "retrieval_score": round(score, 4)})
    return sorted(matches, key=lambda item: item["retrieval_score"], reverse=True)[:limit]

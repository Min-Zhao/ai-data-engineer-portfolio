from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from .schemas import ResearchDocument, SearchHit

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9\-]+")
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "research_corpus.json"


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def term_vector(text: str) -> Counter[str]:
    tokens = tokenize(text)
    counts = Counter(tokens)
    if not tokens:
        return counts
    for token in list(counts):
        counts[token] = counts[token] / len(tokens)
    return counts


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    numerator = sum(left[token] * right.get(token, 0.0) for token in left)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


@lru_cache(maxsize=1)
def load_documents() -> list[ResearchDocument]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return [ResearchDocument(**item) for item in json.load(handle)]


@lru_cache(maxsize=1)
def indexed_documents() -> list[tuple[ResearchDocument, Counter[str]]]:
    return [(doc, term_vector(f"{doc.title} {doc.section} {doc.text} {' '.join(doc.tags)}")) for doc in load_documents()]


def search_documents(query: str, top_k: int = 5) -> list[SearchHit]:
    query_vector = term_vector(query)
    ranked: list[SearchHit] = []

    for document, document_vector in indexed_documents():
        score = cosine_similarity(query_vector, document_vector)
        keyword_boost = sum(0.025 for token in set(tokenize(query)) if token in document.tags)
        score = min(score + keyword_boost, 1.0)
        if score > 0:
            ranked.append(
                SearchHit(
                    id=document.id,
                    title=document.title,
                    section=document.section,
                    text=document.text,
                    tags=document.tags,
                    source=document.source,
                    score=round(score, 4),
                )
            )

    return sorted(ranked, key=lambda hit: hit.score, reverse=True)[:top_k]


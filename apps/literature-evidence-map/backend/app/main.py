from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "papers.json"


class Paper(BaseModel):
    id: str
    title: str
    therapeutic_area: str
    abstract: str
    mechanisms: list[str]
    biomarkers: list[str]
    evidence_level: str


class EvidenceQuery(BaseModel):
    query: str = Field(min_length=3)
    therapeutic_area: str | None = None


class EvidenceCluster(BaseModel):
    label: str
    paper_ids: list[str]
    rationale: str


class EvidenceResponse(BaseModel):
    query: str
    papers: list[Paper]
    clusters: list[EvidenceCluster]
    gaps: list[str]


app = FastAPI(title="Literature Evidence Map", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_papers() -> list[Paper]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return [Paper(**paper) for paper in json.load(handle)]


def score_paper(query: str, paper: Paper) -> int:
    tokens = {token.lower() for token in query.replace("-", " ").split()}
    haystack = " ".join(
        [paper.title, paper.abstract, paper.therapeutic_area, *paper.mechanisms, *paper.biomarkers]
    ).lower()
    return sum(1 for token in tokens if token in haystack)


@app.get("/api/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "papers": len(load_papers())}


@app.post("/api/evidence", response_model=EvidenceResponse)
def evidence(request: EvidenceQuery) -> EvidenceResponse:
    papers = [
        paper
        for paper in load_papers()
        if request.therapeutic_area is None
        or paper.therapeutic_area.lower() == request.therapeutic_area.lower()
    ]
    ranked = sorted(papers, key=lambda paper: score_paper(request.query, paper), reverse=True)[:6]
    relevant = [paper for paper in ranked if score_paper(request.query, paper) > 0] or ranked[:3]

    clusters = [
        EvidenceCluster(
            label=mechanism,
            paper_ids=[paper.id for paper in relevant if mechanism in paper.mechanisms],
            rationale=f"Groups papers that discuss {mechanism} as a mechanism or intervention axis.",
        )
        for mechanism in sorted({item for paper in relevant for item in paper.mechanisms})
    ]
    clusters = [cluster for cluster in clusters if cluster.paper_ids]

    gaps = [
        "Add full-text ingestion and access-control metadata before internal deployment.",
        "Validate cluster labels with scientist review sets.",
        "Track contradictory findings separately from supportive evidence.",
    ]
    return EvidenceResponse(query=request.query, papers=relevant, clusters=clusters, gaps=gaps)


from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "assays.json"


class Assay(BaseModel):
    id: str
    name: str
    target: str
    modality: str
    cost: int
    turnaround_days: int
    confidence: float
    decision_value: float
    risk: str


class PrioritizationRequest(BaseModel):
    target: str | None = None
    max_turnaround_days: int = Field(default=21, ge=1, le=90)
    budget: int = Field(default=50000, ge=1000)
    priority: str = "decision_value"


class PrioritizedAssay(Assay):
    priority_score: float
    rationale: str


class PrioritizationResponse(BaseModel):
    selected: list[PrioritizedAssay]
    deferred: list[PrioritizedAssay]
    summary: str
    operating_constraints: list[str]


app = FastAPI(title="Assay Prioritization Console", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://127.0.0.1:5175"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_assays() -> list[Assay]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return [Assay(**assay) for assay in json.load(handle)]


def compute_score(assay: Assay, priority: str) -> float:
    speed = max(0.1, 1 - assay.turnaround_days / 60)
    affordability = max(0.1, 1 - assay.cost / 70000)
    if priority == "speed":
        return round((speed * 0.5) + (assay.confidence * 0.25) + (assay.decision_value * 0.25), 4)
    if priority == "confidence":
        return round((assay.confidence * 0.5) + (assay.decision_value * 0.3) + (affordability * 0.2), 4)
    return round((assay.decision_value * 0.45) + (assay.confidence * 0.3) + (speed * 0.15) + (affordability * 0.1), 4)


@app.get("/api/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "assays": len(load_assays())}


@app.post("/api/prioritize", response_model=PrioritizationResponse)
def prioritize(request: PrioritizationRequest) -> PrioritizationResponse:
    assays = [
        assay
        for assay in load_assays()
        if request.target is None or assay.target.lower() == request.target.lower()
    ]
    ranked = sorted(
        [
            PrioritizedAssay(
                **assay.model_dump(),
                priority_score=compute_score(assay, request.priority),
                rationale=(
                    f"Balances {assay.decision_value:.0%} decision value, "
                    f"{assay.confidence:.0%} confidence, {assay.turnaround_days} day turnaround, "
                    f"and ${assay.cost:,} cost."
                ),
            )
            for assay in assays
        ],
        key=lambda item: item.priority_score,
        reverse=True,
    )

    selected: list[PrioritizedAssay] = []
    spent = 0
    for assay in ranked:
        if assay.turnaround_days <= request.max_turnaround_days and spent + assay.cost <= request.budget:
            selected.append(assay)
            spent += assay.cost

    selected_ids = {assay.id for assay in selected}
    deferred = [assay for assay in ranked if assay.id not in selected_ids]
    return PrioritizationResponse(
        selected=selected,
        deferred=deferred,
        summary=f"Selected {len(selected)} assays using ${spent:,} of ${request.budget:,}.",
        operating_constraints=[
            "Scores are transparent heuristics for portfolio triage, not validated scientific conclusions.",
            "Final assay plans require domain expert review and protocol feasibility checks.",
        ],
    )


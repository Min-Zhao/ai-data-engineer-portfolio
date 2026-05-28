from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchDocument(BaseModel):
    id: str
    title: str
    section: str
    text: str
    tags: list[str] = Field(default_factory=list)
    source: str = "demo-corpus"


class SearchRequest(BaseModel):
    query: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=12)


class SearchHit(BaseModel):
    id: str
    title: str
    section: str
    text: str
    tags: list[str]
    score: float
    source: str


class SearchResponse(BaseModel):
    query: str
    hits: list[SearchHit]


class ChatRequest(BaseModel):
    question: str = Field(min_length=3)
    project_context: str | None = None
    top_k: int = Field(default=5, ge=1, le=12)


class AgentStep(BaseModel):
    name: str
    role: str
    output: str
    citations: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    confidence: str
    evidence: list[SearchHit]
    agent_trace: list[AgentStep]
    follow_up_questions: list[str]


class WorkflowRequest(BaseModel):
    objective: str = Field(min_length=8)
    constraints: list[str] = Field(default_factory=list)
    top_k: int = Field(default=6, ge=1, le=12)


class WorkflowResponse(BaseModel):
    objective: str
    plan: list[AgentStep]
    risks: list[str]
    success_metrics: list[str]


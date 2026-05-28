from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .agents import build_research_workflow, synthesize_answer
from .retrieval import load_documents, search_documents
from .schemas import ChatRequest, ChatResponse, SearchRequest, SearchResponse, WorkflowRequest, WorkflowResponse

app = FastAPI(
    title="Pharma Research Agent Studio",
    description="RAG and agentic workflow API for drug-discovery research assistance.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "documents": len(load_documents())}


@app.post("/api/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    return SearchResponse(query=request.query, hits=search_documents(request.query, request.top_k))


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    evidence = search_documents(request.question, request.top_k)
    return synthesize_answer(request.question, evidence, request.project_context)


@app.post("/api/workflows", response_model=WorkflowResponse)
def workflows(request: WorkflowRequest) -> WorkflowResponse:
    return build_research_workflow(request.objective, request.constraints, request.top_k)


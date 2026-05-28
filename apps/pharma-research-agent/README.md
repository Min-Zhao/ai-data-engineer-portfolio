# Pharma Research Agent Studio

Production-style portfolio project for an **AI Data Engineer - LLMs / Agentic Systems** role in pharmaceutical research.

The app demonstrates a drug-discovery research assistant that combines a Python API, semantic retrieval, a small agentic workflow, cited responses, guardrail review, and a React/TypeScript interface for scientists.

## Why This Project Matches the Pfizer Posting

- **Python backend:** FastAPI service with typed Pydantic request and response models.
- **React + TypeScript frontend:** scientist-facing workflow UI with evidence, citations, and agent trace.
- **RAG architecture:** local research corpus, deterministic vector-like retrieval, top-k evidence ranking, and source metadata.
- **Agentic systems:** separated retriever, synthesizer, and reviewer roles to reduce unsupported scientific claims.
- **Pharma domain:** examples cover medicinal chemistry, target biology, ADME, assays, ELN ingestion, and cloud deployment.
- **Production signals:** tests, Dockerfile, Docker Compose, CI, CORS setup, health endpoint, and documented API.

This is a portfolio demo, not medical advice, clinical decision support, or a validated drug-discovery platform.

## Architecture

```text
frontend/ React + TypeScript + Vite
   |
   | /api/chat, /api/search, /api/workflows
   v
backend/ FastAPI + Pydantic
   |
   | deterministic local retrieval
   v
data/research_corpus.json
```

## Quick Start

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173).

## API Examples

```bash
curl http://127.0.0.1:8000/api/health
```

```bash
curl -s -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How should we triage EGFR resistance evidence for a new kinase series?",
    "project_context": "Medicinal chemistry team comparing potency, selectivity, and ADME tradeoffs.",
    "top_k": 5
  }'
```

## Docker

```bash
docker compose up --build
```

The API runs on [http://127.0.0.1:8000](http://127.0.0.1:8000), and the frontend runs on [http://127.0.0.1:5173](http://127.0.0.1:5173).

## Tests

```bash
cd backend
python3 -m pytest
```

## Next Production Steps

- Replace deterministic retrieval with OpenAI, Hugging Face, or Bedrock embeddings.
- Persist metadata in PostgreSQL and document chunks in S3 or an internal object store.
- Add a vector database such as pgvector, OpenSearch, Pinecone, Weaviate, or Qdrant.
- Add scientist-labeled evaluation sets for top-k precision and answer faithfulness.
- Add auth, access-control metadata, audit logging, and environment-specific deployment manifests.


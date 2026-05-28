# AI Data Engineer Portfolio: LLMs / Agentic Systems

The portfolio contains production-style full-stack applications with **Python backends** and **React frontends** for pharmaceutical research workflows: RAG, semantic search, agentic orchestration, evidence review, assay prioritization, and scientist-facing user experiences.

## Portfolio Applications

| Application | Backend | Frontend | What It Proves |
| --- | --- | --- | --- |
| [Pharma Research Agent Studio](apps/pharma-research-agent/README.md) | FastAPI, Pydantic, local retrieval, agent trace | React, TypeScript, Vite | RAG, cited LLM-style synthesis, agentic workflow, guardrail review |
| [Literature Evidence Map](apps/literature-evidence-map) | FastAPI evidence clustering API | React evidence mapping UI | Semantic literature triage, mechanism clustering, research gap surfacing |
| [Assay Prioritization Console](apps/assay-prioritization-console) | FastAPI scoring and optimization API | React decision dashboard | Scientific workflow translation, transparent ranking, assay operations UX |

## Alignment to the Job Posting

- **Production-grade full stack applications:** each app has a Python API, typed request/response models, React UI, tests, and documented startup.
- **Python backend frameworks:** FastAPI services model data processing, retrieval, orchestration, and ranking.
- **React and TypeScript frontends:** Vite-based scientist-facing interfaces for repeated research workflows.
- **RAG and semantic search:** retrieval over curated scientific corpora with source metadata and evidence surfacing.
- **Agentic LLM architectures:** retriever, synthesizer, reviewer, and workflow-planning roles are separated for traceability.
- **Scientific domain fluency:** examples use medicinal chemistry, ADME, target biology, assay transfer, biomarkers, and literature evidence.
- **Cloud and DevOps readiness:** Docker Compose, CI, health endpoints, and clear production next steps.

## Run Locally

Each app can be run independently. Example:

```bash
cd apps/pharma-research-agent/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
cd apps/pharma-research-agent/frontend
npm install
npm run dev
```

## Docker Compose

```bash
docker compose up --build
```

Services:

- Pharma API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Literature API: [http://127.0.0.1:8010](http://127.0.0.1:8010)
- Assay API: [http://127.0.0.1:8020](http://127.0.0.1:8020)

Frontend services are configured in each app on ports `5173`, `5174`, and `5175`.

## Portfolio Narrative

This portfolio is designed to show the role’s strongest hiring signals in a concrete way:

1. I can translate scientific workflows into working software.
2. I can build Python services that expose clean AI/data APIs.
3. I can create practical React interfaces for scientists, not just backend demos.
4. I understand RAG, evidence grounding, traceability, evaluation, and guardrails.
5. I know how to frame prototypes for production: tests, deployment shape, monitoring gaps, and next steps.

## Production Upgrade Roadmap

- Replace local deterministic retrieval with OpenAI, Hugging Face, or AWS Bedrock embeddings.
- Add pgvector, Qdrant, Weaviate, Pinecone, or OpenSearch for scalable similarity search.
- Persist metadata in PostgreSQL and source artifacts in S3.
- Add authentication, project-level authorization, and audit logging.
- Add scientist-labeled evaluation sets for retrieval precision, faithfulness, and workflow utility.
- Add GitHub Actions deployment to AWS ECS, App Runner, or Kubernetes.


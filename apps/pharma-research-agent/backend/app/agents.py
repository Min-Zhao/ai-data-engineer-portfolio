from __future__ import annotations

from .retrieval import search_documents
from .schemas import AgentStep, ChatResponse, SearchHit, WorkflowResponse

RISK_TERMS = {
    "clinical decision": "This tool is for research assistance, not clinical decision support.",
    "dose": "Dose recommendations require validated study protocols and expert review.",
    "patient": "Patient-specific guidance is out of scope for this research demo.",
}


def assess_risks(text: str) -> list[str]:
    normalized = text.lower()
    risks = [message for term, message in RISK_TERMS.items() if term in normalized]
    if "novel target" in normalized or "hypothesis" in normalized:
        risks.append("Generated hypotheses must be experimentally validated before use.")
    return risks


def synthesize_answer(question: str, evidence: list[SearchHit], project_context: str | None = None) -> ChatResponse:
    citations = [hit.id for hit in evidence[:3]]
    evidence_summary = "; ".join(f"{hit.title} ({hit.section})" for hit in evidence[:3])
    context_line = f" For the project context, prioritize: {project_context}." if project_context else ""

    if evidence:
        answer = (
            f"Based on the retrieved research notes, start with {evidence_summary}. "
            "The strongest next step is to combine semantic retrieval over assay, target, and "
            "ADME evidence with an agent that separates hypothesis generation from risk review."
            f"{context_line}"
        )
        confidence = "medium"
    else:
        answer = "I could not find enough grounded evidence in the current corpus to answer confidently."
        confidence = "low"

    trace = [
        AgentStep(
            name="retriever",
            role="Find scientific evidence",
            output=f"Retrieved {len(evidence)} relevant documents from the local vector index.",
            citations=[hit.id for hit in evidence],
        ),
        AgentStep(
            name="scientific_synthesizer",
            role="Translate evidence into research guidance",
            output=answer,
            citations=citations,
        ),
        AgentStep(
            name="risk_reviewer",
            role="Flag unsafe or unsupported claims",
            output="; ".join(assess_risks(question)) or "No high-risk research-assistance boundary detected.",
            citations=[],
        ),
    ]

    follow_ups = [
        "Which assay endpoint should be prioritized for the next experiment?",
        "Should the workflow optimize for potency, selectivity, ADME, or novelty?",
        "Which documents or ELN exports should be added to the private corpus next?",
    ]
    return ChatResponse(
        answer=answer,
        confidence=confidence,
        evidence=evidence,
        agent_trace=trace,
        follow_up_questions=follow_ups,
    )


def build_research_workflow(objective: str, constraints: list[str], top_k: int = 6) -> WorkflowResponse:
    evidence = search_documents(" ".join([objective, *constraints]), top_k=top_k)
    citations = [hit.id for hit in evidence[:4]]
    constraint_text = ", ".join(constraints) if constraints else "standard discovery constraints"

    plan = [
        AgentStep(
            name="corpus_builder",
            role="Normalize research inputs",
            output="Ingest assay notes, target biology summaries, ADME observations, and protocol snippets into structured chunks.",
            citations=citations,
        ),
        AgentStep(
            name="semantic_retriever",
            role="Ground every answer in evidence",
            output="Generate embeddings, run vector search, and return ranked passages with source metadata.",
            citations=citations,
        ),
        AgentStep(
            name="hypothesis_agent",
            role="Propose next-best research actions",
            output=f"Create candidate hypotheses for '{objective}' while respecting {constraint_text}.",
            citations=citations[:3],
        ),
        AgentStep(
            name="review_agent",
            role="Check scientific and safety boundaries",
            output="Flag missing controls, unsupported causal claims, assay-transfer risks, and experiment-readiness gaps.",
            citations=[],
        ),
    ]

    risks = assess_risks(objective) + [
        "Retrieval quality depends on curated, current, permissioned research data.",
        "Similarity scores should be monitored for drift when the corpus changes.",
    ]
    success_metrics = [
        "Top-5 retrieval precision against scientist-labeled evidence sets",
        "Time saved per literature or ELN triage workflow",
        "Percentage of generated hypotheses with cited support",
        "User feedback score from medicinal chemistry and biology reviewers",
    ]
    return WorkflowResponse(objective=objective, plan=plan, risks=risks, success_metrics=success_metrics)


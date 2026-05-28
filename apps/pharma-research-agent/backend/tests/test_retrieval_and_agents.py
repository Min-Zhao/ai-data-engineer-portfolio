from app.agents import build_research_workflow, synthesize_answer
from app.retrieval import search_documents


def test_search_prioritizes_relevant_scientific_context():
    hits = search_documents("EGFR resistance assay potency selectivity", top_k=3)

    assert hits
    assert any("egfr" in " ".join(hit.tags).lower() for hit in hits)
    assert hits[0].score >= hits[-1].score


def test_agent_response_returns_traceable_evidence():
    evidence = search_documents("design a RAG workflow for ADME and assay triage", top_k=4)
    response = synthesize_answer("design a RAG workflow for ADME and assay triage", evidence)

    assert response.confidence in {"medium", "low"}
    assert response.agent_trace[0].name == "retriever"
    assert response.evidence
    assert response.agent_trace[1].citations


def test_workflow_flags_research_validation_risk():
    workflow = build_research_workflow("Generate a novel target hypothesis for kinase resistance", [])

    assert len(workflow.plan) == 4
    assert any("validated" in risk.lower() for risk in workflow.risks)
    assert any("retrieval precision" in metric.lower() for metric in workflow.success_metrics)


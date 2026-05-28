from app.main import EvidenceQuery, evidence, health


def test_health_reports_loaded_corpus():
    assert health()["papers"] >= 4


def test_evidence_clusters_relevant_mechanisms():
    response = evidence(EvidenceQuery(query="checkpoint resistance interferon biomarker"))

    assert response.papers
    assert response.clusters
    assert any("biomarker" in gap.lower() or "scientist" in gap.lower() for gap in response.gaps)


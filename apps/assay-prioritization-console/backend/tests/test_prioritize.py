from app.main import PrioritizationRequest, health, prioritize


def test_health_reports_assays():
    assert health()["assays"] >= 4


def test_prioritize_respects_budget_and_turnaround():
    response = prioritize(PrioritizationRequest(target="EGFR", budget=30000, max_turnaround_days=14))

    assert response.selected
    assert sum(assay.cost for assay in response.selected) <= 30000
    assert all(assay.turnaround_days <= 14 for assay in response.selected)
    assert response.deferred


from fastapi.testclient import TestClient

from platform_app.main import app

client = TestClient(app)


def test_health_and_library():
    assert client.get("/api/health").json()["status"] == "ok"
    assert len(client.get("/api/library?kind=skill").json()) == 4
    assert client.get("/api/library?kind=bogus").status_code == 400
    assert client.get("/").status_code == 200


def test_unknown_item_and_empty_input():
    assert client.post("/api/run/nope", json={"input":"test"}).status_code == 404
    assert client.post("/api/run/sales-followup", json={"input":""}).status_code == 422


def test_run_feedback_and_audit():
    result = client.post("/api/run/sales-followup", json={"input":"Invented scenario"}).json()
    assert result["status"] == "complete"
    assert client.post("/api/feedback", json={"run_id":result["run_id"],"rating":5,"comment":"clear"}).json()["status"] == "saved"
    assert any(row["event"] == "feedback_recorded" for row in client.get("/api/audit").json())


def test_pii_input_is_blocked_and_not_stored_as_plaintext():
    result = client.post("/api/run/support-triage", json={"input":"fake person fake@example.com"}).json()
    assert result["status"] == "blocked"
    assert client.get("/api/audit").json()[0]["event"] == "input_blocked"
    confidential = client.post("/api/run/support-triage", json={"input":"INTERNAL ONLY invented note"}).json()
    assert confidential["status"] == "blocked"


def test_risky_action_requires_human_approval():
    result = client.post("/api/run/campaign-outline", json={"input":"publish a fictional campaign"}).json()
    assert result["approval_required"]
    approval = client.post(f"/api/approvals/{result['run_id']}", json={"approved":True,"reviewer":"Demo reviewer"})
    assert approval.json()["status"] == "approved_for_review"
    assert client.post(f"/api/approvals/{result['run_id']}", json={"approved":True,"reviewer":"Demo reviewer"}).status_code == 409

    second = client.post("/api/run/campaign-outline", json={"input":"delete a fictional campaign"}).json()
    rejected = client.post(f"/api/approvals/{second['run_id']}", json={"approved":False,"reviewer":"Demo reviewer"})
    assert rejected.json()["status"] == "rejected"


def test_feedback_and_approval_missing_run():
    assert client.post("/api/feedback", json={"run_id":"missing","rating":1}).status_code == 404
    assert client.post("/api/approvals/missing", json={"approved":False,"reviewer":"Demo reviewer"}).status_code == 404

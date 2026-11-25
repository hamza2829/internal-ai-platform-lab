from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from uuid import uuid4
import hashlib

from . import db as database
from .adapters import create_adapter
from .guardrails import filter_output, inspect_input, risky_action
from .library import get_entry, list_entries
from .schemas import ApprovalRequest, FeedbackRequest, RunRequest
from .tools import run_agent_tools

app = FastAPI(title="Internal AI Platform Lab", version="0.1.0", description="Fictional internal AI demo. Do not submit real company or personal data.")
adapter = create_adapter()


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse((__import__("pathlib").Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8"))


@app.get("/api/health")
def health():
    return {"status": "ok", "adapter": adapter.name, "demo_data": "invented"}


@app.get("/api/library")
def library(kind: str | None = None):
    if kind and kind not in {"prompt", "agent", "skill"}:
        raise HTTPException(400, "kind must be prompt, agent or skill")
    return list_entries(kind)


@app.post("/api/run/{item_id}")
def run(item_id: str, request: RunRequest):
    entry = get_entry(item_id)
    if not entry:
        raise HTTPException(404, "Library item not found")
    run_id = uuid4().hex
    flags = inspect_input(request.input)
    digest = hashlib.sha256(request.input.encode()).hexdigest()
    if flags:
        with database.connect() as conn:
            conn.execute("INSERT INTO runs(id,item_id,input_hash,output,flags,status) VALUES(?,?,?,?,?,?)", (run_id, item_id, digest, "Input withheld by privacy guardrail.", str(flags), "blocked"))
            database.audit(conn, "input_blocked", run_id, {"flags": flags})
        return {"run_id": run_id, "status": "blocked", "output": "Input withheld by privacy guardrail. Remove personal or confidential data and retry.", "flags": flags, "approval_required": False}
    approval_required = risky_action(request.input)
    if approval_required:
        result, status = "This request may cause an external or consequential action. A human must approve it before execution.", "awaiting_approval"
    else:
        prompt = entry.template.format(input=request.input)
        result = adapter.generate(prompt, request.input)
        if entry.kind == "agent":
            result += "\n\nTool notes: " + "; ".join(run_agent_tools(entry.id, request.input))
        result, output_flags = filter_output(result)
        flags.extend(output_flags)
        status = "complete"
    with database.connect() as conn:
        conn.execute("INSERT INTO runs(id,item_id,input_hash,output,flags,status) VALUES(?,?,?,?,?,?)", (run_id, item_id, digest, result, str(flags), status))
        database.audit(conn, "run_created", run_id, {"item_id": item_id, "status": status, "flags": flags, "adapter": adapter.name})
    return {"run_id": run_id, "status": status, "output": result, "flags": flags, "approval_required": approval_required}


@app.post("/api/approvals/{run_id}")
def approve(run_id: str, request: ApprovalRequest):
    with database.connect() as conn:
        row = conn.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Run not found")
        if row["status"] != "awaiting_approval":
            raise HTTPException(409, "Run is not awaiting approval")
        status = "approved_for_review" if request.approved else "rejected"
        conn.execute("UPDATE runs SET status=? WHERE id=?", (status, run_id))
        database.audit(conn, "human_approval", run_id, {"approved": request.approved, "reviewer": request.reviewer})
    return {"run_id": run_id, "status": status, "note": "Approval records review only; no external action is executed."}


@app.post("/api/feedback")
def feedback(request: FeedbackRequest):
    with database.connect() as conn:
        if not conn.execute("SELECT 1 FROM runs WHERE id=?", (request.run_id,)).fetchone():
            raise HTTPException(404, "Run not found")
        conn.execute("INSERT INTO feedback(run_id,rating,comment) VALUES(?,?,?)", (request.run_id, request.rating, request.comment))
        database.audit(conn, "feedback_recorded", request.run_id, {"rating": request.rating})
    return {"status": "saved"}


@app.get("/api/audit")
def audit_log(limit: int = 100):
    with database.connect() as conn:
        rows = conn.execute("SELECT event,run_id,details,created_at FROM audit ORDER BY id DESC LIMIT ?", (max(1, min(limit, 500)),)).fetchall()
    return [dict(row) for row in rows]

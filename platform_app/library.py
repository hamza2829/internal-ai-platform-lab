"""Small, versioned prompt, agent, and skill registry using fictional examples."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    id: str
    name: str
    kind: str
    department: str
    version: str
    description: str
    template: str
    tools: tuple[str, ...] = ()


ENTRIES = (
    Entry("sales-followup", "Discovery follow-up", "prompt", "sales", "1.0.0", "Draft a concise follow-up using only supplied notes.", "Draft a helpful follow-up for this fictional prospect. Do not invent commitments. Notes: {input}"),
    Entry("product-brief", "Product brief helper", "prompt", "product-development", "1.0.0", "Turn an idea into a testable brief.", "Create a short problem, user, outcome, and validation brief. Mark assumptions. Idea: {input}"),
    Entry("support-triage", "Support triage", "prompt", "customer-service", "1.0.0", "Classify a fictional request and suggest a next step.", "Classify the issue and suggest one safe next step. Escalate uncertainty. Request: {input}"),
    Entry("campaign-outline", "Campaign outline", "prompt", "marketing", "1.0.0", "Create a campaign outline without unsupported claims.", "Draft audience, message, channel, and measurement ideas. Flag unverified claims. Brief: {input}"),
    Entry("sales-coach", "Sales coach", "agent", "sales", "1.0.0", "Prepares a follow-up and records a fictional CRM note.", "Prepare a follow-up and summarize the notes: {input}", ("fictional_crm_lookup", "draft_followup")),
    Entry("product-discovery", "Product discovery agent", "agent", "product-development", "1.0.0", "Turns an opportunity into hypotheses and tests.", "Produce hypotheses and a lightweight test plan: {input}", ("fictional_feedback_search", "draft_experiment")),
    Entry("service-guide", "Service guide agent", "agent", "customer-service", "1.0.0", "Suggests a response and escalates sensitive cases.", "Suggest a response and escalation path: {input}", ("fictional_policy_lookup", "draft_reply")),
    Entry("sales-call-prep", "Call preparation", "skill", "sales", "1.0.0", "Prepare a discovery call from approved fictional context.", "Use the call-prep skill instructions for: {input}"),
    Entry("product-experiment", "Experiment design", "skill", "product-development", "1.0.0", "Frame a product question as a small experiment.", "Use the experiment skill instructions for: {input}"),
    Entry("service-triage", "Support triage", "skill", "customer-service", "1.0.0", "Triage with empathy, boundaries, and clear escalation.", "Use the support-triage skill instructions for: {input}"),
    Entry("campaign-review", "Campaign review", "skill", "marketing", "1.0.0", "Review a campaign draft for evidence and clarity.", "Use the campaign-review skill instructions for: {input}"),
)

BY_ID = {entry.id: entry for entry in ENTRIES}


def list_entries(kind: str | None = None) -> list[dict]:
    return [entry.__dict__ for entry in ENTRIES if kind is None or entry.kind == kind]


def get_entry(entry_id: str) -> Entry | None:
    return BY_ID.get(entry_id)

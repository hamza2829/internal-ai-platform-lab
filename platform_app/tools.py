"""Allow-listed, read-only fictional tools used by the example agents."""

def fictional_crm_lookup(query: str) -> str:
    return f"CRM lookup is a mock; no record exists for: {query[:80]}"


def draft_followup(query: str) -> str:
    return "Follow-up draft prepared; a human must review it before sending."


def fictional_feedback_search(query: str) -> str:
    return "No real feedback is connected; use this as a hypothesis only."


def draft_experiment(query: str) -> str:
    return "Experiment outline prepared with a measurable outcome and a review step."


def fictional_policy_lookup(query: str) -> str:
    return "Demo policy lookup only; check the approved policy source in real work."


def draft_reply(query: str) -> str:
    return "Reply draft prepared; do not send without a human review."


AGENT_TOOLS = {
    "sales-coach": (fictional_crm_lookup, draft_followup),
    "product-discovery": (fictional_feedback_search, draft_experiment),
    "service-guide": (fictional_policy_lookup, draft_reply),
}


def run_agent_tools(agent_id: str, query: str) -> list[str]:
    return [tool(query) for tool in AGENT_TOOLS.get(agent_id, ())]

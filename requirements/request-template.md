# Department request template

Copy this form into an issue or workshop note. Use invented or anonymized examples only.

- Department / owner:
- User and task:
- Current workflow and pain point:
- Desired outcome and success measure:
- Inputs the assistant may use:
- Data sensitivity / prohibited inputs:
- Actions it may draft (never execute in v1):
- Human review point:
- Failure modes and escalation:
- Example input and expected answer:
- Example input that must be blocked:
- Reviewer and version:

## Worked example: customer service triage skill

**Request:** Customer service wants consistent first responses to simple troubleshooting questions. Use fictional cases; no account lookup or action.

**Boundaries:** No real personal data, credentials, refunds, promises, or account changes. Escalate uncertainty. A human reviews any reply before sending.

**Skill created:** `library/skills/customer-service/support-triage/SKILL.md`, version 1.0.0. It summarizes neutrally, suggests a reversible step, and identifies escalation.

**Test:** Given “Invented user says a demo export looks blank,” expect an empathetic acknowledgement, a sample-data retry suggestion, and escalation if it persists; must not claim a real account was checked. The scorecard is in `evals/skills.json` and automated assertions are in `tests/test_library.py`.

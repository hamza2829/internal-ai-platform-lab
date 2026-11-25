# Using the platform

The Actions quality workflow installs Python 3.12, runs the FastAPI API and test suite, and publishes this guide to GitHub Pages from `main`. The small web interface is served at `/` when the API is run by the workflow or in a disposable development environment. It lists library items, submits a fictional input, shows guardrail status, and stores a rating and comment in SQLite.

## API tour

- `GET /api/library` lists versioned prompts, agents, and skills.
- `POST /api/run/{id}` runs an item. Personal data and confidentiality markers are blocked before generation.
- `POST /api/approvals/{run_id}` records a named human decision for a risky request; it never executes an external action.
- `POST /api/feedback` stores a 1–5 rating and comment against a run.
- `GET /api/audit` returns the recent audit trail.

The default adapter is deterministic. The Actions model smoke job attempts `sshleifer/tiny-gpt2`; initialization errors fall back to the mock. Outputs are demos and require human review.

# Agent Onboarding — TransferFlow

Quick purpose
- Small FastAPI service demonstrating atomic transfers between accounts.
- This document provides a minimal reproducible path, required checks, and a handoff format for an automated agent.

First things to do (quick verification)
1. Clone the repository and install dependencies (locally or in a container).
2. Start an isolated environment: bring up PostgreSQL and Redis with Docker Compose.
3. Run tests and the smoke checks listed below.

Prerequisites
- Docker and Docker Compose
- Python 3.10 (only needed locally if not using containers)

Quick start (local using Docker Compose)
```bash
git clone https://github.com/anastasiakrivova-stack/TransferFlow.git
cd TransferFlow
docker compose build --pull
docker compose up -d
# wait for postgres/redis to be ready, then:
pytest -q
```

Mandatory checks for any change
- All tests pass: `pytest` — this is the primary acceptance criterion.
- Health endpoint: `GET http://localhost:8000/health` returns 200.
- Core transfer scenarios: idempotency, insufficient balance, same-account, and cache invalidation are exercised.
- API responses should not leak stack traces for expected errors — expected errors must map to 4xx responses or a generic 500 for unexpected failures.

Smoke-check commands (copy & run)
```bash
curl -f http://localhost:8000/health
pytest tests/test_app.py::test_transfer_success -q
```

Handoff / PR checklist (required)
- Short description: what the change does and why.
- Areas changed: list modified modules/files.
- Acceptance criteria: list tests / behavioral expectations confirmed (include exact commands to reproduce).
- How to run: exact commands to verify (docker compose, pytest, environment variables).
- Rollback plan: how to revert the change (git revert / rollback migration/data considerations).
- Notes: risks, remaining TODOs, observations during test runs.

Example minimal handoff in a PR description
```
Summary: Fix account owner check for GET /clients/{client_id}/accounts

Files: app/api/accounts.py, app/api/auth.py, tests/test_app.py

Acceptance:
- `pytest -q` passes
- `curl -f -H "X-Client-Id: 1" http://localhost:8000/clients/1/accounts` returns 200 for client 1 and 403 for other ids

How to run:
docker compose up -d
pytest -q

Rollback: git revert <commit>
```

Additional notes
- If you are an automated agent submitting code: leave assumptions and reasoning in the PR description.
- If the change requires product decisions (currency rules, Kafka contract, etc.), mark the PR as draft and request a human owner.

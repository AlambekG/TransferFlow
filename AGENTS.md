# Agents entrypoint

This file is a short, authoritative entry for humans and automation (agents) working on TransferFlow.

Quick summary:
- Purpose: a small FastAPI service that models money transfers between accounts.
- Key guarantees: atomic transfer creation, idempotency via `Idempotency-Key`, balance checks, row-level locking.

Where to start:
- README.md — runnable instructions and endpoints.
- TRANSFER_CONTRACT.md — domain contract and invariants to rely on when changing core logic.
- docs/adr/0001-kafka-circuit-breaker.md — design decision regarding Kafka and the circuit breaker.
- tests/ — executable tests that show the guarded behaviors (idempotency, insufficient balance, etc.).

Notes for agents:
- Do not change domain invariants without updating `TRANSFER_CONTRACT.md` and adding an integration test that demonstrates the new behaviour.
- Fraud, ledger and notification are currently implemented as mocks with best-effort behaviour; see ADR for policy.

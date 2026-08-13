# Transfer Contract (short)

This document lists the domain invariants and expected behaviour for `POST /transfers`.

Invariants
- `amount` must be a positive number (greater than 0).
- Transfers must be between two different accounts.
- Currency must match for sender and receiver (current implementation assumes single currency USD).
- A transfer is idempotent by `Idempotency-Key`: repeated requests with the same key must return the same transfer.

Statuses
- `pending` (not currently used in demo) — reserved for async processing.
- `completed` — the transfer succeeded and balances were adjusted.
- `failed` — the transfer failed (insufficient funds, fraud detected, missing account, etc.).

External effects and failure semantics
- Fraud check: treated as a blocking precondition — if fraud check returns false, transfer is aborted and client receives 400.
- Notification and ledger update: currently best-effort background tasks; transfer completes even if they fail. In future they may be made transactional or retried via durable queue (Kafka).

Concurrency
- Row-level locking with `SELECT ... FOR UPDATE` is used to avoid races on balances. Tests should exercise concurrent attempts when adding stronger guarantees.

Evolution
- Any change to these invariants must be accompanied by a test and a short ADR describing intent and migration steps.

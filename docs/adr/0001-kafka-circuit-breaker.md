# ADR 0001 — Kafka and Circuit Breaker

Status: proposed

Context
-------
The repository README mentions Kafka-based async processing and circuit breakers as active protections. The current codebase contains a commented Kafka publish block and a `CircuitBreaker` implementation that was not wired into external calls. External services (`fraud`, `notification`, `ledger`) exist as simple mocks.

Decision
--------
1. Keep Kafka disabled in the mainline for now. Remove commented Kafka code from hot paths to reduce confusion. Reintroduce only when a clear contract, test coverage and infra support are available.
2. Use the `CircuitBreaker` implementation around external calls that may fail repeatedly. For the current development/demo environment we wrap mocks to exercise the behaviour; in production replace mocks with clients and keep the breaker in place.

Consequences
------------
- README and code are consistent about async processing being out-of-band (no active Kafka publish). If Kafka is reintroduced it must be accompanied by an ADR that specifies the message schema and delivery semantics.
- Circuit breaker protects external calls from repeated failure; it should be monitored in production and tuned according to expected failure modes.

Rationale
---------
This keeps the codebase's behaviour explicit and reduces accidental drift between documentation and implementation. It enables safe evolution: mock behavior is explicit, and operators know the expected protections.

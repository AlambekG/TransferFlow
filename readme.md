# Financial Transaction System

A high-performance financial transaction system built with FastAPI.


## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Redis
- Kafka
- Docker
- Pytest


## Modules

### Account
- Fetch client accounts
- Redis caching for faster access

### Transfers
- Money transfers with atomic transactions
- Row-level locking to prevent race conditions
- Balance validation
- Idempotency to prevent duplicate transfers
- Retry mechanism for temporary external service failures
- Kafka for async processing 

### Services
- Fraud detection
- Notification
- Ledger updates

Circuit breaker / mocks:
External services (`fraud`, `notification`, `ledger`) are currently implemented as lightweight mocks.
The codebase contains a `CircuitBreaker` implementation which is used to exercise protection around those mocks; in production these mocks should be replaced with real clients and the breaker tuned appropriately.

Kafka:
As of this commit Kafka is not enabled (the publish block is commented). Reintroduce Kafka only after defining a message contract and adding integration tests; see `docs/adr/0001-kafka-circuit-breaker.md`.

## Running

Requirements:
- Docker
- Docker Compose

Start the application:

```bash
docker compose build
docker compose up
```

API:

http://localhost:8000

Health check:

GET /health

Swagger:
http://localhost:8000/docs

Endpoints

Get accounts:

GET /clients/{client_id}/accounts

Create transfer:

POST /transfers

Tests

Run tests:
```bash
pytest
```
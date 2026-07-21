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

Circuit breaker:
External services are protected with circuit breakers.
If fraud/ledger services fail repeatedly, requests are temporarily blocked
to prevent cascading failures.

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
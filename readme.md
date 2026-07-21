# Financial Transaction System

A high-performance financial transaction system built with FastAPI.

## Modules

### Account
- Fetch client accounts
- Redis caching for faster access

### Transfers
- Money transfers with atomic transactions
- Balance validation
- Idempotency to prevent duplicate transfers
- Retries for external service failure
- Kafka for async processing 

Circuit breaker:
External services are protected with circuit breakers.
If fraud/ledger services fail repeatedly, requests are temporarily blocked
to prevent cascading failures.

### Services
- Fraud detection
- Notification
- Ledger updates

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
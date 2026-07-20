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
docker compose up --build
```

API:

http://localhost:8000

Health check:

GET /health

Endpoints

Get accounts:

GET /clients/{client_id}/accounts

Create transfer:

POST /transfers
# Data Ingestion Service

Microservice for ingesting data from webhooks and polling sources.

---

## Features

| Feature | Description |
|---------|-------------|
| **Webhooks** | Receive events from Meta (FB/IG), Twitter/X |
| **Polling** | Poll Google Play, Apple App Store reviews |
| **Normalization** | Transform all data to standardized format |
| **Message Queue** | Publish to SQS (replaceable) |

---

## Quick Start

### 1. Install Poetry

```bash
brew install poetry
```

### 2. Setup Project

```bash
cd data_ingestion_service
poetry install
cp .env.example .env
```

### 3. Edit `.env`

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/tenant_db
```

### 4. Start Database

```bash
docker compose up -d postgres
```

### 5. Run Migrations

```bash
poetry run alembic revision --autogenerate -m "initial"
poetry run alembic upgrade head
```

### 6. Start Service

```bash
poetry run python main.py
```

**Service:** http://localhost:8002
**Docs:** http://localhost:8002/docs

---

## Project Structure

```
data_ingestion_service/
├── main.py              # Entry point
├── core/                # Config, exceptions
├── schemas/             # Pydantic models
├── db/models/           # SQLAlchemy models
├── repositories/        # Data access
├── handlers/            # Webhook handlers
├── workers/             # Polling workers
├── normalizers/         # Data normalization
├── publishers/          # Message queue
├── api/v1/              # API endpoints
└── alembic/             # Migrations
```

---

## API Endpoints

### Health
- `GET /health` - Health check

### Webhooks
- `POST /api/v1/webhooks/meta/{tenant_id}` - Meta webhook
- `GET /api/v1/webhooks/meta/{tenant_id}` - Meta verify
- `POST /api/v1/webhooks/twitter/{tenant_id}` - Twitter webhook
- `GET /api/v1/webhooks/twitter/{tenant_id}` - Twitter CRC

---

## Docker

```bash
# Start everything
docker compose up --build

# Stop
docker compose down
```

---

## Architecture

```
┌─────────────┐     ┌─────────────┐
│   Webhook   │     │   Polling   │
│  (Meta, X)  │     │(Play, Apple)│
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────┐
│         Normalizer              │
└──────────────┬──────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │  SQS Queue   │
│  (ingestion) │ │  (inbound)   │
└──────────────┘ └──────────────┘
```

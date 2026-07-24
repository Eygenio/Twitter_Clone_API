# 🐦 Twitter Clone API v1.0.0 — FastAPI + Celery + RabbitMQ + PostgreSQL + Nginx

High-performance backend application implementing core Twitter functionality:
users, tweets, likes, follows, and background tasks.

> ⚠️ The project implements the **backend only**.
> The frontend is provided as a ready-made package and is used for integration and API testing.

---

## ✨ Features

* 📝 Create tweets and browse the feed
* ❤️ Like/unlike tweets with like statistics
* 🔔 Follow / unfollow users
* ⚙️ Celery background tasks (notifications, test tasks)
* 🐇 RabbitMQ as a message broker
*  🗄 PostgreSQL database
* 🌐 Nginx for static file serving and reverse proxying
* 🐳 Full Docker & docker-compose support
* 📡 Interactive API documentation (Swagger UI / ReDoc)
* 🧪 Automated tests (unit, integration, e2e)
* 🧹 Code quality tools: `ruff`, `mypy`, `pre-commit`
* 📦 Dependency management with `poetry`
* 📝 Structured logging with `colorlog`

---

## 🏗️ Architecture

The application follows **Clean Architecture** principles with clear layer separation:

* **Domain** – pure business entities and abstract repository interfaces
* **Application** – service layer with business logic
* **Infrastructure** – SQLAlchemy ORM models, repository implementations, and Unit of Work
* **Presentation** – FastAPI routers, Pydantic schemas, and dependencies

```
project/
├── src/
│ ├── application/
│ │ └── services/ # Business logic
│ ├── domain/
│ │ ├── entities.py # Pydantic domain models
│ │ ├── repositories.py # Abstract repository interfaces
│ │ └── unit_of_work.py # Abstract Unit of Work
│ ├── infrastructure/
│ │ ├── models/ # SQLAlchemy ORM models
│ │ ├── repositories/ # Repository implementations
│ │ └── unit_of_work.py # Concrete Unit of Work
│ ├── presentation/
│ │ ├── api/ # FastAPI routers
│ │ ├── schemas/ # Pydantic request/response schemas
│ │ └── dependencies.py # FastAPI dependencies (including UoW injection)
│ ├── config/ # Application settings (Pydantic-settings)
│ ├── db/ # Database engine and session factory
│ ├── middleware/ # Custom middleware (Request-ID, error handlers)
│ ├── exceptions/ # Custom application exceptions
│ ├── tasks/ # Celery tasks
│ ├── app.py # FastAPI application entry point
│ └── celery_app.py # Celery application configuration
├── tests/
│ ├── conftest.py # Shared fixtures and test configuration
│ ├── e2e/ # End-to-end API tests
│ ├── integration/ # Integration API tests
│ └── unit/ # Unit tests for services and domain logic
├── alembic/ # Database migrations
├── scripts/ # Helper scripts (seed DB, send test tasks, wait-for-db)
├── nginx/ # Nginx configuration
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml # Poetry dependencies and tool configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md
```

## 🧰 Technology Stack

* **Python** 3.13
* **FastAPI**
* **Celery**
* **RabbitMQ**
* **PostgreSQL**
* **SQLAlchemy 2.0**
* **Pydantic**
* **Alembic**
* **Nginx**
* **Docker** & **docker-compose**
* **Poetry**
* **Pytest**
* **Ruff / MyPy / Pre-commit**

---

## 💡 Functionality

### 👤 Users

* User profile with followers / following
* API‑key authentication

### 📝 Tweets

* Create, view, and delete tweets
* Media attachments
* Like / unlike tweets

### ⚙️ Background tasks (Celery)

* Send follow notifications (demo logging)
* Test tasks for worker health check

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Eygenio/Twitter_Clone_API
```

## 2. Create a `.env` file (or copy from the provided template):

```
APP__HOST=
APP__PORT=

DB__NAME=
DB__USER=
DB__PASSWORD=
DB__HOST=
DB__PORT=
DB__DRIVER_NAME=

BROKER__URL=
BROKER__RESULT_BACKEND=

POOL__ECHO=
POOL__POOL_PRE_PING=
POOL__POOL_SIZE=
POOL__MAX_OVERFLOW=

RABBIT_USER=
RABBIT_PASSWORD=

```

## 3. 🐳 Build & run with Docker

```bash
docker-compose build
docker-compose up -d
```
The application will be available at `http://0.0.0.0:8080/`.
Interactive API docs: `http://0.0.0.0:8080/docs/`.

## 🧪 Testing

Run all tests (unit, integration, e2e):

```bash
docker-compose exec app pytest -v
```

## 🧹 Code Quality

All code quality tools are configured in `pyproject.toml` and `.pre-commit-config.yaml`.

```bash
# Formatting and linting
ruff check . --fix
ruff format .

# Import sorting
isort .

# Type checking
mypy src
```

Pre-commit hooks run automatically on `git commit`.


## 🔐 Security

* API‑key authentication via custom HTTP header
* PostgreSQL isolated within Docker network
* Custom exception handlers with request‑ID tracking
* Minimal privilege principle

---

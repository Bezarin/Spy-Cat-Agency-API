# Spy Cat Agency API

A FastAPI-based REST API for managing spy cats, their missions, and mission targets for a secret cat agency.

## Features

- **Cat Management**: Full CRUD operations for spy cats with breed validation via TheCatAPI
- **Mission Management**: Create missions with 1-3 targets, assign cats, track completion
- **Target Management**: Update mission target notes and completion status

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLModel** - SQL databases in Python, designed by the creator of FastAPI
- **PostgreSQL** - Robust relational database
- **Pydantic** - Data validation using Python type hints
- **Alembic** - Database migration tool
- **Docker & Docker Compose** - Containerization and orchestration
- **UV** - Ultra-fast Python package installer and resolver

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Bezarin/Spy-Cat-Agency-API
cd DevelopsToday-test-task
```

### 2. Start the Application

```bash
docker-compose up --build -d
```

This will start:

- **API Server** on <http://localhost:8000>
- **PostgreSQL Database** on localhost:5432

### 3. Run Database Migrations

```bash
POSTGRES_HOST=localhost uv run alembic upgrade head
```

### 4. Verify Installation

Visit <http://localhost:8000/docs> to see the interactive API documentation (Swagger UI).

## Postman Collection

You can test all API endpoints using the provided Postman collection:

**📁 [Spy Cat Agency API - Postman Collection](./postman/Spy_Cat_Agency_API.postman_collection.json)**

## API Endpoints

### Cats

- `POST /cats/` - Create a new spy cat
- `GET /cats/` - List all cats
- `GET /cats/{id}` - Get cat by ID
- `PUT /cats/{id}` - Update cat salary
- `DELETE /cats/{id}` - Delete cat (if no active missions)

### Missions

- `POST /missions/` - Create mission with targets
- `GET /missions/` - List all missions
- `GET /missions/{id}` - Get mission by ID
- `PUT /missions/{id}/assign/{cat_id}` - Assign cat to mission
- `DELETE /missions/{id}` - Delete mission (if not assigned)

### Targets

- `PUT /targets/{id}` - Update target notes and/or completion status

## Project Structure

```txt
├── alembic/                 # Database migrations
├── app/
    ├── api/                 # API endpoints
    │   ├── cats.py          # Cat management endpoints
    │   ├── missions.py      # Mission management endpoints
    │   └── targets.py       # Target update endpoints
    ├── db/                  # Database configuration
    │   └── session.py       # Database session management
    ├── models/              # SQLModel database models
    │   ├── cat.py           # Cat model
    │   ├── mission.py       # Mission model
    │   └── target.py        # Target model
    ├── schemas/             # Pydantic validation schemas
    │   ├── cat.py           # Cat request/response schemas
    │   ├── mission.py       # Mission request/response schemas
    │   └── target.py        # Target request/response schemas
    ├── services/            # Business logic services
    │   └── breeds.py        # TheCatAPI breed validation
    ├── main.py              # FastAPI application entry point
    └── settings.py          # Application configuration
├── postman/                 # Postman collection for API testing
├── alembic.ini              # Alembic configuration
├── docker-compose.yml       # Docker services configuration
├── Dockerfile.dev           # Development Docker image
├── pyproject.toml           # Python dependencies and project config
├── README.md                # Project documentation
```

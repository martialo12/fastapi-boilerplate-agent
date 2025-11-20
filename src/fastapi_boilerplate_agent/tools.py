from langchain.tools import tool
from typing import Dict


# Main application file
MAIN_PY = """\"\"\"Main FastAPI application for {project_name}.\"\"\" 

from fastapi import FastAPI

from app.core.constants import (
    DOCS_URL,
    DOCUMENTATION_KEY,
    MESSAGE_KEY,
    REDOC_URL,
    VERSION_KEY,
    WELCOME_MESSAGE,
)
from app.core.database import engine
from app.{module_name}.constants import API_DESCRIPTION, API_TITLE, API_VERSION
from app.{module_name}.models import Base
from app.{module_name}.router import router as {module_name}_router

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
)

# Include routers
app.include_router({module_name}_router)


@app.on_event(\"startup\")
async def startup_event():
    \"\"\"Create database tables on startup (for development only).\"\"\" 
    # Note: In production, use Alembic migrations instead
    Base.metadata.create_all(bind=engine)


@app.get(\"/\", tags=[\"Root\"])
def read_root():
    \"\"\"Root endpoint returning API information.\"\"\" 
    return {{
        MESSAGE_KEY: WELCOME_MESSAGE,
        DOCUMENTATION_KEY: DOCS_URL,
        VERSION_KEY: API_VERSION,
    }}
"""

# Core database configuration - SQLite version
DATABASE_SQLITE_PY = """\"\"\"Database configuration and session management.\"\"\"

from abc import ABC, abstractmethod
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from app.core.constants import DATABASE_URL

# Constants
DB_NOT_CONNECTED_ERROR = "Database not connected. Call connect() first."

# Declarative base for models
Base = declarative_base()


class Database(ABC):
    \"\"\"Abstract base class for database connections.\"\"\"

    @abstractmethod
    def connect(self) -> Engine:
        \"\"\"Establish database connection and return engine.\"\"\"
        pass

    @abstractmethod
    def get_session(self) -> Session:
        \"\"\"Get a database session.\"\"\"
        pass

    @abstractmethod
    def close(self) -> None:
        \"\"\"Close database connection.\"\"\"
        pass


class SQLiteDatabase(Database):
    \"\"\"SQLite database implementation with singleton pattern.\"\"\"

    _instance: Optional["SQLiteDatabase"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls):
        \"\"\"Ensure only one instance of database connection exists (Singleton).\"\"\"
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_url: str = DATABASE_URL):
        \"\"\"Initialize SQLite database connection.\"\"\"
        # Only initialize once
        if self._engine is None:
            self.database_url = database_url
            self.connect()

    def connect(self) -> Engine:
        \"\"\"Establish SQLite database connection.\"\"\"
        if self._engine is None:
            self._engine = create_engine(
                self.database_url,
                connect_args={{"check_same_thread": False}},
                pool_pre_ping=True,  # Verify connections before using
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
        return self._engine

    def get_session(self) -> Session:
        \"\"\"Get a new database session.\"\"\"
        if self._session_factory is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._session_factory()

    def close(self) -> None:
        \"\"\"Close database connection.\"\"\"
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @property
    def engine(self) -> Engine:
        \"\"\"Get database engine.\"\"\"
        if self._engine is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._engine


# Global database instance (Singleton)
# This ensures only one connection throughout the application lifetime
db_instance = SQLiteDatabase()

# Legacy compatibility: expose engine for models
engine = db_instance.engine


def get_db() -> Generator[Session, None, None]:
    \"\"\"Dependency to get database session.

    This is used by FastAPI's dependency injection system.
    It ensures proper session lifecycle management.
    \"\"\"
    session = db_instance.get_session()
    try:
        yield session
    finally:
        session.close()


def get_database_instance() -> Database:
    \"\"\"Get the singleton database instance.

    Returns:
        The global database instance
    \"\"\"
    return db_instance
"""

# Core database configuration - PostgreSQL version
DATABASE_POSTGRES_PY = """\"\"\"Database configuration and session management.\"\"\"

from abc import ABC, abstractmethod
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.constants import DATABASE_URL

# Constants
DB_NOT_CONNECTED_ERROR = "Database not connected. Call connect() first."

# Declarative base for models
Base = declarative_base()


class Database(ABC):
    \"\"\"Abstract base class for database connections.\"\"\"

    @abstractmethod
    def connect(self) -> Engine:
        \"\"\"Establish database connection and return engine.\"\"\"
        pass

    @abstractmethod
    def get_session(self) -> Session:
        \"\"\"Get a database session.\"\"\"
        pass

    @abstractmethod
    def close(self) -> None:
        \"\"\"Close database connection.\"\"\"
        pass


class PostgreSQLDatabase(Database):
    \"\"\"PostgreSQL database implementation with singleton pattern.\"\"\"

    _instance: Optional["PostgreSQLDatabase"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls):
        \"\"\"Ensure only one instance of database connection exists (Singleton).\"\"\"
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_url: str = DATABASE_URL):
        \"\"\"Initialize PostgreSQL database connection.\"\"\"
        # Only initialize once
        if self._engine is None:
            self.database_url = database_url
            self.connect()

    def connect(self) -> Engine:
        \"\"\"Establish PostgreSQL database connection.\"\"\"
        if self._engine is None:
            self._engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,  # Verify connections before using
                pool_recycle=3600,   # Recycle connections after 1 hour
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
        return self._engine

    def get_session(self) -> Session:
        \"\"\"Get a new database session.\"\"\"
        if self._session_factory is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._session_factory()

    def close(self) -> None:
        \"\"\"Close database connection.\"\"\"
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @property
    def engine(self) -> Engine:
        \"\"\"Get database engine.\"\"\"
        if self._engine is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._engine


# Global database instance (Singleton)
# This ensures only one connection throughout the application lifetime
db_instance = PostgreSQLDatabase()

# Legacy compatibility: expose engine for models
engine = db_instance.engine


def get_db() -> Generator[Session, None, None]:
    \"\"\"Dependency to get database session.

    This is used by FastAPI's dependency injection system.
    It ensures proper session lifecycle management.
    \"\"\"
    session = db_instance.get_session()
    try:
        yield session
    finally:
        session.close()


def get_database_instance() -> Database:
    \"\"\"Get the singleton database instance.

    Returns:
        The global database instance
    \"\"\"
    return db_instance
"""

# Core constants
CORE_CONSTANTS_PY = """\"\"\" 
Core constants for the application.
\"\"\" 
import os

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "{database_url}"
)

# API Documentation URLs
DOCS_URL = \"/docs\"
REDOC_URL = \"/redoc\"

# API Messages
WELCOME_MESSAGE = \"Welcome to the {project_name} API\"
DOCUMENTATION_KEY = \"documentation\"
VERSION_KEY = \"version\"
MESSAGE_KEY = \"message\"
"""

# Tickets models
TICKETS_MODELS_PY = """from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from datetime import datetime
from app.core.database import Base
import enum


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
"""

# Tickets schemas
TICKETS_SCHEMAS_PY = """from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.tickets.models import TicketStatus


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TicketStatus = TicketStatus.OPEN


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None


class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
"""

# Tickets repositories
TICKETS_REPOSITORIES_PY = """from sqlalchemy.orm import Session
from app.tickets.models import Ticket
from app.tickets.schemas import TicketCreate, TicketUpdate
from typing import List, Optional


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        return self.db.query(Ticket).offset(skip).limit(limit).all()

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def create(self, ticket: TicketCreate) -> Ticket:
        db_ticket = Ticket(**ticket.model_dump())
        self.db.add(db_ticket)
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket

    def update(self, ticket_id: int, ticket_update: TicketUpdate) -> Optional[Ticket]:
        db_ticket = self.get_by_id(ticket_id)
        if not db_ticket:
            return None
        
        update_data = ticket_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ticket, field, value)
        
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket

    def delete(self, ticket_id: int) -> bool:
        db_ticket = self.get_by_id(ticket_id)
        if not db_ticket:
            return False
        
        self.db.delete(db_ticket)
        self.db.commit()
        return True
"""

# Tickets services
TICKETS_SERVICES_PY = """from app.tickets.repositories import TicketRepository
from app.tickets.schemas import TicketCreate, TicketUpdate, TicketResponse
from app.tickets.exceptions import TicketNotFoundException
from typing import List


class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def get_all_tickets(self, skip: int = 0, limit: int = 100) -> List[TicketResponse]:
        tickets = self.repository.get_all(skip=skip, limit=limit)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    def get_ticket(self, ticket_id: int) -> TicketResponse:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundException(ticket_id)
        return TicketResponse.model_validate(ticket)

    def create_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        ticket = self.repository.create(ticket_data)
        return TicketResponse.model_validate(ticket)

    def update_ticket(self, ticket_id: int, ticket_data: TicketUpdate) -> TicketResponse:
        ticket = self.repository.update(ticket_id, ticket_data)
        if not ticket:
            raise TicketNotFoundException(ticket_id)
        return TicketResponse.model_validate(ticket)

    def delete_ticket(self, ticket_id: int) -> None:
        if not self.repository.delete(ticket_id):
            raise TicketNotFoundException(ticket_id)
"""

# Tickets exceptions
TICKETS_EXCEPTIONS_PY = """class TicketNotFoundException(Exception):
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id
        super().__init__(f"Ticket with id {ticket_id} not found")
"""

# Tickets constants
TICKETS_CONSTANTS_PY = """\"\"\" 
Constants for the {module_name} module.
\"\"\" 

# API Documentation
API_TITLE = \"{project_name} API\"
API_DESCRIPTION = \"REST API for {module_name} management\"
API_VERSION = \"1.0.0\"

# Path parameter descriptions
{CLASS_NAME}_ID_PATH_DESC = \"Unique {module_name} ID\"

# Field descriptions
{CLASS_NAME}_ID_DESC = \"Unique {module_name} identifier (auto-incremented)\"
{CLASS_NAME}_TITLE_DESC = \"{class_name} title\"
{CLASS_NAME}_DESCRIPTION_DESC = \"Detailed {module_name} description\"
{CLASS_NAME}_STATUS_DESC = \"{class_name} status (open, in_progress, closed)\"
{CLASS_NAME}_CREATED_AT_DESC = \"{class_name} creation date and time (UTC)\"

# Validation messages
{CLASS_NAME}_NOT_FOUND = \"{class_name} not found\"
DATABASE_OPERATION_FAILED = \"Database operation failed\"

# Example values
EXAMPLE_{CLASS_NAME}_ID = \"550e8400-e29b-41d4-a716-446655440000\"
EXAMPLE_TITLE = \"Application bug\"
EXAMPLE_DESCRIPTION = \"Application crashes on startup\"
EXAMPLE_STATUS_OPEN = \"open\"
EXAMPLE_STATUS_IN_PROGRESS = \"in_progress\"
EXAMPLE_STATUS_CLOSED = \"closed\"
EXAMPLE_CREATED_AT = \"2025-01-15T10:30:00.000Z\"

# Pagination defaults
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000

# Field constraints
MAX_TITLE_LENGTH = 255
"""

# Tickets dependencies
TICKETS_DEPENDENCIES_PY = """from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.tickets.repositories import TicketRepository
from app.tickets.services import TicketService


def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository)
) -> TicketService:
    return TicketService(repository)
"""

# Tickets router
TICKETS_ROUTER_PY = """from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.ticket.schemas import TicketCreate, TicketUpdate, TicketResponse
from app.ticket.services import TicketService
from app.ticket.dependencies import get_ticket_service
from app.ticket.exceptions import TicketNotFoundException

router = APIRouter()


@router.get("/", response_model=List[TicketResponse])
def list_tickets(
    skip: int = 0,
    limit: int = 100,
    service: TicketService = Depends(get_ticket_service)
):
    return service.get_all_tickets(skip=skip, limit=limit)


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    service: TicketService = Depends(get_ticket_service)
):
    return service.create_ticket(ticket)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service)
):
    try:
        return service.get_ticket(ticket_id)
    except TicketNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    service: TicketService = Depends(get_ticket_service)
):
    try:
        return service.update_ticket(ticket_id, ticket)
    except TicketNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service)
):
    try:
        service.delete_ticket(ticket_id)
    except TicketNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
"""

# Dockerfile
DOCKERFILE = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# Docker Compose
DOCKER_COMPOSE = """version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL={database_url_docker}
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""

# Makefile
MAKEFILE = """install:
\tpip install -r requirements.txt

run:
\tuvicorn app.main:app --reload

test:
\tpytest tests/ -v

lint:
\tflake8 app tests

format:
\tblack app tests

docker-build:
\tdocker-compose build

docker-up:
\tdocker-compose up

docker-down:
\tdocker-compose down

migrate:
\talembic upgrade head

.PHONY: install run test lint format docker-build docker-up docker-down migrate
"""

# Requirements
REQUIREMENTS = """fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
pydantic==2.10.0
pydantic-settings==2.6.1
psycopg2-binary==2.9.10
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.28.0
"""

# pyproject.toml
PYPROJECT_TOML = """[project]
name = "{project_name}"
version = "1.0.0"
description = "{project_name} FastAPI application"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[tool.black]
line-length = 88
target-version = ['py311']
"""

# README
README = """# {project_name}

A FastAPI application with PostgreSQL database.

## Setup

1. Install dependencies:
```bash
make install
```

2. Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/app"
```

3. Run the application:
```bash
make run
```

Or use Docker:
```bash
make docker-up
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
make test
```

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── database.py
│   ├── main.py
│   └── tickets
│       ├── __init__.py
│       ├── constants.py
│       ├── dependencies.py
│       ├── exceptions.py
│       ├── models.py
│       ├── repositories.py
│       ├── router.py
│       ├── schemas.py
│       └── services.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_api.py
    └── test_services.py
```
"""

# GitHub Actions CI
GITHUB_ACTIONS = """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://user:password@localhost:5432/test_db
      run: |
        pytest tests/ -v --cov=app --cov-report=term-missing

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black
    
    - name: Lint with flake8
      run: |
        flake8 app tests --max-line-length=88 --extend-ignore=E203
    
    - name: Check formatting with black
      run: |
        black --check app tests
"""

# Test conftest
TEST_CONFTEST = """import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={{"check_same_thread": False}})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
"""

# Test API
TEST_API = """def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {{"status": "ok"}}


def test_create_ticket(client):
    ticket_data = {{
        "title": "Test Ticket",
        "description": "Test description",
        "status": "open"
    }}
    response = client.post("/api/v1/tickets/", json=ticket_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == ticket_data["title"]
    assert data["description"] == ticket_data["description"]
    assert "id" in data


def test_list_tickets(client):
    response = client.get("/api/v1/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_ticket(client):
    # Create a ticket first
    ticket_data = {{
        "title": "Test Ticket",
        "description": "Test description"
    }}
    create_response = client.post("/api/v1/tickets/", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Get the ticket
    response = client.get(f"/api/v1/tickets/{{ticket_id}}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == ticket_data["title"]


def test_update_ticket(client):
    # Create a ticket first
    ticket_data = {{
        "title": "Original Title",
        "description": "Original description"
    }}
    create_response = client.post("/api/v1/tickets/", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Update the ticket
    update_data = {{"title": "Updated Title"}}
    response = client.put(f"/api/v1/tickets/{{ticket_id}}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == ticket_data["description"]


def test_delete_ticket(client):
    # Create a ticket first
    ticket_data = {{
        "title": "Test Ticket",
        "description": "Test description"
    }}
    create_response = client.post("/api/v1/tickets/", json=ticket_data)
    ticket_id = create_response.json()["id"]
    
    # Delete the ticket
    response = client.delete(f"/api/v1/tickets/{{ticket_id}}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tickets/{{ticket_id}}")
    assert get_response.status_code == 404
"""

# Test Services
TEST_SERVICES = """from app.tickets.repositories import TicketRepository
from app.tickets.services import TicketService
from app.tickets.schemas import TicketCreate, TicketUpdate
from app.tickets.exceptions import TicketNotFoundException
import pytest


def test_create_ticket(db):
    repository = TicketRepository(db)
    service = TicketService(repository)
    
    ticket_data = TicketCreate(title="Test", description="Test description")
    ticket = service.create_ticket(ticket_data)
    
    assert ticket.id is not None
    assert ticket.title == "Test"


def test_get_all_tickets(db):
    repository = TicketRepository(db)
    service = TicketService(repository)
    
    # Create some tickets
    for i in range(3):
        service.create_ticket(TicketCreate(title=f"Ticket {{i}}"))
    
    tickets = service.get_all_tickets()
    assert len(tickets) == 3


def test_get_ticket_not_found(db):
    repository = TicketRepository(db)
    service = TicketService(repository)
    
    with pytest.raises(TicketNotFoundException):
        service.get_ticket(999)


def test_update_ticket(db):
    repository = TicketRepository(db)
    service = TicketService(repository)
    
    ticket = service.create_ticket(TicketCreate(title="Original"))
    updated = service.update_ticket(ticket.id, TicketUpdate(title="Updated"))
    
    assert updated.title == "Updated"


def test_delete_ticket(db):
    repository = TicketRepository(db)
    service = TicketService(repository)
    
    ticket = service.create_ticket(TicketCreate(title="To Delete"))
    service.delete_ticket(ticket.id)
    
    with pytest.raises(TicketNotFoundException):
        service.get_ticket(ticket.id)
"""

# Empty __init__ files
INIT_PY = ""


def to_snake_case(name: str) -> str:
    """Convert project name to snake_case for module names."""
    import re
    # Insert underscores before uppercase letters and convert to lowercase
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return name.lower().replace('-', '_').replace(' ', '_')


def to_class_name(name: str) -> str:
    """Convert project name to PascalCase for class names."""
    import re
    # Remove special characters and convert to PascalCase
    name = re.sub(r'[^a-zA-Z0-9]', ' ', name)
    return ''.join(word.capitalize() for word in name.split())


def generate_fastapi_boilerplate_func(config: Dict) -> Dict[str, str]:
    """Generate a comprehensive FastAPI boilerplate with clean architecture.

    Args:
        config: A dict following ProjectConfig fields.

    Returns:
        Mapping of file path -> file content.
    """
    project_name = config.get("project_name", "fastapi_app")
    db = config.get("db", "postgres")
    docker = config.get("docker", True)
    
    # Convert project name to different formats
    module_name = to_snake_case(project_name)  # e.g., "BrainROI" -> "brain_roi"
    class_name = to_class_name(project_name)   # e.g., "BrainROI" -> "Brainroi"
    CLASS_NAME = class_name.upper()            # e.g., "Brainroi" -> "BRAINROI"
    
    # Database URLs
    if db == "postgres":
        database_url = "postgresql://user:password@localhost:5432/app"
        database_url_docker = "postgresql://user:password@db:5432/app"
    else:
        database_url = "sqlite:///./app.db"
        database_url_docker = "sqlite:///./app.db"
    
    # Format templates with project-specific names
    # Main.py uses both format() for placeholders and module_name variable
    main_py = MAIN_PY.format(
        project_name=project_name,
        module_name=module_name
    )
    
    # Core constants
    core_constants_py = CORE_CONSTANTS_PY.format(
        database_url=database_url,
        project_name=project_name
    )
    
    # Module constants with all variables
    constants_py = TICKETS_CONSTANTS_PY.format(
        project_name=project_name,
        module_name=module_name,
        class_name=class_name,
        CLASS_NAME=CLASS_NAME
    )
    
    # Replace "tickets" with module_name and "Ticket" with class_name in other templates
    models_py = TICKETS_MODELS_PY.replace("Ticket", class_name).replace("ticket", module_name)
    schemas_py = TICKETS_SCHEMAS_PY.replace("Ticket", class_name).replace("ticket", module_name)
    repositories_py = TICKETS_REPOSITORIES_PY.replace("Ticket", class_name).replace("ticket", module_name)
    services_py = TICKETS_SERVICES_PY.replace("Ticket", class_name).replace("ticket", module_name)
    router_py = TICKETS_ROUTER_PY.replace("Ticket", class_name).replace("ticket", module_name)
    dependencies_py = TICKETS_DEPENDENCIES_PY.replace("Ticket", class_name).replace("ticket", module_name)
    exceptions_py = TICKETS_EXCEPTIONS_PY.replace("Ticket", class_name).replace("ticket", module_name)
    
    # Update tests to use the new module name
    test_api = TEST_API.replace("tickets", module_name).replace("Ticket", class_name).replace("ticket", module_name)
    test_services = TEST_SERVICES.replace("Ticket", class_name).replace("ticket", module_name)
    
    files: Dict[str, str] = {}
    
    # App structure
    files["app/__init__.py"] = INIT_PY
    files["app/main.py"] = main_py
    
    # Core module
    files["app/core/__init__.py"] = INIT_PY
    # Choose the appropriate database implementation
    if db == "sqlite":
        files["app/core/database.py"] = DATABASE_SQLITE_PY
    else:
        files["app/core/database.py"] = DATABASE_POSTGRES_PY
    files["app/core/constants.py"] = core_constants_py
    
    # Domain module (named after the project)
    files[f"app/{module_name}/__init__.py"] = INIT_PY
    files[f"app/{module_name}/models.py"] = models_py
    files[f"app/{module_name}/schemas.py"] = schemas_py
    files[f"app/{module_name}/repositories.py"] = repositories_py
    files[f"app/{module_name}/services.py"] = services_py
    files[f"app/{module_name}/router.py"] = router_py
    files[f"app/{module_name}/dependencies.py"] = dependencies_py
    files[f"app/{module_name}/exceptions.py"] = exceptions_py
    files[f"app/{module_name}/constants.py"] = constants_py
    
    # Tests
    files["tests/__init__.py"] = INIT_PY
    files["tests/conftest.py"] = TEST_CONFTEST
    files["tests/test_api.py"] = test_api
    files["tests/test_services.py"] = test_services
    
    # Root files
    files["requirements.txt"] = REQUIREMENTS
    files["pyproject.toml"] = PYPROJECT_TOML.format(project_name=project_name)
    files["README.md"] = README.format(project_name=project_name)
    files["Makefile"] = MAKEFILE
    files[".github/workflows/ci.yml"] = GITHUB_ACTIONS
    
    # Docker files
    if docker:
        files["Dockerfile"] = DOCKERFILE
        if db == "postgres":
            files["docker-compose.yml"] = DOCKER_COMPOSE.format(
                database_url_docker=database_url_docker
            )
    
    return files


# Export as a tool for potential use with LangChain agents
generate_fastapi_boilerplate = tool(generate_fastapi_boilerplate_func)

import pytest
import os
import tempfile
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app import models
from app.config import DATABASE_URL

# Test database URL - use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    """Create test database and tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db) -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """Create test client with database session override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }


@pytest.fixture
def sample_user_login_data() -> Dict[str, Any]:
    """Sample user login data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_nonprofit_profile_data() -> Dict[str, Any]:
    """Sample nonprofit profile data for testing."""
    return {
        "user_id": 1,
        "name": "Test Nonprofit",
        "mission": "To test nonprofit functionality",
        "demographics": "Young adults aged 18-35",
        "past_methods": "Social media campaigns, fundraising events",
        "fundraising_goals": "Raise $10,000 for community programs",
        "service_tags": ["education", "community", "youth"],
        "sustainability_practices": "Use renewable energy, minimize waste"
    }


@pytest.fixture
def sample_strategy_request_data() -> Dict[str, Any]:
    """Sample strategy request data for testing."""
    return {
        "profile_id": 1,
        "query": "How can we improve our digital fundraising strategy?"
    }


@pytest.fixture
def created_user(client: TestClient, sample_user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a test user and return user data."""
    response = client.post("/api/auth/register", json=sample_user_data)
    assert response.status_code == 200
    return sample_user_data


@pytest.fixture
def created_nonprofit_profile(
    client: TestClient,
    created_user: Dict[str, Any],
    sample_nonprofit_profile_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a test nonprofit profile and return profile data."""
    response = client.post("/api/profile/", json=sample_nonprofit_profile_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for AI testing."""
    with patch('app.ai.strategy_agent.client') as mock_client:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mock AI generated strategy content"
        mock_client.chat.completions.create.return_value = mock_response
        yield mock_client


@pytest.fixture
def mock_groq_api_key():
    """Mock GROQ API key for testing."""
    with patch.dict(os.environ, {'GROQ_API_KEY': 'test-api-key'}):
        yield


@pytest.fixture
def sample_ai_strategy_response() -> Dict[str, Any]:
    """Sample AI strategy response for testing."""
    return {
        "title": "Digital Fundraising Strategy",
        "content": "Here's a comprehensive digital fundraising strategy:\n\n1. Social Media Campaigns\n2. Email Marketing\n3. Crowdfunding Platforms\n4. Corporate Partnerships"
    }


@pytest.fixture(scope="session")
def test_env_vars():
    """Set up test environment variables."""
    original_env = os.environ.copy()

    # Set test environment variables
    test_vars = {
        "DATABASE_URL": TEST_DATABASE_URL,
        "GROQ_API_KEY": "test-groq-key",
        "LLAMA_MODEL": "llama3-8b-8192",
        "TESTING": "true"
    }

    for key, value in test_vars.items():
        os.environ[key] = value

    yield test_vars

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def cleanup_test_db():
    """Clean up test database after tests."""
    yield
    # Clean up test database file if it exists
    if os.path.exists("test.db"):
        os.remove("test.db")


# Async fixtures for async testing
@pytest.fixture
async def async_client(db_session) -> Generator[TestClient, None, None]:
    """Create async test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Database model fixtures
@pytest.fixture
def user_model_instance(db_session: Session, sample_user_data: Dict[str, Any]) -> models.User:
    """Create a User model instance in the database."""
    from app.routes.auth import hash_password

    user = models.User(
        email=sample_user_data["email"],
        name=sample_user_data["name"],
        hashed_password=hash_password(sample_user_data["password"])
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def nonprofit_profile_model_instance(
    db_session: Session,
    user_model_instance: models.User,
    sample_nonprofit_profile_data: Dict[str, Any]
) -> models.NonProfitProfile:
    """Create a NonProfitProfile model instance in the database."""
    profile_data = sample_nonprofit_profile_data.copy()
    profile_data["user_id"] = user_model_instance.id
    profile_data["service_tags"] = ",".join(profile_data["service_tags"])

    profile = models.NonProfitProfile(**profile_data)
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


@pytest.fixture
def strategy_model_instance(
    db_session: Session,
    nonprofit_profile_model_instance: models.NonProfitProfile,
    sample_ai_strategy_response: Dict[str, Any]
) -> models.Strategy:
    """Create a Strategy model instance in the database."""
    strategy = models.Strategy(
        profile_id=nonprofit_profile_model_instance.id,
        title=sample_ai_strategy_response["title"],
        content=sample_ai_strategy_response["content"]
    )
    db_session.add(strategy)
    db_session.commit()
    db_session.refresh(strategy)
    return strategy


# Parametrized fixtures for different test scenarios
@pytest.fixture(params=[
    {"email": "user1@test.com", "name": "User One", "password": "password123"},
    {"email": "user2@test.com", "name": "User Two", "password": "password456"},
    {"email": "user3@test.com", "name": "User Three", "password": "password789"}
])
def multiple_users_data(request):
    """Parametrized fixture for multiple user test scenarios."""
    return request.param


@pytest.fixture(params=[
    "How can we improve our social media presence?",
    "What are the best fundraising events for our cause?",
    "How do we engage corporate sponsors?",
    "What digital tools should we use for donor management?"
])
def strategy_queries(request):
    """Parametrized fixture for different strategy queries."""
    return request.param

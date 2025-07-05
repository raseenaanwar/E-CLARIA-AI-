# E-CLARIA AI - Testing & Docker Setup

This document provides comprehensive instructions for setting up Docker, running tests, and understanding the testing architecture for the E-CLARIA AI project.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Setup](#docker-setup)
- [Testing Architecture](#testing-architecture)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Environment Setup](#environment-setup)
- [CI/CD Integration](#cicd-integration)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.12+ (for local development)
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd E-CLARIA-AI-

# Switch to dev branch
git checkout dev

# Copy environment file
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

### 2. Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Check service status
docker-compose ps
```

### 3. Run Tests

```bash
# Run all tests
python run_tests.py

# Run tests in Docker
docker-compose run --rm test

# Run with coverage
python run_tests.py --coverage
```

## Docker Setup

### Architecture

The Docker setup includes:

- **app**: Main FastAPI application
- **db**: PostgreSQL database
- **redis**: Redis for caching
- **test**: Isolated test environment

### Services

#### Application Service
```yaml
app:
  - Builds from Dockerfile
  - Exposes port 8000
  - Depends on db and redis
  - Auto-reloads in development
```

#### Database Service
```yaml
db:
  - PostgreSQL 15 Alpine
  - Persistent data volume
  - Health checks enabled
  - Initialization scripts
```

#### Redis Service
```yaml
redis:
  - Redis 7 Alpine
  - Persistent data volume
  - Health checks enabled
```

#### Test Service
```yaml
test:
  - Same image as app
  - Separate test database
  - Runs pytest automatically
  - Isolated environment
```

### Docker Commands

```bash
# Build services
docker-compose build

# Start services
docker-compose up

# Start specific service
docker-compose up app

# Run tests
docker-compose run --rm test

# Access application shell
docker-compose exec app bash

# Access database
docker-compose exec db psql -U eclaria_user -d eclaria_db

# View logs
docker-compose logs app

# Clean up
docker-compose down
docker-compose down -v  # Remove volumes
```

## Testing Architecture

### Directory Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_models.py       # Database model tests
│   ├── test_schemas.py      # Pydantic schema tests
│   └── test_ai_strategy_agent.py # AI component tests
├── integration/             # Integration tests
│   ├── test_auth_routes.py  # Authentication API tests
│   ├── test_profile_routes.py # Profile API tests
│   └── test_strategy_routes.py # Strategy API tests
└── fixtures/                # Test data and fixtures
    └── test_data.py         # Reusable test data
```

### Test Configuration

The project uses pytest with the following plugins:

- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **pytest-xdist**: Parallel test execution
- **pytest-html**: HTML reports

### Fixtures

Common fixtures available in all tests:

- `client`: FastAPI test client
- `db_session`: Database session
- `created_user`: Pre-created test user
- `created_nonprofit_profile`: Pre-created test profile
- `mock_openai_client`: Mocked AI client
- `sample_*_data`: Sample data generators

## Running Tests

### Basic Test Commands

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit
python run_tests.py --integration

# Run with verbose output
python run_tests.py --verbose

# Run with coverage
python run_tests.py --coverage

# Run tests with specific markers
python run_tests.py --markers auth
python run_tests.py --markers "auth or profile"
```

### Advanced Test Commands

```bash
# Run tests in parallel
python run_tests.py --parallel

# Run fast tests only (skip slow tests)
python run_tests.py --fast

# Generate detailed reports
python run_tests.py --reports

# Run performance tests
python run_tests.py --performance

# Discover available tests
python run_tests.py --discover
```

### Docker Test Commands

```bash
# Run tests in Docker
docker-compose run --rm test

# Run specific test file
docker-compose run --rm test python -m pytest tests/unit/test_models.py

# Run with coverage in Docker
docker-compose run --rm test python -m pytest --cov=app

# Interactive test session
docker-compose run --rm test bash
```

### Direct Pytest Commands

```bash
# Run specific test file
pytest tests/unit/test_models.py

# Run specific test function
pytest tests/unit/test_models.py::TestUserModel::test_user_creation

# Run tests with specific marker
pytest -m "auth"

# Run tests with keyword
pytest -k "user_creation"

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## Test Categories

### Unit Tests

Test individual components in isolation:

- **Models**: Database model validation, relationships
- **Schemas**: Pydantic model validation, serialization
- **AI Components**: Strategy generation, error handling
- **Utilities**: Helper functions, data processing

Example:
```python
@pytest.mark.unit
def test_user_creation(db_session):
    user = models.User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

### Integration Tests

Test API endpoints and component interactions:

- **Authentication**: Registration, login, validation
- **Profile Management**: CRUD operations, validation
- **Strategy Generation**: End-to-end AI integration
- **Database Operations**: Complex queries, transactions

Example:
```python
@pytest.mark.integration
def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    })
    assert response.status_code == 200
```

### Test Markers

Available test markers:

- `unit`: Unit tests
- `integration`: Integration tests
- `auth`: Authentication tests
- `profile`: Profile tests
- `strategy`: Strategy tests
- `ai`: AI-related tests
- `database`: Database tests
- `slow`: Slow-running tests
- `api`: API endpoint tests

## Environment Setup

### Local Development

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

2. **Set Environment Variables**
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/eclaria_db"
   export GROQ_API_KEY="your-api-key"
   export TESTING=true
   ```

3. **Initialize Database**
   ```bash
   python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(engine)"
   ```

### Docker Development

1. **Start Services**
   ```bash
   docker-compose up -d
   ```

2. **Run Application**
   ```bash
   docker-compose exec app python run.py
   ```

3. **Access Services**
   - Application: http://localhost:8000
   - Database: localhost:5432
   - Redis: localhost:6379

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: python run_tests.py --coverage
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost/test_db
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Docker CI

```yaml
test-docker:
  runs-on: ubuntu-latest
  steps:
  - uses: actions/checkout@v3
  
  - name: Build and test
    run: |
      docker-compose build
      docker-compose run --rm test
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Start development environment
docker-compose up -d

# Run tests during development
python run_tests.py --unit --verbose

# Run specific test file
pytest tests/unit/test_new_feature.py -v
```

### 2. Pre-commit Checks

```bash
# Run all checks
python run_tests.py --lint
python run_tests.py --security
python run_tests.py --coverage

# Format code
python run_tests.py --format

# Run full test suite
python run_tests.py --reports
```

### 3. Code Quality

```bash
# Check code style
flake8 app/ tests/

# Format code
black app/ tests/
isort app/ tests/

# Type checking
mypy app/

# Security check
bandit -r app/
```

## Test Data Management

### Fixtures

The project uses pytest fixtures for reusable test data:

```python
@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }

@pytest.fixture
def created_user(client, sample_user_data):
    response = client.post("/api/auth/register", json=sample_user_data)
    return sample_user_data
```

### Test Data Generators

Use factories for generating test data:

```python
from tests.fixtures.test_data import TestDataGenerator

# Generate random user data
user_data = TestDataGenerator.generate_user_data()

# Generate specific user data
user_data = TestDataGenerator.generate_user_data(
    email="specific@example.com",
    name="Specific User"
)
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database service
   docker-compose ps db
   
   # Check database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

2. **Test Database Not Found**
   ```bash
   # Create test database
   docker-compose exec db createdb -U eclaria_user eclaria_test_db
   ```

3. **Permission Errors**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   
   # Fix Docker permissions
   docker-compose exec app chown -R eclaria:eclaria /app
   ```

4. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   
   # Or change port in docker-compose.yml
   ```

### Debug Commands

```bash
# Check service health
docker-compose ps

# View service logs
docker-compose logs app
docker-compose logs db

# Access application shell
docker-compose exec app bash

# Check database connection
docker-compose exec db psql -U eclaria_user -d eclaria_db -c "SELECT 1;"

# Check Redis connection
docker-compose exec redis redis-cli ping

# Run individual test with debug
pytest tests/unit/test_models.py::test_user_creation -v -s --pdb
```

### Performance Issues

```bash
# Run performance tests
python run_tests.py --performance

# Profile test execution
pytest --profile tests/

# Run tests with memory profiling
pytest --memray tests/

# Check database performance
docker-compose exec db pg_stat_activity
```

## Coverage Reports

### Generate Coverage

```bash
# Run tests with coverage
python run_tests.py --coverage

# Generate HTML report
pytest --cov=app --cov-report=html

# Generate XML report
pytest --cov=app --cov-report=xml
```

### Coverage Targets

- **Minimum Coverage**: 80%
- **Target Coverage**: 90%
- **Critical Paths**: 95%+

### View Coverage

```bash
# View in browser
open htmlcov/index.html

# View in terminal
pytest --cov=app --cov-report=term-missing
```

## Contributing

### Adding Tests

1. **Create test file** in appropriate directory
2. **Use appropriate markers** (`@pytest.mark.unit`, etc.)
3. **Add fixtures** for reusable data
4. **Follow naming convention** (`test_*` functions)
5. **Add docstrings** for complex tests

### Test Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Keep tests independent and isolated

### Code Review

- All tests must pass
- Coverage must not decrease
- Follow existing patterns
- Add integration tests for new APIs
- Document complex test scenarios

---

For more information, see the main [README.md](README.md) or contact the development team.
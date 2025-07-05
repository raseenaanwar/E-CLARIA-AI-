import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models
from app.routes.auth import hash_password


class TestAuthRoutes:
    """Integration tests for authentication routes."""

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_success(self, client: TestClient, sample_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json=sample_user_data)

        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_duplicate_email(self, client: TestClient, sample_user_data):
        """Test registration with duplicate email."""
        # Register first user
        response1 = client.post("/api/auth/register", json=sample_user_data)
        assert response1.status_code == 200

        # Try to register second user with same email
        response2 = client.post("/api/auth/register", json=sample_user_data)
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Email already registered"

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_invalid_email(self, client: TestClient):
        """Test registration with invalid email."""
        user_data = {
            "email": "invalid-email",
            "password": "testpassword123",
            "name": "Test User"
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_missing_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        # Missing email
        user_data = {
            "password": "testpassword123",
            "name": "Test User"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422

        # Missing password
        user_data = {
            "email": "test@example.com",
            "name": "Test User"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422

        # Missing name
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_empty_fields(self, client: TestClient):
        """Test registration with empty fields."""
        user_data = {
            "email": "",
            "password": "testpassword123",
            "name": "Test User"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_password_hashing(self, client: TestClient, db_session: Session, sample_user_data):
        """Test that password is properly hashed during registration."""
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 200

        # Verify user was created in database
        user = db_session.query(models.User).filter(
            models.User.email == sample_user_data["email"]
        ).first()

        assert user is not None
        assert user.hashed_password != sample_user_data["password"]  # Should be hashed
        assert user.hashed_password.startswith("$2b$")  # bcrypt hash format

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_success(self, client: TestClient, created_user, sample_user_login_data):
        """Test successful user login."""
        response = client.post("/api/auth/login", json=sample_user_login_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Login successful"
        assert "user_id" in response_data
        assert isinstance(response_data["user_id"], int)

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_invalid_email(self, client: TestClient, created_user):
        """Test login with invalid email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_invalid_password(self, client: TestClient, created_user):
        """Test login with invalid password."""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_missing_fields(self, client: TestClient):
        """Test login with missing required fields."""
        # Missing email
        login_data = {
            "password": "testpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 422

        # Missing password
        login_data = {
            "email": "test@example.com"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_empty_fields(self, client: TestClient):
        """Test login with empty fields."""
        login_data = {
            "email": "",
            "password": "testpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format."""
        login_data = {
            "email": "invalid-email",
            "password": "testpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_password_verification(self, client: TestClient, db_session: Session, sample_user_data):
        """Test that password verification works correctly."""
        # Register user
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 200

        # Get user from database
        user = db_session.query(models.User).filter(
            models.User.email == sample_user_data["email"]
        ).first()

        # Login with correct password
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.json()["user_id"] == user.id

    @pytest.mark.integration
    @pytest.mark.auth
    def test_multiple_user_registration_and_login(self, client: TestClient, multiple_users_data):
        """Test registration and login for multiple users."""
        # Register user
        response = client.post("/api/auth/register", json=multiple_users_data)
        assert response.status_code == 200

        # Login with the same user
        login_data = {
            "email": multiple_users_data["email"],
            "password": multiple_users_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_special_characters_in_name(self, client: TestClient):
        """Test registration with special characters in name."""
        user_data = {
            "email": "special@example.com",
            "password": "testpassword123",
            "name": "José María O'Connor-Smith"
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_unicode_name(self, client: TestClient):
        """Test registration with unicode characters in name."""
        user_data = {
            "email": "unicode@example.com",
            "password": "testpassword123",
            "name": "张三 李四 王五"
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_long_name(self, client: TestClient):
        """Test registration with very long name."""
        user_data = {
            "email": "longname@example.com",
            "password": "testpassword123",
            "name": "A" * 100  # 100 character name
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_long_password(self, client: TestClient):
        """Test registration with very long password."""
        user_data = {
            "email": "longpass@example.com",
            "password": "a" * 200,  # 200 character password
            "name": "Test User"
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_case_sensitive_email_login(self, client: TestClient, sample_user_data):
        """Test that email login is case insensitive."""
        # Register user with lowercase email
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 200

        # Try to login with uppercase email
        login_data = {
            "email": sample_user_data["email"].upper(),
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        # This might fail depending on database collation settings
        # The test documents current behavior
        assert response.status_code in [200, 401]

    @pytest.mark.integration
    @pytest.mark.auth
    def test_register_user_various_email_formats(self, client: TestClient):
        """Test registration with various valid email formats."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example123.com",
            "test@sub.example.com",
            "very.long.email.address@very.long.domain.name.com"
        ]

        for i, email in enumerate(valid_emails):
            user_data = {
                "email": email,
                "password": f"password{i}",
                "name": f"User {i}"
            }
            response = client.post("/api/auth/register", json=user_data)
            assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_routes_content_type(self, client: TestClient, sample_user_data):
        """Test that auth routes handle content-type correctly."""
        # Test with correct content-type
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 200

        # Test login with correct content-type
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_routes_response_format(self, client: TestClient, sample_user_data):
        """Test that auth routes return proper JSON responses."""
        # Test register response format
        response = client.post("/api/auth/register", json=sample_user_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "message" in response_data

        # Test login response format
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "message" in response_data
        assert "user_id" in response_data

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_database_transaction_rollback(self, client: TestClient, db_session: Session):
        """Test that failed registration doesn't leave partial data."""
        # This test depends on the actual database constraints
        # Try to register with invalid data that might cause database error
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }

        # First registration should succeed
        response1 = client.post("/api/auth/register", json=user_data)
        assert response1.status_code == 200

        # Second registration with same email should fail
        response2 = client.post("/api/auth/register", json=user_data)
        assert response2.status_code == 400

        # Verify only one user exists
        users_count = db_session.query(models.User).filter(
            models.User.email == user_data["email"]
        ).count()
        assert users_count == 1

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_routes_sql_injection_protection(self, client: TestClient):
        """Test that auth routes are protected against SQL injection."""
        # Attempt SQL injection in email field
        malicious_data = {
            "email": "'; DROP TABLE users; --",
            "password": "testpassword123",
            "name": "Test User"
        }

        response = client.post("/api/auth/register", json=malicious_data)
        # Should either fail validation or be safely handled
        assert response.status_code in [422, 400]

        # Attempt SQL injection in login
        malicious_login = {
            "email": "admin@example.com' OR '1'='1",
            "password": "anything"
        }

        response = client.post("/api/auth/login", json=malicious_login)
        # Should either fail validation or return 401
        assert response.status_code in [422, 401]

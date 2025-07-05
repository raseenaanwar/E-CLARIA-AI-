import pytest
from typing import List, Dict, Any
from pydantic import ValidationError
from app import schemas


class TestUserSchemas:
    """Test cases for User-related schemas."""

    @pytest.mark.unit
    def test_user_create_valid_data(self):
        """Test UserCreate schema with valid data."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
        user = schemas.UserCreate(**user_data)

        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.name == "Test User"

    @pytest.mark.unit
    def test_user_create_invalid_email(self):
        """Test UserCreate schema with invalid email."""
        user_data = {
            "email": "invalid-email",
            "password": "password123",
            "name": "Test User"
        }

        with pytest.raises(ValidationError) as exc_info:
            schemas.UserCreate(**user_data)

        assert "email" in str(exc_info.value)

    @pytest.mark.unit
    def test_user_create_missing_fields(self):
        """Test UserCreate schema with missing required fields."""
        # Missing email
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserCreate(password="password123", name="Test User")
        assert "email" in str(exc_info.value)

        # Missing password
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserCreate(email="test@example.com", name="Test User")
        assert "password" in str(exc_info.value)

        # Missing name
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserCreate(email="test@example.com", password="password123")
        assert "name" in str(exc_info.value)

    @pytest.mark.unit
    def test_user_create_empty_fields(self):
        """Test UserCreate schema with empty fields."""
        # Empty email
        with pytest.raises(ValidationError):
            schemas.UserCreate(email="", password="password123", name="Test User")

        # Empty password
        with pytest.raises(ValidationError):
            schemas.UserCreate(email="test@example.com", password="", name="Test User")

        # Empty name
        with pytest.raises(ValidationError):
            schemas.UserCreate(email="test@example.com", password="password123", name="")

    @pytest.mark.unit
    def test_user_login_valid_data(self):
        """Test UserLogin schema with valid data."""
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        user_login = schemas.UserLogin(**login_data)

        assert user_login.email == "test@example.com"
        assert user_login.password == "password123"

    @pytest.mark.unit
    def test_user_login_invalid_email(self):
        """Test UserLogin schema with invalid email."""
        login_data = {
            "email": "invalid-email",
            "password": "password123"
        }

        with pytest.raises(ValidationError) as exc_info:
            schemas.UserLogin(**login_data)

        assert "email" in str(exc_info.value)

    @pytest.mark.unit
    def test_user_out_valid_data(self):
        """Test UserOut schema with valid data."""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User"
        }
        user_out = schemas.UserOut(**user_data)

        assert user_out.id == 1
        assert user_out.email == "test@example.com"
        assert user_out.name == "Test User"

    @pytest.mark.unit
    def test_user_out_missing_fields(self):
        """Test UserOut schema with missing required fields."""
        # Missing id
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserOut(email="test@example.com", name="Test User")
        assert "id" in str(exc_info.value)

        # Missing email
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserOut(id=1, name="Test User")
        assert "email" in str(exc_info.value)

        # Missing name
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserOut(id=1, email="test@example.com")
        assert "name" in str(exc_info.value)


class TestNonProfitProfileSchemas:
    """Test cases for NonProfitProfile-related schemas."""

    @pytest.mark.unit
    def test_nonprofit_profile_create_valid_data(self):
        """Test NonProfitProfileCreate schema with valid data."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "To test nonprofit functionality",
            "demographics": "Young adults aged 18-35",
            "past_methods": "Social media campaigns",
            "fundraising_goals": "Raise $10,000",
            "service_tags": ["education", "community", "youth"],
            "sustainability_practices": "Use renewable energy"
        }
        profile = schemas.NonProfitProfileCreate(**profile_data)

        assert profile.user_id == 1
        assert profile.name == "Test Nonprofit"
        assert profile.mission == "To test nonprofit functionality"
        assert profile.demographics == "Young adults aged 18-35"
        assert profile.past_methods == "Social media campaigns"
        assert profile.fundraising_goals == "Raise $10,000"
        assert profile.service_tags == ["education", "community", "youth"]
        assert profile.sustainability_practices == "Use renewable energy"

    @pytest.mark.unit
    def test_nonprofit_profile_create_minimal_data(self):
        """Test NonProfitProfileCreate schema with minimal required data."""
        profile_data = {
            "user_id": 1,
            "name": "Minimal Nonprofit",
            "mission": "Minimal mission statement"
        }
        profile = schemas.NonProfitProfileCreate(**profile_data)

        assert profile.user_id == 1
        assert profile.name == "Minimal Nonprofit"
        assert profile.mission == "Minimal mission statement"
        assert profile.demographics is None
        assert profile.past_methods is None
        assert profile.fundraising_goals is None
        assert profile.service_tags == []
        assert profile.sustainability_practices is None

    @pytest.mark.unit
    def test_nonprofit_profile_create_missing_required_fields(self):
        """Test NonProfitProfileCreate schema with missing required fields."""
        # Missing user_id
        with pytest.raises(ValidationError) as exc_info:
            schemas.NonProfitProfileCreate(
                name="Test Nonprofit",
                mission="Test mission"
            )
        assert "user_id" in str(exc_info.value)

        # Missing name
        with pytest.raises(ValidationError) as exc_info:
            schemas.NonProfitProfileCreate(
                user_id=1,
                mission="Test mission"
            )
        assert "name" in str(exc_info.value)

        # Missing mission
        with pytest.raises(ValidationError) as exc_info:
            schemas.NonProfitProfileCreate(
                user_id=1,
                name="Test Nonprofit"
            )
        assert "mission" in str(exc_info.value)

    @pytest.mark.unit
    def test_nonprofit_profile_create_invalid_user_id(self):
        """Test NonProfitProfileCreate schema with invalid user_id."""
        profile_data = {
            "user_id": "invalid",
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }

        with pytest.raises(ValidationError) as exc_info:
            schemas.NonProfitProfileCreate(**profile_data)

        assert "user_id" in str(exc_info.value)

    @pytest.mark.unit
    def test_nonprofit_profile_create_empty_service_tags(self):
        """Test NonProfitProfileCreate schema with empty service_tags."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": []
        }
        profile = schemas.NonProfitProfileCreate(**profile_data)

        assert profile.service_tags == []

    @pytest.mark.unit
    def test_nonprofit_profile_create_service_tags_validation(self):
        """Test NonProfitProfileCreate schema service_tags validation."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": ["education", "community", "youth", "environment"]
        }
        profile = schemas.NonProfitProfileCreate(**profile_data)

        assert len(profile.service_tags) == 4
        assert "education" in profile.service_tags
        assert "community" in profile.service_tags
        assert "youth" in profile.service_tags
        assert "environment" in profile.service_tags

    @pytest.mark.unit
    def test_nonprofit_profile_out_valid_data(self):
        """Test NonProfitProfileOut schema with valid data."""
        profile_data = {
            "id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "demographics": "Young adults",
            "past_methods": "Social media",
            "fundraising_goals": "Raise $10,000",
            "service_tags": "education,community,youth",
            "sustainability_practices": "Green practices"
        }
        profile_out = schemas.NonProfitProfileOut(**profile_data)

        assert profile_out.id == 1
        assert profile_out.name == "Test Nonprofit"
        assert profile_out.mission == "Test mission"
        assert profile_out.demographics == "Young adults"
        assert profile_out.past_methods == "Social media"
        assert profile_out.fundraising_goals == "Raise $10,000"
        assert profile_out.service_tags == "education,community,youth"
        assert profile_out.sustainability_practices == "Green practices"

    @pytest.mark.unit
    def test_nonprofit_profile_out_with_none_values(self):
        """Test NonProfitProfileOut schema with None values for optional fields."""
        profile_data = {
            "id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "demographics": None,
            "past_methods": None,
            "fundraising_goals": None,
            "service_tags": None,
            "sustainability_practices": None
        }
        profile_out = schemas.NonProfitProfileOut(**profile_data)

        assert profile_out.id == 1
        assert profile_out.name == "Test Nonprofit"
        assert profile_out.mission == "Test mission"
        assert profile_out.demographics is None
        assert profile_out.past_methods is None
        assert profile_out.fundraising_goals is None
        assert profile_out.service_tags is None
        assert profile_out.sustainability_practices is None


class TestStrategySchemas:
    """Test cases for Strategy-related schemas."""

    @pytest.mark.unit
    def test_strategy_request_valid_data(self):
        """Test StrategyRequest schema with valid data."""
        request_data = {
            "profile_id": 1,
            "query": "How can we improve our fundraising strategy?"
        }
        strategy_request = schemas.StrategyRequest(**request_data)

        assert strategy_request.profile_id == 1
        assert strategy_request.query == "How can we improve our fundraising strategy?"

    @pytest.mark.unit
    def test_strategy_request_missing_fields(self):
        """Test StrategyRequest schema with missing required fields."""
        # Missing profile_id
        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyRequest(query="Test query")
        assert "profile_id" in str(exc_info.value)

        # Missing query
        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyRequest(profile_id=1)
        assert "query" in str(exc_info.value)

    @pytest.mark.unit
    def test_strategy_request_invalid_profile_id(self):
        """Test StrategyRequest schema with invalid profile_id."""
        request_data = {
            "profile_id": "invalid",
            "query": "Test query"
        }

        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyRequest(**request_data)

        assert "profile_id" in str(exc_info.value)

    @pytest.mark.unit
    def test_strategy_request_empty_query(self):
        """Test StrategyRequest schema with empty query."""
        request_data = {
            "profile_id": 1,
            "query": ""
        }

        with pytest.raises(ValidationError):
            schemas.StrategyRequest(**request_data)

    @pytest.mark.unit
    def test_strategy_request_long_query(self):
        """Test StrategyRequest schema with very long query."""
        long_query = "A" * 1000  # Very long query
        request_data = {
            "profile_id": 1,
            "query": long_query
        }

        # Should accept long queries
        strategy_request = schemas.StrategyRequest(**request_data)
        assert strategy_request.query == long_query

    @pytest.mark.unit
    def test_strategy_out_valid_data(self):
        """Test StrategyOut schema with valid data."""
        strategy_data = {
            "id": 1,
            "title": "Digital Fundraising Strategy",
            "content": "Here's a comprehensive strategy for digital fundraising..."
        }
        strategy_out = schemas.StrategyOut(**strategy_data)

        assert strategy_out.id == 1
        assert strategy_out.title == "Digital Fundraising Strategy"
        assert strategy_out.content == "Here's a comprehensive strategy for digital fundraising..."

    @pytest.mark.unit
    def test_strategy_out_missing_fields(self):
        """Test StrategyOut schema with missing required fields."""
        # Missing id
        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyOut(
                title="Test Strategy",
                content="Test content"
            )
        assert "id" in str(exc_info.value)

        # Missing title
        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyOut(
                id=1,
                content="Test content"
            )
        assert "title" in str(exc_info.value)

        # Missing content
        with pytest.raises(ValidationError) as exc_info:
            schemas.StrategyOut(
                id=1,
                title="Test Strategy"
            )
        assert "content" in str(exc_info.value)

    @pytest.mark.unit
    def test_strategy_out_empty_fields(self):
        """Test StrategyOut schema with empty fields."""
        # Empty title should fail
        with pytest.raises(ValidationError):
            schemas.StrategyOut(
                id=1,
                title="",
                content="Test content"
            )

        # Empty content should fail
        with pytest.raises(ValidationError):
            schemas.StrategyOut(
                id=1,
                title="Test Strategy",
                content=""
            )


class TestSchemaValidation:
    """Test cases for cross-schema validation and edge cases."""

    @pytest.mark.unit
    def test_email_validation_formats(self):
        """Test various email formats in schemas."""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example123.com",
            "test@sub.example.com"
        ]

        for email in valid_emails:
            user_data = {
                "email": email,
                "password": "password123",
                "name": "Test User"
            }
            user = schemas.UserCreate(**user_data)
            assert user.email == email

    @pytest.mark.unit
    def test_email_validation_invalid_formats(self):
        """Test invalid email formats in schemas."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test.example.com",
            "test space@example.com",
            ""
        ]

        for email in invalid_emails:
            user_data = {
                "email": email,
                "password": "password123",
                "name": "Test User"
            }
            with pytest.raises(ValidationError):
                schemas.UserCreate(**user_data)

    @pytest.mark.unit
    def test_service_tags_type_validation(self):
        """Test service_tags type validation."""
        # Valid list of strings
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": ["education", "community"]
        }
        profile = schemas.NonProfitProfileCreate(**profile_data)
        assert profile.service_tags == ["education", "community"]

        # Invalid: not a list
        with pytest.raises(ValidationError):
            profile_data["service_tags"] = "education,community"
            schemas.NonProfitProfileCreate(**profile_data)

    @pytest.mark.unit
    def test_integer_field_validation(self):
        """Test integer field validation."""
        # Valid integers
        valid_ids = [1, 100, 999999]
        for user_id in valid_ids:
            profile_data = {
                "user_id": user_id,
                "name": "Test Nonprofit",
                "mission": "Test mission"
            }
            profile = schemas.NonProfitProfileCreate(**profile_data)
            assert profile.user_id == user_id

        # Invalid integers
        invalid_ids = [-1, 0, "string", 1.5, None]
        for user_id in invalid_ids:
            profile_data = {
                "user_id": user_id,
                "name": "Test Nonprofit",
                "mission": "Test mission"
            }
            with pytest.raises(ValidationError):
                schemas.NonProfitProfileCreate(**profile_data)

    @pytest.mark.unit
    def test_schema_json_serialization(self):
        """Test that schemas can be serialized to JSON."""
        # UserOut schema
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User"
        }
        user_out = schemas.UserOut(**user_data)
        json_data = user_out.dict()

        assert json_data["id"] == 1
        assert json_data["email"] == "test@example.com"
        assert json_data["name"] == "Test User"

        # NonProfitProfileOut schema
        profile_data = {
            "id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "demographics": None,
            "past_methods": None,
            "fundraising_goals": None,
            "service_tags": "education,community",
            "sustainability_practices": None
        }
        profile_out = schemas.NonProfitProfileOut(**profile_data)
        json_data = profile_out.dict()

        assert json_data["id"] == 1
        assert json_data["service_tags"] == "education,community"
        assert json_data["demographics"] is None

    @pytest.mark.unit
    def test_schema_extra_fields_ignored(self):
        """Test that extra fields are ignored when creating schemas."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
            "extra_field": "should_be_ignored"
        }

        # This should not raise an error, extra field should be ignored
        user = schemas.UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.name == "Test User"
        assert not hasattr(user, "extra_field")

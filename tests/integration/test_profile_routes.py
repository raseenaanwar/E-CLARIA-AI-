import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models


class TestProfileRoutes:
    """Integration tests for profile routes."""

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_success(self, client: TestClient, created_user, sample_nonprofit_profile_data):
        """Test successful profile creation."""
        response = client.post("/api/profile/", json=sample_nonprofit_profile_data)

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["id"] is not None
        assert response_data["name"] == sample_nonprofit_profile_data["name"]
        assert response_data["mission"] == sample_nonprofit_profile_data["mission"]
        assert response_data["demographics"] == sample_nonprofit_profile_data["demographics"]
        assert response_data["past_methods"] == sample_nonprofit_profile_data["past_methods"]
        assert response_data["fundraising_goals"] == sample_nonprofit_profile_data["fundraising_goals"]
        assert response_data["service_tags"] == ",".join(sample_nonprofit_profile_data["service_tags"])
        assert response_data["sustainability_practices"] == sample_nonprofit_profile_data["sustainability_practices"]

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_minimal_data(self, client: TestClient, created_user):
        """Test profile creation with minimal required data."""
        minimal_profile_data = {
            "user_id": 1,
            "name": "Minimal Nonprofit",
            "mission": "Basic mission statement"
        }

        response = client.post("/api/profile/", json=minimal_profile_data)

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["id"] is not None
        assert response_data["name"] == "Minimal Nonprofit"
        assert response_data["mission"] == "Basic mission statement"
        assert response_data["demographics"] is None
        assert response_data["past_methods"] is None
        assert response_data["fundraising_goals"] is None
        assert response_data["service_tags"] is None
        assert response_data["sustainability_practices"] is None

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_missing_required_fields(self, client: TestClient):
        """Test profile creation with missing required fields."""
        # Missing user_id
        profile_data = {
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 422

        # Missing name
        profile_data = {
            "user_id": 1,
            "mission": "Test mission"
        }
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 422

        # Missing mission
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit"
        }
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_invalid_user_id(self, client: TestClient):
        """Test profile creation with invalid user_id."""
        profile_data = {
            "user_id": 999,  # Non-existent user
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }

        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 500  # Foreign key constraint error

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_empty_service_tags(self, client: TestClient, created_user):
        """Test profile creation with empty service tags."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": []
        }

        response = client.post("/api/profile/", json=profile_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["service_tags"] == ""

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_multiple_service_tags(self, client: TestClient, created_user):
        """Test profile creation with multiple service tags."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": ["education", "community", "youth", "environment", "health"]
        }

        response = client.post("/api/profile/", json=profile_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["service_tags"] == "education,community,youth,environment,health"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_long_text_fields(self, client: TestClient, created_user):
        """Test profile creation with long text fields."""
        long_text = "A" * 1000  # 1000 character text

        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": long_text,
            "demographics": long_text,
            "past_methods": long_text,
            "fundraising_goals": long_text,
            "sustainability_practices": long_text
        }

        response = client.post("/api/profile/", json=profile_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["mission"] == long_text
        assert response_data["demographics"] == long_text

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_unicode_characters(self, client: TestClient, created_user):
        """Test profile creation with unicode characters."""
        profile_data = {
            "user_id": 1,
            "name": "Fundación Esperanza 🌟",
            "mission": "Ayudar a las comunidades más necesitadas 💙",
            "demographics": "Familias de bajos recursos económicos",
            "service_tags": ["educación", "salud", "alimentación"]
        }

        response = client.post("/api/profile/", json=profile_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == "Fundación Esperanza 🌟"
        assert response_data["mission"] == "Ayudar a las comunidades más necesitadas 💙"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_get_profile_success(self, client: TestClient, created_nonprofit_profile):
        """Test successful profile retrieval."""
        user_id = 1
        response = client.get(f"/api/profile/{user_id}")

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["id"] == created_nonprofit_profile["id"]
        assert response_data["name"] == created_nonprofit_profile["name"]
        assert response_data["mission"] == created_nonprofit_profile["mission"]

    @pytest.mark.integration
    @pytest.mark.profile
    def test_get_profile_not_found(self, client: TestClient):
        """Test profile retrieval for non-existent user."""
        user_id = 999
        response = client.get(f"/api/profile/{user_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Profile not found"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_get_profile_invalid_user_id(self, client: TestClient):
        """Test profile retrieval with invalid user ID format."""
        response = client.get("/api/profile/invalid")

        assert response.status_code == 422  # Validation error

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_multiple_profiles_same_user(self, client: TestClient, created_user):
        """Test creating multiple profiles for the same user."""
        # Create first profile
        profile_data1 = {
            "user_id": 1,
            "name": "First Nonprofit",
            "mission": "First mission"
        }
        response1 = client.post("/api/profile/", json=profile_data1)
        assert response1.status_code == 200

        # Create second profile for same user
        profile_data2 = {
            "user_id": 1,
            "name": "Second Nonprofit",
            "mission": "Second mission"
        }
        response2 = client.post("/api/profile/", json=profile_data2)
        assert response2.status_code == 200

        # Both profiles should be created successfully
        assert response1.json()["id"] != response2.json()["id"]

    @pytest.mark.integration
    @pytest.mark.profile
    def test_create_profile_database_persistence(self, client: TestClient, created_user, db_session: Session):
        """Test that created profile is properly persisted in database."""
        profile_data = {
            "user_id": 1,
            "name": "Persistent Nonprofit",
            "mission": "Test persistence"
        }

        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 200

        profile_id = response.json()["id"]

        # Verify profile exists in database
        db_profile = db_session.query(models.NonProfitProfile).filter(
            models.NonProfitProfile.id == profile_id
        ).first()

        assert db_profile is not None
        assert db_profile.name == "Persistent Nonprofit"
        assert db_profile.mission == "Test persistence"
        assert db_profile.user_id == 1

    @pytest.mark.integration
    @pytest.mark.profile
    def test_get_profile_database_consistency(self, client: TestClient, created_nonprofit_profile, db_session: Session):
        """Test that GET profile returns consistent data with database."""
        user_id = 1
        response = client.get(f"/api/profile/{user_id}")
        assert response.status_code == 200

        api_profile = response.json()

        # Get profile from database
        db_profile = db_session.query(models.NonProfitProfile).filter(
            models.NonProfitProfile.user_id == user_id
        ).first()

        assert db_profile is not None
        assert api_profile["id"] == db_profile.id
        assert api_profile["name"] == db_profile.name
        assert api_profile["mission"] == db_profile.mission
        assert api_profile["demographics"] == db_profile.demographics

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_routes_content_type(self, client: TestClient, created_user):
        """Test that profile routes handle content-type correctly."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }

        # Test POST with JSON content-type
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Test GET response content-type
        user_id = 1
        response = client.get(f"/api/profile/{user_id}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_routes_response_format(self, client: TestClient, created_user):
        """Test that profile routes return proper response format."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }

        # Test POST response format
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert "name" in response_data
        assert "mission" in response_data

        # Test GET response format
        user_id = 1
        response = client.get(f"/api/profile/{user_id}")
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert "name" in response_data
        assert "mission" in response_data

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_service_tags_conversion(self, client: TestClient, created_user):
        """Test that service tags are properly converted between list and string."""
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "service_tags": ["education", "health", "environment"]
        }

        # Create profile with list of tags
        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 200

        # Response should have comma-separated string
        response_data = response.json()
        assert response_data["service_tags"] == "education,health,environment"

        # GET should return the same format
        user_id = 1
        response = client.get(f"/api/profile/{user_id}")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["service_tags"] == "education,health,environment"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_optional_fields_handling(self, client: TestClient, created_user):
        """Test that optional fields are handled correctly."""
        # Create profile with some optional fields as None
        profile_data = {
            "user_id": 1,
            "name": "Test Nonprofit",
            "mission": "Test mission",
            "demographics": "Young adults",
            "past_methods": None,
            "fundraising_goals": None,
            "sustainability_practices": "Green practices"
        }

        response = client.post("/api/profile/", json=profile_data)
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["demographics"] == "Young adults"
        assert response_data["past_methods"] is None
        assert response_data["fundraising_goals"] is None
        assert response_data["sustainability_practices"] == "Green practices"

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_field_validation(self, client: TestClient, created_user):
        """Test field validation for profile creation."""
        # Test with invalid field types
        invalid_profile_data = {
            "user_id": "invalid",  # Should be integer
            "name": "Test Nonprofit",
            "mission": "Test mission"
        }

        response = client.post("/api/profile/", json=invalid_profile_data)
        assert response.status_code == 422

        # Test with None for required fields
        invalid_profile_data = {
            "user_id": 1,
            "name": None,  # Required field
            "mission": "Test mission"
        }

        response = client.post("/api/profile/", json=invalid_profile_data)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_routes_error_handling(self, client: TestClient):
        """Test error handling in profile routes."""
        # Test POST with malformed JSON
        response = client.post(
            "/api/profile/",
            data="malformed json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

        # Test GET with malformed user_id
        response = client.get("/api/profile/not-a-number")
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_large_dataset_handling(self, client: TestClient, created_user):
        """Test profile creation with large amounts of data."""
        # Create profile with maximum realistic field sizes
        large_profile_data = {
            "user_id": 1,
            "name": "Very Long Nonprofit Organization Name With Many Words",
            "mission": "A" * 2000,  # Very long mission statement
            "demographics": "B" * 1000,  # Long demographics
            "past_methods": "C" * 1000,  # Long past methods
            "fundraising_goals": "D" * 1000,  # Long fundraising goals
            "service_tags": [f"tag{i}" for i in range(50)],  # Many tags
            "sustainability_practices": "E" * 1000  # Long sustainability practices
        }

        response = client.post("/api/profile/", json=large_profile_data)
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 422, 413]  # 413 = Payload Too Large

    @pytest.mark.integration
    @pytest.mark.profile
    def test_profile_concurrent_creation(self, client: TestClient, created_user):
        """Test concurrent profile creation (basic test)."""
        # This is a basic test - real concurrent testing would require threading
        profiles = []

        for i in range(3):
            profile_data = {
                "user_id": 1,
                "name": f"Nonprofit {i}",
                "mission": f"Mission {i}"
            }
            response = client.post("/api/profile/", json=profile_data)
            assert response.status_code == 200
            profiles.append(response.json())

        # All profiles should have unique IDs
        profile_ids = [p["id"] for p in profiles]
        assert len(set(profile_ids)) == len(profile_ids)  # All IDs unique

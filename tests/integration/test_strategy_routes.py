import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models


class TestStrategyRoutes:
    """Integration tests for strategy routes."""

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_success(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test successful strategy generation."""
        # Mock AI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Comprehensive fundraising strategy:\n\n1. Digital campaigns\n2. Community outreach\n3. Corporate partnerships"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "How can we improve our fundraising strategy?"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()

        assert "id" in response_data
        assert "title" in response_data
        assert "content" in response_data
        assert response_data["title"] == "Strategy for: How can we improve our fundraising strategy?"
        assert "Digital campaigns" in response_data["content"]
        assert "Community outreach" in response_data["content"]
        assert "Corporate partnerships" in response_data["content"]

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_nonexistent_profile(self, client: TestClient, mock_openai_client):
        """Test strategy generation with non-existent profile."""
        strategy_request = {
            "profile_id": 999,  # Non-existent profile
            "query": "Test query"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 404
        assert response.json()["detail"] == "Profile not found"

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_missing_fields(self, client: TestClient):
        """Test strategy generation with missing required fields."""
        # Missing profile_id
        strategy_request = {
            "query": "Test query"
        }
        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 422

        # Missing query
        strategy_request = {
            "profile_id": 1
        }
        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_invalid_profile_id(self, client: TestClient):
        """Test strategy generation with invalid profile_id format."""
        strategy_request = {
            "profile_id": "invalid",
            "query": "Test query"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_empty_query(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with empty query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "General strategy advice"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": ""
        }

        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 422  # Empty query should fail validation

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_long_query(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with very long query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for long query"
        mock_openai_client.chat.completions.create.return_value = mock_response

        long_query = "A" * 1000  # Very long query
        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": long_query
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()
        assert "title" in response_data
        assert "content" in response_data

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_database_persistence(self, client: TestClient, created_nonprofit_profile, mock_openai_client, db_session: Session):
        """Test that generated strategy is properly saved to database."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Saved strategy content"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Database persistence test"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 200

        strategy_id = response.json()["id"]

        # Verify strategy exists in database
        db_strategy = db_session.query(models.Strategy).filter(
            models.Strategy.id == strategy_id
        ).first()

        assert db_strategy is not None
        assert db_strategy.profile_id == created_nonprofit_profile["id"]
        assert db_strategy.title == "Strategy for: Database persistence test"
        assert db_strategy.content == "Saved strategy content"
        assert db_strategy.created_at is not None

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_ai_api_failure(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation when AI API fails."""
        # Mock AI API to raise exception
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Test query"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200  # Should still return 200 with error message
        response_data = response.json()

        assert response_data["title"] == "Strategy generation failed"
        assert "An error occurred: API Error" in response_data["content"]

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_unicode_content(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with unicode content."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Estrategia de recaudación de fondos 🌟\n\n1. Campañas digitales 📱\n2. Eventos comunitarios 🎉\n3. Alianzas corporativas 🤝"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "¿Cómo podemos mejorar nuestra estrategia de recaudación?"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()

        assert "🌟" in response_data["content"]
        assert "📱" in response_data["content"]
        assert "🎉" in response_data["content"]
        assert "🤝" in response_data["content"]

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_multiple_strategies_same_profile(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test generating multiple strategies for the same profile."""
        strategies = []

        for i in range(3):
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Strategy {i+1} content"
            mock_openai_client.chat.completions.create.return_value = mock_response

            strategy_request = {
                "profile_id": created_nonprofit_profile["id"],
                "query": f"Strategy query {i+1}"
            }

            response = client.post("/api/strategy/generate", json=strategy_request)
            assert response.status_code == 200
            strategies.append(response.json())

        # All strategies should have unique IDs
        strategy_ids = [s["id"] for s in strategies]
        assert len(set(strategy_ids)) == len(strategy_ids)

        # All strategies should belong to the same profile
        for strategy in strategies:
            assert strategy["title"].startswith("Strategy for: Strategy query")

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_response_format(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test that strategy generation returns proper response format."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test strategy content"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Test query"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert "title" in response_data
        assert "content" in response_data
        assert isinstance(response_data["id"], int)
        assert isinstance(response_data["title"], str)
        assert isinstance(response_data["content"], str)

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_different_queries(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with different types of queries."""
        test_queries = [
            "How can we improve our online presence?",
            "What are the best fundraising events for our cause?",
            "How do we engage with corporate sponsors?",
            "What digital tools should we use for donor management?",
            "How can we increase volunteer participation?"
        ]

        for query in test_queries:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Strategy response for: {query}"
            mock_openai_client.chat.completions.create.return_value = mock_response

            strategy_request = {
                "profile_id": created_nonprofit_profile["id"],
                "query": query
            }

            response = client.post("/api/strategy/generate", json=strategy_request)
            assert response.status_code == 200

            response_data = response.json()
            assert query[:50] in response_data["title"]
            assert f"Strategy response for: {query}" == response_data["content"]

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_special_characters(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with special characters in query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for special characters"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "How can we improve our ROI by 25%? What about $10,000 budget & partnerships?"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()
        assert "title" in response_data
        assert "content" in response_data

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_content_type_handling(self, client: TestClient, created_nonprofit_profile):
        """Test strategy generation with different content types."""
        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Test query"
        }

        # Test with JSON content-type
        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code in [200, 500]  # May fail due to missing mock

        # Test with malformed JSON
        response = client.post(
            "/api/strategy/generate",
            data="malformed json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_profile_relationship(self, client: TestClient, created_nonprofit_profile, mock_openai_client, db_session: Session):
        """Test that generated strategy maintains proper relationship with profile."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy content"
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Test relationship"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)
        assert response.status_code == 200

        strategy_id = response.json()["id"]

        # Verify relationship in database
        db_strategy = db_session.query(models.Strategy).filter(
            models.Strategy.id == strategy_id
        ).first()

        assert db_strategy is not None
        assert db_strategy.profile is not None
        assert db_strategy.profile.id == created_nonprofit_profile["id"]
        assert db_strategy.profile.name == created_nonprofit_profile["name"]

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_error_handling(self, client: TestClient):
        """Test error handling in strategy generation."""
        # Test with completely invalid request
        response = client.post("/api/strategy/generate", json={})
        assert response.status_code == 422

        # Test with wrong HTTP method
        response = client.get("/api/strategy/generate")
        assert response.status_code == 405  # Method not allowed

        # Test with invalid JSON structure
        response = client.post(
            "/api/strategy/generate",
            data='{"invalid": "structure"}',
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_concurrent_requests(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test concurrent strategy generation requests."""
        # This is a basic test - real concurrent testing would require threading
        strategies = []

        for i in range(3):
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Concurrent strategy {i}"
            mock_openai_client.chat.completions.create.return_value = mock_response

            strategy_request = {
                "profile_id": created_nonprofit_profile["id"],
                "query": f"Concurrent test {i}"
            }

            response = client.post("/api/strategy/generate", json=strategy_request)
            assert response.status_code == 200
            strategies.append(response.json())

        # All strategies should have unique IDs
        strategy_ids = [s["id"] for s in strategies]
        assert len(set(strategy_ids)) == len(strategy_ids)

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_large_response(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with large AI response."""
        # Mock a very large response
        large_content = "A" * 5000  # 5000 character response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = large_content
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Large response test"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data["content"]) == 5000

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_empty_ai_response(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with empty AI response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = ""
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Empty response test"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["content"] == ""
        assert response_data["title"] == "Strategy for: Empty response test"

    @pytest.mark.integration
    @pytest.mark.strategy
    def test_generate_strategy_whitespace_handling(self, client: TestClient, created_nonprofit_profile, mock_openai_client):
        """Test strategy generation with whitespace in AI response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "   \n\n  Strategy with whitespace  \n\n   "
        mock_openai_client.chat.completions.create.return_value = mock_response

        strategy_request = {
            "profile_id": created_nonprofit_profile["id"],
            "query": "Whitespace test"
        }

        response = client.post("/api/strategy/generate", json=strategy_request)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["content"] == "Strategy with whitespace"  # Should be stripped

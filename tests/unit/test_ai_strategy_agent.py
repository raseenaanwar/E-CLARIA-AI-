import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from app.ai.strategy_agent import generate_strategy
from app import models


class TestStrategyAgent:
    """Test cases for AI strategy agent."""

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_success(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test successful strategy generation."""
        # Mock the OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Here's a comprehensive fundraising strategy:\n\n1. Social Media Campaigns\n2. Email Marketing\n3. Corporate Partnerships"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "How can we improve our digital fundraising?"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["title"] == "Strategy for: How can we improve our digital fundraising?"
        assert "Social Media Campaigns" in result["content"]
        assert "Email Marketing" in result["content"]
        assert "Corporate Partnerships" in result["content"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_with_empty_query(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with empty query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "General fundraising strategy advice"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = ""
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["title"] == "Strategy for: "
        assert result["content"] == "General fundraising strategy advice"

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_with_long_query(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with very long query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for long query"
        mock_openai_client.chat.completions.create.return_value = mock_response

        long_query = "A" * 100  # 100 character query
        result = generate_strategy(nonprofit_profile_model_instance, long_query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        # Title should be truncated to 50 characters
        assert len(result["title"]) <= len("Strategy for: ") + 50
        assert result["title"].startswith("Strategy for: ")

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_openai_exception(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation when OpenAI API raises exception."""
        # Mock OpenAI to raise an exception
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["title"] == "Strategy generation failed"
        assert "An error occurred: API Error" in result["content"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_profile_data_formatting(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test that profile data is properly formatted in the prompt."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test strategy content"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        # Check that the API was called with correct parameters
        mock_openai_client.chat.completions.create.assert_called_once()
        call_args = mock_openai_client.chat.completions.create.call_args

        # Verify the prompt contains profile information
        messages = call_args[1]['messages']
        user_message = messages[1]['content']

        assert nonprofit_profile_model_instance.name in user_message
        assert nonprofit_profile_model_instance.mission in user_message
        assert query in user_message

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_api_parameters(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test that correct parameters are passed to OpenAI API."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test strategy content"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"
        generate_strategy(nonprofit_profile_model_instance, query)

        # Verify API call parameters
        mock_openai_client.chat.completions.create.assert_called_once()
        call_args = mock_openai_client.chat.completions.create.call_args

        assert call_args[1]['model'] == 'llama3-8b-8192'
        assert call_args[1]['temperature'] == 0.7
        assert call_args[1]['max_tokens'] == 800
        assert len(call_args[1]['messages']) == 2
        assert call_args[1]['messages'][0]['role'] == 'system'
        assert call_args[1]['messages'][1]['role'] == 'user'

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_with_none_profile_fields(self, mock_openai_client, db_session, user_model_instance):
        """Test strategy generation with profile having None values."""
        # Create a profile with minimal data (None values for optional fields)
        profile = models.NonProfitProfile(
            user_id=user_model_instance.id,
            name="Minimal Nonprofit",
            mission="Basic mission",
            demographics=None,
            past_methods=None,
            fundraising_goals=None,
            service_tags=None,
            sustainability_practices=None
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for minimal profile"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"
        result = generate_strategy(profile, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["content"] == "Strategy for minimal profile"

        # Verify the prompt was created without errors
        mock_openai_client.chat.completions.create.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_response_content_stripping(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test that response content is properly stripped of whitespace."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "   \n\nStrategy content with extra whitespace\n\n   "
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert result["content"] == "Strategy content with extra whitespace"

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_different_queries(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with different types of queries."""
        test_queries = [
            "How can we improve our online presence?",
            "What are the best fundraising events?",
            "How do we engage with corporate sponsors?",
            "What digital tools should we use?",
            "How can we increase donor retention?"
        ]

        for query in test_queries:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Strategy for: {query}"
            mock_openai_client.chat.completions.create.return_value = mock_response

            result = generate_strategy(nonprofit_profile_model_instance, query)

            assert isinstance(result, dict)
            assert "title" in result
            assert "content" in result
            assert query[:50] in result["title"]
            assert f"Strategy for: {query}" == result["content"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_empty_response(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation when OpenAI returns empty response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = ""
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["content"] == ""

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_special_characters_in_query(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with special characters in query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for special characters"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "How can we improve our ROI by 25%? What about $10,000 budget?"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert result["content"] == "Strategy for special characters"

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_unicode_characters(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with unicode characters."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy with unicode: 🚀 📈 💰"
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "How can we reach más personas in our communidad?"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result
        assert "🚀 📈 💰" in result["content"]


class TestStrategyAgentEnvironment:
    """Test cases for environment-related functionality."""

    @pytest.mark.unit
    @pytest.mark.ai
    def test_environment_variables_loading(self):
        """Test that environment variables are properly loaded."""
        with patch.dict(os.environ, {
            'GROQ_API_KEY': 'test-key',
            'LLAMA_MODEL': 'custom-model'
        }):
            # Re-import to pick up new environment variables
            from app.ai import strategy_agent

            # The module should have loaded the environment variables
            assert hasattr(strategy_agent, 'GROQ_API_KEY')
            assert hasattr(strategy_agent, 'LLAMA_MODEL')

    @pytest.mark.unit
    @pytest.mark.ai
    def test_missing_groq_api_key(self, nonprofit_profile_model_instance):
        """Test behavior when GROQ_API_KEY is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('app.ai.strategy_agent.GROQ_API_KEY', None):
                # Mock the client to raise an authentication error
                with patch('app.ai.strategy_agent.client') as mock_client:
                    mock_client.chat.completions.create.side_effect = Exception("Authentication failed")

                    query = "Test query"
                    result = generate_strategy(nonprofit_profile_model_instance, query)

                    assert result["title"] == "Strategy generation failed"
                    assert "Authentication failed" in result["content"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_custom_llama_model(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test using custom LLAMA model."""
        custom_model = "llama3-70b-8192"

        with patch.dict(os.environ, {'LLAMA_MODEL': custom_model}):
            with patch('app.ai.strategy_agent.LLAMA_MODEL', custom_model):
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = "Strategy from custom model"
                mock_openai_client.chat.completions.create.return_value = mock_response

                query = "Test query"
                result = generate_strategy(nonprofit_profile_model_instance, query)

                # Verify the custom model was used
                call_args = mock_openai_client.chat.completions.create.call_args
                assert call_args[1]['model'] == custom_model
                assert result["content"] == "Strategy from custom model"


class TestStrategyAgentEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_with_none_profile(self, mock_openai_client):
        """Test strategy generation with None profile."""
        query = "Test query"

        with pytest.raises(AttributeError):
            generate_strategy(None, query)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_with_none_query(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test strategy generation with None query."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Strategy for None query"
        mock_openai_client.chat.completions.create.return_value = mock_response

        result = generate_strategy(nonprofit_profile_model_instance, None)

        assert isinstance(result, dict)
        assert "title" in result
        assert "content" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_malformed_api_response(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test handling of malformed API response."""
        # Mock a response with missing expected structure
        mock_response = Mock()
        mock_response.choices = []
        mock_openai_client.chat.completions.create.return_value = mock_response

        query = "Test query"

        with pytest.raises(IndexError):
            generate_strategy(nonprofit_profile_model_instance, query)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_network_timeout(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test handling of network timeout."""
        mock_openai_client.chat.completions.create.side_effect = Exception("Request timeout")

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert result["title"] == "Strategy generation failed"
        assert "Request timeout" in result["content"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_strategy_rate_limit_error(self, mock_openai_client, nonprofit_profile_model_instance):
        """Test handling of rate limit error."""
        mock_openai_client.chat.completions.create.side_effect = Exception("Rate limit exceeded")

        query = "Test query"
        result = generate_strategy(nonprofit_profile_model_instance, query)

        assert result["title"] == "Strategy generation failed"
        assert "Rate limit exceeded" in result["content"]

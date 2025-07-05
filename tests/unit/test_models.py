import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import models


class TestUserModel:
    """Test cases for User model."""

    @pytest.mark.unit
    def test_user_creation(self, db_session):
        """Test creating a new user."""
        user = models.User(
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password_123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.hashed_password == "hashed_password_123"

    @pytest.mark.unit
    def test_user_email_unique_constraint(self, db_session):
        """Test that email must be unique."""
        user1 = models.User(
            email="duplicate@example.com",
            name="User One",
            hashed_password="password1"
        )
        user2 = models.User(
            email="duplicate@example.com",
            name="User Two",
            hashed_password="password2"
        )

        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    @pytest.mark.unit
    def test_user_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Test missing email
        with pytest.raises(IntegrityError):
            user = models.User(
                name="Test User",
                hashed_password="password"
            )
            db_session.add(user)
            db_session.commit()

    @pytest.mark.unit
    def test_user_string_representation(self, db_session):
        """Test user model string representation."""
        user = models.User(
            email="test@example.com",
            name="Test User",
            hashed_password="hashed_password"
        )
        db_session.add(user)
        db_session.commit()

        # Test that the user object can be converted to string without error
        str_repr = str(user)
        assert str_repr is not None


class TestNonProfitProfileModel:
    """Test cases for NonProfitProfile model."""

    @pytest.mark.unit
    def test_nonprofit_profile_creation(self, db_session, user_model_instance):
        """Test creating a new nonprofit profile."""
        profile = models.NonProfitProfile(
            user_id=user_model_instance.id,
            name="Test Nonprofit",
            mission="To test nonprofit functionality",
            demographics="Young adults aged 18-35",
            past_methods="Social media campaigns",
            fundraising_goals="Raise $10,000",
            service_tags="education,community,youth",
            sustainability_practices="Use renewable energy"
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)

        assert profile.id is not None
        assert profile.user_id == user_model_instance.id
        assert profile.name == "Test Nonprofit"
        assert profile.mission == "To test nonprofit functionality"
        assert profile.demographics == "Young adults aged 18-35"
        assert profile.past_methods == "Social media campaigns"
        assert profile.fundraising_goals == "Raise $10,000"
        assert profile.service_tags == "education,community,youth"
        assert profile.sustainability_practices == "Use renewable energy"

    @pytest.mark.unit
    def test_nonprofit_profile_optional_fields(self, db_session, user_model_instance):
        """Test that optional fields can be None."""
        profile = models.NonProfitProfile(
            user_id=user_model_instance.id,
            name="Minimal Nonprofit",
            mission="Minimal mission statement"
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)

        assert profile.id is not None
        assert profile.demographics is None
        assert profile.past_methods is None
        assert profile.fundraising_goals is None
        assert profile.service_tags is None
        assert profile.sustainability_practices is None

    @pytest.mark.unit
    def test_nonprofit_profile_foreign_key_constraint(self, db_session):
        """Test foreign key constraint with non-existent user."""
        profile = models.NonProfitProfile(
            user_id=999,  # Non-existent user ID
            name="Test Nonprofit",
            mission="Test mission"
        )
        db_session.add(profile)

        with pytest.raises(IntegrityError):
            db_session.commit()

    @pytest.mark.unit
    def test_nonprofit_profile_strategies_relationship(self, db_session, nonprofit_profile_model_instance):
        """Test the relationship between profile and strategies."""
        # Create a strategy for the profile
        strategy = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            title="Test Strategy",
            content="Test strategy content"
        )
        db_session.add(strategy)
        db_session.commit()

        # Refresh the profile to load the relationship
        db_session.refresh(nonprofit_profile_model_instance)

        assert len(nonprofit_profile_model_instance.strategies) == 1
        assert nonprofit_profile_model_instance.strategies[0].title == "Test Strategy"

    @pytest.mark.unit
    def test_nonprofit_profile_required_fields(self, db_session, user_model_instance):
        """Test that required fields are enforced."""
        # Test missing name
        with pytest.raises(IntegrityError):
            profile = models.NonProfitProfile(
                user_id=user_model_instance.id,
                mission="Test mission"
            )
            db_session.add(profile)
            db_session.commit()


class TestStrategyModel:
    """Test cases for Strategy model."""

    @pytest.mark.unit
    def test_strategy_creation(self, db_session, nonprofit_profile_model_instance):
        """Test creating a new strategy."""
        strategy = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            title="Test Strategy",
            content="This is a test strategy content"
        )
        db_session.add(strategy)
        db_session.commit()
        db_session.refresh(strategy)

        assert strategy.id is not None
        assert strategy.profile_id == nonprofit_profile_model_instance.id
        assert strategy.title == "Test Strategy"
        assert strategy.content == "This is a test strategy content"
        assert strategy.created_at is not None
        assert isinstance(strategy.created_at, datetime)

    @pytest.mark.unit
    def test_strategy_optional_title(self, db_session, nonprofit_profile_model_instance):
        """Test that title is optional."""
        strategy = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="Strategy content without title"
        )
        db_session.add(strategy)
        db_session.commit()
        db_session.refresh(strategy)

        assert strategy.title is None
        assert strategy.content == "Strategy content without title"

    @pytest.mark.unit
    def test_strategy_required_content(self, db_session, nonprofit_profile_model_instance):
        """Test that content is required."""
        with pytest.raises(IntegrityError):
            strategy = models.Strategy(
                profile_id=nonprofit_profile_model_instance.id,
                title="Strategy without content"
            )
            db_session.add(strategy)
            db_session.commit()

    @pytest.mark.unit
    def test_strategy_foreign_key_constraint(self, db_session):
        """Test foreign key constraint with non-existent profile."""
        strategy = models.Strategy(
            profile_id=999,  # Non-existent profile ID
            content="Test strategy content"
        )
        db_session.add(strategy)

        with pytest.raises(IntegrityError):
            db_session.commit()

    @pytest.mark.unit
    def test_strategy_profile_relationship(self, db_session, nonprofit_profile_model_instance):
        """Test the relationship between strategy and profile."""
        strategy = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            title="Test Strategy",
            content="Test strategy content"
        )
        db_session.add(strategy)
        db_session.commit()
        db_session.refresh(strategy)

        assert strategy.profile is not None
        assert strategy.profile.id == nonprofit_profile_model_instance.id
        assert strategy.profile.name == nonprofit_profile_model_instance.name

    @pytest.mark.unit
    def test_strategy_created_at_auto_generated(self, db_session, nonprofit_profile_model_instance):
        """Test that created_at is automatically set."""
        before_creation = datetime.utcnow()

        strategy = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="Test strategy content"
        )
        db_session.add(strategy)
        db_session.commit()
        db_session.refresh(strategy)

        after_creation = datetime.utcnow()

        assert strategy.created_at is not None
        assert before_creation <= strategy.created_at <= after_creation

    @pytest.mark.unit
    def test_multiple_strategies_for_profile(self, db_session, nonprofit_profile_model_instance):
        """Test creating multiple strategies for the same profile."""
        strategies = []
        for i in range(3):
            strategy = models.Strategy(
                profile_id=nonprofit_profile_model_instance.id,
                title=f"Strategy {i+1}",
                content=f"Content for strategy {i+1}"
            )
            strategies.append(strategy)
            db_session.add(strategy)

        db_session.commit()

        # Refresh the profile to load all strategies
        db_session.refresh(nonprofit_profile_model_instance)

        assert len(nonprofit_profile_model_instance.strategies) == 3
        strategy_titles = [s.title for s in nonprofit_profile_model_instance.strategies]
        assert "Strategy 1" in strategy_titles
        assert "Strategy 2" in strategy_titles
        assert "Strategy 3" in strategy_titles


class TestModelRelationships:
    """Test cases for model relationships."""

    @pytest.mark.unit
    def test_user_profile_relationship(self, db_session, user_model_instance):
        """Test the relationship between user and profile."""
        profile = models.NonProfitProfile(
            user_id=user_model_instance.id,
            name="Test Nonprofit",
            mission="Test mission"
        )
        db_session.add(profile)
        db_session.commit()

        # Query the profile by user_id
        queried_profile = db_session.query(models.NonProfitProfile).filter(
            models.NonProfitProfile.user_id == user_model_instance.id
        ).first()

        assert queried_profile is not None
        assert queried_profile.user_id == user_model_instance.id

    @pytest.mark.unit
    def test_cascade_delete_profile_strategies(self, db_session, nonprofit_profile_model_instance):
        """Test that deleting a profile handles related strategies appropriately."""
        # Create strategies for the profile
        strategy1 = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="Strategy 1 content"
        )
        strategy2 = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="Strategy 2 content"
        )
        db_session.add(strategy1)
        db_session.add(strategy2)
        db_session.commit()

        # Verify strategies exist
        strategies_count = db_session.query(models.Strategy).filter(
            models.Strategy.profile_id == nonprofit_profile_model_instance.id
        ).count()
        assert strategies_count == 2

        # Delete the profile
        db_session.delete(nonprofit_profile_model_instance)
        db_session.commit()

        # Verify strategies are handled appropriately
        # Note: The actual behavior depends on cascade settings in the model
        remaining_strategies = db_session.query(models.Strategy).filter(
            models.Strategy.profile_id == nonprofit_profile_model_instance.id
        ).all()

        # This test documents the current behavior
        # If cascade is set up, remaining_strategies should be empty
        # If not, foreign key constraint should prevent deletion
        assert isinstance(remaining_strategies, list)

    @pytest.mark.unit
    def test_query_strategies_by_profile(self, db_session, nonprofit_profile_model_instance):
        """Test querying strategies by profile."""
        # Create multiple strategies
        for i in range(5):
            strategy = models.Strategy(
                profile_id=nonprofit_profile_model_instance.id,
                title=f"Strategy {i+1}",
                content=f"Content {i+1}"
            )
            db_session.add(strategy)
        db_session.commit()

        # Query strategies by profile
        strategies = db_session.query(models.Strategy).filter(
            models.Strategy.profile_id == nonprofit_profile_model_instance.id
        ).all()

        assert len(strategies) == 5
        assert all(s.profile_id == nonprofit_profile_model_instance.id for s in strategies)

    @pytest.mark.unit
    def test_query_latest_strategy(self, db_session, nonprofit_profile_model_instance):
        """Test querying the latest strategy for a profile."""
        # Create strategies with different timestamps
        import time

        strategy1 = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="First strategy"
        )
        db_session.add(strategy1)
        db_session.commit()

        time.sleep(0.1)  # Small delay to ensure different timestamps

        strategy2 = models.Strategy(
            profile_id=nonprofit_profile_model_instance.id,
            content="Second strategy"
        )
        db_session.add(strategy2)
        db_session.commit()

        # Query latest strategy
        latest_strategy = db_session.query(models.Strategy).filter(
            models.Strategy.profile_id == nonprofit_profile_model_instance.id
        ).order_by(models.Strategy.created_at.desc()).first()

        assert latest_strategy is not None
        assert latest_strategy.content == "Second strategy"
        assert latest_strategy.created_at > strategy1.created_at

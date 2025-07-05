"""
Test fixtures and data generators for E-CLARIA AI testing.

This module provides reusable test data and fixtures for various test scenarios.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from faker import Faker

fake = Faker()


class TestDataGenerator:
    """Generate test data for various entities."""

    @staticmethod
    def generate_user_data(
        email: Optional[str] = None,
        name: Optional[str] = None,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate user test data."""
        return {
            "email": email or fake.email(),
            "name": name or fake.name(),
            "password": password or fake.password(length=12)
        }

    @staticmethod
    def generate_nonprofit_profile_data(
        user_id: int = 1,
        name: Optional[str] = None,
        mission: Optional[str] = None,
        demographics: Optional[str] = None,
        past_methods: Optional[str] = None,
        fundraising_goals: Optional[str] = None,
        service_tags: Optional[List[str]] = None,
        sustainability_practices: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate nonprofit profile test data."""
        return {
            "user_id": user_id,
            "name": name or fake.company(),
            "mission": mission or fake.text(max_nb_chars=200),
            "demographics": demographics or fake.text(max_nb_chars=100),
            "past_methods": past_methods or fake.text(max_nb_chars=150),
            "fundraising_goals": fundraising_goals or fake.text(max_nb_chars=120),
            "service_tags": service_tags or fake.words(nb=random.randint(2, 5)),
            "sustainability_practices": sustainability_practices or fake.text(max_nb_chars=100)
        }

    @staticmethod
    def generate_strategy_request_data(
        profile_id: int = 1,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate strategy request test data."""
        return {
            "profile_id": profile_id,
            "query": query or fake.sentence(nb_words=random.randint(5, 15))
        }

    @staticmethod
    def generate_strategy_response_data(
        title: Optional[str] = None,
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate strategy response test data."""
        return {
            "title": title or fake.sentence(nb_words=random.randint(3, 8)),
            "content": content or fake.text(max_nb_chars=500)
        }


class SampleData:
    """Predefined sample data for testing."""

    # Sample users
    USERS = [
        {
            "email": "john.doe@example.com",
            "name": "John Doe",
            "password": "password123"
        },
        {
            "email": "jane.smith@example.com",
            "name": "Jane Smith",
            "password": "securepass456"
        },
        {
            "email": "admin@nonprofit.org",
            "name": "Admin User",
            "password": "adminpass789"
        }
    ]

    # Sample nonprofit profiles
    NONPROFIT_PROFILES = [
        {
            "user_id": 1,
            "name": "Education First Foundation",
            "mission": "To provide quality education to underserved communities",
            "demographics": "Children aged 6-18 in rural areas",
            "past_methods": "School building projects, teacher training programs",
            "fundraising_goals": "Raise $50,000 for new school construction",
            "service_tags": ["education", "children", "rural", "infrastructure"],
            "sustainability_practices": "Use of renewable energy in school buildings"
        },
        {
            "user_id": 2,
            "name": "Health for All Initiative",
            "mission": "Improving healthcare access in developing regions",
            "demographics": "Adults and children in low-income communities",
            "past_methods": "Mobile health clinics, vaccination campaigns",
            "fundraising_goals": "Raise $100,000 for medical equipment",
            "service_tags": ["healthcare", "medical", "community", "mobile"],
            "sustainability_practices": "Eco-friendly medical waste disposal"
        },
        {
            "user_id": 3,
            "name": "Environmental Conservation Society",
            "mission": "Protecting natural habitats and wildlife",
            "demographics": "Environmental activists and local communities",
            "past_methods": "Tree planting campaigns, wildlife rescue operations",
            "fundraising_goals": "Raise $75,000 for habitat restoration",
            "service_tags": ["environment", "wildlife", "conservation", "nature"],
            "sustainability_practices": "Carbon-neutral operations and renewable energy use"
        }
    ]

    # Sample strategy queries
    STRATEGY_QUERIES = [
        "How can we improve our online fundraising presence?",
        "What are the most effective corporate partnership strategies?",
        "How do we engage younger donors in our cause?",
        "What digital tools should we use for donor management?",
        "How can we increase volunteer participation?",
        "What are the best practices for grant writing?",
        "How do we create compelling storytelling for our campaigns?",
        "What social media strategies work best for nonprofits?",
        "How can we improve donor retention rates?",
        "What are effective ways to reach new audiences?"
    ]

    # Sample AI strategy responses
    AI_STRATEGY_RESPONSES = [
        {
            "title": "Digital Fundraising Strategy",
            "content": """
Here's a comprehensive digital fundraising strategy:

1. **Social Media Campaigns**
   - Create engaging content on Facebook, Instagram, and Twitter
   - Use storytelling to showcase impact
   - Leverage user-generated content

2. **Email Marketing**
   - Segment your donor database
   - Create personalized campaigns
   - Use automation for follow-ups

3. **Crowdfunding Platforms**
   - Launch campaigns on GoFundMe, Kickstarter
   - Set realistic goals and timelines
   - Offer meaningful rewards

4. **Corporate Partnerships**
   - Identify aligned companies
   - Propose mutually beneficial partnerships
   - Create sponsorship packages
            """
        },
        {
            "title": "Community Engagement Strategy",
            "content": """
Build stronger community connections:

1. **Local Events**
   - Host community meetings
   - Participate in local festivals
   - Organize volunteer appreciation events

2. **Partnership Building**
   - Collaborate with other nonprofits
   - Work with local businesses
   - Engage with government agencies

3. **Communication**
   - Regular newsletter updates
   - Community feedback sessions
   - Social media engagement

4. **Volunteer Programs**
   - Create diverse volunteer opportunities
   - Provide proper training
   - Recognize contributions
            """
        }
    ]

    # Sample service tags
    SERVICE_TAGS = [
        "education", "healthcare", "environment", "community", "youth",
        "elderly", "poverty", "homelessness", "mental health", "disability",
        "arts", "culture", "sports", "technology", "research", "advocacy",
        "human rights", "animal welfare", "disaster relief", "international"
    ]

    # Sample fundraising goals
    FUNDRAISING_GOALS = [
        "Raise $10,000 for program expansion",
        "Secure $25,000 for equipment purchase",
        "Generate $50,000 for facility renovation",
        "Collect $100,000 for scholarship fund",
        "Obtain $200,000 for research project",
        "Gather $5,000 for emergency relief",
        "Accumulate $15,000 for staff training",
        "Achieve $75,000 for community outreach"
    ]

    # Sample sustainability practices
    SUSTAINABILITY_PRACTICES = [
        "Use renewable energy sources",
        "Implement recycling programs",
        "Reduce paper usage through digitization",
        "Promote sustainable transportation",
        "Practice water conservation",
        "Source materials locally",
        "Minimize waste generation",
        "Use eco-friendly products"
    ]


class TestScenarios:
    """Predefined test scenarios for various use cases."""

    @staticmethod
    def get_user_registration_scenarios():
        """Get user registration test scenarios."""
        return [
            {
                "name": "valid_user",
                "data": TestDataGenerator.generate_user_data(),
                "expected_status": 200
            },
            {
                "name": "duplicate_email",
                "data": TestDataGenerator.generate_user_data(email="duplicate@test.com"),
                "expected_status": 400
            },
            {
                "name": "invalid_email",
                "data": TestDataGenerator.generate_user_data(email="invalid-email"),
                "expected_status": 422
            },
            {
                "name": "empty_password",
                "data": TestDataGenerator.generate_user_data(password=""),
                "expected_status": 422
            }
        ]

    @staticmethod
    def get_profile_creation_scenarios():
        """Get profile creation test scenarios."""
        return [
            {
                "name": "complete_profile",
                "data": TestDataGenerator.generate_nonprofit_profile_data(),
                "expected_status": 200
            },
            {
                "name": "minimal_profile",
                "data": TestDataGenerator.generate_nonprofit_profile_data(
                    demographics=None,
                    past_methods=None,
                    fundraising_goals=None,
                    service_tags=None,
                    sustainability_practices=None
                ),
                "expected_status": 200
            },
            {
                "name": "invalid_user_id",
                "data": TestDataGenerator.generate_nonprofit_profile_data(user_id=999),
                "expected_status": 500
            }
        ]

    @staticmethod
    def get_strategy_generation_scenarios():
        """Get strategy generation test scenarios."""
        return [
            {
                "name": "valid_request",
                "data": TestDataGenerator.generate_strategy_request_data(),
                "expected_status": 200
            },
            {
                "name": "nonexistent_profile",
                "data": TestDataGenerator.generate_strategy_request_data(profile_id=999),
                "expected_status": 404
            },
            {
                "name": "empty_query",
                "data": TestDataGenerator.generate_strategy_request_data(query=""),
                "expected_status": 422
            }
        ]


class DatabaseTestData:
    """Database-specific test data for seeding test databases."""

    @staticmethod
    def get_users_seed_data():
        """Get user data for seeding test database."""
        return [
            {
                "email": "test1@example.com",
                "name": "Test User 1",
                "hashed_password": "$2b$12$example_hashed_password_1"
            },
            {
                "email": "test2@example.com",
                "name": "Test User 2",
                "hashed_password": "$2b$12$example_hashed_password_2"
            },
            {
                "email": "test3@example.com",
                "name": "Test User 3",
                "hashed_password": "$2b$12$example_hashed_password_3"
            }
        ]

    @staticmethod
    def get_profiles_seed_data():
        """Get profile data for seeding test database."""
        return [
            {
                "user_id": 1,
                "name": "Test Nonprofit 1",
                "mission": "Test mission 1",
                "demographics": "Test demographics 1",
                "past_methods": "Test methods 1",
                "fundraising_goals": "Test goals 1",
                "service_tags": "education,community",
                "sustainability_practices": "Test practices 1"
            },
            {
                "user_id": 2,
                "name": "Test Nonprofit 2",
                "mission": "Test mission 2",
                "demographics": "Test demographics 2",
                "past_methods": "Test methods 2",
                "fundraising_goals": "Test goals 2",
                "service_tags": "healthcare,youth",
                "sustainability_practices": "Test practices 2"
            }
        ]

    @staticmethod
    def get_strategies_seed_data():
        """Get strategy data for seeding test database."""
        return [
            {
                "profile_id": 1,
                "title": "Test Strategy 1",
                "content": "Test strategy content 1",
                "created_at": datetime.utcnow()
            },
            {
                "profile_id": 1,
                "title": "Test Strategy 2",
                "content": "Test strategy content 2",
                "created_at": datetime.utcnow() - timedelta(days=1)
            },
            {
                "profile_id": 2,
                "title": "Test Strategy 3",
                "content": "Test strategy content 3",
                "created_at": datetime.utcnow() - timedelta(hours=1)
            }
        ]


class MockResponses:
    """Mock responses for external API calls."""

    @staticmethod
    def get_openai_success_response():
        """Get successful OpenAI API response."""
        return {
            "choices": [
                {
                    "message": {
                        "content": "Here's a comprehensive fundraising strategy:\n\n1. Digital Marketing\n2. Community Outreach\n3. Corporate Partnerships\n4. Grant Applications"
                    }
                }
            ]
        }

    @staticmethod
    def get_openai_error_response():
        """Get error OpenAI API response."""
        return {
            "error": {
                "message": "API rate limit exceeded",
                "type": "rate_limit_error"
            }
        }

    @staticmethod
    def get_groq_success_response():
        """Get successful Groq API response."""
        return {
            "choices": [
                {
                    "message": {
                        "content": "Fundraising strategy using LLaMA model:\n\n• Social media campaigns\n• Email marketing\n• Event fundraising\n• Corporate sponsorships"
                    }
                }
            ]
        }


class ValidationData:
    """Data for testing validation scenarios."""

    # Invalid email formats
    INVALID_EMAILS = [
        "invalid-email",
        "@example.com",
        "test@",
        "test.example.com",
        "test space@example.com",
        "",
        "test@.com",
        "test@com",
        "test@@example.com"
    ]

    # Valid email formats
    VALID_EMAILS = [
        "test@example.com",
        "user.name@example.com",
        "user+tag@example.com",
        "user123@example123.com",
        "test@sub.example.com",
        "very.long.email.address@very.long.domain.name.com"
    ]

    # Edge case strings
    EDGE_CASE_STRINGS = [
        "",  # Empty string
        " ",  # Space
        "a" * 1000,  # Very long string
        "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?",
        "Unicode: 你好世界 🌍 émojis 🎉",
        "SQL injection attempt: '; DROP TABLE users; --",
        "XSS attempt: <script>alert('xss')</script>",
        "\n\r\t",  # Whitespace characters
        "null",  # String null
        "undefined",  # String undefined
    ]

    # Test numbers
    TEST_NUMBERS = [
        -1,  # Negative
        0,   # Zero
        1,   # Positive
        999999,  # Large positive
        -999999,  # Large negative
        1.5,  # Float
        "123",  # String number
        "abc",  # Non-numeric string
    ]


class PerformanceTestData:
    """Data for performance testing."""

    @staticmethod
    def generate_bulk_users(count: int = 100):
        """Generate bulk user data for performance testing."""
        return [
            TestDataGenerator.generate_user_data(
                email=f"user{i}@example.com",
                name=f"User {i}",
                password=f"password{i}"
            ) for i in range(count)
        ]

    @staticmethod
    def generate_bulk_profiles(count: int = 100):
        """Generate bulk profile data for performance testing."""
        return [
            TestDataGenerator.generate_nonprofit_profile_data(
                user_id=i % 10 + 1,  # Distribute across 10 users
                name=f"Nonprofit {i}",
                mission=f"Mission for nonprofit {i}"
            ) for i in range(count)
        ]

    @staticmethod
    def generate_bulk_strategies(count: int = 100):
        """Generate bulk strategy data for performance testing."""
        return [
            TestDataGenerator.generate_strategy_request_data(
                profile_id=i % 10 + 1,  # Distribute across 10 profiles
                query=f"Strategy query {i}"
            ) for i in range(count)
        ]


# Export commonly used data
__all__ = [
    'TestDataGenerator',
    'SampleData',
    'TestScenarios',
    'DatabaseTestData',
    'MockResponses',
    'ValidationData',
    'PerformanceTestData'
]

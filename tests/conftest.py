"""Shared pytest fixtures across the test suite.


Provides pre-configured API clients, authenticated users, and hermetic AI mocks.
"""


import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Unauthenticated DRF APIClient."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Standard verified test user."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="Password123!"
    )


@pytest.fixture
def other_user(db):
    """Second user for multi-tenant isolation testing."""
    return User.objects.create_user(
        username="otheruser",
        email="other@example.com",
        password="Password123!"
    )


@pytest.fixture
def auth_client(api_client, test_user):
    """APIClient authenticated as test_user via force_authenticate."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def jwt_auth_client(api_client, test_user):
    """APIClient authenticated using real Bearer JWT token in Authorization header."""
    refresh = RefreshToken.for_user(test_user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client


@pytest.fixture
def mock_gemini_response():
    """Deterministic AI response payload for mocking external LLM calls."""
    return {
        "executive_summary": "This is a hermetic mock summary of the document.",
        "key_takeaways": [
            "Contract is valid for 12 months",
            "Payment due net 30 days",
            "Service tier is enterprise"
        ],
        "topics": ["Legal", "Contract", "Services"],
        "sentiment": "POSITIVE",
        "tokens_used": 120
    }



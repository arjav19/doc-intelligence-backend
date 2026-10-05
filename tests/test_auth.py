"""Tests for user registration, authentication, and JWT token issuance."""


import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestAuthenticationFlow:
    """Covers /api/auth/register/, /api/auth/token/, and token refresh endpoints."""


    REGISTER_URL = '/api/auth/register/'
    TOKEN_OBTAIN_URL = '/api/auth/token/'
    TOKEN_REFRESH_URL = '/api/auth/token/refresh/'


    def test_user_registration_success(self, api_client):
        payload = {
            "username": "newdeveloper",
            "email": "developer@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }
        response = api_client.post(self.REGISTER_URL, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "newdeveloper"
        assert response.data["email"] == "developer@example.com"
        assert "password" not in response.data


        # Ensure user exists in database with hashed password
        user = User.objects.get(username="newdeveloper")
        assert user.check_password("SecurePassword123!")


    def test_user_registration_password_mismatch(self, api_client):
        payload = {
            "username": "newdeveloper",
            "email": "developer@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "MismatchedPassword999!"
        }
        response = api_client.post(self.REGISTER_URL, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data


    def test_user_registration_duplicate_username(self, api_client, test_user):
        payload = {
            "username": test_user.username,
            "email": "different_email@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }
        response = api_client.post(self.REGISTER_URL, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data


    def test_jwt_token_obtain_pair_success(self, api_client, test_user):
        payload = {
            "username": "testuser",
            "password": "Password123!"
        }
        response = api_client.post(self.TOKEN_OBTAIN_URL, payload, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data


    def test_jwt_token_obtain_pair_invalid_credentials(self, api_client, test_user):
        payload = {
            "username": "testuser",
            "password": "WrongPassword!"
        }
        response = api_client.post(self.TOKEN_OBTAIN_URL, payload, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_jwt_token_refresh_success(self, api_client, test_user):
        # Obtain tokens first
        obtain_res = api_client.post(
            self.TOKEN_OBTAIN_URL,
            {"username": "testuser", "password": "Password123!"},
            format='json'
        )
        refresh_token = obtain_res.data["refresh"]


        # Use refresh token to get a new access token
        refresh_res = api_client.post(
            self.TOKEN_REFRESH_URL,
            {"refresh": refresh_token},
            format='json'
        )
        assert refresh_res.status_code == status.HTTP_200_OK
        assert "access" in refresh_res.data

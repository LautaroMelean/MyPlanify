import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRegister:
    url = "/api/v1/auth/register/"

    def test_register_success(self, api_client):
        payload = {
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "access" in data["data"]
        assert "refresh" in data["data"]
        assert data["data"]["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, api_client, regular_user):
        payload = {
            "email": regular_user.email,
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 400

    def test_register_password_mismatch(self, api_client):
        payload = {
            "email": "mismatch@example.com",
            "password": "SecurePass123!",
            "password_confirm": "WrongPass!",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 400

    def test_register_missing_fields(self, api_client):
        response = api_client.post(self.url, {"email": "x@x.com"}, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    url = "/api/v1/auth/login/"

    def test_login_success(self, api_client, regular_user):
        response = api_client.post(self.url, {"email": regular_user.email, "password": "TestPass123!"}, format="json")
        assert response.status_code == 200
        data = response.json()
        assert "access" in data["data"]
        assert "refresh" in data["data"]

    def test_login_wrong_password(self, api_client, regular_user):
        response = api_client.post(self.url, {"email": regular_user.email, "password": "WrongPass!"}, format="json")
        assert response.status_code in (400, 401, 403)

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post(self.url, {"email": "ghost@example.com", "password": "Pass!"}, format="json")
        assert response.status_code in (400, 401, 403)

    def test_login_missing_credentials(self, api_client):
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestMe:
    url = "/api/v1/auth/me/"

    def test_me_authenticated(self, authenticated_client, regular_user):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == regular_user.email

    def test_me_unauthenticated(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestLogout:
    url = "/api/v1/auth/logout/"

    def test_logout_requires_auth(self, api_client):
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == 401

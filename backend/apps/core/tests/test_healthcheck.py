import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_healthcheck_returns_200(api_client):
    url = reverse("healthcheck")
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_healthcheck_response_structure(api_client):
    url = reverse("healthcheck")
    response = api_client.get(url)
    data = response.json()
    assert "success" in data
    assert "data" in data
    assert "status" in data["data"]
    assert "database" in data["data"]


@pytest.mark.django_db
def test_healthcheck_database_connected(api_client):
    url = reverse("healthcheck")
    response = api_client.get(url)
    data = response.json()
    assert data["data"]["database"] == "connected"


@pytest.mark.django_db
def test_healthcheck_no_auth_required(api_client):
    """Healthcheck must be public — no authentication needed."""
    url = reverse("healthcheck")
    response = api_client.get(url)
    assert response.status_code != 401
    assert response.status_code != 403

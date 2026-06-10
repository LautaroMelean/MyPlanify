import pytest


@pytest.fixture
def place_payload():
    return {
        "name": "La Biela",
        "description": "Café histórico",
        "category": "cafe",
        "address": "Av. Quintana 596",
        "city": "Buenos Aires",
        "price_level": 2,
    }


@pytest.fixture
def admin_place(admin_client, place_payload):
    r = admin_client.post("/api/v1/places/", place_payload, format="json")
    return r.json()["data"]


@pytest.fixture
def business_owner(user_factory):
    return user_factory(email="biz@example.com", role="business_owner")


@pytest.fixture
def biz_client(business_owner):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=business_owner)
    return client


@pytest.mark.django_db
class TestPlaceList:
    url = "/api/v1/places/"

    def test_unauthenticated_can_list(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_regular_user_cannot_create(self, authenticated_client, place_payload):
        response = authenticated_client.post(self.url, place_payload, format="json")
        assert response.status_code == 403

    def test_admin_can_create(self, admin_client, place_payload):
        response = admin_client.post(self.url, place_payload, format="json")
        assert response.status_code == 201

    def test_business_owner_can_create(self, biz_client, place_payload):
        response = biz_client.post(self.url, place_payload, format="json")
        assert response.status_code == 201

    def test_filter_by_city(self, admin_client, place_payload):
        admin_client.post(self.url, place_payload, format="json")
        response = admin_client.get(self.url, {"city": "Buenos Aires"})
        assert response.status_code == 200
        assert len(response.json()["data"]) >= 1

    def test_filter_by_category(self, admin_client, place_payload):
        admin_client.post(self.url, place_payload, format="json")
        response = admin_client.get(self.url, {"category": "cafe"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert all("cafe" in p["category"].lower() for p in data)


@pytest.mark.django_db
class TestPlaceDetail:
    def test_get_place(self, admin_client, admin_place):
        url = f"/api/v1/places/{admin_place['id']}/"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "La Biela"

    def test_admin_can_update(self, admin_client, admin_place):
        url = f"/api/v1/places/{admin_place['id']}/"
        response = admin_client.patch(url, {"name": "La Biela Renovada"}, format="json")
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "La Biela Renovada"

    def test_regular_user_cannot_update(self, authenticated_client, admin_place):
        url = f"/api/v1/places/{admin_place['id']}/"
        response = authenticated_client.patch(url, {"name": "Hack"}, format="json")
        assert response.status_code == 403

    def test_admin_can_delete(self, admin_client, admin_place):
        url = f"/api/v1/places/{admin_place['id']}/"
        response = admin_client.delete(url)
        assert response.status_code == 204

    def test_get_nonexistent_returns_404(self, admin_client):
        response = admin_client.get("/api/v1/places/00000000-0000-0000-0000-000000000000/")
        assert response.status_code == 404

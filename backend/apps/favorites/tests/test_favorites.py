import pytest


@pytest.fixture
def place(db):
    from apps.places.models import Place
    return Place.objects.create(
        name="Café Tortoni",
        category="cafe",
        address="Av. de Mayo 829",
        city="Buenos Aires",
    )


@pytest.fixture
def activity(db):
    from apps.activities.models import Activity
    return Activity.objects.create(
        name="Tango show",
        category="música",
        activity_type="concert",
        indoor=True,
        score_base=80,
    )


@pytest.fixture
def second_user(user_factory):
    return user_factory(email="second@example.com", role="user")


@pytest.fixture
def second_client(second_user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=second_user)
    return client


@pytest.mark.django_db
class TestFavoriteList:
    url = "/api/v1/favorites/"

    def test_unauthenticated_denied(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 401

    def test_get_empty_favorites(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_add_place_favorite(self, authenticated_client, place):
        payload = {"place": str(place.id)}
        response = authenticated_client.post(self.url, payload, format="json")
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["item_type"] == "place"

    def test_add_activity_favorite(self, authenticated_client, activity):
        payload = {"activity": str(activity.id)}
        response = authenticated_client.post(self.url, payload, format="json")
        assert response.status_code == 201

    def test_duplicate_favorite_rejected(self, authenticated_client, place):
        payload = {"place": str(place.id)}
        authenticated_client.post(self.url, payload, format="json")
        response = authenticated_client.post(self.url, payload, format="json")
        assert response.status_code == 400

    def test_user_isolation(self, authenticated_client, second_client, place):
        authenticated_client.post(self.url, {"place": str(place.id)}, format="json")
        response = second_client.get(self.url)
        assert response.json()["data"] == []

    def test_audit_log_on_add(self, authenticated_client, regular_user, place):
        from apps.audit.models import AuditLog
        authenticated_client.post(self.url, {"place": str(place.id)}, format="json")
        assert AuditLog.objects.filter(user=regular_user, action="favorite").exists()


@pytest.mark.django_db
class TestFavoriteDelete:
    url = "/api/v1/favorites/"

    def test_delete_own_favorite(self, authenticated_client, place):
        r = authenticated_client.post(self.url, {"place": str(place.id)}, format="json")
        fav_id = r.json()["data"]["id"]
        response = authenticated_client.delete(f"{self.url}{fav_id}/")
        assert response.status_code == 204

    def test_cannot_delete_other_user_favorite(self, authenticated_client, second_client, place):
        r = authenticated_client.post(self.url, {"place": str(place.id)}, format="json")
        fav_id = r.json()["data"]["id"]
        response = second_client.delete(f"{self.url}{fav_id}/")
        assert response.status_code == 404

    def test_audit_log_on_remove(self, authenticated_client, regular_user, place):
        from apps.audit.models import AuditLog
        r = authenticated_client.post(self.url, {"place": str(place.id)}, format="json")
        fav_id = r.json()["data"]["id"]
        authenticated_client.delete(f"{self.url}{fav_id}/")
        assert AuditLog.objects.filter(user=regular_user, action="unfavorite").exists()

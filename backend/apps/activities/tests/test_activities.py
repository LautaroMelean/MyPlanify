import pytest


@pytest.fixture
def activity_payload():
    return {
        "name": "Visitar el MALBA",
        "description": "Museo de Arte Latinoamericano",
        "category": "museo",
        "activity_type": "museum",
        "min_budget": "0",
        "max_budget": "2000",
        "min_people": 1,
        "indoor": True,
        "outdoor": False,
        "score_base": 70,
    }


@pytest.fixture
def activity(admin_client, activity_payload):
    r = admin_client.post("/api/v1/activities/", activity_payload, format="json")
    return r.json()["data"]


@pytest.mark.django_db
class TestActivityList:
    url = "/api/v1/activities/"

    def test_unauthenticated_can_list(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_authenticated_can_list(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200

    def test_admin_can_create(self, admin_client, activity_payload):
        response = admin_client.post(self.url, activity_payload, format="json")
        assert response.status_code == 201
        assert response.json()["data"]["name"] == "Visitar el MALBA"

    def test_regular_user_cannot_create(self, authenticated_client, activity_payload):
        response = authenticated_client.post(self.url, activity_payload, format="json")
        assert response.status_code == 403

    def test_filter_by_type(self, admin_client, activity):
        response = admin_client.get(self.url, {"type": "museum"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert all(a["activity_type"] == "museum" for a in data)

    def test_filter_by_indoor(self, admin_client, activity):
        response = admin_client.get(self.url, {"indoor": "true"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert all(a["indoor"] is True for a in data)

    def test_filter_by_category(self, admin_client, activity):
        response = admin_client.get(self.url, {"category": "museo"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1


@pytest.mark.django_db
class TestActivityDetail:
    def test_get_activity(self, authenticated_client, activity):
        url = f"/api/v1/activities/{activity['id']}/"
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Visitar el MALBA"

    def test_admin_can_update(self, admin_client, activity):
        url = f"/api/v1/activities/{activity['id']}/"
        response = admin_client.patch(url, {"score_base": 90}, format="json")
        assert response.status_code == 200
        assert response.json()["data"]["score_base"] == 90

    def test_regular_user_cannot_update(self, authenticated_client, activity):
        url = f"/api/v1/activities/{activity['id']}/"
        response = authenticated_client.patch(url, {"score_base": 10}, format="json")
        assert response.status_code == 403

    def test_admin_can_deactivate(self, admin_client, activity):
        url = f"/api/v1/activities/{activity['id']}/"
        response = admin_client.delete(url)
        assert response.status_code == 204

    def test_get_nonexistent(self, authenticated_client):
        response = authenticated_client.get("/api/v1/activities/00000000-0000-0000-0000-000000000000/")
        assert response.status_code == 404

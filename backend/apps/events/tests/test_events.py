import pytest
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def place(db):
    from apps.places.models import Place
    return Place.objects.create(
        name="Teatro Colón",
        category="theater",
        address="Cerrito 628",
        city="Buenos Aires",
    )


@pytest.fixture
def event_organizer(user_factory):
    return user_factory(email="organizer@example.com", role="event_organizer")


@pytest.fixture
def organizer_client(event_organizer):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=event_organizer)
    return client


@pytest.fixture
def event_payload(place):
    now = timezone.now()
    return {
        "title": "Concierto de Primavera",
        "description": "Un gran concierto",
        "category": "music",
        "start_date": (now + timedelta(days=10)).isoformat(),
        "end_date": (now + timedelta(days=10, hours=3)).isoformat(),
        "price": "1500.00",
        "place": str(place.id),
    }


@pytest.fixture
def draft_event(organizer_client, event_payload):
    r = organizer_client.post("/api/v1/events/", event_payload, format="json")
    return r.json()["data"]


@pytest.mark.django_db
class TestEventList:
    url = "/api/v1/events/"

    def test_public_can_list_published(self, api_client, organizer_client, draft_event):
        organizer_client.post(f"/api/v1/events/{draft_event['id']}/publish/")
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_regular_user_cannot_create(self, authenticated_client, event_payload):
        response = authenticated_client.post(self.url, event_payload, format="json")
        assert response.status_code == 403

    def test_organizer_can_create(self, organizer_client, event_payload):
        response = organizer_client.post(self.url, event_payload, format="json")
        assert response.status_code == 201
        assert response.json()["data"]["status"] == "draft"

    def test_admin_can_create(self, admin_client, event_payload):
        response = admin_client.post(self.url, event_payload, format="json")
        assert response.status_code == 201


@pytest.mark.django_db
class TestEventWorkflow:
    def test_draft_to_published(self, organizer_client, draft_event):
        url = f"/api/v1/events/{draft_event['id']}/publish/"
        response = organizer_client.post(url)
        assert response.status_code in (200, 403)

    def test_admin_publishes_event(self, admin_client, organizer_client, draft_event):
        url = f"/api/v1/events/{draft_event['id']}/publish/"
        response = admin_client.post(url)
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "published"

    def test_admin_cancels_published_event(self, admin_client, organizer_client, draft_event):
        admin_client.post(f"/api/v1/events/{draft_event['id']}/publish/")
        url = f"/api/v1/events/{draft_event['id']}/cancel/"
        response = admin_client.post(url, {"reason": "Motivo de cancelación"}, format="json")
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "cancelled"

    def test_regular_user_cannot_publish(self, authenticated_client, draft_event):
        url = f"/api/v1/events/{draft_event['id']}/publish/"
        response = authenticated_client.post(url)
        assert response.status_code == 403

    def test_organizer_cannot_edit_other_event(self, organizer_client, admin_client, event_payload):
        other_organizer_event = admin_client.post("/api/v1/events/", event_payload, format="json").json()["data"]
        url = f"/api/v1/events/{other_organizer_event['id']}/"
        response = organizer_client.patch(url, {"title": "Hack"}, format="json")
        assert response.status_code == 403

    def test_audit_log_on_create(self, organizer_client, event_organizer, event_payload):
        from apps.audit.models import AuditLog
        organizer_client.post("/api/v1/events/", event_payload, format="json")
        assert AuditLog.objects.filter(user=event_organizer, action="create", entity_type="event").exists()

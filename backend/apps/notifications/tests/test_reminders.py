import pytest
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def published_event(db):
    from apps.places.models import Place
    from apps.events.models import Event, EventStatus
    place = Place.objects.create(name="Luna Park", category="arena", address="Bouchard 465", city="Buenos Aires")
    return Event.objects.create(
        title="Lollapalooza",
        category="music",
        start_date=timezone.now() + timedelta(days=30),
        end_date=timezone.now() + timedelta(days=30, hours=8),
        status=EventStatus.PUBLISHED,
        place=place,
    )


@pytest.fixture
def reminder_payload(published_event):
    return {
        "event": str(published_event.id),
        "reminder_date": (timezone.now() + timedelta(days=25)).isoformat(),
    }


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
class TestReminderList:
    url = "/api/v1/reminders/"

    def test_unauthenticated_denied(self, api_client):
        assert api_client.get(self.url).status_code == 401

    def test_get_empty_reminders(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_create_reminder(self, authenticated_client, reminder_payload):
        response = authenticated_client.post(self.url, reminder_payload, format="json")
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["event_title"] == "Lollapalooza"

    def test_duplicate_reminder_rejected(self, authenticated_client, reminder_payload):
        authenticated_client.post(self.url, reminder_payload, format="json")
        response = authenticated_client.post(self.url, reminder_payload, format="json")
        assert response.status_code == 400

    def test_reminder_creates_notification(self, authenticated_client, regular_user, reminder_payload):
        from apps.notifications.models import Notification
        authenticated_client.post(self.url, reminder_payload, format="json")
        assert Notification.objects.filter(user=regular_user, notification_type="event_reminder").exists()

    def test_user_isolation(self, authenticated_client, second_client, reminder_payload):
        authenticated_client.post(self.url, reminder_payload, format="json")
        response = second_client.get(self.url)
        assert response.json()["data"] == []

    def test_audit_log_on_create(self, authenticated_client, regular_user, reminder_payload):
        from apps.audit.models import AuditLog
        authenticated_client.post(self.url, reminder_payload, format="json")
        assert AuditLog.objects.filter(user=regular_user, action="reminder").exists()


@pytest.mark.django_db
class TestReminderDelete:
    url = "/api/v1/reminders/"

    def test_delete_own_reminder(self, authenticated_client, reminder_payload):
        r = authenticated_client.post(self.url, reminder_payload, format="json")
        pk = r.json()["data"]["id"]
        response = authenticated_client.delete(f"{self.url}{pk}/")
        assert response.status_code == 204

    def test_cannot_delete_other_user_reminder(self, authenticated_client, second_client, reminder_payload):
        r = authenticated_client.post(self.url, reminder_payload, format="json")
        pk = r.json()["data"]["id"]
        response = second_client.delete(f"{self.url}{pk}/")
        assert response.status_code == 404

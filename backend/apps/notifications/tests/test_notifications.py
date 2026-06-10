import pytest
from apps.notifications.models import Notification, NotificationType


@pytest.fixture
def user_notification(regular_user):
    return Notification.objects.create(
        user=regular_user,
        title="Bienvenido a Planify",
        message="Configurá tus preferencias.",
        notification_type=NotificationType.SYSTEM,
    )


@pytest.mark.django_db
class TestNotificationList:
    url = "/api/v1/notifications/"

    def test_unauthenticated_denied(self, api_client):
        assert api_client.get(self.url).status_code == 401

    def test_get_notifications(self, authenticated_client, user_notification):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["title"] == "Bienvenido a Planify"
        assert data[0]["read"] is False

    def test_user_isolation(self, authenticated_client, admin_client, user_notification):
        response = admin_client.get(self.url)
        assert response.json()["data"] == []


@pytest.mark.django_db
class TestNotificationMarkRead:
    def test_mark_read(self, authenticated_client, user_notification):
        url = f"/api/v1/notifications/{user_notification.id}/read/"
        response = authenticated_client.patch(url)
        assert response.status_code == 200
        assert response.json()["data"]["read"] is True

    def test_cannot_mark_other_user_notification(self, admin_client, user_notification):
        url = f"/api/v1/notifications/{user_notification.id}/read/"
        response = admin_client.patch(url)
        assert response.status_code == 404

    def test_audit_on_mark_read(self, authenticated_client, regular_user, user_notification):
        authenticated_client.patch(f"/api/v1/notifications/{user_notification.id}/read/")
        user_notification.refresh_from_db()
        assert user_notification.read is True

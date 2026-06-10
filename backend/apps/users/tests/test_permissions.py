import pytest


@pytest.mark.django_db
class TestUserListPermissions:
    url = "/api/v1/users/"

    def test_unauthenticated_denied(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 401

    def test_regular_user_denied(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == 403

    def test_admin_allowed(self, admin_client):
        response = admin_client.get(self.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserDetailPermissions:
    def test_user_can_see_own_profile(self, authenticated_client, regular_user):
        url = f"/api/v1/users/{regular_user.id}/"
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_user_cannot_see_other_profile(self, authenticated_client, admin_user):
        url = f"/api/v1/users/{admin_user.id}/"
        response = authenticated_client.get(url)
        assert response.status_code == 403

    def test_admin_can_see_any_profile(self, admin_client, regular_user):
        url = f"/api/v1/users/{regular_user.id}/"
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_unauthenticated_denied(self, api_client, regular_user):
        url = f"/api/v1/users/{regular_user.id}/"
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestUserServices:
    def test_register_creates_user_with_correct_role(self):
        from apps.users.services import register_user
        from apps.users.models import User, UserRole

        user = register_user(
            email="service@test.com",
            password="StrongPass123!",
            first_name="Service",
            last_name="Test",
        )
        assert user.role == UserRole.USER
        assert user.is_active is True

    def test_register_duplicate_raises_error(self, regular_user):
        from apps.users.services import register_user
        from rest_framework.exceptions import ValidationError

        with pytest.raises(ValidationError):
            register_user(
                email=regular_user.email,
                password="StrongPass123!",
                first_name="Dup",
                last_name="User",
            )

    def test_soft_delete_deactivates_user(self, regular_user):
        from apps.users.services import delete_user

        delete_user(requesting_user=regular_user, target_user=regular_user)
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_audit_log_created_on_register(self):
        from apps.users.services import register_user
        from apps.audit.models import AuditLog

        user = register_user(
            email="auditcheck@test.com",
            password="StrongPass123!",
            first_name="Audit",
            last_name="Check",
        )
        assert AuditLog.objects.filter(user=user, action="register").exists()

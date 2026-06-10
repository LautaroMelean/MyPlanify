import pytest
from apps.users.models import User, UserRole, UserStatus


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email="model@test.com",
            password="Pass123!",
            first_name="Model",
            last_name="Test",
        )
        assert user.pk is not None
        assert user.email == "model@test.com"
        assert user.role == UserRole.USER
        assert user.status == UserStatus.ACTIVE
        assert user.is_active is True
        assert not user.check_password("wrong")
        assert user.check_password("Pass123!")

    def test_full_name_property(self):
        user = User(first_name="John", last_name="Doe")
        assert user.full_name == "John Doe"

    def test_soft_delete(self, regular_user):
        regular_user.soft_delete()
        assert regular_user.status == UserStatus.DELETED
        assert regular_user.is_active is False

    def test_suspend(self, regular_user):
        regular_user.suspend()
        assert regular_user.status == UserStatus.SUSPENDED

    def test_activate(self, regular_user):
        regular_user.suspend()
        regular_user.activate()
        assert regular_user.status == UserStatus.ACTIVE
        assert regular_user.is_active is True

    def test_superuser_has_admin_role(self):
        admin = User.objects.create_superuser(
            email="super@test.com",
            password="SuperPass123!",
            first_name="Super",
            last_name="User",
        )
        assert admin.role == UserRole.ADMIN
        assert admin.is_staff is True
        assert admin.is_superuser is True

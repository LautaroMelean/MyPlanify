import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory(db):
    from apps.users.models import User

    def make_user(email="test@example.com", password="TestPass123!", role="user", **kwargs):
        return User.objects.create_user(
            email=email, password=password, role=role,
            first_name="Test", last_name="User", **kwargs,
        )
    return make_user


@pytest.fixture
def admin_user(user_factory):
    return user_factory(email="admin@example.com", role="admin")


@pytest.fixture
def regular_user(user_factory):
    return user_factory(email="user@example.com", role="user")


@pytest.fixture
def authenticated_client(regular_user):
    client = APIClient()
    client.force_authenticate(user=regular_user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

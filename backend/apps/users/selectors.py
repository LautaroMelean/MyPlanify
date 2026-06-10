from .models import User, UserPreference


def get_user_by_id(user_id: str) -> User:
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> User:
    try:
        return User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return None


def get_user_preferences(user: User):
    return UserPreference.objects.filter(user=user)


def list_active_users():
    return User.objects.filter(is_active=True).order_by("-created_at")

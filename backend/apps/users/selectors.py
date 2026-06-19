from .models import User, UserPreference


def get_user_preferences(user: User):
    return UserPreference.objects.filter(user=user)


def list_active_users():
    return User.objects.filter(is_active=True).order_by("-created_at")

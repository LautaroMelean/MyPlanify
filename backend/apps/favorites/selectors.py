from .models import Favorite


def get_user_favorites(user):
    return Favorite.objects.filter(user=user).select_related("event", "place", "activity").order_by("-created_at")


def get_favorite_by_id(favorite_id, user):
    try:
        return Favorite.objects.get(id=favorite_id, user=user)
    except Favorite.DoesNotExist:
        return None

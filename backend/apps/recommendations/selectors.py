from .models import Recommendation


def get_user_recommendations(user):
    return Recommendation.objects.filter(user=user).order_by("-score")

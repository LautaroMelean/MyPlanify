from rest_framework.permissions import IsAuthenticated


class RecommendationPermission(IsAuthenticated):
    pass

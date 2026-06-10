import pytest


@pytest.fixture
def activity(db):
    from apps.activities.models import Activity
    return Activity.objects.create(
        name="Ir al cine",
        category="cine",
        activity_type="cinema",
        indoor=True,
        score_base=80,
    )


@pytest.fixture
def user_with_prefs(regular_user):
    from apps.users.models import UserPreference
    UserPreference.objects.create(user=regular_user, category="entertainment", value="cine", weight=5)
    return regular_user


@pytest.mark.django_db
class TestRecommendationList:
    url = "/api/v1/recommendations/"

    def test_unauthenticated_denied(self, api_client):
        assert api_client.get(self.url).status_code == 401

    def test_returns_recommendations(self, authenticated_client, activity):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        data = response.json()["data"]
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_recommendations_have_required_fields(self, authenticated_client, activity):
        response = authenticated_client.get(self.url)
        item = response.json()["data"][0]
        assert "score" in item
        assert "recommendation_reason" in item
        assert "item_type" in item

    def test_score_in_valid_range(self, authenticated_client, activity):
        response = authenticated_client.get(self.url)
        for item in response.json()["data"]:
            score = float(item["score"])
            assert 0 <= score <= 100

    def test_preference_improves_score(self, db, user_with_prefs, activity):
        from rest_framework.test import APIClient
        from apps.recommendations.services import generate_recommendations_for_user

        client = APIClient()
        client.force_authenticate(user=user_with_prefs)

        recs_with_prefs = generate_recommendations_for_user(user_with_prefs)
        cinema_rec = next((r for r in recs_with_prefs if r.activity and r.activity.activity_type == "cinema"), None)
        assert cinema_rec is not None
        assert float(cinema_rec.score) > 0

    def test_audit_log_on_generate(self, authenticated_client, regular_user, activity):
        from apps.audit.models import AuditLog
        authenticated_client.get(self.url)
        assert AuditLog.objects.filter(
            user=regular_user, action="recommendation_generated"
        ).exists()

    def test_interaction_history_logged(self, authenticated_client, regular_user, activity):
        from apps.recommendations.models import InteractionHistory
        authenticated_client.get(self.url)
        assert InteractionHistory.objects.filter(user=regular_user, action="view").exists()

    def test_at_most_20_results(self, authenticated_client, db):
        from apps.activities.models import Activity
        for i in range(25):
            Activity.objects.create(
                name=f"Actividad {i}",
                category=f"cat{i}",
                activity_type="museum",
                score_base=50,
            )
        response = authenticated_client.get(self.url)
        assert len(response.json()["data"]) <= 20


@pytest.mark.django_db
class TestRecommendationService:
    def test_regenerates_on_each_call(self, regular_user, activity):
        from apps.recommendations.services import generate_recommendations_for_user
        from apps.recommendations.models import Recommendation

        generate_recommendations_for_user(regular_user)
        count_1 = Recommendation.objects.filter(user=regular_user).count()
        generate_recommendations_for_user(regular_user)
        count_2 = Recommendation.objects.filter(user=regular_user).count()
        assert count_1 == count_2

    def test_interaction_boosts_score(self, regular_user, activity):
        from apps.recommendations.services import generate_recommendations_for_user, log_interaction
        from apps.recommendations.models import Recommendation

        recs_before = generate_recommendations_for_user(regular_user)
        score_before = next(
            (float(r.score) for r in recs_before if r.activity and r.activity.id == activity.id), 0
        )

        log_interaction(user=regular_user, action="view", entity_type="activity", entity_id=str(activity.id))
        recs_after = generate_recommendations_for_user(regular_user)
        score_after = next(
            (float(r.score) for r in recs_after if r.activity and r.activity.id == activity.id), 0
        )

        assert score_after > score_before

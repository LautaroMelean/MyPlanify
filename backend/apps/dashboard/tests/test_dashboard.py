import uuid
import pytest
from datetime import date, timedelta


@pytest.mark.django_db
class TestUserActivityStats:
    url = "/api/v1/dashboard/me/stats/"

    def test_unauthenticated_cannot_access(self, api_client):
        assert api_client.get(self.url).status_code == 401

    def test_authenticated_user_gets_stats(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == 200
        data = response.json()["data"]
        for field in (
            "plans_completed", "places_visited", "cities_explored",
            "favorite_category", "current_streak_weeks", "best_streak_weeks",
            "total_plans", "avg_rating_given",
        ):
            assert field in data

    def test_plans_completed_reflects_completed_status(self, authenticated_client, regular_user):
        from apps.planner.models import Plan
        Plan.objects.create(
            user=regular_user, title="Done Plan", date=date(2026, 6, 1),
            budget=1000, people_count=1, city="BA",
            slug=f"done-{str(uuid.uuid4())[:8]}", status="completed",
        )
        response = authenticated_client.get(self.url)
        data = response.json()["data"]
        assert data["plans_completed"] >= 1

    def test_current_streak_is_zero_with_no_completed_plans(self, authenticated_client):
        response = authenticated_client.get(self.url)
        data = response.json()["data"]
        assert data["current_streak_weeks"] == 0

    def test_total_plans_includes_all_statuses(self, authenticated_client, regular_user):
        from apps.planner.models import Plan
        for status in ("draft", "generated", "planned"):
            Plan.objects.create(
                user=regular_user, title=f"Plan {status}", date=date(2026, 7, 1),
                budget=1000, people_count=1, city="BA",
                slug=f"plan-{status}-{str(uuid.uuid4())[:8]}", status=status,
            )
        response = authenticated_client.get(self.url)
        data = response.json()["data"]
        assert data["total_plans"] >= 3

    def test_avg_rating_given_is_none_when_no_feedback(self, authenticated_client):
        response = authenticated_client.get(self.url)
        data = response.json()["data"]
        assert data["avg_rating_given"] is None

    def test_all_roles_can_access(self, api_client, user_factory):
        for role in ("user", "business_owner", "event_organizer", "moderator"):
            u = user_factory(email=f"stats-{role}@example.com", role=role)
            api_client.force_authenticate(user=u)
            assert api_client.get(self.url).status_code == 200

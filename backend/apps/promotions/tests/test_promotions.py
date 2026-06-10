import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient


URL = "/api/v1/promotions/"


def make_promo_data(place_id):
    now = timezone.now()
    return {
        "place": str(place_id),
        "title": "Test Promo",
        "description": "Desc",
        "discount_percentage": "20.00",
        "start_date": (now - timedelta(hours=1)).isoformat(),
        "end_date": (now + timedelta(days=7)).isoformat(),
    }


@pytest.fixture
def place(db):
    from apps.places.models import Place
    return Place.objects.create(
        name="Test Place", category="restaurant", address="Av. Test 123",
        city="Buenos Aires", is_active=True,
    )


@pytest.fixture
def business_user(user_factory):
    return user_factory(email="biz@example.com", role="business_owner")


@pytest.fixture
def business_client(business_user):
    client = APIClient()
    client.force_authenticate(user=business_user)
    return client


@pytest.fixture
def active_promo(db, place, business_user):
    from apps.promotions.models import Promotion, PromotionStatus
    now = timezone.now()
    return Promotion.objects.create(
        place=place, owner=business_user,
        title="Active Promo", discount_percentage=15,
        start_date=now - timedelta(hours=1),
        end_date=now + timedelta(days=7),
        status=PromotionStatus.ACTIVE,
    )


# ── GET list (public) ────────────────────────────────────────────────────────

def test_list_active_promotions(db, api_client, active_promo):
    resp = api_client.get(URL)
    assert resp.status_code == 200
    assert resp.data["success"] is True
    assert any(p["id"] == str(active_promo.id) for p in resp.data["data"])


def test_list_excludes_draft_promotions(db, api_client, place, business_user):
    from apps.promotions.models import Promotion, PromotionStatus
    now = timezone.now()
    Promotion.objects.create(
        place=place, owner=business_user, title="Draft",
        discount_percentage=5,
        start_date=now, end_date=now + timedelta(days=3),
        status=PromotionStatus.DRAFT,
    )
    resp = api_client.get(URL)
    assert resp.status_code == 200
    assert all(p["status"] == "active" for p in resp.data["data"])


# ── POST (business_owner) ────────────────────────────────────────────────────

def test_create_promotion_business_owner(db, business_client, place):
    data = make_promo_data(place.id)
    resp = business_client.post(URL, data, format="json")
    assert resp.status_code == 201
    assert resp.data["data"]["title"] == "Test Promo"
    assert resp.data["data"]["status"] == "draft"


def test_create_promotion_regular_user_forbidden(db, authenticated_client, place):
    data = make_promo_data(place.id)
    resp = authenticated_client.post(URL, data, format="json")
    assert resp.status_code == 403


def test_create_promotion_unauthenticated_forbidden(db, api_client, place):
    data = make_promo_data(place.id)
    resp = api_client.post(URL, data, format="json")
    assert resp.status_code in (401, 403)


def test_create_promotion_invalid_dates(db, business_client, place):
    now = timezone.now()
    data = make_promo_data(place.id)
    data["end_date"] = (now - timedelta(days=2)).isoformat()
    resp = business_client.post(URL, data, format="json")
    assert resp.status_code == 400


# ── GET detail ───────────────────────────────────────────────────────────────

def test_get_promotion_detail(db, api_client, active_promo):
    resp = api_client.get(f"{URL}{active_promo.id}/")
    assert resp.status_code == 200
    assert resp.data["data"]["id"] == str(active_promo.id)


def test_get_promotion_detail_404(db, api_client):
    import uuid
    resp = api_client.get(f"{URL}{uuid.uuid4()}/")
    assert resp.status_code == 404


# ── PATCH ────────────────────────────────────────────────────────────────────

def test_owner_can_patch_promotion(db, business_client, active_promo):
    resp = business_client.patch(f"{URL}{active_promo.id}/", {"title": "Updated"}, format="json")
    assert resp.status_code == 200
    assert resp.data["data"]["title"] == "Updated"


def test_other_user_cannot_patch_promotion(db, authenticated_client, active_promo):
    resp = authenticated_client.patch(f"{URL}{active_promo.id}/", {"title": "Hack"}, format="json")
    assert resp.status_code in (403, 400)


# ── DELETE ───────────────────────────────────────────────────────────────────

def test_owner_can_delete_promotion(db, business_client, active_promo):
    resp = business_client.delete(f"{URL}{active_promo.id}/")
    assert resp.status_code == 204
    active_promo.refresh_from_db()
    assert active_promo.status == "cancelled"


def test_other_user_cannot_delete_promotion(db, authenticated_client, active_promo):
    resp = authenticated_client.delete(f"{URL}{active_promo.id}/")
    assert resp.status_code in (403, 400)


def test_admin_can_delete_any_promotion(db, admin_client, active_promo):
    resp = admin_client.delete(f"{URL}{active_promo.id}/")
    assert resp.status_code == 204


# ── Activate / Cancel ────────────────────────────────────────────────────────

def test_activate_draft_promotion(db, business_client, place, business_user):
    from apps.promotions.models import Promotion, PromotionStatus
    now = timezone.now()
    promo = Promotion.objects.create(
        place=place, owner=business_user, title="Draft",
        discount_percentage=10,
        start_date=now, end_date=now + timedelta(days=3),
        status=PromotionStatus.DRAFT,
    )
    resp = business_client.post(f"{URL}{promo.id}/activate/")
    assert resp.status_code == 200
    assert resp.data["data"]["status"] == "active"


def test_cannot_activate_already_active_promotion(db, business_client, active_promo):
    resp = business_client.post(f"{URL}{active_promo.id}/activate/")
    assert resp.status_code == 400


def test_cancel_active_promotion(db, business_client, active_promo):
    resp = business_client.post(f"{URL}{active_promo.id}/cancel/")
    assert resp.status_code == 200
    assert resp.data["data"]["status"] == "cancelled"


# ── Audit ────────────────────────────────────────────────────────────────────

def test_create_promotion_generates_audit(db, business_client, place):
    from apps.audit.models import AuditLog
    data = make_promo_data(place.id)
    business_client.post(URL, data, format="json")
    assert AuditLog.objects.filter(action="create", entity_type="promotion").exists()

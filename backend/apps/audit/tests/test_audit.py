import pytest
from apps.audit.models import AuditLog
from apps.audit.services import log_action


@pytest.mark.django_db
class TestAuditService:
    def test_log_action_creates_record(self, regular_user):
        log = log_action(
            user=regular_user,
            action="test_action",
            entity_type="user",
            entity_id=str(regular_user.id),
        )
        assert log.pk is not None
        assert log.action == "test_action"
        assert log.user == regular_user

    def test_log_action_without_user(self):
        log = log_action(
            user=None,
            action="system_action",
            entity_type="system",
            entity_id=None,
        )
        assert log.pk is not None
        assert log.user is None

    def test_log_action_stores_metadata(self, regular_user):
        log = log_action(
            user=regular_user,
            action="update",
            entity_type="event",
            entity_id=str(regular_user.id),
            metadata={"changed_fields": ["title"]},
        )
        assert log.metadata == {"changed_fields": ["title"]}

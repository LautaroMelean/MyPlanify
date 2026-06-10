from .models import AuditLog


def get_audit_logs_for_user(user):
    return AuditLog.objects.filter(user=user).order_by("-created_at")


def get_audit_logs_for_entity(entity_type: str, entity_id: str):
    return AuditLog.objects.filter(entity_type=entity_type, entity_id=entity_id).order_by("-created_at")

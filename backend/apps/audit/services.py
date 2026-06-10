from .models import AuditLog


def log_action(
    *,
    user=None,
    action: str,
    entity_type: str,
    entity_id: str = None,
    metadata: dict = None,
    ip_address: str = None,
) -> AuditLog:
    return AuditLog.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata or {},
        ip_address=ip_address,
    )

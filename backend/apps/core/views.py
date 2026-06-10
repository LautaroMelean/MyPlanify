from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection


@api_view(["GET"])
@permission_classes([AllowAny])
def healthcheck(request):
    db_ok = True
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False

    status_code = 200 if db_ok else 503
    return Response(
        {
            "success": db_ok,
            "data": {
                "status": "healthy" if db_ok else "unhealthy",
                "database": "connected" if db_ok else "disconnected",
            },
        },
        status=status_code,
    )

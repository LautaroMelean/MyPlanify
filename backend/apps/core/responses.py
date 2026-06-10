from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, status_code=status.HTTP_200_OK):
    return Response({"success": True, "data": data}, status=status_code)


def created_response(data=None):
    return success_response(data, status.HTTP_201_CREATED)


def no_content_response():
    return Response(status=status.HTTP_204_NO_CONTENT)


def error_response(code, message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    payload = {"success": False, "error": {"code": code, "message": message}}
    if details:
        payload["error"]["details"] = details
    return Response(payload, status=status_code)

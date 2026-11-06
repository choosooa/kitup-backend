from rest_framework.response import Response


def success(data=None, status=200, message=None):
    return Response({"success": True, "message": message, "data": data}, status=status)


def error(code, message, status=400, detail=None):
    return Response(
        {"success": False, "error": {"code": code, "message": message, "detail": detail}},
        status=status,
    )

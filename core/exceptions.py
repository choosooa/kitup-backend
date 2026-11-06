from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "현재 상태에서 처리할 수 없는 요청입니다."
    default_code = "conflict"


class AlreadyStartedError(ConflictError):
    """이미 데이터 불러오기(운영 시작)가 끝난 테스트."""

    default_detail = "이미 주문·리뷰 데이터를 불러온 테스트입니다."
    default_code = "already_started"


class FrozenError(ConflictError):
    """리포트 생성(ended_at 기록) 이후 원가·고정비 수정 시도."""

    default_detail = "리포트가 생성된 테스트는 수정할 수 없습니다."
    default_code = "frozen"


class ReportAlreadyExistsError(ConflictError):
    default_detail = "이미 리포트가 생성되었습니다."
    default_code = "report_exists"


class RecommendationNotRetryableError(ConflictError):
    default_detail = "개선안 생성이 실패한 경우에만 다시 시도할 수 있습니다."
    default_code = "recommendation_not_retryable"


class AIServiceError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "AI 응답을 처리하지 못했습니다."
    default_code = "ai_error"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    code = getattr(exc, "default_code", "error")
    detail = response.data
    if isinstance(detail, dict) and "detail" in detail:
        message = str(detail["detail"])
    else:
        message = "요청 값을 확인해주세요."
    response.data = {
        "success": False,
        "error": {"code": code, "message": message, "detail": detail},
    }
    return response

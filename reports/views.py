from rest_framework.views import APIView


class ReportView(APIView):
    """GET 리포트 개요 / POST 리포트 생성 (테스트 종료 + Freeze)"""


class ReportPrecheckView(APIView):
    """GET 리포트 생성 전 점검"""


class SalesPatternView(APIView):
    """GET 판매 패턴 분석"""


class ProfitStructureView(APIView):
    """GET 수익 구조 분석"""


class CustomerReactionView(APIView):
    """GET 고객 반응 분석 (카테고리별 비율·건수)"""


class CategoryReviewsView(APIView):
    """GET 카테고리별 근거 리뷰"""


class RecommendationView(APIView):
    """GET AI 추천 개선안"""


class RecommendationRetryView(APIView):
    """POST 개선안 다시 생성 (FAILED 일 때만)"""

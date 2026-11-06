from rest_framework.views import APIView


class MenuTestListCreateView(APIView):
    """GET 테스트 목록 / POST 테스트 생성(빈 초안)"""


class TestDefaultsView(APIView):
    """GET 입력 기본값 + 샘플 데이터 정보"""


class MenuTestDetailView(APIView):
    """GET 테스트 상세 / PATCH 기본 정보 수정"""


class IngredientView(APIView):
    """GET 재료 목록 / PUT 재료 일괄 저장"""


class IngredientAIEstimateView(APIView):
    """POST AI 재료 원가 추정"""


class CostView(APIView):
    """GET 원가·예상 공헌이익 / PATCH 원가 수정(실측 원가 반영)"""

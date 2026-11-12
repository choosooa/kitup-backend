from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.views import APIView

from core.responses import success
from core.schema import envelope
from menu_tests.services.menu_test_service import get_test_or_404

from .serializers import (
    ChannelComparisonSerializer,
    DailySalesSerializer,
    HourlyLimitSerializer,
    HourlySalesSerializer,
    SummarySerializer,
)
from .services import metrics

TAGS = ["dashboard"]
NOT_FOUND = OpenApiResponse(description="not_found")


class DashboardSummaryView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="핵심 지표 카드 조회",
        description="완료 주문, 완료 매출, 추정 총공헌이익, 평균 건당 공헌이익. "
                    "추가 고정비는 차감하지 않음(fixed_cost_applied=false). 주문이 없으면 0, 평균은 null.",
        responses={200: envelope("DashboardSummaryResponse", SummarySerializer()), 404: NOT_FOUND},
    )
    def get(self, request, test_id):
        test = get_test_or_404(test_id)
        return success(SummarySerializer(metrics.summary(test)).data)


class HourlySalesView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="시간대별 판매 조회",
        description="1시간 단위(한국 시간) 주문 건수와 비중. 건수 내림차순, 같으면 시각 오름차순. "
                    "peak는 최다 건수 시간대(동률 포함)이며 limit과 무관하게 전체 기준.",
        parameters=[OpenApiParameter("limit", int, description="1~24, 기본 5")],
        responses={
            200: envelope("HourlySalesResponse", HourlySalesSerializer()),
            400: OpenApiResponse(description="limit 범위 오류"),
            404: NOT_FOUND,
        },
    )
    def get(self, request, test_id):
        test = get_test_or_404(test_id)
        params = HourlyLimitSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        data = metrics.hourly_sales(test, params.validated_data["limit"])
        return success(HourlySalesSerializer(data).data)


class ChannelComparisonView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="배달·픽업 비교 조회",
        description="유형별 완료 주문, 건당 공헌이익, 총공헌이익. 0건인 채널도 포함(건당 공헌이익 null).",
        responses={200: envelope("ChannelComparisonResponse", ChannelComparisonSerializer()), 404: NOT_FOUND},
    )
    def get(self, request, test_id):
        test = get_test_or_404(test_id)
        return success(ChannelComparisonSerializer(metrics.channels(test)).data)


class DailySalesView(APIView):
    @extend_schema(
        tags=TAGS,
        summary="일별 판매 조회",
        description="날짜별(한국 시간) 주문 건수와 판매 금액. 운영 기간 14일 중 주문 없는 날은 0건으로 포함.",
        responses={200: envelope("DailySalesResponse", DailySalesSerializer()), 404: NOT_FOUND},
    )
    def get(self, request, test_id):
        test = get_test_or_404(test_id)
        return success(DailySalesSerializer(metrics.daily_sales(test)).data)

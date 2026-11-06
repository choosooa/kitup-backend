from rest_framework.views import APIView


class DashboardSummaryView(APIView):
    """GET 핵심 지표 카드"""


class HourlySalesView(APIView):
    """GET 시간대별 판매"""


class ChannelComparisonView(APIView):
    """GET 배달·픽업 비교"""


class DailySalesView(APIView):
    """GET 일별 판매"""

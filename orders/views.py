from rest_framework.views import APIView


class OrderListView(APIView):
    """GET 주문·리뷰 목록"""


class OrderImportSampleView(APIView):
    """POST 가상 주문·리뷰 불러오기 (운영 시작)"""


class OrderStatusView(APIView):
    """(보류) PATCH 주문 상태 변경"""

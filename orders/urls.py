from django.urls import path

from .views import OrderImportSampleView, OrderListView, OrderStatusView

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("import-sample/", OrderImportSampleView.as_view(), name="order-import-sample"),
    path("<int:order_id>/status/", OrderStatusView.as_view(), name="order-status"),
]

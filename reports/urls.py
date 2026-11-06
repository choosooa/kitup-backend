from django.urls import path

from .views import (
    CategoryReviewsView,
    CustomerReactionView,
    ProfitStructureView,
    RecommendationRetryView,
    RecommendationView,
    ReportPrecheckView,
    ReportView,
    SalesPatternView,
)

urlpatterns = [
    path("", ReportView.as_view(), name="report-detail"),
    path("precheck/", ReportPrecheckView.as_view(), name="report-precheck"),
    path("sales-pattern/", SalesPatternView.as_view(), name="report-sales-pattern"),
    path("profit/", ProfitStructureView.as_view(), name="report-profit"),
    path("customer-reaction/", CustomerReactionView.as_view(), name="report-customer-reaction"),
    path(
        "customer-reaction/<str:category>/reviews/",
        CategoryReviewsView.as_view(),
        name="report-category-reviews",
    ),
    path("recommendation/", RecommendationView.as_view(), name="report-recommendation"),
    path(
        "recommendation/retry/",
        RecommendationRetryView.as_view(),
        name="report-recommendation-retry",
    ),
]

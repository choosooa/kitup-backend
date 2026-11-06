from django.urls import path

from .views import (
    CostView,
    IngredientAIEstimateView,
    IngredientView,
    MenuTestDetailView,
    MenuTestListCreateView,
    TestDefaultsView,
)

urlpatterns = [
    path("", MenuTestListCreateView.as_view(), name="test-list"),
    path("defaults/", TestDefaultsView.as_view(), name="test-defaults"),
    path("<int:test_id>/", MenuTestDetailView.as_view(), name="test-detail"),

    path("<int:test_id>/ingredients/", IngredientView.as_view(), name="test-ingredients"),
    path(
        "<int:test_id>/ingredients/ai-estimate/",
        IngredientAIEstimateView.as_view(),
        name="test-ingredients-ai-estimate",
    ),

    path("<int:test_id>/cost/", CostView.as_view(), name="test-cost"),
]

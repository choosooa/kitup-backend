from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/tests/<int:test_id>/orders/", include("orders.urls")),
    path("api/tests/<int:test_id>/dashboard/", include("dashboard.urls")),
    path("api/tests/<int:test_id>/report/", include("reports.urls")),
    path("api/tests/", include("menu_tests.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

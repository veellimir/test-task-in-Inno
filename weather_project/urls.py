from typing import List

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Test task in Inno",
        default_version="v1",
        description="API documentation for Inno",
        contact=openapi.Contact(email="kkazancov@gmail.com"),
    ),
    public=True,
)

urlpatterns: List[path] = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("", include("apps.weather.urls")),
]

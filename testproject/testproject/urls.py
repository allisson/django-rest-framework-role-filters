from django.urls import include, path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path(r"^api/", include("testapp.urls")),
]

urlpatterns += [
    path(
        r"^openapi-schema",
        get_schema_view(
            title="Tutorial app",
            description="tutorial app",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
]

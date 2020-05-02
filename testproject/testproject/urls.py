from django.conf.urls import include, url
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

urlpatterns = [
    url(r"^api/", include("testapp.urls")),
]

urlpatterns += [
    url(
        r"^openapi-schema",
        get_schema_view(title="Tutorial app", description="tutorial app", version="1.0.0",),
        name="openapi-schema",
    ),
]

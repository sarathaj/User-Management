from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="UserHub API",
        default_version="v1",
        description="API documentation for the UserHub Task Management System",
        contact=openapi.Contact(email="sarathraj9027@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes for different apps
    path("api/auth/", include("accounts.urls")),
    path("api/tasks/", include("tasks.urls")),
    # Swagger/ReDoc routes from your README
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Frontend route - This must be the last URL pattern to catch the root
    path("", include("frontend.urls", namespace="frontend")),
]

# Serve media files during development (for task attachments)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

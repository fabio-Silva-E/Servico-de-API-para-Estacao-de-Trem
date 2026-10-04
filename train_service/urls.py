from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/train/", include("train.urls", namespace="train")),
    path("__debug__/", include("debug_toolbar.urls")),

    # Documentação da API (Swagger / ReDoc)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    # Páginas (templates)
    path("", TemplateView.as_view(template_name="home.html")),
    path("login/", TemplateView.as_view(template_name="user/login.html")),
    path("register/", TemplateView.as_view(template_name="user/register.html")),
    path("profile/", TemplateView.as_view(template_name="user/profile.html")),
    path("stations/", TemplateView.as_view(template_name="stations/list.html")),
    path("routes/", TemplateView.as_view(template_name="routes/list.html")),
    path("crew/", TemplateView.as_view(template_name="crew/list.html")),
    path("train-types/", TemplateView.as_view(template_name="train_types/list.html")),
    path("trains/", TemplateView.as_view(template_name="trains/list.html")),
    path("journeys/", TemplateView.as_view(template_name="journeys/list.html")),
    path("journeys/detail/", TemplateView.as_view(template_name="journeys/detail.html")),
    path("orders/", TemplateView.as_view(template_name="orders/list.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

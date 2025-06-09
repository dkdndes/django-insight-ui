"""URL-Konfiguration für Tests."""

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        TemplateView.as_view(
            template_name="index.html",
            extra_context={
                "nav_links": [
                    {"url": "/", "text": "Home", "active": True},
                    {"url": "/about/", "text": "Über uns"},
                    {"url": "/contact/", "text": "Kontakt"},
                ]
            },
        ),
        name="home",
    ),
]

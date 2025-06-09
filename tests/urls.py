"""URL-Konfiguration für Tests."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path(
        "",
        TemplateView.as_view(
            template_name="index.html",
            extra_context={
                "nav_links": [
                    {"url": "/", "text": "Home", "active": True},
                    {"url": "/about/", "text": "Über uns"},
                    {"url": "/contact/", "text": "Kontakt"},
                ],
                "breadcrumb_items": [
                    {"url": "/", "text": "Home"},
                    {"url": "/demo/", "text": "Demo"},
                    {"text": "Aktuelle Seite"},
                ],
                "table_headers": ["Name", "E-Mail", "Status"],
                "table_rows": [
                    ["Max Mustermann", "max@example.com", "Aktiv"],
                    ["Anna Schmidt", "anna@example.com", "Inaktiv"],
                ],
                "card_actions": [
                    {"url": "/details/", "text": "Details", "type": "primary"},
                    {"url": "/edit/", "text": "Bearbeiten", "type": "secondary"},
                ],
                "form_fields": [
                    {
                        "id": "name",
                        "name": "name",
                        "label": "Name",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "id": "email",
                        "name": "email",
                        "label": "E-Mail",
                        "type": "email",
                        "placeholder": "ihre@email.com",
                    },
                ],
                "form_actions": [
                    {"text": "Senden", "type": "submit", "style": "primary"},
                ],
                "modal_actions": [
                    {"text": "Abbrechen", "type": "secondary", "dismiss": True},
                    {"text": "Speichern", "type": "primary"},
                ],
                "sidebar_items": [
                    {"url": "/dashboard/", "text": "Dashboard", "active": True},
                    {"url": "/settings/", "text": "Einstellungen", "icon": "⚙️"},
                ],
            },
        ),
        name="home",
    ),
    prefix_default_language=False,
)

"""URL-Konfiguration für Tests."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from insight_ui import views as insight_views
import json
import time


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path("api/live-data/", insight_views.live_data_view, name="live_data"),
    path("api/more-items/", insight_views.more_items_view, name="more_items"),
    path("api/form-submit/", insight_views.htmx_form_submit, name="htmx_form_submit"),
    path("components/<str:component_name>/", insight_views.component_demo_view, name="component_demo"),
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
                "htmx_form_fields": [
                    {
                        "id": "htmx_name",
                        "name": "name",
                        "label": "Name (HTMX)",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "id": "htmx_message",
                        "name": "message",
                        "label": "Nachricht (HTMX)",
                        "type": "textarea",
                        "rows": 3,
                    },
                ],
                "htmx_config": {
                    "url": "/api/form-submit/",
                    "target": "#form-result",
                    "swap": "innerHTML",
                    "validate": True,
                },
                "scroll_items": [
                    f"Scroll-Element {i}" for i in range(1, 6)
                ],
            },
        ),
        name="home",
    ),
    prefix_default_language=False,
)

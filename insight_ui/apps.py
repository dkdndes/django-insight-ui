"""Django App-Konfiguration für Insight UI."""

from django.apps import AppConfig


class InsightUiConfig(AppConfig):
    """Konfiguration für die Insight UI Django-App."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "insight_ui"
    verbose_name = "Django Insight UI"

"""URL-Konfiguration für Tests."""

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.views.i18n import set_language

from insight_ui.views import insight_ui

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
]

urlpatterns += i18n_patterns(
    path("", insight_ui, name="home"),
    prefix_default_language=False,
)

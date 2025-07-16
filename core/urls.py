"""URL-Konfiguration für Tests."""

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path("", include("insight_ui.urls")),
]

urlpatterns += i18n_patterns(path("", include("insight_ui.urls")), prefix_default_language=False)

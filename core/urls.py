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
    path("api/normal-form-submit/", insight_views.normal_form_submit, name="normal_form_submit"),
    path("components/<str:component_name>/", insight_views.component_demo_view, name="component_demo"),
]

urlpatterns += i18n_patterns(
    path("", insight_views.index_view, name="home"),
    prefix_default_language=False,
)

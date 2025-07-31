"""URL-Konfiguration für Tests."""

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import set_language
from insight_ui.views import get_nav_and_footer_context

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="insight_ui/login.html", extra_context=get_nav_and_footer_context()),
        name="login",
    ),
    path("i18n/setlang/", set_language, name="set_language"),
    path("", include("insight_ui.urls")),
]

urlpatterns += i18n_patterns(path("", include("insight_ui.urls")), prefix_default_language=False)

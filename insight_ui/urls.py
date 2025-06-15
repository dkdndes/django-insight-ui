from django.urls import path

from . import views

urlpatterns = [
    path("api/live-data/", views.live_data_view, name="live_data"),
    path("api/more-items/", views.more_items_view, name="more_items"),
    path("api/form-submit/", views.htmx_form_submit, name="htmx_form_submit"),
    path(
        "api/normal-form-submit/",
        views.normal_form_submit,
        name="normal_form_submit",
    ),
    path(
        "components/<str:component_name>/",
        views.component_demo_view,
        name="component_demo",
    ),
    path("toggle_view/", views.toggle_view, name="toggle_view"),
    path("", views.storybook_view, name="storybook_view"),
]

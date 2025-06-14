from django.urls import path
from views import (
    component_demo_view,
    htmx_form_submit,
    live_data_view,
    more_items_view,
    normal_form_submit,
    toggle_view,
)

urlpatterns = [
    path("api/live-data/", live_data_view, name="live_data"),
    path("api/more-items/", more_items_view, name="more_items"),
    path("api/form-submit/", htmx_form_submit, name="htmx_form_submit"),
    path(
        "api/normal-form-submit/",
        normal_form_submit,
        name="normal_form_submit",
    ),
    path(
        "components/<str:component_name>/",
        component_demo_view,
        name="component_demo",
    ),
    path("toggle_view/", toggle_view, name="toggle_view"),
]

import pytest
from django.test import override_settings
from django.core.management import call_command
from django.conf import settings
import os


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup für Django-Datenbank in Tests."""
    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb")


@pytest.fixture
def live_server_url(live_server):
    """Fixture für Live-Server-URL."""
    return live_server.url


# Playwright-spezifische Fixtures
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Konfiguration für Browser-Kontext."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def page_with_context(page):
    """Page-Fixture mit zusätzlichem Kontext."""
    # Setze längere Timeouts für HTMX-Requests
    page.set_default_timeout(10000)
    return page

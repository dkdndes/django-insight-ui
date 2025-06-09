import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import call_command


def pytest_configure(config):
    """Configure Django settings for pytest."""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup für Django-Datenbank in Tests."""
    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb", verbosity=0)


@pytest.fixture(scope="session")
def live_server_class():
    """Use Django's StaticLiveServerTestCase for serving static files."""
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    return StaticLiveServerTestCase


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
        "locale": "de-DE",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Browser-Launch-Argumente."""
    return {
        **browser_type_launch_args,
        "headless": True,
    }


@pytest.fixture
def page_with_context(page):
    """Page-Fixture mit zusätzlichem Kontext."""
    # Setze längere Timeouts für HTMX-Requests
    page.set_default_timeout(10000)
    return page


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass

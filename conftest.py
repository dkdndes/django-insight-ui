import os

import django
import pytest
from django.conf import settings
from django.core.management import call_command


def pytest_configure(config) -> None:
    """Configure Django settings for pytest."""
    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        django.setup()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker) -> None:
    """Setup für Django-Datenbank in Tests."""
    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb", verbosity=0)


@pytest.fixture(scope="session")
def live_server_class():
    """Use Django's StaticLiveServerTestCase for serving static files."""
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase

    return StaticLiveServerTestCase


@pytest.fixture
def live_server_url(live_server) -> None:
    """Fixture für Live-Server-URL."""
    return live_server.url


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db) -> None:
    """Enable database access for all tests."""

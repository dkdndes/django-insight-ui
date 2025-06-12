from playwright.sync_api import Playwright, Browser
import pytest


def pytest_configure(config):
    """Playwright-Konfiguration für pytest"""
    pass


@pytest.fixture(scope="session")
def browser():
    """Browser-Fixture für Tests"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # Nicht-headless für Debugging
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Page-Fixture für Tests"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

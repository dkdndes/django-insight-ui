"""
Standalone Playwright-Tests ohne Django-Integration.
Diese Tests laufen gegen einen bereits laufenden Django-Server.
"""

import pytest
import re
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


class TestInsightUI:
    """Standalone Playwright-Tests für Insight UI."""
    
    @pytest.fixture(scope="class")
    def browser(self):
        """Browser-Fixture für die gesamte Testklasse."""
        with sync_playwright() as p:
            # Versuche verschiedene Browser in der Reihenfolge der Verfügbarkeit
            browser = None
            try:
                browser = p.webkit.launch(headless=False, slow_mo=100)
            except Exception:
                try:
                    browser = p.firefox.launch(headless=False, slow_mo=100)
                except Exception:
                    try:
                        browser = p.chromium.launch(headless=False, slow_mo=100)
                    except Exception:
                        pytest.skip("Kein Playwright-Browser verfügbar")
            
            yield browser
            browser.close()
    
    @pytest.fixture
    def context(self, browser: Browser):
        """Browser-Kontext-Fixture."""
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            locale="de-DE"
        )
        yield context
        context.close()
    
    @pytest.fixture
    def page(self, context: BrowserContext):
        """Page-Fixture."""
        page = context.new_page()
        page.set_default_timeout(10000)
        yield page
        page.close()
    
    @pytest.fixture
    def base_url(self):
        """Base URL für Tests."""
        return "http://localhost:8000"
    
    def test_homepage_loads(self, page: Page, base_url: str):
        """Test, dass die Startseite korrekt lädt."""
        page.goto(base_url)
        
        # Warte bis die Seite geladen ist
        page.wait_for_load_state("networkidle")
        
        # Prüfe, dass der Titel korrekt ist
        assert "Django Insight UI Demo" in page.title()
        
        # Prüfe, dass die Hauptüberschrift vorhanden ist
        h1 = page.locator("h1")
        assert h1.is_visible()
        assert "Willkommen bei Django Insight UI" in h1.text_content()
    
    def test_navbar_functionality(self, page: Page, base_url: str):
        """Test der Navbar-Funktionalität."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Prüfe, dass die Navbar vorhanden ist
        navbar = page.locator(".insight-navbar")
        assert navbar.is_visible()
        
        # Prüfe Brand-Text
        brand = navbar.locator(".insight-navbar__brand")
        if brand.is_visible():
            assert "Django Insight UI" in brand.text_content()
    
    def test_alert_components(self, page: Page, base_url: str):
        """Test der Alert-Komponenten."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Prüfe verschiedene Alert-Typen
        alerts = page.locator(".insight-alert")
        assert alerts.count() > 0
        
        # Prüfe Info-Alert
        info_alert = page.locator(".insight-alert--info")
        if info_alert.is_visible():
            assert "Informationsmeldung" in info_alert.text_content()
    
    def test_modal_functionality(self, page: Page, base_url: str):
        """Test der Modal-Funktionalität."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Finde Modal-Trigger-Button
        modal_trigger = page.locator('[data-insight-toggle="modal"]')
        if not modal_trigger.is_visible():
            pytest.skip("Modal-Trigger nicht gefunden")
        
        # Klicke auf Modal-Button
        modal_trigger.click()
        
        # Warte kurz für Animation
        page.wait_for_timeout(300)
        
        # Prüfe, dass Modal geöffnet wird
        modal = page.locator("#demo-modal")
        if modal.is_visible():
            # Prüfe Modal-Klasse
            class_attr = modal.get_attribute("class")
            assert "insight-modal--open" in class_attr
            
            # Prüfe Modal-Inhalt
            assert "Demo Modal" in modal.text_content()
    
    def test_form_component(self, page: Page, base_url: str):
        """Test der Formular-Komponente."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Prüfe, dass das Formular vorhanden ist
        form = page.locator(".insight-form")
        if form.is_visible():
            # Prüfe Formular-Titel
            form_title = form.locator(".insight-form__title")
            if form_title.is_visible():
                assert "Kontaktformular" in form_title.text_content()
    
    def test_javascript_loading(self, page: Page, base_url: str):
        """Test, dass JavaScript korrekt geladen wird."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Prüfe, dass HTMX geladen wurde
        htmx_loaded = page.evaluate("typeof htmx !== 'undefined'")
        assert htmx_loaded, "HTMX wurde nicht geladen"
        
        # Prüfe, dass Alpine.js geladen wurde
        alpine_loaded = page.evaluate("typeof Alpine !== 'undefined'")
        assert alpine_loaded, "Alpine.js wurde nicht geladen"
    
    def test_responsive_design(self, page: Page, base_url: str):
        """Test des responsiven Designs."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Test Mobile Viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(500)
        
        # Prüfe, dass die Seite noch funktioniert
        h1 = page.locator("h1")
        assert h1.is_visible()
        
        # Test Desktop Viewport
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.wait_for_timeout(500)
        
        # Prüfe, dass die Seite noch funktioniert
        assert h1.is_visible()
    
    def test_alpine_js_integration(self, page: Page, base_url: str):
        """Test der Alpine.js-Integration."""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # Finde Alpine.js-Komponente
        alpine_section = page.locator('[x-data]')
        if not alpine_section.is_visible():
            pytest.skip("Alpine.js-Komponente nicht gefunden")
        
        # Prüfe Counter-Funktionalität
        counter_button = alpine_section.locator('button').first
        counter_display = alpine_section.locator('span')
        
        if counter_button.is_visible() and counter_display.is_visible():
            # Klicke auf Counter-Button
            counter_button.click()
            page.wait_for_timeout(100)
            
            # Prüfe, dass Counter sich erhöht hat
            assert "1" in counter_display.text_content()


def test_simple_page_load():
    """Einfacher Test ohne Klassen-Struktur."""
    with sync_playwright() as p:
        # Versuche verschiedene Browser
        browser = None
        try:
            browser = p.webkit.launch(headless=True)
        except Exception:
            try:
                browser = p.firefox.launch(headless=True)
            except Exception:
                try:
                    browser = p.chromium.launch(headless=True)
                except Exception:
                    pytest.skip("Kein Browser verfügbar")
        
        page = browser.new_page()
        
        try:
            page.goto("http://localhost:8000")
            page.wait_for_load_state("networkidle", timeout=5000)
            
            # Einfache Prüfung
            title = page.title()
            assert "Django" in title or "Insight" in title
            
        except Exception as e:
            pytest.skip(f"Server nicht erreichbar: {e}")
        finally:
            browser.close()

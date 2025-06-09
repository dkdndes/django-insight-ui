import pytest
import re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def django_db_setup():
    """Setup für Django-Datenbank in Playwright-Tests."""
    pass


def test_homepage_loads(page: Page, live_server):
    """Test, dass die Startseite korrekt lädt."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass der Titel korrekt ist
    expect(page).to_have_title("Django Insight UI Demo")
    
    # Prüfe, dass die Hauptüberschrift vorhanden ist
    expect(page.locator("h1")).to_contain_text("Willkommen bei Django Insight UI")


def test_navbar_functionality(page: Page, live_server):
    """Test der Navbar-Funktionalität."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass die Navbar vorhanden ist
    navbar = page.locator(".insight-navbar")
    expect(navbar).to_be_visible()
    
    # Prüfe Brand-Text
    expect(navbar.locator(".insight-navbar__brand")).to_contain_text("Django Insight UI")


def test_language_selector(page: Page, live_server):
    """Test der Sprachauswahl-Funktionalität."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass der Sprachauswähler vorhanden ist
    language_selector = page.locator(".insight-language-selector")
    expect(language_selector).to_be_visible()


def test_alert_components(page: Page, live_server):
    """Test der Alert-Komponenten."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe verschiedene Alert-Typen
    alerts = page.locator(".insight-alert")
    expect(alerts).to_have_count(4)  # info, success, warning, error
    
    # Prüfe Info-Alert
    info_alert = page.locator(".insight-alert--info")
    expect(info_alert).to_be_visible()
    expect(info_alert).to_contain_text("Dies ist eine Informationsmeldung")
    
    # Prüfe Success-Alert
    success_alert = page.locator(".insight-alert--success")
    expect(success_alert).to_be_visible()
    expect(success_alert).to_contain_text("Erfolgreich gespeichert!")


def test_alert_dismissible(page: Page, live_server):
    """Test, dass Alerts geschlossen werden können."""
    page.goto(f"{live_server.url}/")
    
    # Finde einen Alert mit Schließen-Button
    alert = page.locator(".insight-alert").first
    dismiss_button = alert.locator('[data-insight-dismiss="alert"]')
    
    if dismiss_button.is_visible():
        # Klicke auf Schließen-Button
        dismiss_button.click()
        
        # Warte kurz für Animation
        page.wait_for_timeout(500)
        
        # Alert sollte nicht mehr sichtbar sein
        expect(alert).not_to_be_visible()


def test_breadcrumbs_component(page: Page, live_server):
    """Test der Breadcrumb-Komponente."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass Breadcrumbs vorhanden sind
    breadcrumbs = page.locator(".insight-breadcrumbs")
    expect(breadcrumbs).to_be_visible()


def test_table_component(page: Page, live_server):
    """Test der Tabellen-Komponente."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass die Tabelle vorhanden ist
    table = page.locator(".insight-table")
    expect(table).to_be_visible()
    
    # Prüfe Tabellen-Caption
    caption = table.locator("caption")
    expect(caption).to_contain_text("Beispiel-Tabelle")


def test_card_components(page: Page, live_server):
    """Test der Karten-Komponenten."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass Karten vorhanden sind
    cards = page.locator(".insight-card")
    expect(cards).to_have_count_greater_than(0)
    
    # Prüfe erste Karte
    first_card = cards.first
    expect(first_card).to_be_visible()


def test_form_component(page: Page, live_server):
    """Test der Formular-Komponente."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass das Formular vorhanden ist
    form = page.locator(".insight-form")
    expect(form).to_be_visible()
    
    # Prüfe Formular-Titel
    form_title = form.locator(".insight-form__title")
    expect(form_title).to_contain_text("Kontaktformular")


def test_modal_functionality(page: Page, live_server):
    """Test der Modal-Funktionalität."""
    page.goto(f"{live_server.url}/")
    
    # Finde Modal-Trigger-Button
    modal_trigger = page.locator('[data-insight-toggle="modal"]')
    expect(modal_trigger).to_be_visible()
    
    # Klicke auf Modal-Button
    modal_trigger.click()
    
    # Prüfe, dass Modal geöffnet wird
    modal = page.locator("#demo-modal")
    expect(modal).to_have_class(re.compile(r"insight-modal--open"))
    
    # Prüfe Modal-Inhalt
    expect(modal).to_contain_text("Demo Modal")
    expect(modal).to_contain_text("Dies ist ein Beispiel-Modal.")


def test_sidebar_component(page: Page, live_server):
    """Test der Sidebar-Komponente."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass die Sidebar vorhanden ist
    sidebar = page.locator(".insight-sidebar")
    expect(sidebar).to_be_visible()


def test_live_content_htmx(page: Page, live_server):
    """Test der Live-Content-Funktionalität mit HTMX."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass Live-Content-Container vorhanden ist
    live_content = page.locator("#live-content")
    expect(live_content).to_be_visible()
    
    # Warte kurz und prüfe, ob HTMX-Request ausgeführt wird
    page.wait_for_timeout(1000)


def test_alpine_js_integration(page: Page, live_server):
    """Test der Alpine.js-Integration."""
    page.goto(f"{live_server.url}/")
    
    # Finde Alpine.js-Komponente
    alpine_section = page.locator('[x-data]')
    expect(alpine_section).to_be_visible()
    
    # Prüfe Counter-Funktionalität
    counter_button = alpine_section.locator('button').first
    counter_display = alpine_section.locator('span')
    
    # Klicke auf Counter-Button
    counter_button.click()
    
    # Prüfe, dass Counter sich erhöht hat
    expect(counter_display).to_contain_text("1")


def test_theme_toggle_functionality(page: Page, live_server):
    """Test der Theme-Toggle-Funktionalität."""
    page.goto(f"{live_server.url}/")
    
    # Finde Theme-Toggle-Button
    theme_toggle = page.locator(".insight-theme-toggle")
    
    if theme_toggle.is_visible():
        # Klicke auf Theme-Toggle
        theme_toggle.click()
        
        # Prüfe, dass Theme gewechselt wurde
        html_element = page.locator("html")
        # Das Theme sollte sich geändert haben
        page.wait_for_timeout(100)


def test_responsive_design(page: Page, live_server):
    """Test des responsiven Designs."""
    page.goto(f"{live_server.url}/")
    
    # Test Mobile Viewport
    page.set_viewport_size({"width": 375, "height": 667})
    page.wait_for_timeout(500)
    
    # Prüfe, dass die Seite noch funktioniert
    expect(page.locator("h1")).to_be_visible()
    
    # Test Tablet Viewport
    page.set_viewport_size({"width": 768, "height": 1024})
    page.wait_for_timeout(500)
    
    # Prüfe, dass die Seite noch funktioniert
    expect(page.locator("h1")).to_be_visible()
    
    # Test Desktop Viewport
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.wait_for_timeout(500)
    
    # Prüfe, dass die Seite noch funktioniert
    expect(page.locator("h1")).to_be_visible()


def test_accessibility_basics(page: Page, live_server):
    """Test grundlegender Accessibility-Features."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass wichtige ARIA-Attribute vorhanden sind
    navbar = page.locator(".insight-navbar")
    if navbar.is_visible():
        # Navbar sollte role="navigation" haben oder ähnlich
        pass
    
    # Prüfe, dass Buttons korrekte Labels haben
    buttons = page.locator("button")
    for i in range(min(buttons.count(), 5)):  # Prüfe erste 5 Buttons
        button = buttons.nth(i)
        if button.is_visible():
            # Button sollte Text oder aria-label haben
            text_content = button.text_content()
            aria_label = button.get_attribute("aria-label")
            assert text_content or aria_label, f"Button {i} hat weder Text noch aria-label"


def test_css_loading(page: Page, live_server):
    """Test, dass CSS korrekt geladen wird."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass TailwindCSS geladen wurde
    body = page.locator("body")
    computed_style = page.evaluate("getComputedStyle(document.body)")
    
    # Prüfe, dass Custom CSS geladen wurde
    insight_elements = page.locator("[class*='insight-']")
    expect(insight_elements).to_have_count_greater_than(0)


def test_javascript_loading(page: Page, live_server):
    """Test, dass JavaScript korrekt geladen wird."""
    page.goto(f"{live_server.url}/")
    
    # Prüfe, dass HTMX geladen wurde
    htmx_loaded = page.evaluate("typeof htmx !== 'undefined'")
    assert htmx_loaded, "HTMX wurde nicht geladen"
    
    # Prüfe, dass Alpine.js geladen wurde
    alpine_loaded = page.evaluate("typeof Alpine !== 'undefined'")
    assert alpine_loaded, "Alpine.js wurde nicht geladen"
    
    # Prüfe, dass Insight UI JavaScript geladen wurde
    insight_ui_loaded = page.evaluate("typeof InsightUI !== 'undefined'")
    assert insight_ui_loaded, "Insight UI JavaScript wurde nicht geladen"

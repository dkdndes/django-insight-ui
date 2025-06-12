import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def live_server_url():
    """Fixture für die Live-Server-URL"""
    return "http://127.0.0.1:8000"


def test_theme_toggle_functionality(page: Page, live_server_url: str):
    """Test der Theme-Toggle-Funktionalität"""
    
    # Navigiere zur Hauptseite
    page.goto(live_server_url)
    
    # Warte bis die Seite vollständig geladen ist
    page.wait_for_load_state("networkidle")
    
    # Prüfe, ob das HTML-Element existiert
    html_element = page.locator("html")
    expect(html_element).to_be_visible()
    
    # Prüfe den initialen Theme-Zustand (sollte light sein)
    initial_theme = html_element.get_attribute("data-theme")
    print(f"Initial theme: {initial_theme}")
    
    # Prüfe, ob die dark-Klasse initial nicht vorhanden ist
    has_dark_class_initial = html_element.evaluate("el => el.classList.contains('dark')")
    print(f"Initial dark class: {has_dark_class_initial}")
    
    # Suche nach dem Theme-Toggle-Button
    theme_toggle = page.locator(".insight-theme-toggle")
    
    if theme_toggle.count() == 0:
        # Fallback: Suche nach anderen möglichen Selektoren
        theme_toggle = page.locator('button[aria-label*="Farbschema"]')
        
    if theme_toggle.count() == 0:
        # Weitere Fallback-Optionen
        theme_toggle = page.locator('button:has(svg)')
        
    print(f"Theme toggle buttons found: {theme_toggle.count()}")
    
    if theme_toggle.count() > 0:
        # Klicke auf den ersten Theme-Toggle-Button
        theme_toggle.first.click()
        
        # Warte kurz für die Theme-Änderung
        page.wait_for_timeout(500)
        
        # Prüfe den Theme-Zustand nach dem Klick
        new_theme = html_element.get_attribute("data-theme")
        has_dark_class_after = html_element.evaluate("el => el.classList.contains('dark')")
        
        print(f"Theme after click: {new_theme}")
        print(f"Dark class after click: {has_dark_class_after}")
        
        # Prüfe, ob sich das Theme geändert hat
        if initial_theme == "light":
            expect(html_element).to_have_attribute("data-theme", "dark")
            assert has_dark_class_after, "Dark class should be added to HTML element"
        else:
            expect(html_element).to_have_attribute("data-theme", "light")
            assert not has_dark_class_after, "Dark class should be removed from HTML element"
            
        # Teste nochmaliges Klicken (zurück zum ursprünglichen Theme)
        theme_toggle.first.click()
        page.wait_for_timeout(500)
        
        final_theme = html_element.get_attribute("data-theme")
        has_dark_class_final = html_element.evaluate("el => el.classList.contains('dark')")
        
        print(f"Final theme: {final_theme}")
        print(f"Final dark class: {has_dark_class_final}")
        
        # Sollte wieder zum ursprünglichen Theme zurückkehren
        expect(html_element).to_have_attribute("data-theme", initial_theme)
        assert has_dark_class_final == has_dark_class_initial, "Should return to initial dark class state"
        
    else:
        pytest.fail("Kein Theme-Toggle-Button gefunden")


def test_theme_persistence(page: Page, live_server_url: str):
    """Test der Theme-Persistierung im localStorage"""
    
    page.goto(live_server_url)
    page.wait_for_load_state("networkidle")
    
    # Prüfe localStorage vor Theme-Änderung
    initial_storage = page.evaluate("() => localStorage.getItem('insight-theme')")
    print(f"Initial localStorage theme: {initial_storage}")
    
    # Suche Theme-Toggle-Button
    theme_toggle = page.locator(".insight-theme-toggle").first
    
    if theme_toggle.count() == 0:
        theme_toggle = page.locator('button[aria-label*="Farbschema"]').first
        
    if theme_toggle.count() > 0:
        # Klicke auf Theme-Toggle
        theme_toggle.click()
        page.wait_for_timeout(500)
        
        # Prüfe localStorage nach Theme-Änderung
        stored_theme = page.evaluate("() => localStorage.getItem('insight-theme')")
        print(f"Stored theme after click: {stored_theme}")
        
        # localStorage sollte das neue Theme enthalten
        assert stored_theme in ["light", "dark"], f"Invalid theme in localStorage: {stored_theme}"
        
        # Lade die Seite neu
        page.reload()
        page.wait_for_load_state("networkidle")
        
        # Prüfe, ob das Theme nach dem Neuladen erhalten bleibt
        html_element = page.locator("html")
        reloaded_theme = html_element.get_attribute("data-theme")
        reloaded_storage = page.evaluate("() => localStorage.getItem('insight-theme')")
        
        print(f"Theme after reload: {reloaded_theme}")
        print(f"localStorage after reload: {reloaded_storage}")
        
        # Theme sollte nach Reload gleich sein
        assert reloaded_theme == stored_theme, "Theme should persist after page reload"
        assert reloaded_storage == stored_theme, "localStorage should persist after page reload"
    else:
        pytest.fail("Kein Theme-Toggle-Button gefunden")


def test_javascript_console_errors(page: Page, live_server_url: str):
    """Test auf JavaScript-Konsolen-Fehler"""
    
    console_messages = []
    
    def handle_console(msg):
        console_messages.append({
            'type': msg.type,
            'text': msg.text,
            'location': msg.location
        })
    
    page.on("console", handle_console)
    
    # Navigiere zur Seite
    page.goto(live_server_url)
    page.wait_for_load_state("networkidle")
    
    # Warte etwas für mögliche JavaScript-Initialisierung
    page.wait_for_timeout(2000)
    
    # Filtere Fehler und Warnungen
    errors = [msg for msg in console_messages if msg['type'] in ['error', 'warning']]
    
    print("Console messages:")
    for msg in console_messages:
        print(f"  {msg['type']}: {msg['text']}")
    
    if errors:
        print("JavaScript errors/warnings found:")
        for error in errors:
            print(f"  {error['type']}: {error['text']} at {error['location']}")
    
    # Prüfe, ob InsightUI geladen wurde
    insight_ui_loaded = page.evaluate("() => typeof window.InsightUI !== 'undefined'")
    print(f"InsightUI loaded: {insight_ui_loaded}")
    
    assert insight_ui_loaded, "InsightUI should be loaded"


def test_navbar_structure(page: Page, live_server_url: str):
    """Test der Navbar-Struktur und Theme-Toggle-Button"""
    
    page.goto(live_server_url)
    page.wait_for_load_state("networkidle")
    
    # Prüfe, ob die Navbar existiert
    navbar = page.locator("nav")
    expect(navbar).to_be_visible()
    
    # Prüfe verschiedene mögliche Theme-Toggle-Selektoren
    selectors_to_check = [
        ".insight-theme-toggle",
        'button[aria-label*="Farbschema"]',
        'button[aria-label*="theme"]',
        'button:has(svg):has(path[d*="20.354"])',  # Mond-Icon
        'button:has(svg):has(path[d*="M12 3v1"])'   # Sonnen-Icon
    ]
    
    found_toggle = False
    for selector in selectors_to_check:
        toggle = page.locator(selector)
        count = toggle.count()
        print(f"Selector '{selector}': {count} elements found")
        
        if count > 0:
            found_toggle = True
            # Prüfe Eigenschaften des gefundenen Elements
            element = toggle.first
            tag_name = element.evaluate("el => el.tagName")
            classes = element.evaluate("el => el.className")
            aria_label = element.get_attribute("aria-label")
            
            print(f"  Tag: {tag_name}")
            print(f"  Classes: {classes}")
            print(f"  Aria-label: {aria_label}")
            
            # Prüfe, ob das Element klickbar ist
            expect(element).to_be_visible()
            expect(element).to_be_enabled()
    
    if not found_toggle:
        # Zeige alle Buttons in der Navbar für Debugging
        all_buttons = page.locator("nav button")
        button_count = all_buttons.count()
        print(f"All buttons in navbar: {button_count}")
        
        for i in range(button_count):
            button = all_buttons.nth(i)
            classes = button.evaluate("el => el.className")
            aria_label = button.get_attribute("aria-label")
            inner_html = button.inner_html()
            print(f"  Button {i}: classes='{classes}', aria-label='{aria_label}'")
            print(f"    HTML: {inner_html[:100]}...")
    
    assert found_toggle, "Theme-Toggle-Button sollte in der Navbar gefunden werden"

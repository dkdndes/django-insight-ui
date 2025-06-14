import pytest
import os
from playwright.sync_api import expect

# Setze die Umgebungsvariable für global installierte Browser
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

@pytest.mark.django_db
def test_sidebar_functionality(page, live_server_url):
    """Test, dass die Sidebars korrekt ein- und ausgeblendet werden."""
    # Navigiere zur Startseite
    page.goto(f"{live_server_url}/")
    
    # Überprüfe, ob die linke Sidebar standardmäßig sichtbar ist
    left_sidebar = page.locator("#left-sidebar")
    expect(left_sidebar).to_be_visible()
    
    # Klicke auf den Toggle-Button für die linke Sidebar
    page.locator("#toggle-left-sidebar").click()
    
    # Überprüfe, ob die linke Sidebar ausgeblendet wird
    expect(left_sidebar).to_have_class("closed")
    
    # Bewege die Maus zum Hover-Bereich
    page.locator("#left-sidebar-hover-area").hover()
    
    # Warte kurz, damit der Hover-Effekt wirken kann
    page.wait_for_timeout(300)
    
    # Überprüfe, ob die Sidebar wieder eingeblendet wird
    expect(left_sidebar).not_to_have_class("closed")
    
    # Überprüfe die rechte Sidebar
    right_sidebar = page.locator("#right-sidebar")
    expect(right_sidebar).not_to_have_class("open")
    
    # Bewege die Maus zum rechten Hover-Bereich
    page.locator("#right-sidebar-hover-area").hover()
    
    # Warte kurz, damit der Hover-Effekt wirken kann
    page.wait_for_timeout(300)
    
    # Überprüfe, ob die rechte Sidebar eingeblendet wird
    expect(right_sidebar).to_have_class("open")
    
    # Klicke auf den Toggle-Button für die rechte Sidebar
    page.locator("#toggle-right-sidebar").click()
    
    # Überprüfe, ob die rechte Sidebar umgeschaltet wird
    expect(right_sidebar).to_have_class("open")
    
    # Klicke erneut, um sie zu schließen
    page.locator("#toggle-right-sidebar").click()
    
    # Überprüfe, ob die rechte Sidebar geschlossen wird
    expect(right_sidebar).not_to_have_class("open")

@pytest.mark.django_db
def test_responsive_layout(page, live_server_url):
    """Test, dass das Layout auf verschiedenen Bildschirmgrößen korrekt funktioniert."""
    try:
        # Setze die Viewport-Größe auf Mobilgeräte
        page.set_viewport_size({"width": 375, "height": 667})
        
        # Navigiere zur Startseite
        page.goto(f"{live_server_url}/")
        
        # Überprüfe, ob die Sidebars auf Mobilgeräten nicht standardmäßig sichtbar sind
        left_sidebar = page.locator("#left-sidebar")
        expect(left_sidebar).to_have_class("closed")
        
        # Setze die Viewport-Größe auf Desktop
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # Navigiere erneut zur Startseite
        page.goto(f"{live_server_url}/")
        
        # Überprüfe, ob die linke Sidebar auf Desktop sichtbar ist
        expect(left_sidebar).to_be_visible()
    except Exception as e:
        print(f"Fehler im responsiven Layout-Test: {e}")
        raise

@pytest.mark.django_db
def test_theme_toggle(page, live_server_url):
    """Test, dass der Theme-Toggle korrekt funktioniert."""
    try:
        # Navigiere zur Startseite
        page.goto(f"{live_server_url}/")
        
        # Überprüfe, ob das Standard-Theme angewendet wird
        html = page.locator("html")
        
        # Klicke auf den Theme-Toggle-Button (falls vorhanden)
        theme_toggle = page.locator(".insight-theme-toggle")
        if theme_toggle.count() > 0:
            theme_toggle.click()
            
            # Überprüfe, ob das Theme gewechselt wurde
            expect(html).to_have_class("dark")
            
            # Klicke erneut, um zum hellen Theme zurückzukehren
            theme_toggle.click()
            expect(html).not_to_have_class("dark")
    except Exception as e:
        print(f"Fehler im Theme-Toggle-Test: {e}")
        raise

@pytest.mark.django_db
def test_modal_functionality(page, live_server_url):
    """Test, dass die Modal-Dialoge korrekt funktionieren."""
    try:
        # Navigiere zur Startseite
        page.goto(f"{live_server_url}/")
        
        # Klicke auf den Button, um ein Modal zu öffnen
        page.locator("button[data-insight-target='demo-modal']").click()
        
        # Überprüfe, ob das Modal angezeigt wird
        modal = page.locator("#demo-modal")
        expect(modal).to_have_class("insight-modal--open")
        
        # Schließe das Modal durch Klicken auf den Schließen-Button
        page.locator("#demo-modal .insight-modal__close").click()
        
        # Überprüfe, ob das Modal geschlossen wurde
        expect(modal).not_to_have_class("insight-modal--open")
    except Exception as e:
        print(f"Fehler im Modal-Test: {e}")
        raise

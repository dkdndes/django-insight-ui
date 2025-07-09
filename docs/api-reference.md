# API-Referenz

Diese Seite dokumentiert die öffentliche API von Django Insight UI.

## Template-Tags

### insight_tags

```python
from insight_ui.templatetags import insight_tags
```

#### navbar

```python
@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(
    brand: str = "",
    links: Optional[List[Dict[str, Any]]] = None,
    theme: str = "light",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Navigationsleiste.

    Args:
        brand: Der Name oder Titel der Anwendung
        links: Eine Liste von Dictionaries mit Link-Informationen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen für die Navbar

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
```

#### alert

```python
@register.inclusion_tag("insight_ui/components/alert.html")
def alert(
    message: str,
    type: str = "info",
    dismissible: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Benachrichtigung.

    Args:
        message: Die Nachricht, die angezeigt werden soll
        type: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error')
        dismissible: Ob die Benachrichtigung schließbar sein soll
        **kwargs: Zusätzliche Optionen für die Benachrichtigung

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
```

## JavaScript-API

### InsightUI.Navbar

```javascript
InsightUI.Navbar.init()
```

Initialisiert alle Navbar-Komponenten auf der Seite.

### InsightUI.Alert

```javascript
InsightUI.Alert.init()
```

Initialisiert alle Alert-Komponenten auf der Seite.

```javascript
InsightUI.Alert.close(element)
```

Schließt eine Alert-Komponente.

- `element`: Das DOM-Element der Alert-Komponente

### InsightUI.ThemeToggle

```javascript
InsightUI.ThemeToggle.init()
```

Initialisiert alle Theme-Toggle-Komponenten auf der Seite.

## Einstellungen

### INSIGHT_UI

```python
INSIGHT_UI = {
    "theme": "light",  # 'light', 'dark', oder 'high-contrast'
    "branding": {
        "name": "Django Insight UI",
        "logo": None,
    },
    "features": {
        "theme_toggle": True,
        "language_selector": True,
    },
}
```

## CSS-Variablen

Django Insight UI verwendet CSS-Variablen für Theming und Anpassung. Hier sind die wichtigsten Variablen:

### Farben

```css
--insight-color-primary: #3b82f6;
--insight-color-primary-dark: #2563eb;
--insight-color-primary-light: #60a5fa;
--insight-color-secondary: #6b7280;
--insight-color-secondary-dark: #4b5563;
--insight-color-secondary-light: #9ca3af;
--insight-color-success: #10b981;
--insight-color-warning: #f59e0b;
--insight-color-error: #ef4444;
--insight-color-info: #3b82f6;
--insight-color-background: #ffffff;
--insight-color-background-alt: #f3f4f6;
--insight-color-surface: #ffffff;
--insight-color-text: #1f2937;
--insight-color-text-light: #6b7280;
--insight-color-text-inverted: #ffffff;
```

### Typografie

```css
--insight-font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--insight-font-size-xs: 0.75rem;
--insight-font-size-sm: 0.875rem;
--insight-font-size-md: 1rem;
--insight-font-size-lg: 1.125rem;
--insight-font-size-xl: 1.25rem;
```

### Abstände

```css
--insight-spacing-xs: 0.25rem;
--insight-spacing-sm: 0.5rem;
--insight-spacing-md: 1rem;
--insight-spacing-lg: 1.5rem;
--insight-spacing-xl: 2rem;
```

### Rahmen und Schatten

```css
--insight-border-radius-sm: 0.25rem;
--insight-border-radius-md: 0.375rem;
--insight-border-radius-lg: 0.5rem;
--insight-border-width: 1px;
--insight-border-color: #e5e7eb;
--insight-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--insight-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--insight-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
```

### Fokus und Übergänge

```css
--insight-focus-ring-color: rgba(59, 130, 246, 0.5);
--insight-focus-ring-width: 3px;
--insight-transition-fast: 150ms;
--insight-transition-normal: 300ms;
--insight-transition-slow: 500ms;
```

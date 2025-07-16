# Anpassung

Django Insight UI bietet verschiedene Möglichkeiten zur Anpassung, von einfachen Konfigurationsoptionen bis hin zu tiefgreifenden Anpassungen.

## Konfiguration über settings.py

Die einfachste Methode zur Anpassung ist die Konfiguration über die INSIGHT_UI-Einstellung in Ihrer settings.py:

```python
INSIGHT_UI = {
    # Allgemeine Einstellungen
    "theme": "light",  # 'light', 'dark', oder 'high-contrast'

    # Branding
    "branding": {
        "name": "Meine App",
        "logo": "path/to/logo.svg",
        "favicon": "path/to/favicon.ico",
    },

    # Funktionen
    "features": {
        "theme_toggle": True,
        "language_selector": True,
        "skip_links": True,
    },

    # Komponenten-Überschreibungen
    "components": {
        "navbar": {
            "fixed": True,
            "container_class": "container-fluid",
        },
        "alert": {
            "auto_dismiss": 5000,  # Automatisches Ausblenden nach 5 Sekunden
        },
    },
}
```

## CSS-Anpassung

### CSS-Variablen überschreiben

Sie können die CSS-Variablen von Insight UI überschreiben, um das Aussehen anzupassen:

```css
:root {
  /* Primärfarbe ändern */
  --insight-color-primary: #ff5722;
  --insight-color-primary-dark: #e64a19;
  --insight-color-primary-light: #ff7e47;

  /* Schriftart ändern */
  --insight-font-family: 'Roboto', sans-serif;

  /* Abstände ändern */
  --insight-spacing-md: 1.25rem;
}
```

### Komponenten-Klassen überschreiben

Sie können auch die Komponenten-Klassen direkt überschreiben:

```css
/* Navbar-Hintergrund ändern */
.insight-navbar {
  background-color: #f8f9fa;
}

/* Alert-Rahmen ändern */
.insight-alert {
  border-width: 2px;
}
```

## Template-Überschreibungen

Sie können die Templates von Insight UI überschreiben, indem Sie eigene Versionen in Ihrem Projekt erstellen:

1. Erstellen Sie ein Verzeichnis `templates/insight_ui/components/` in Ihrer App
2. Kopieren Sie die Komponenten-Templates, die Sie überschreiben möchten, in dieses Verzeichnis
3. Passen Sie die Templates nach Ihren Wünschen an

Beispiel:

```
myapp/
  templates/
    insight_ui/
      components/
        navbar.html  # Überschreibt das Standard-Navbar-Template
```

## Eigene Komponenten erstellen

Sie können eigene Komponenten erstellen, die auf Insight UI aufbauen:

1. Erstellen Sie ein Template für Ihre Komponente
2. Erstellen Sie ein Template-Tag für Ihre Komponente
3. Verwenden Sie die CSS-Variablen und Klassen von Insight UI

Beispiel für ein Template-Tag:

```python
# myapp/templatetags/my_tags.py
from django import template

register = template.Library()

@register.inclusion_tag("myapp/components/card.html")
def card(title, content, footer=None):
    return {
        "title": title,
        "content": content,
        "footer": footer,
    }
```

Beispiel für ein Template:

```django
<!-- myapp/templates/myapp/components/card.html -->
<div class="insight-card">
    <div class="insight-card__header">
        <h3 class="insight-card__title">{{ title }}</h3>
    </div>
    <div class="insight-card__body">
        {{ content }}
    </div>
    {% if footer %}
    <div class="insight-card__footer">
        {{ footer }}
    </div>
    {% endif %}
</div>
```

## JavaScript-Erweiterungen

Sie können die JavaScript-Funktionalität von Insight UI erweitern:

```javascript
// Erweitern Sie den InsightUI-Namespace
InsightUI.MyComponent = {
  init: function() {
    // Initialisierungscode
  },

  doSomething: function() {
    // Funktionalität
  }
};

// Initialisieren Sie Ihre Komponente
document.addEventListener('DOMContentLoaded', function() {
  InsightUI.MyComponent.init();
});
```

# Django Insight UI

Willkommen zur Dokumentation von Django Insight UI, einem modernen, erweiterbaren und hochgradig zugänglichen UI-Framework für Django-Projekte.

## Überblick

Django Insight UI bietet eine umfassende Sammlung von UI-Komponenten und Hilfsmitteln, die speziell für die Entwicklung von barrierefreien Webanwendungen konzipiert sind. Das Paket legt besonderen Wert auf:

- **Barrierefreiheit**: Alle Komponenten entsprechen den WCAG 2.1 AA-Richtlinien
- **Moderne Technologien**: Integration mit HTMX, TailwindCSS und Alpine.js
- **Internationalisierung**: Mehrsprachige Unterstützung und RTL-Layout
- **Leistung**: Optimierte Komponenten für schnelle Ladezeiten
- **Sicherheit**: Best Practices für CSRF, XSS und mehr

## Installation

```bash
uv add django-insight-ui
```

## Schnellstart

1. Fügen Sie 'insight_ui' zu Ihren INSTALLED_APPS in settings.py hinzu:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

2. Laden Sie die Template-Tags in Ihren Templates:

```django
{% load insight_tags %}
```

3. Verwenden Sie die Komponenten in Ihren Templates:

```django
{% navbar brand="Meine App" %}

{% alert message="Willkommen bei Insight UI!" type="success" %}
```

## Konfiguration

Sie können das Verhalten und Aussehen von Insight UI über die INSIGHT_UI-Einstellung in Ihrer settings.py anpassen:

```python
INSIGHT_UI = {
    "theme": "light",  # 'light', 'dark', oder 'high-contrast'
    "branding": {
        "name": "Meine App",
        "logo": "path/to/logo.svg",
    },
    "features": {
        "theme_toggle": True,
        "language_selector": True,
    },
}
```

## Nächste Schritte

- [Komponenten](components/index.md): Entdecken Sie alle verfügbaren UI-Komponenten
- [Template-Tags](template-tags.md): Lernen Sie die Template-Tags kennen
- [Anpassung](customization.md): Erfahren Sie, wie Sie das Aussehen anpassen können
- [Barrierefreiheit](accessibility.md): Verstehen Sie die Barrierefreiheitsfunktionen

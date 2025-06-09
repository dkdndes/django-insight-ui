# Django Insight UI

Ein modernes, erweiterbares und hochgradig zugängliches Django UI-Framework, das wiederverwendbare, WCAG 2.1 AA-konforme Komponenten und Entwicklungs-Best-Practices bietet.

## Überblick

Django Insight UI ist ein umfassendes UI-Paket für Django-Projekte mit Fokus auf:

- **Barrierefreiheit**: WCAG 2.1 AA-Konformität für alle Komponenten
- **Moderne Technologien**: Integration mit HTMX, TailwindCSS und Alpine.js
- **Internationalisierung**: Mehrsprachige Unterstützung und RTL-Layout
- **Leistung**: Optimierte Komponenten für schnelle Ladezeiten
- **Sicherheit**: Best Practices für CSRF, XSS und mehr

## Hauptfunktionen

- Responsive UI-Komponenten (Navbar, Sidebar, Tabellen, Formulare, etc.)
- Template-Tags für alle UI-Elemente
- Dunkler/Heller/Kontrastreicher Modus
- Vollständige Tastaturnavigation
- ARIA-Rollen und semantisches Markup
- Internationalisierung und RTL-Unterstützung
- HTMX-Integration für dynamische Updates

## Installation

```bash
uv add django-insight-ui
```

## Schnellstart

Fügen Sie 'insight_ui' zu Ihren INSTALLED_APPS in settings.py hinzu:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

## Dokumentation

Ausführliche Dokumentation finden Sie unter [docs/](docs/).

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

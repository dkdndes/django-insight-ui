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

## Entwicklung

```bash
uv sync --all-groups

python manage.py migrate
python manage.py runserver
```

### Websocket

Um das Beispiel der Websocket Kommunikation zu verwenden muss ein weiterer Prozess gestartet werden. Dieser befindet sich in dem Verzeichnis _/utils_.

```bash
uv run ./utils/main.py
```

In dem Verzeichnis _/utils_ gibt es eine extra Readme mit weiteren Informationen.

### Styling

Für das Styling der Frontend Komponenten kann bzw. sollte TailwindCSS verwendet werden. Dazu muss **npm** bzw. **node.js** installiert sein. Der Tailwind-Compiler muss in einem separaten Konsolenfenster ausgeführt werden, um neue CSS-Klassen dynamisch hinzuzufügen. Der Compiler läuft am besten während der Entwicklung in einer separaten Kommandozeile.

```bash
npx tailwindcss@3 -i ./src/input.css -o ./insight_ui/static/insight_ui/css/tailwind.css --watch
```

## Installation (in externes Projekt)

```bash
uv add django-insight-ui
```

Fügen Sie 'insight_ui' zu Ihren INSTALLED_APPS in settings.py hinzu:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

## Komponenten

### Implementiert

- Navigation (Navbar)
- Alerts (Notifications)
- Breadcrumbs
- Dialoge (Modals)
- HTML-Formular
- HTMX-Formular (ohne Seiten-Reload)
- Live-Update (Polling mit HTMX)
- WebSockets
- Tabellen/Listen-Ansicht (umschaltbar)
- Karten/Kachel-Ansicht (umschaltbar)
- Infinite Scroll
- Sidebar (Rechts)
- Footer

### Geplant

- Mehr Input-Elemente (Buttons, Dropdown-Menüs, Radio-Buttons, Radio-Groups)
- Mehr Varianten für Karten/Kacheln
- SQL like Filterung (Dynamische Filterung)
- Standard Listen-Filterung (Dropdowns mit festen Werten)
- Suchleiste (auch für die Navbar)
- Layout: Text + Tags
- KI-Chat
- Anbindung einer Charts Library (bspw. Apache Echarts)
- Karussell (für Karten Ansicht)
- Pagination (für Tabellen/Listen Ansicht)
- Sortierung
    - Einfach (nur eine Parameter)
    - Komplex (nach mehreren Parametern)
- Differentiator (GitHub like Diff-Ansicht)
- Geo-Karten Einbindung (leaflet)
- Tabellenspaltengröße vom Nutzer anpassbar

## Dokumentation

Ausführliche Dokumentation finden Sie unter [docs/](docs/).

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

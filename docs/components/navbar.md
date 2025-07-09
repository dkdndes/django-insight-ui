# Navbar-Komponente

Die Navbar-Komponente bietet eine vollständig responsive, barrierefreie Navigationsleiste für Ihre Django-Anwendung.

## Funktionen

- Responsive Design mit Mobile-First-Ansatz
- Unterstützung für Markenlogo und -text
- Navigationslinks mit aktiven Zuständen
- Optionale Aktionen wie Sprachumschalter und Themenwechsler
- Vollständige Tastaturnavigation
- ARIA-Attribute für Screenreader

## Verwendung

```django
{% load insight_tags %}

{% navbar 
   brand="Meine App" 
   links=nav_links 
   theme="light"
   show_theme_toggle=True
   show_language_selector=True
%}
```

## Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `brand` | `str` | `""` | Der Name oder Titel der Anwendung |
| `links` | `List[Dict]` | `[]` | Eine Liste von Dictionaries mit Link-Informationen |
| `theme` | `str` | `"light"` | Das Farbschema (`"light"`, `"dark"`, `"high-contrast"`) |
| `show_theme_toggle` | `bool` | `False` | Ob der Themenwechsler angezeigt werden soll |
| `show_language_selector` | `bool` | `False` | Ob der Sprachumschalter angezeigt werden soll |
| `brand_url` | `str` | `"#"` | Die URL, zu der der Markenname/das Logo verlinkt |
| `brand_logo` | `str` | `None` | Der Pfad zum Markenlogo |
| `id` | `str` | `None` | Eine optionale ID für das Navbar-Element |

## Link-Format

Die `links`-Parameter erwartet eine Liste von Dictionaries mit folgenden Schlüsseln:

```python
links = [
    {
        "url": "/",             # URL des Links
        "text": "Home",         # Anzeigetext
        "active": True,         # Ob der Link aktiv ist
        "icon": "<svg>...</svg>", # Optionales Icon (HTML/SVG)
        "external": False,      # Ob der Link extern ist
    },
    # Weitere Links...
]
```

## Beispiele

### Einfache Navbar

```django
{% navbar brand="Meine App" %}
```

### Navbar mit Links

```django
{% load insight_tags %}

{% navbar 
   brand="Meine App" 
   links=nav_links 
%}
```

In Ihrer View:

```python
def my_view(request):
    nav_links = [
        {"url": "/", "text": "Home", "active": True},
        {"url": "/about/", "text": "Über uns"},
        {"url": "/contact/", "text": "Kontakt"},
    ]
    return render(request, "my_template.html", {"nav_links": nav_links})
```

### Navbar mit Themenwechsler

```django
{% navbar 
   brand="Meine App" 
   links=nav_links 
   show_theme_toggle=True 
%}
```

## Barrierefreiheit

Die Navbar-Komponente enthält:

- Einen Skip-Link zum Hauptinhalt
- ARIA-Attribute für Screenreader
- Vollständige Tastaturunterstützung
- Semantisches HTML

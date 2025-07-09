# Schnellstart

Diese Anleitung hilft Ihnen, schnell mit Django Insight UI zu beginnen.

## Grundlegende Einrichtung

Nachdem Sie [Django Insight UI installiert](installation.md) haben, können Sie die Komponenten in Ihren Templates verwenden.

## Template-Tags laden

Laden Sie die Template-Tags in Ihren Templates:

```django
{% load insight_tags %}
```

## Komponenten verwenden

### Navbar

```django
{% navbar brand="Meine App" %}
```

Mit Links:

```django
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

### Alert

```django
{% alert message="Willkommen bei Insight UI!" type="success" %}
```

## Vollständiges Beispiel

Hier ist ein vollständiges Beispiel für ein Template:

```django
{% load insight_tags %}
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meine Django-App</title>
    <link rel="stylesheet" href="{% static 'insight_ui/css/insight-ui.css' %}">
</head>
<body>
    {% navbar brand="Meine App" links=nav_links %}
    
    <main id="main-content">
        <div class="container">
            {% alert message="Willkommen bei Insight UI!" type="success" %}
            
            <h1>Willkommen bei meiner App</h1>
            <p>Dies ist ein Beispiel für die Verwendung von Django Insight UI.</p>
        </div>
    </main>
    
    <script src="{% static 'insight_ui/js/insight-ui.js' %}"></script>
</body>
</html>
```

## Anpassung

Sie können das Aussehen und Verhalten von Insight UI über die INSIGHT_UI-Einstellung in Ihrer settings.py anpassen:

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

- Erkunden Sie die [verfügbaren Komponenten](components/index.md)
- Erfahren Sie mehr über [Barrierefreiheit](accessibility.md)
- Lernen Sie, wie Sie [Insight UI anpassen](customization.md) können

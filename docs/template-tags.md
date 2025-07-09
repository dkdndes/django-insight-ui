# Template-Tags

Django Insight UI bietet eine Reihe von Template-Tags, die Sie in Ihren Django-Templates verwenden können, um UI-Komponenten zu rendern.

## Verwendung

Um die Template-Tags zu verwenden, müssen Sie sie zuerst in Ihrem Template laden:

```django
{% load insight_tags %}
```

## Verfügbare Template-Tags

### navbar

Rendert eine barrierefreie Navigationsleiste.

```django
{% navbar 
   brand="Meine App" 
   links=nav_links 
   theme="light"
   show_theme_toggle=True
%}
```

Parameter:
- `brand`: Der Name oder Titel der Anwendung
- `links`: Eine Liste von Dictionaries mit Link-Informationen
- `theme`: Das Farbschema ('light', 'dark', 'high-contrast')
- `show_theme_toggle`: Ob der Themenwechsler angezeigt werden soll
- `show_language_selector`: Ob der Sprachumschalter angezeigt werden soll
- `brand_url`: Die URL, zu der der Markenname/das Logo verlinkt
- `brand_logo`: Der Pfad zum Markenlogo
- `id`: Eine optionale ID für das Navbar-Element

Weitere Informationen finden Sie in der [Navbar-Dokumentation](components/navbar.md).

### alert

Rendert eine barrierefreie Benachrichtigung.

```django
{% alert 
   message="Ihre Änderungen wurden gespeichert." 
   type="success" 
   dismissible=True 
%}
```

Parameter:
- `message`: Die Hauptnachricht der Benachrichtigung
- `type`: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error')
- `dismissible`: Ob die Benachrichtigung schließbar sein soll
- `details`: Zusätzliche Details zur Hauptnachricht
- `id`: Eine optionale ID für das Alert-Element

Weitere Informationen finden Sie in der [Alert-Dokumentation](components/alert.md).

## Eigene Template-Tags erstellen

Sie können eigene Template-Tags erstellen, indem Sie die vorhandenen Template-Tags als Basis verwenden oder neue Template-Tags von Grund auf entwickeln.

Hier ist ein Beispiel für ein eigenes Template-Tag:

```python
# myapp/templatetags/my_tags.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag("myapp/components/my_component.html")
def my_component(title, content):
    return {
        "title": title,
        "content": content,
    }
```

Und das entsprechende Template:

```django
<!-- myapp/templates/myapp/components/my_component.html -->
<div class="my-component">
    <h2 class="my-component__title">{{ title }}</h2>
    <div class="my-component__content">{{ content }}</div>
</div>
```

Verwendung:

```django
{% load my_tags %}

{% my_component title="Mein Titel" content="Mein Inhalt" %}
```

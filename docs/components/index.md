# UI-Komponenten

Django Insight UI bietet eine Reihe von barrierefreien, responsiven UI-Komponenten, die Sie in Ihren Django-Projekten verwenden können.

## Verfügbare Komponenten

- [Navbar](navbar.md): Eine responsive Navigationsleiste mit Unterstützung für Markenlogo, Links und Aktionen
- [Alert](alert.md): Benachrichtigungen und Warnmeldungen in verschiedenen Stilen

Jede Komponente ist:

- **Barrierefrei**: Entspricht den WCAG 2.1 AA-Richtlinien
- **Responsiv**: Funktioniert auf allen Bildschirmgrößen
- **Themenfähig**: Unterstützt helles, dunkles und kontrastarmes Farbschema
- **Anpassbar**: Kann über Template-Tags und CSS-Variablen angepasst werden

## Verwendung

Alle Komponenten können über Template-Tags verwendet werden:

```django
{% load insight_tags %}

{% navbar brand="Meine App" %}

{% alert message="Operation erfolgreich!" type="success" %}
```

## Eigene Komponenten erstellen

Sie können eigene Komponenten erstellen, indem Sie die vorhandenen Komponenten als Basis verwenden oder neue Komponenten von Grund auf entwickeln. Weitere Informationen finden Sie im Abschnitt [Anpassung](../customization.md).

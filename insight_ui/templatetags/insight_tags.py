"""Template-Tags für Insight UI-Komponenten."""

from typing import Any, Dict, List, Optional

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


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
    if links is None:
        links = []

    return {
        "brand": brand,
        "links": links,
        "theme": theme,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/language_selector.html")
def language_selector(
    current_language: str = "",
    available_languages: Optional[List[Dict[str, str]]] = None,
    theme: str = "light",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert einen barrierefreien Sprachauswähler.

    Args:
        current_language: Der aktuelle Sprachcode
        available_languages: Eine Liste verfügbarer Sprachen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if available_languages is None:
        available_languages = [
            {"code": "de", "name": "Deutsch", "native": "Deutsch"},
            {"code": "en", "name": "English", "native": "English"},
            {"code": "es", "name": "Spanish", "native": "Español"},
            {"code": "fr", "name": "French", "native": "Français"},
            {"code": "ar", "name": "Arabic", "native": "العربية"},
            {"code": "zh", "name": "Chinese", "native": "中文"},
        ]

    return {
        "current_language": current_language,
        "available_languages": available_languages,
        "theme": theme,
        "options": kwargs,
    }


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
    return {
        "message": message,
        "type": type,
        "dismissible": dismissible,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    title: str = "",
    items: Optional[List[Dict[str, Any]]] = None,
    theme: str = "light",
    collapsible: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Seitennavigation.

    Args:
        title: Der Titel der Sidebar
        items: Eine Liste von Dictionaries mit Navigation-Elementen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        collapsible: Ob die Sidebar einklappbar sein soll
        **kwargs: Zusätzliche Optionen für die Sidebar

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if items is None:
        items = []

    return {
        "title": title,
        "items": items,
        "theme": theme,
        "collapsible": collapsible,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(
    items: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Breadcrumb-Navigation.

    Args:
        items: Eine Liste von Dictionaries mit Breadcrumb-Elementen
        **kwargs: Zusätzliche Optionen für die Breadcrumbs

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if items is None:
        items = []

    return {
        "items": items,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/table.html")
def table(
    headers: Optional[List[str]] = None,
    rows: Optional[List[List[Any]]] = None,
    caption: str = "",
    theme: str = "light",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Tabelle.

    Args:
        headers: Eine Liste von Spaltenüberschriften
        rows: Eine Liste von Listen mit Zellendaten
        caption: Eine Beschreibung der Tabelle
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen für die Tabelle

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if headers is None:
        headers = []
    if rows is None:
        rows = []

    return {
        "headers": headers,
        "rows": rows,
        "caption": caption,
        "theme": theme,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(
    id: str,
    title: str,
    content: str = "",
    description: str = "",
    theme: str = "light",
    actions: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert ein barrierefreies Modal-Dialog.

    Args:
        id: Die eindeutige ID des Modals
        title: Der Titel des Modals
        content: Der Inhalt des Modals
        description: Eine optionale Beschreibung
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        actions: Eine Liste von Aktions-Buttons
        **kwargs: Zusätzliche Optionen für das Modal

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if actions is None:
        actions = []

    return {
        "id": id,
        "title": title,
        "content": content,
        "description": description,
        "theme": theme,
        "actions": actions,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/card.html")
def card(
    title: str = "",
    subtitle: str = "",
    content: str = "",
    theme: str = "light",
    image: Optional[Dict[str, str]] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert eine barrierefreie Karte.

    Args:
        title: Der Titel der Karte
        subtitle: Ein optionaler Untertitel
        content: Der Inhalt der Karte
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        image: Ein Dictionary mit Bild-Informationen (url, alt)
        actions: Eine Liste von Aktions-Links
        **kwargs: Zusätzliche Optionen für die Karte

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if actions is None:
        actions = []

    return {
        "title": title,
        "subtitle": subtitle,
        "content": content,
        "theme": theme,
        "image": image,
        "actions": actions,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/form.html")
def form(
    fields: Optional[List[Dict[str, Any]]] = None,
    title: str = "",
    description: str = "",
    action: str = "",
    method: str = "post",
    theme: str = "light",
    actions: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Rendert ein barrierefreies Formular.

    Args:
        fields: Eine Liste von Formularfeldern
        title: Der Titel des Formulars
        description: Eine optionale Beschreibung
        action: Die URL für die Formular-Übermittlung
        method: Die HTTP-Methode ('post', 'get')
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        actions: Eine Liste von Aktions-Buttons
        **kwargs: Zusätzliche Optionen für das Formular

    Returns:
        Dict mit Kontext-Variablen für das Template
    """
    if fields is None:
        fields = []
    if actions is None:
        actions = []

    return {
        "fields": fields,
        "title": title,
        "description": description,
        "action": action,
        "method": method,
        "theme": theme,
        "actions": actions,
        "options": kwargs,
    }

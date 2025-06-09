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

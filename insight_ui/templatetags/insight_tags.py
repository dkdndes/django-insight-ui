"""Template-Tags für Insight UI-Komponenten."""

from typing import Any

from django import template

register = template.Library()


@register.inclusion_tag("insight_ui/components/navbar.html")
def navbar(
    brand: str = "",
    links: list[dict[str, Any]] = [],
    theme: str = "light",
    show_language_selector: bool = True,
    **kwargs,
) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Navigationsleiste.

    Args:
    ----
        brand: Der Name oder Titel der Anwendung
        links: Eine Liste von Dictionaries mit Link-Informationen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        show_language_selector: 'True' wenn ein Menü zum wechseln der Sprache angezeigt werden soll
        **kwargs: Zusätzliche Optionen für die Navbar

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "brand": brand,
        "links": links,
        "theme": theme,
        "options": {**kwargs, "show_language_selector": show_language_selector},
    }


@register.inclusion_tag("insight_ui/components/live_content.html")
def live_content(
    url: str = "", theme: str = "light", interval: int = 0, initial_content: str = "", **kwargs
) -> dict[str, Any]:
    """
    Rendert einen Container für Live-Updates via HTMX.

    Args:
    ----
        url: Die URL für HTMX-Updates
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        interval: Intervall für automatische Updates in Millisekunden
        initial_content: Initialer Inhalt
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    htmx_config = {}

    if url:
        htmx_config = {
            "url": url,
            "trigger": kwargs.get("trigger", f"load, every {interval}s"),
            "swap": kwargs.get("swap", "innerHTML"),
        }
        if interval != 0:
            htmx_config["interval"] = interval

    return {
        "theme": theme,
        "initial_content": initial_content,
        "options": {**kwargs, "htmx": htmx_config if htmx_config else None},
    }


@register.inclusion_tag("insight_ui/components/websocket.html")
def insight_websocket(
    html_tag_id: str = "insight-websocket", ws_url: str = "", initial_content: str = "", **kwargs
) -> dict[str, Any]:
    """
    Rendert eine WebSocket-Komponente als Wrapper für die htmx v2 ws-Extension.

    Args:
    ----
        html_tag_id: Die ID des WebSocket-Containers
        ws_url: Die WebSocket-URL (z.B. ws://localhost:8765)
        initial_content: Initialer Inhalt
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"options": {"id": html_tag_id, "ws_url": ws_url, "initial_content": initial_content, **kwargs}}


@register.inclusion_tag("insight_ui/components/infinite_scroll.html")
def infinite_scroll(
    items: list[Any] = [], next_url: str = "", has_next: bool = True, threshold: int = 100, **kwargs
) -> dict[str, Any]:
    """
    Rendert einen Container für Infinite Scroll.

    Args:
    ----
        items: Liste der aktuellen Elemente
        next_url: URL für das Laden weiterer Elemente
        has_next: Ob weitere Elemente verfügbar sind
        threshold: Pixel-Schwellenwert für das Laden
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"items": items, "next_url": next_url, "has_next": has_next, "threshold": threshold, "options": kwargs}


@register.inclusion_tag("insight_ui/components/toggle_language.html")
def language_selector(
    current_language: str = "", available_languages: list[dict[str, str]] = [], theme: str = "light", **kwargs
) -> dict[str, Any]:
    """
    Rendert einen barrierefreien Sprachauswähler.

    Args:
    ----
        current_language: Der aktuelle Sprachcode
        available_languages: Eine Liste verfügbarer Sprachen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    if not available_languages:
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
def alert(message: str, alert_type: str = "info", dismissible: bool = True, **kwargs) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Benachrichtigung.

    Args:
    ----
        message: Die Nachricht, die angezeigt werden soll
        alert_type: Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error')
        dismissible: Ob die Benachrichtigung schließbar sein soll
        **kwargs: Zusätzliche Optionen für die Benachrichtigung

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"message": message, "type": alert_type, "dismissible": dismissible, "options": kwargs}


@register.inclusion_tag("insight_ui/components/sidebar.html")
def sidebar(
    title: str = "", items: list[dict[str, Any]] = [], theme: str = "light", collapsible: bool = False, **kwargs
) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Seitennavigation.

    Args:
    ----
        title: Der Titel der Sidebar
        items: Eine Liste von Dictionaries mit Navigation-Elementen
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        collapsible: Ob die Sidebar einklappbar sein soll
        **kwargs: Zusätzliche Optionen für die Sidebar

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"title": title, "items": items, "theme": theme, "collapsible": collapsible, "options": kwargs}


@register.inclusion_tag("insight_ui/components/breadcrumbs.html")
def breadcrumbs(items: list[dict[str, Any]] = [], **kwargs) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Breadcrumb-Navigation.

    Args:
    ----
        items: Eine Liste von Dictionaries mit Breadcrumb-Elementen
        **kwargs: Zusätzliche Optionen für die Breadcrumbs

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"items": items, "options": kwargs}


@register.inclusion_tag("insight_ui/components/table.html")
def table(
    headers: list[str] = [], rows: list[list[Any]] = [], caption: str = "", theme: str = "light", **kwargs
) -> dict[str, Any]:
    """
    Rendert eine barrierefreie Tabelle.

    Args:
    ----
        headers: Eine Liste von Spaltenüberschriften
        rows: Eine Liste von Listen mit Zellendaten
        caption: Eine Beschreibung der Tabelle
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen für die Tabelle

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"headers": headers, "rows": rows, "caption": caption, "theme": theme, "options": kwargs}


@register.inclusion_tag("insight_ui/components/modal.html")
def modal(  # noqa: PLR0913 (too many args)
    html_tag_id: str,
    title: str,
    content: str = "",
    description: str = "",
    theme: str = "light",
    actions: list[dict[str, Any]] = [],
    **kwargs,
) -> dict[str, Any]:
    """
    Rendert ein barrierefreies Modal-Dialog.

    Args:
    ----
        html_tag_id: Die eindeutige ID des Modals
        title: Der Titel des Modals
        content: Der Inhalt des Modals
        description: Eine optionale Beschreibung
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        actions: Eine Liste von Aktions-Buttons
        **kwargs: Zusätzliche Optionen für das Modal

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "id": html_tag_id,
        "title": title,
        "content": content,
        "description": description,
        "theme": theme,
        "actions": actions,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/carousel.html")
def carousel(  # noqa: PLR0913 (too many args)
    carousel_items: list = [],
    autoplay: bool = False,
    show_dots: bool = True,
    show_index: bool = False,
    slides_count: range = [],
    items_per_slide: int = 1,
    **kwargs,
) -> dict[str, Any]:
    """
    Rendert ein Karussell.

    Args:
    ----
        carousel_items: Darzustellender Inhalt (Karten)
        autoplay: Wechsle automatisch nach einer bestimmten Zeit (5s) zur nächsten Seite
        show_dots: Zeige Pagination Dots unter dem Inhalt
        show_index: Zeige Anzahl und aktuelle Seite in der unteren rechten Ecke
        slides_count: Anzahl der Seiten als Iterable
        items_per_slide: Anzahl der Items pro Seite
        **kwargs: Zusätzliche Optionen für die Karte

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "carousel_items": carousel_items,
        "autoplay": autoplay,
        "show_dots": show_dots,
        "show_index": show_index,
        "slides_count": slides_count,
        "items_per_slide": items_per_slide,
        "options": kwargs,
    }


@register.inclusion_tag("insight_ui/components/cards/card.html")
def card(card: dict) -> dict[str, Any]:
    """
    Rendert eine Karte.

    Folgende Informationen müssen in dem Dictionary enthalten sein:
        - title (str)
        - subtitle (str) (Optional)
        - content (str)
        - image (dict[url: str, alt: str]) (Optional)
        - actions (list[dict[text: str, url: str, type: str]]) (Optional)

    Args:
    ----
        card: Ein dictionary mit allen Informationen über die Karte, wie Titel, Content, etc..

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "title": card.get("title"),
        "subtitle": card.get("subtitle"),
        "content": card.get("content"),
        "image": card.get("image"),
        "actions": card.get("actions"),
        "options": card.get("kwargs"),
    }


@register.inclusion_tag("insight_ui/components/cards/horizontale_card.html")
def card_horizontale(card: dict) -> dict[str, Any]:
    """
    Rendert eine horizontal ausgerichtete Karte.

    Mit einem Bild am oberen Rand. Darunter befindet sich der Titel und der Content, sowie wenn angegeben,
    eine Liste von Tags. Am Ende werden die angegebenen Action Buttons übereinander dargestellt.

    Folgende Informationen müssen in dem Dictionary enthalten sein:
        - title (str)
        - content (str)
        - tags (list[str]) (Optional)
        - url (str) (Optional)
        - image (dict[url: str, alt: str]) (Optional)
        - actions (list[dict[text: str, url: str, type: str]]) (Optional)

    Args:
    ----
        card: Ein dictionary mit allen Informationen über die Karte, wie Titel, Content, etc..

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {
        "title": card.get("title"),
        "content": card.get("content"),
        "tags": card.get("tags"),
        "url": card.get("url"),
        "image": card.get("image"),
        "actions": card.get("actions"),
        "options": card.get("kwargs"),
    }


@register.inclusion_tag("insight_ui/components/form.html")
def form(  # noqa: PLR0913 (too many args)
    fields: list[dict[str, Any]] = [],
    title: str = "",
    description: str = "",
    action: str = "",
    method: str = "post",
    theme: str = "light",
    actions: list[dict[str, Any]] = [],
    htmx: dict[str, Any] = {},
    **kwargs,
) -> dict[str, Any]:
    """
    Rendert ein barrierefreies Formular mit HTMX-Unterstützung.

    Args:
    ----
        fields: Eine Liste von Formularfeldern
        title: Der Titel des Formulars
        description: Eine optionale Beschreibung
        action: Die URL für die Formular-Übermittlung
        method: Die HTTP-Methode ('post', 'get')
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        actions: Eine Liste von Aktions-Buttons
        htmx: HTMX Konfiguration für AJAX-Requests
        **kwargs: Zusätzliche Optionen für das Formular

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    # HTMX-Konfiguration
    htmx_config = None
    if htmx:
        htmx_config = {
            "url": htmx.get("url"),
            "method": htmx.get("method"),
            "target": htmx.get("target"),
            "swap": htmx.get("swap"),
            "trigger": htmx.get("trigger"),
            "confirm": htmx.get("confirm"),
            "boost": htmx.get("boost"),
            "validate": kwargs.get("htmx_validate", True),
            "indicator": kwargs.get("htmx_indicator", ".htmx-indicator"),
        }

    return {
        "fields": fields,
        "title": title,
        "description": description,
        "action": action,
        "method": method,
        "theme": theme,
        "actions": actions,
        "htmx": htmx_config,
        "options": {**kwargs},
    }


@register.inclusion_tag("insight_ui/components/footer.html")
def footer(theme: str = "light", **kwargs) -> dict[str, Any]:
    """
    Rendert einen barrierefreien Footer.

    Args:
    ----
        theme: Das Farbschema ('light', 'dark', 'high-contrast')
        **kwargs: Zusätzliche Optionen für den Footer

    Returns:
    -------
        Dict mit Kontext-Variablen für das Template

    """
    return {"theme": theme, "options": kwargs}

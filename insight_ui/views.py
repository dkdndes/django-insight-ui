import asyncio
import time
from datetime import datetime
from typing import Any

import structlog
from asgiref.sync import sync_to_async
from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods

logger = structlog.get_logger(__name__)


def get_storybook_context() -> dict:
    """Hilfsfunktion für Index-Seiten Context."""
    page_obj, surrounding_pages = get_page()

    return {
        "nav_links": [
            {"text": _("Startseite"), "url": "/", "active": True},
            {"text": _("Storybook"), "url": "/components/", "active": False},
            {"text": _("Dokumentation"), "url": "/docs/", "active": False},
        ],
        "breadcrumb_items": [
            {"text": _("Startseite"), "url": "/"},
            {"text": _("Demo"), "url": "/demo/"},
            {"text": _("Komponenten"), "url": None, "active": True},
        ],
        "table_headers": [_("Name"), _("E-Mail"), _("Status"), _("Aktionen")],
        "table_rows": [
            [
                "Max Mustermann",
                "max@example.com",
                _("Aktiv"),
                mark_safe('<button class="btn btn-sm">Bearbeiten</button>'),
            ],
            [
                "Anna Schmidt",
                "anna@example.com",
                _("Inaktiv"),
                mark_safe('<button class="btn btn-sm">Bearbeiten</button>'),
            ],
            ["Tom Weber", "tom@example.com", _("Aktiv"), mark_safe('<button class="btn btn-sm">Bearbeiten</button>')],
        ],
        "card_actions": [
            {"text": _("Mehr erfahren"), "url": "#", "type": "primary"},
            {"text": _("Teilen"), "url": "#", "type": "secondary"},
        ],
        "form_fields": [
            {
                "type": "text",
                "name": "name",
                "label": _("Name"),
                "placeholder": _("Ihr vollständiger Name"),
                "required": True,
            },
            {
                "type": "email",
                "name": "email",
                "label": _("E-Mail"),
                "placeholder": _("ihre.email@example.com"),
                "required": True,
            },
            {
                "type": "textarea",
                "name": "message",
                "label": _("Nachricht"),
                "placeholder": _("Ihre Nachricht..."),
                "rows": 4,
            },
        ],
        "form_actions": [
            {"text": _("Absenden"), "type": "submit", "style": "primary"},
            {"text": _("Zurücksetzen"), "type": "reset", "style": "secondary"},
        ],
        "modal_actions": [
            {"text": _("Speichern"), "type": "primary"},
            {"text": _("Abbrechen"), "type": "cancel", "dismiss": True},
        ],
        "confirm_modal_actions": [
            {"text": _("Ja, fortfahren"), "type": "primary", "onclick": 'alert("Aktion bestätigt!")'},
            {"text": _("Abbrechen"), "type": "cancel", "dismiss": True},
        ],
        "right_sidebar_items": [
            {"text": _("Benachrichtigungen"), "icon": "🔔", "badge": "3"},
            {"text": _("Nachrichten"), "icon": "💬", "badge": "12"},
            {"text": _("Aufgaben"), "icon": "✅", "badge": "5"},
            {"text": _("Kalender"), "icon": "📅"},
            {"text": _("Einstellungen"), "icon": "⚙️"},
            {"text": _("Profil"), "icon": "👤"},
        ],
        "left_sidebar_items": [
            {"text": _("Dashboard"), "url": "/", "icon": "📊"},
            {"text": _("Benutzer"), "url": "/users/", "icon": "👥"},
            {"text": _("Einstellungen"), "url": "/settings/", "icon": "⚙️"},
            {"text": _("Hilfe"), "url": "/help/", "icon": "❓"},
        ],
        "scroll_items": [{"title": f"Element {i}", "content": f"Inhalt für Element {i}"} for i in range(1, 11)],
        "htmx_config": {"url": "/api/form-submit/", "method": "post", "target": "#htmx-form", "swap": "innerHTML"},
        "available_languages": [
            {"code": "de", "name": "Deutsch"},
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Español"},
            {"code": "fr", "name": "Français"},
            {"code": "ar", "name": "العربية"},
            {"code": "zh", "name": "中文"},
        ],
        "carousel_items": map_payload_to_cards(generate_random_payload()),
        "range_total_slides": range(3),
        "start_page": {"page_obj": page_obj, "surrounding_pages": surrounding_pages},
    }


def get_page(page: int = 1, max_neighbor_pages: int = 3) -> tuple[Page, list[str]]:
    items = generate_random_payload(100)
    paginator = Paginator(items, 10)

    max_neighbor_pages2 = max_neighbor_pages * 2

    # Berechnen der benachbarten Seiten
    surrounding_pages = []
    total_surrounding_pages = 6  # Immer insgesamt 6 benachbarte Seiten
    half = total_surrounding_pages // 2

    # Berechnung der Start- und Endseiten für die benachbarten Seiten
    start = max(1, page - half)
    end = min(paginator.num_pages, page + half)

    # Falls nicht genügend Seiten vor der aktuellen Seite sind, nach vorne ausgleichen
    if page - start < half:
        end = min(paginator.num_pages, end + (half - (page - start)))

    # Falls nicht genügend Seiten nach der aktuellen Seite sind, nach hinten ausgleichen
    if end - page < half:
        start = max(1, start - (half - (end - page)))

    # Füllen der Liste der benachbarten Seiten
    surrounding_pages = list(range(start, end + 1))

    page_links = []
    for i in range(1, paginator.num_pages + 1):
        if i in surrounding_pages:
            page_links.append(i)
        elif i == 1 or i == paginator.num_pages or (i in surrounding_pages and i not in page_links[-1:]):
            page_links.append("...")

    return paginator.get_page(page), page_links


def pagination(request: HttpRequest) -> HttpResponse:
    page_obj, surrounding_pages = get_page(int(request.GET.get("page")))

    if request.htmx:
        return render(
            request,
            "insight_ui/components/list_partial.html",
            {"pagination": {"page_obj": page_obj, "surrounding_pages": surrounding_pages}},
        )

    context = get_storybook_context()
    context["page_obj"] = {"page_obj": page_obj, "surrounding_pages": surrounding_pages}
    return render(request, "insight_ui/storybook.html", context)


@require_http_methods(["GET"])
def live_data_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX Endpoint für Live-Daten."""
    current_time = datetime.now().strftime("%H:%M:%S")
    data = {
        "time": current_time,
        "message": _("Daten aktualisiert um %(time)s") % {"time": current_time},
        "status": "success",
    }

    if request.headers.get("HX-Request"):
        # HTMX Request - nur den Inhalt zurückgeben
        html = render_to_string(
            "insight_ui/components/live_content_partial.html", {"data": data, "timestamp": current_time}
        )
        return HttpResponse(html)

    # Normale Request - JSON zurückgeben
    return JsonResponse(data)


@require_http_methods(["GET"])
def more_items_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX Endpoint für Infinite Scroll."""
    page = int(request.GET.get("page", 1))
    items_per_page = 5

    # Simuliere mehr Items
    start = (page - 1) * items_per_page + 11  # +11 weil wir schon 10 Items haben
    end = start + items_per_page

    new_items = [
        {"title": f"Element {i}", "content": f"Dynamisch geladener Inhalt für Element {i}"} for i in range(start, end)
    ]

    has_next = page < 5  # Simuliere max 5 Seiten
    next_url = f"/api/more-items/?page={page + 1}" if has_next else ""

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "insight_ui/components/infinite_scroll_items.html",
            {"items": new_items, "next_url": next_url, "has_next": has_next, "page": page + 1},
        )
        return HttpResponse(html)

    return JsonResponse({"items": new_items, "has_next": has_next, "next_url": next_url})


@require_http_methods(["POST"])
async def htmx_form_submit(request: HttpRequest) -> HttpResponse | JsonResponse:
    """HTMX Endpoint für Formular-Übermittlung mit asynchronem Logging."""
    if request.headers.get("HX-Request"):
        # Debug: Alle POST-Daten loggen
        content_type = request.content_type

        logger.info("Empfangene POST-Daten: %s", request.POST)
        logger.info("Content-Type: %s", content_type)

        # Eingabedaten extrahieren
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        logger.info("Extrahierte Werte - Name: '%s', Email: '%s', Message: '%s'", name, email, message)

        # Asynchrones Logging der Eingabedaten
        await log_form_input_async(name, email, message)

        # Einfache Validierung
        errors = {}
        if not name:
            errors["name"] = _("Name ist erforderlich")
        if not email:
            errors["email"] = _("E-Mail ist erforderlich")
        elif "@" not in email:
            errors["email"] = _("Ungültige E-Mail-Adresse")

        if errors:
            logger.warning("Formular-Validierungsfehler: %s", errors)
            # Fehler zurückgeben
            html = await sync_to_async(render_to_string)(
                "insight_ui/components/form_errors.html", {"errors": errors, "type": "error"}
            )
            return HttpResponse(html, status=400)

        # Erfolg simulieren mit asynchroner Verarbeitung
        await asyncio.sleep(1)  # Simuliere asynchrone Verarbeitungszeit

        logger.info("Formular erfolgreich verarbeitet")
        success_html = await sync_to_async(render_to_string)(
            "insight_ui/components/form_success.html",
            {"message": _("Formular erfolgreich übermittelt!"), "name": name, "email": email, "type": "success"},
        )
        # Erfolgreiche Antwort ohne Redirect - bleibt auf der Seite
        return HttpResponse(success_html)

    logger.warning("Nicht-HTMX Request an htmx_form_submit erhalten")
    return JsonResponse({"error": _("Nur HTMX-Requests erlaubt")}, status=400)


@require_http_methods(["POST"])
def normal_form_submit(request: HttpRequest) -> HttpResponse:
    """Normale Formular-Übermittlung mit synchronem Logging."""
    # Debug: Alle POST-Daten loggen
    logger.info("Empfangene POST-Daten: %s", dict(request.POST))
    logger.info("Content-Type: %s", request.content_type)

    # Eingabedaten extrahieren
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    logger.info("Extrahierte Werte - Name: '%s', Email: '%s', Message: '%s'", name, email, message)

    # Synchrones Logging der Eingabedaten
    log_form_input_sync(name, email, message)

    # Einfache Validierung
    errors = {}
    if not name:
        errors["name"] = _("Name ist erforderlich")
    if not email:
        errors["email"] = _("E-Mail ist erforderlich")
    elif "@" not in email:
        errors["email"] = _("Ungültige E-Mail-Adresse")

    if errors:
        logger.warning("Formular-Validierungsfehler: %s", errors)
        # Bei Fehlern die komplette Seite mit Fehlermeldungen rendern
        context = get_storybook_context()
        context["form_errors"] = errors
        context["form_data"] = {"name": name, "email": email, "message": message}
        return render(request, "insight_ui/storybook.html", context)

    # Erfolg simulieren mit synchroner Verarbeitung
    time.sleep(1)  # Simuliere synchrone Verarbeitungszeit

    logger.info("Normales Formular erfolgreich verarbeitet")

    # Bei erfolgreichem Submit die komplette Seite mit Erfolgsmeldung rendern
    context = get_storybook_context()
    context["form_success"] = {
        "message": _("Normales Formular erfolgreich übermittelt!"),
        "name": name,
        "email": email,
        "type": "success",
    }

    return render(request, "insight_ui/storybook.html", context)


def log_form_input_sync(name: str, email: str, message: str) -> None:
    """
    Synchrone Funktion zum Loggen der Formular-Eingaben.

    Args:
    ----
        name (str): Name des Benutzers
        email (str): E-Mail-Adresse des Benutzers
        message (str): Nachricht des Benutzers
        logger: Logger-Instanz

    """
    # Simuliere synchrone Verarbeitung
    time.sleep(0.1)

    # Detailliertes Logging der Eingabedaten
    separator = "=" * 30
    logger.info(separator)
    logger.info("NORMALES Kontaktformular - Neue Eingabe erhalten")
    logger.info(separator)
    logger.info("Name: %s", name)
    logger.info("E-Mail: %s", email)
    logger.info("Nachricht: %s", message)
    logger.info(separator)

    # Simuliere weitere synchrone Verarbeitung
    time.sleep(0.05)
    logger.debug("Synchrones Logging abgeschlossen")


async def log_form_input_async(name: str, email: str, message: str) -> None:
    """
    Asynchrone Funktion zum Loggen der Formular-Eingaben.

    Args:
    ----
        name (str): Name des Benutzers
        email (str): E-Mail-Adresse des Benutzers
        message (str): Nachricht des Benutzers
        logger: Logger-Instanz

    """
    # Simuliere asynchrone Verarbeitung
    await asyncio.sleep(0.1)

    # Detailliertes Logging der Eingabedaten
    separator = "=" * 30
    logger.info(separator)
    logger.info("HTMX Kontaktformular - Neue Eingabe erhalten")
    logger.info(separator)
    logger.info("Name: %s", name)
    logger.info("E-Mail: %s", email)
    logger.info("Nachricht: %s", message)
    logger.info(separator)

    # Simuliere weitere asynchrone Verarbeitung
    await asyncio.sleep(0.05)
    logger.debug("Asynchrones Logging abgeschlossen")


@require_http_methods(["GET"])
def component_demo_view(request: HttpRequest, component_name: str) -> HttpResponse | JsonResponse:
    """Einzelne Storybook-Demo für HTMX."""
    component_templates = {
        "alert": "insight_ui/components/alert.html",
        "card": "insight_ui/components/card.html",
        "modal": "insight_ui/components/modal.html",
        "table": "insight_ui/components/table.html",
        "form": "insight_ui/components/form.html",
        "sidebar": "insight_ui/components/sidebar.html",
        "breadcrumbs": "insight_ui/components/breadcrumbs.html",
        "navbar": "insight_ui/components/navbar.html",
    }

    if component_name not in component_templates:
        return JsonResponse({"error": _("Komponente nicht gefunden")}, status=404)

    # Beispieldaten für die jeweilige Komponente
    context = get_component_context(component_name)

    if request.headers.get("HX-Request"):
        html = render_to_string(component_templates[component_name], context)
        return HttpResponse(html)

    return render(
        request,
        "insight_ui/component_demo.html",
        {
            "component_name": component_name,
            "component_html": render_to_string(component_templates[component_name], context),
        },
    )


def get_component_context(component_name: str) -> Any:
    """Hilfsfunktion für Komponenten-Beispieldaten."""
    contexts = {
        "alert": {"message": _("Dies ist eine Beispiel-Benachrichtigung"), "type": "info", "dismissible": True},
        "card": {
            "title": _("Beispiel-Karte"),
            "subtitle": _("Untertitel"),
            "content": _("Dies ist der Inhalt einer Beispiel-Karte."),
            "actions": [
                {"text": _("Aktion 1"), "url": "#", "type": "primary"},
                {"text": _("Aktion 2"), "url": "#", "type": "secondary"},
            ],
        },
        "modal": {
            "id": "demo-modal",
            "title": _("Demo Modal"),
            "content": _("Dies ist ein Beispiel-Modal-Dialog."),
            "actions": [
                {"text": _("Speichern"), "type": "button", "style": "primary"},
                {"text": _("Abbrechen"), "type": "button", "style": "secondary"},
            ],
        },
        "table": {
            "headers": [_("Name"), _("E-Mail"), _("Status")],
            "rows": [
                ["Max Mustermann", "max@example.com", _("Aktiv")],
                ["Anna Schmidt", "anna@example.com", _("Inaktiv")],
            ],
            "caption": _("Beispiel-Tabelle"),
        },
        "form": {
            "title": _("Beispiel-Formular"),
            "fields": [
                {"type": "text", "name": "name", "label": _("Name"), "required": True},
                {"type": "email", "name": "email", "label": _("E-Mail"), "required": True},
            ],
            "actions": [{"text": _("Absenden"), "type": "submit", "style": "primary"}],
        },
        "sidebar": {
            "title": _("Navigation"),
            "items": [
                {"text": _("Dashboard"), "url": "/", "icon": "📊"},
                {"text": _("Einstellungen"), "url": "/settings/", "icon": "⚙️"},
            ],
        },
        "breadcrumbs": {
            "items": [{"text": _("Startseite"), "url": "/"}, {"text": _("Komponenten"), "url": None, "active": True}]
        },
        "navbar": {
            "brand": "Demo App",
            "links": [
                {"text": _("Startseite"), "url": "/", "active": True},
                {"text": _("Über uns"), "url": "/about/", "active": False},
            ],
        },
    }

    return contexts.get(component_name, {})


def storybook_view(request: HttpRequest) -> HttpResponse:
    """Hauptseite mit allen Insight UI Komponenten."""
    # Wenn es ein POST-Request ist, leite an normale Formular-Verarbeitung weiter
    if request.method == "POST":
        return normal_form_submit(request)

    # Beispieldaten für die Komponenten
    context = get_storybook_context()

    # Toggle-View: Initiale Tabellendaten für das Storybook bereitstellen
    payload = generate_random_payload()
    headers, rows = map_payload_to_table(payload)
    context["table_headers"] = headers
    context["table_rows"] = rows
    context["toggle_current_view"] = "table"

    return render(request, "insight_ui/storybook.html", context)


def generate_random_payload(count: int = 5) -> list:
    """Erstellt eine zufällige Anzahl von Einträgen als Payload-Daten."""
    entries = []
    for i in range(1, count + 1):
        entries.append(
            {
                "title": f"Element {i}",
                "subtitle": f"Untertitel {i}",
                "content": f"Dies ist der Inhalt von Eintrag {i}.",
                "actions": [
                    {"text": "Mehr erfahren", "url": "#", "type": "primary"},
                    {"text": "Teilen", "url": "#", "type": "secondary"},
                ],
                "name": f"Name {i}",
                "status": "Aktiv" if i % 2 == 0 else "Inaktiv",
                "action_link": f"<a href='#' class='underline text-insight-text-link hover:text-insight-text-link-hover'>Details {i}</a>",
            }
        )
    return entries


def map_payload_to_cards(payload: list) -> list:
    """Mappt Payload-Daten auf Karten-Darstellung."""
    elements = []
    for item in payload:
        elements.append(
            {
                "title": item["title"],
                "subtitle": item["subtitle"],
                "content": item["content"],
                "actions": item["actions"],
            }
        )
    return elements


def map_payload_to_table(payload: list) -> tuple[list[str], list]:
    """Mappt Payload-Daten auf Tabellen-Darstellung."""
    headers = ["Title", "Status", "Content", "URL"]
    rows = []
    for item in payload:
        content = item["content"]
        rows.append([item["title"], item["status"], content, item["action_link"]])
    return headers, rows


@require_GET
def toggle_view(request: HttpRequest) -> HttpResponse:
    """
    Toggle between table and card views, based on the `view` GET parameter.
    Loads and maps payload data to the appropriate format.
    """
    view = request.GET.get("view", "table")
    valid_views = {"table", "card", "carousel"}

    if view not in valid_views:
        logger.warning("log: toggle_view - Ungültiger 'view'-Parameter empfangen: %s. Fallback auf 'table'.", view)
        view = "table"

    # Generate the base payload
    payload = generate_random_payload()
    context = {"current_view": view}

    if view == "card":
        context["cards"] = map_payload_to_cards(payload)
        logger.info("log: toggle_view - Kartenansicht ausgewählt")
    elif view == "carousel":
        context["cards"] = map_payload_to_cards(payload)
        logger.info("log: toggle_view - Karussell-Ansicht ausgewählt")
    else:
        # default: table view
        headers, rows = map_payload_to_table(payload)
        context["table_headers"] = headers
        context["table_rows"] = rows
        logger.info("log: toggle_view - Tabellenansicht ausgewählt")

    return render(request, "insight_ui/components/toggle_view.html", context)

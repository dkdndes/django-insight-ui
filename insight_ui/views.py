import asyncio
import logging

logger = logging.getLogger(__name__)
import random
import time
from datetime import datetime
from typing import List

from asgiref.sync import sync_to_async
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods


def get_storybook_context():
    """Hilfsfunktion für Index-Seiten Context"""
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
            [
                "Tom Weber",
                "tom@example.com",
                _("Aktiv"),
                mark_safe('<button class="btn btn-sm">Bearbeiten</button>'),
            ],
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
            {
                "text": _("Ja, fortfahren"),
                "type": "primary",
                "onclick": 'alert("Aktion bestätigt!")',
            },
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
        "sidebar_items": [
            {"text": _("Dashboard"), "url": "/", "icon": "📊"},
            {"text": _("Benutzer"), "url": "/users/", "icon": "👥"},
            {"text": _("Einstellungen"), "url": "/settings/", "icon": "⚙️"},
            {"text": _("Hilfe"), "url": "/help/", "icon": "❓"},
        ],
        "scroll_items": [
            {"title": f"Element {i}", "content": f"Inhalt für Element {i}"}
            for i in range(1, 11)
        ],
        "htmx_form_fields": [
            {
                "type": "text",
                "name": "htmx_name",
                "label": _("Name (HTMX)"),
                "placeholder": _("Name eingeben"),
                "required": True,
            },
            {
                "type": "email",
                "name": "htmx_email",
                "label": _("E-Mail (HTMX)"),
                "placeholder": _("E-Mail eingeben"),
                "required": True,
            },
            {
                "type": "textarea",
                "name": "message",
                "label": _("Nachricht (HTMX)"),
                "placeholder": _("Ihre Nachricht..."),
                "rows": 4,
                "required": False,
            },
        ],
        "htmx_config": {
            "url": "/api/form-submit/",
            "method": "post",
            "target": "#form-result",
            "swap": "innerHTML",
        },
    }


@require_http_methods(["GET"])
def live_data_view(request):
    """HTMX Endpoint für Live-Daten"""
    current_time = datetime.now().strftime("%H:%M:%S")
    data = {
        "time": current_time,
        "message": _("Daten aktualisiert um %(time)s") % {"time": current_time},
        "status": "success",
    }

    if request.headers.get("HX-Request"):
        # HTMX Request - nur den Inhalt zurückgeben
        html = render_to_string(
            "insight_ui/components/live_content_partial.html",
            {"data": data, "timestamp": current_time},
        )
        return HttpResponse(html)

    # Normale Request - JSON zurückgeben
    return JsonResponse(data)


@require_http_methods(["GET"])
def more_items_view(request):
    """HTMX Endpoint für Infinite Scroll"""
    page = int(request.GET.get("page", 1))
    items_per_page = 5

    # Simuliere mehr Items
    start = (page - 1) * items_per_page + 11  # +11 weil wir schon 10 Items haben
    end = start + items_per_page

    new_items = [
        {
            "title": f"Element {i}",
            "content": f"Dynamisch geladener Inhalt für Element {i}",
        }
        for i in range(start, end)
    ]

    has_next = page < 5  # Simuliere max 5 Seiten
    next_url = f"/api/more-items/?page={page + 1}" if has_next else ""

    if request.headers.get("HX-Request"):
        html = render_to_string(
            "insight_ui/components/infinite_scroll_items.html",
            {
                "items": new_items,
                "next_url": next_url,
                "has_next": has_next,
                "page": page + 1,
            },
        )
        return HttpResponse(html)

    return JsonResponse(
        {"items": new_items, "has_next": has_next, "next_url": next_url}
    )


@require_http_methods(["POST"])
async def htmx_form_submit(request):
    """HTMX Endpoint für Formular-Übermittlung mit asynchronem Logging"""
    logger = logging.getLogger(__name__)

    if request.headers.get("HX-Request"):
        # Debug: Alle POST-Daten loggen
        post_data = await sync_to_async(lambda: dict(request.POST))()
        content_type = request.content_type

        print(f"[HTMX FORM] Empfangene POST-Daten: {request.POST}")
        print(f"[HTMX FORM] Content-Type: {content_type}")
        logger.info(f"Empfangene POST-Daten: {request.POST}")
        logger.info(f"Content-Type: {content_type}")

        # Eingabedaten extrahieren
        name = request.POST.get("htmx_name", "")
        email = request.POST.get("htmx_email", "")
        message = request.POST.get("message", "")

        print(
            f"[HTMX FORM] Extrahierte Werte - Name: '{name}', Email: '{email}', Message: '{message}'"
        )
        logger.info(
            f"Extrahierte Werte - Name: '{name}', Email: '{email}', Message: '{message}'"
        )

        # Asynchrones Logging der Eingabedaten
        await log_form_input_async(name, email, message, logger)

        # Einfache Validierung
        errors = {}
        if not name:
            errors["htmx_name"] = _("Name ist erforderlich")
        if not email:
            errors["htmx_email"] = _("E-Mail ist erforderlich")
        elif "@" not in email:
            errors["htmx_email"] = _("Ungültige E-Mail-Adresse")

        if errors:
            logger.warning(f"Formular-Validierungsfehler: {errors}")
            # Fehler zurückgeben
            html = await sync_to_async(render_to_string)(
                "insight_ui/components/form_errors.html",
                {"errors": errors, "type": "error"},
            )
            response = HttpResponse(html, status=400)
            return response

        # Erfolg simulieren mit asynchroner Verarbeitung
        await asyncio.sleep(1)  # Simuliere asynchrone Verarbeitungszeit

        print("[HTMX FORM] Formular erfolgreich verarbeitet")
        logger.info("Formular erfolgreich verarbeitet")
        success_html = await sync_to_async(render_to_string)(
            "insight_ui/components/form_success.html",
            {
                "message": _("Formular erfolgreich übermittelt!"),
                "name": name,
                "email": email,
                "type": "success",
            },
        )
        # Erfolgreiche Antwort ohne Redirect - bleibt auf der Seite
        response = HttpResponse(success_html)
        return response

    logger.warning("Nicht-HTMX Request an htmx_form_submit erhalten")
    response = JsonResponse({"error": _("Nur HTMX-Requests erlaubt")}, status=400)
    return response


@require_http_methods(["POST"])
def normal_form_submit(request):
    """Normale Formular-Übermittlung mit synchronem Logging"""
    logger = logging.getLogger(__name__)

    # Debug: Alle POST-Daten loggen
    print(f"[NORMAL FORM] Empfangene POST-Daten: {dict(request.POST)}")
    print(f"[NORMAL FORM] Content-Type: {request.content_type}")
    logger.info(f"Empfangene POST-Daten: {dict(request.POST)}")
    logger.info(f"Content-Type: {request.content_type}")

    # Eingabedaten extrahieren
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    print(
        f"[NORMAL FORM] Extrahierte Werte - Name: '{name}', Email: '{email}', Message: '{message}'"
    )
    logger.info(
        f"Extrahierte Werte - Name: '{name}', Email: '{email}', Message: '{message}'"
    )

    # Synchrones Logging der Eingabedaten
    log_form_input_sync(name, email, message, logger)

    # Einfache Validierung
    errors = {}
    if not name:
        errors["name"] = _("Name ist erforderlich")
    if not email:
        errors["email"] = _("E-Mail ist erforderlich")
    elif "@" not in email:
        errors["email"] = _("Ungültige E-Mail-Adresse")

    if errors:
        logger.warning(f"Formular-Validierungsfehler: {errors}")
        # Bei Fehlern die komplette Seite mit Fehlermeldungen rendern
        context = get_storybook_context()
        context["form_errors"] = errors
        context["form_data"] = {"name": name, "email": email, "message": message}
        return render(request, "index.html", context)

    # Erfolg simulieren mit synchroner Verarbeitung
    time.sleep(1)  # Simuliere synchrone Verarbeitungszeit

    print("[NORMAL FORM] Normales Formular erfolgreich verarbeitet")
    logger.info("Normales Formular erfolgreich verarbeitet")

    # Bei erfolgreichem Submit die komplette Seite mit Erfolgsmeldung rendern
    context = get_storybook_context()
    context["form_success"] = {
        "message": _("Normales Formular erfolgreich übermittelt!"),
        "name": name,
        "email": email,
        "type": "success",
    }

    return render(request, "index.html", context)


def log_form_input_sync(name, email, message, logger) -> None:
    """
    Synchrone Funktion zum Loggen der Formular-Eingaben

    Args:
        name (str): Name des Benutzers
        email (str): E-Mail-Adresse des Benutzers
        message (str): Nachricht des Benutzers
        logger: Logger-Instanz
    """
    # Simuliere synchrone Verarbeitung
    time.sleep(0.1)

    # Detailliertes Logging der Eingabedaten - sowohl print als auch logger
    separator = "=" * 50
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(separator)
    print("NORMALES Kontaktformular - Neue Eingabe erhalten")
    print(separator)
    print(f"Zeitstempel: {timestamp}")
    print(f"Name: {name}")
    print(f"E-Mail: {email}")
    print(f"Nachricht: {message}")
    print(f"Name-Länge: {len(name)} Zeichen")
    print(f"E-Mail-Länge: {len(email)} Zeichen")
    print(f"Nachricht-Länge: {len(message)} Zeichen")

    logger.info(separator)
    logger.info("NORMALES Kontaktformular - Neue Eingabe erhalten")
    logger.info(separator)
    logger.info(f"Zeitstempel: {timestamp}")
    logger.info(f"Name: {name}")
    logger.info(f"E-Mail: {email}")
    logger.info(f"Nachricht: {message}")
    logger.info(f"Name-Länge: {len(name)} Zeichen")
    logger.info(f"E-Mail-Länge: {len(email)} Zeichen")
    logger.info(f"Nachricht-Länge: {len(message)} Zeichen")

    # Zusätzliche Validierungsinfos
    if "@" in email:
        email_parts = email.split("@")
        domain = email_parts[1] if len(email_parts) > 1 else "Unbekannt"
        print(f"E-Mail Domain: {domain}")
        logger.info(f"E-Mail Domain: {domain}")

    print(separator)
    logger.info(separator)

    # Simuliere weitere synchrone Verarbeitung
    time.sleep(0.05)
    print("Synchrones Logging abgeschlossen")
    logger.debug("Synchrones Logging abgeschlossen")


async def log_form_input_async(name, email, message, logger) -> None:
    """
    Asynchrone Funktion zum Loggen der Formular-Eingaben

    Args:
        name (str): Name des Benutzers
        email (str): E-Mail-Adresse des Benutzers
        message (str): Nachricht des Benutzers
        logger: Logger-Instanz
    """
    # Simuliere asynchrone Verarbeitung
    await asyncio.sleep(0.1)

    # Detailliertes Logging der Eingabedaten - sowohl print als auch logger
    separator = "=" * 50
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(separator)
    print("HTMX Kontaktformular - Neue Eingabe erhalten")
    print(separator)
    print(f"Zeitstempel: {timestamp}")
    print(f"Name: {name}")
    print(f"E-Mail: {email}")
    print(f"Nachricht: {message}")
    print(f"Name-Länge: {len(name)} Zeichen")
    print(f"E-Mail-Länge: {len(email)} Zeichen")
    print(f"Nachricht-Länge: {len(message)} Zeichen")

    logger.info(separator)
    logger.info("HTMX Kontaktformular - Neue Eingabe erhalten")
    logger.info(separator)
    logger.info(f"Zeitstempel: {timestamp}")
    logger.info(f"Name: {name}")
    logger.info(f"E-Mail: {email}")
    logger.info(f"Nachricht: {message}")
    logger.info(f"Name-Länge: {len(name)} Zeichen")
    logger.info(f"E-Mail-Länge: {len(email)} Zeichen")
    logger.info(f"Nachricht-Länge: {len(message)} Zeichen")

    # Zusätzliche Validierungsinfos
    if "@" in email:
        email_parts = email.split("@")
        domain = email_parts[1] if len(email_parts) > 1 else "Unbekannt"
        print(f"E-Mail Domain: {domain}")
        logger.info(f"E-Mail Domain: {domain}")

    print(separator)
    logger.info(separator)

    # Simuliere weitere asynchrone Verarbeitung
    await asyncio.sleep(0.05)
    print("Asynchrones Logging abgeschlossen")
    logger.debug("Asynchrones Logging abgeschlossen")


@require_http_methods(["GET"])
def component_demo_view(request, component_name):
    """Einzelne Storybook-Demo für HTMX"""
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
            "component_html": render_to_string(
                component_templates[component_name], context
            ),
        },
    )


def get_component_context(component_name):
    """Hilfsfunktion für Komponenten-Beispieldaten"""
    contexts = {
        "alert": {
            "message": _("Dies ist eine Beispiel-Benachrichtigung"),
            "type": "info",
            "dismissible": True,
        },
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
                {
                    "type": "email",
                    "name": "email",
                    "label": _("E-Mail"),
                    "required": True,
                },
            ],
            "actions": [
                {"text": _("Absenden"), "type": "submit", "style": "primary"},
            ],
        },
        "sidebar": {
            "title": _("Navigation"),
            "items": [
                {"text": _("Dashboard"), "url": "/", "icon": "📊"},
                {"text": _("Einstellungen"), "url": "/settings/", "icon": "⚙️"},
            ],
        },
        "breadcrumbs": {
            "items": [
                {"text": _("Startseite"), "url": "/"},
                {"text": _("Komponenten"), "url": None, "active": True},
            ]
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

def storybook_view(request):
    """Hauptseite mit allen Insight UI Komponenten"""

    # Wenn es ein POST-Request ist, leite an normale Formular-Verarbeitung weiter
    if request.method == "POST":
        return normal_form_submit(request)

    # Beispieldaten für die Komponenten
    context = get_storybook_context()

    return render(request, "index.html", context)

def storybook_view(request):
    """Hauptseite mit allen Insight UI Komponenten"""

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
    
    return render(request, "index.html", context)

def generate_random_payload():
    """Erstellt eine zufällige Anzahl von Einträgen als Payload-Daten."""
    count = random.randint(3, 7)  # zufällige Anzahl zwischen 3 und 7
    entries = []
    for i in range(1, count + 1):
        entries.append({
            "title": f"Element {i}",
            "subtitle": f"Untertitel {i}",
            "content": f"Dies ist der Inhalt von Eintrag {i}.",
            "actions": [
                {"text": "Mehr erfahren", "url": "#", "type": "primary"},
                {"text": "Teilen", "url": "#", "type": "secondary"},
            ],
            "name": f"Name {i}",
            "status": "Aktiv" if i % 2 == 0 else "Inaktiv",
            "action_link": f"<a href='#'>Details {i}</a>",
        })
    return entries

def map_payload_to_cards(payload):
    """Mappt Payload-Daten auf Karten-Darstellung."""
    elements = []
    for item in payload:
        elements.append({
            "title": item["title"],
            "subtitle": item["subtitle"],
            "content": item["content"],
            "actions": item["actions"],
        })
    return elements

def map_payload_to_table(payload):
    """Mappt Payload-Daten auf Tabellen-Darstellung."""
    headers = ["title", "status", "content", "action_link"]
    rows = []
    for item in payload:
        content = item["content"]
        if len(content) > 10:
            content = content[:10] + "..."
        rows.append([item["title"], item["status"], content, item["action_link"]])
    return headers, rows

@require_GET
def toggle_view(request):
    view = request.GET.get("view", "table")

    payload = generate_random_payload()
    
    context = {
        "current_view": view,
    }

    # Initial Daten für Tabelle bereitstellen, wenn Ansicht "table" ist
    if view == "table":
        headers, rows = map_payload_to_table(payload)
        context["table_headers"] = headers
        context["table_rows"] = rows
    elif view == "card":
        context["cards"] = map_payload_to_cards(payload)

    if view == "card":
        logger.info("log: toggle_view - Kartenansicht ausgewählt")
        return render(request, "insight_ui/components/toggle_view_cards.html", context)
    else:
        logger.info("log: toggle_view - Tabellenansicht ausgewählt")
        return render(request, "insight_ui/components/toggle_view_table.html", context)

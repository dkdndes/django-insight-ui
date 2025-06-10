from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.conf import settings
import json
import time
from datetime import datetime


def index_view(request):
    """Hauptseite mit allen Insight UI Komponenten"""
    
    # Beispieldaten für die Komponenten
    context = {
        'nav_links': [
            {'text': _('Startseite'), 'url': '/', 'active': True},
            {'text': _('Komponenten'), 'url': '/components/', 'active': False},
            {'text': _('Dokumentation'), 'url': '/docs/', 'active': False},
        ],
        'breadcrumb_items': [
            {'text': _('Startseite'), 'url': '/'},
            {'text': _('Demo'), 'url': '/demo/'},
            {'text': _('Komponenten'), 'url': None, 'active': True},
        ],
        'table_headers': [_('Name'), _('E-Mail'), _('Status'), _('Aktionen')],
        'table_rows': [
            ['Max Mustermann', 'max@example.com', _('Aktiv'), '<button class="btn btn-sm">Bearbeiten</button>'],
            ['Anna Schmidt', 'anna@example.com', _('Inaktiv'), '<button class="btn btn-sm">Bearbeiten</button>'],
            ['Tom Weber', 'tom@example.com', _('Aktiv'), '<button class="btn btn-sm">Bearbeiten</button>'],
        ],
        'card_actions': [
            {'text': _('Mehr erfahren'), 'url': '#', 'type': 'primary'},
            {'text': _('Teilen'), 'url': '#', 'type': 'secondary'},
        ],
        'form_fields': [
            {
                'type': 'text',
                'name': 'name',
                'label': _('Name'),
                'placeholder': _('Ihr vollständiger Name'),
                'required': True,
            },
            {
                'type': 'email',
                'name': 'email',
                'label': _('E-Mail'),
                'placeholder': _('ihre.email@example.com'),
                'required': True,
            },
            {
                'type': 'textarea',
                'name': 'message',
                'label': _('Nachricht'),
                'placeholder': _('Ihre Nachricht...'),
                'rows': 4,
            },
        ],
        'form_actions': [
            {'text': _('Absenden'), 'type': 'submit', 'style': 'primary'},
            {'text': _('Zurücksetzen'), 'type': 'reset', 'style': 'secondary'},
        ],
        'modal_actions': [
            {'text': _('Speichern'), 'type': 'button', 'style': 'primary', 'action': 'save'},
            {'text': _('Abbrechen'), 'type': 'button', 'style': 'secondary', 'action': 'close'},
        ],
        'sidebar_items': [
            {'text': _('Dashboard'), 'url': '/', 'icon': '📊'},
            {'text': _('Benutzer'), 'url': '/users/', 'icon': '👥'},
            {'text': _('Einstellungen'), 'url': '/settings/', 'icon': '⚙️'},
            {'text': _('Hilfe'), 'url': '/help/', 'icon': '❓'},
        ],
        'scroll_items': [
            {'title': f'Element {i}', 'content': f'Inhalt für Element {i}'} 
            for i in range(1, 11)
        ],
        'htmx_form_fields': [
            {
                'type': 'text',
                'name': 'htmx_name',
                'label': _('Name (HTMX)'),
                'placeholder': _('Name eingeben'),
                'required': True,
            },
            {
                'type': 'email',
                'name': 'htmx_email',
                'label': _('E-Mail (HTMX)'),
                'placeholder': _('E-Mail eingeben'),
                'required': True,
            },
        ],
        'htmx_config': {
            'url': '/api/form-submit/',
            'method': 'post',
            'target': '#form-result',
            'swap': 'innerHTML',
        },
    }
    
    return render(request, 'index.html', context)


@require_http_methods(["GET"])
def live_data_view(request):
    """HTMX Endpoint für Live-Daten"""
    current_time = datetime.now().strftime("%H:%M:%S")
    data = {
        'time': current_time,
        'message': _('Daten aktualisiert um %(time)s') % {'time': current_time},
        'status': 'success'
    }
    
    if request.headers.get('HX-Request'):
        # HTMX Request - nur den Inhalt zurückgeben
        html = render_to_string('insight_ui/components/live_content_partial.html', {
            'data': data,
            'timestamp': current_time
        })
        return HttpResponse(html)
    
    # Normale Request - JSON zurückgeben
    return JsonResponse(data)


@require_http_methods(["GET"])
def more_items_view(request):
    """HTMX Endpoint für Infinite Scroll"""
    page = int(request.GET.get('page', 1))
    items_per_page = 5
    
    # Simuliere mehr Items
    start = (page - 1) * items_per_page + 11  # +11 weil wir schon 10 Items haben
    end = start + items_per_page
    
    new_items = [
        {'title': f'Element {i}', 'content': f'Dynamisch geladener Inhalt für Element {i}'} 
        for i in range(start, end)
    ]
    
    has_next = page < 5  # Simuliere max 5 Seiten
    next_url = f"/api/more-items/?page={page + 1}" if has_next else ""
    
    if request.headers.get('HX-Request'):
        html = render_to_string('insight_ui/components/infinite_scroll_items.html', {
            'items': new_items,
            'next_url': next_url,
            'has_next': has_next,
            'page': page + 1
        })
        return HttpResponse(html)
    
    return JsonResponse({
        'items': new_items,
        'has_next': has_next,
        'next_url': next_url
    })


@require_http_methods(["POST"])
def htmx_form_submit(request):
    """HTMX Endpoint für Formular-Übermittlung"""
    if request.headers.get('HX-Request'):
        # Simuliere Formular-Verarbeitung
        name = request.POST.get('htmx_name', '')
        email = request.POST.get('htmx_email', '')
        
        # Einfache Validierung
        errors = {}
        if not name:
            errors['htmx_name'] = _('Name ist erforderlich')
        if not email:
            errors['htmx_email'] = _('E-Mail ist erforderlich')
        elif '@' not in email:
            errors['htmx_email'] = _('Ungültige E-Mail-Adresse')
        
        if errors:
            # Fehler zurückgeben
            html = render_to_string('insight_ui/components/form_errors.html', {
                'errors': errors,
                'type': 'error'
            })
            return HttpResponse(html, status=400)
        
        # Erfolg simulieren
        time.sleep(1)  # Simuliere Verarbeitungszeit
        
        success_html = render_to_string('insight_ui/components/form_success.html', {
            'message': _('Formular erfolgreich übermittelt!'),
            'name': name,
            'email': email,
            'type': 'success'
        })
        return HttpResponse(success_html)
    
    return JsonResponse({'error': _('Nur HTMX-Requests erlaubt')}, status=400)


@require_http_methods(["GET"])
def component_demo_view(request, component_name):
    """Einzelne Komponenten-Demo für HTMX"""
    component_templates = {
        'alert': 'insight_ui/components/alert.html',
        'card': 'insight_ui/components/card.html',
        'modal': 'insight_ui/components/modal.html',
        'table': 'insight_ui/components/table.html',
        'form': 'insight_ui/components/form.html',
        'sidebar': 'insight_ui/components/sidebar.html',
        'breadcrumbs': 'insight_ui/components/breadcrumbs.html',
        'navbar': 'insight_ui/components/navbar.html',
    }
    
    if component_name not in component_templates:
        return JsonResponse({'error': _('Komponente nicht gefunden')}, status=404)
    
    # Beispieldaten für die jeweilige Komponente
    context = get_component_context(component_name)
    
    if request.headers.get('HX-Request'):
        html = render_to_string(component_templates[component_name], context)
        return HttpResponse(html)
    
    return render(request, 'insight_ui/component_demo.html', {
        'component_name': component_name,
        'component_html': render_to_string(component_templates[component_name], context)
    })


def get_component_context(component_name):
    """Hilfsfunktion für Komponenten-Beispieldaten"""
    contexts = {
        'alert': {
            'message': _('Dies ist eine Beispiel-Benachrichtigung'),
            'type': 'info',
            'dismissible': True
        },
        'card': {
            'title': _('Beispiel-Karte'),
            'subtitle': _('Untertitel'),
            'content': _('Dies ist der Inhalt einer Beispiel-Karte.'),
            'actions': [
                {'text': _('Aktion 1'), 'url': '#', 'type': 'primary'},
                {'text': _('Aktion 2'), 'url': '#', 'type': 'secondary'},
            ]
        },
        'modal': {
            'id': 'demo-modal',
            'title': _('Demo Modal'),
            'content': _('Dies ist ein Beispiel-Modal-Dialog.'),
            'actions': [
                {'text': _('Speichern'), 'type': 'button', 'style': 'primary'},
                {'text': _('Abbrechen'), 'type': 'button', 'style': 'secondary'},
            ]
        },
        'table': {
            'headers': [_('Name'), _('E-Mail'), _('Status')],
            'rows': [
                ['Max Mustermann', 'max@example.com', _('Aktiv')],
                ['Anna Schmidt', 'anna@example.com', _('Inaktiv')],
            ],
            'caption': _('Beispiel-Tabelle')
        },
        'form': {
            'title': _('Beispiel-Formular'),
            'fields': [
                {'type': 'text', 'name': 'name', 'label': _('Name'), 'required': True},
                {'type': 'email', 'name': 'email', 'label': _('E-Mail'), 'required': True},
            ],
            'actions': [
                {'text': _('Absenden'), 'type': 'submit', 'style': 'primary'},
            ]
        },
        'sidebar': {
            'title': _('Navigation'),
            'items': [
                {'text': _('Dashboard'), 'url': '/', 'icon': '📊'},
                {'text': _('Einstellungen'), 'url': '/settings/', 'icon': '⚙️'},
            ]
        },
        'breadcrumbs': {
            'items': [
                {'text': _('Startseite'), 'url': '/'},
                {'text': _('Komponenten'), 'url': None, 'active': True},
            ]
        },
        'navbar': {
            'brand': 'Demo App',
            'links': [
                {'text': _('Startseite'), 'url': '/', 'active': True},
                {'text': _('Über uns'), 'url': '/about/', 'active': False},
            ]
        }
    }
    
    return contexts.get(component_name, {})

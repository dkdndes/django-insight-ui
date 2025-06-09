"""
Tests für die Template-Tags des Insight UI-Pakets.
"""

import pytest
from django.template import Context, Template


@pytest.mark.django_db
def test_navbar_tag():
    """Test, dass das navbar-Tag korrekt gerendert wird."""
    template = Template(
        "{% load insight_tags %}"
        "{% navbar brand='Test App' %}"
    )
    rendered = template.render(Context({}))
    
    # Überprüfe, ob die wichtigsten Elemente vorhanden sind
    assert 'role="navigation"' in rendered
    assert 'aria-label="Hauptnavigation"' in rendered
    assert 'Test App' in rendered
    assert 'insight-navbar' in rendered


@pytest.mark.django_db
def test_navbar_with_links():
    """Test, dass das navbar-Tag mit Links korrekt gerendert wird."""
    links = [
        {"url": "/", "text": "Home", "active": True},
        {"url": "/about/", "text": "Über uns"},
    ]
    
    template = Template(
        "{% load insight_tags %}"
        "{% navbar brand='Test App' links=links %}"
    )
    rendered = template.render(Context({"links": links}))
    
    # Überprüfe, ob die Links korrekt gerendert werden
    assert 'Home' in rendered
    assert 'Über uns' in rendered
    assert 'aria-current="page"' in rendered


@pytest.mark.django_db
def test_alert_tag():
    """Test, dass das alert-Tag korrekt gerendert wird."""
    template = Template(
        "{% load insight_tags %}"
        "{% alert message='Dies ist eine Testnachricht' type='info' %}"
    )
    rendered = template.render(Context({}))
    
    # Überprüfe, ob die wichtigsten Elemente vorhanden sind
    assert 'role="alert"' in rendered
    assert 'insight-alert--info' in rendered
    assert 'Dies ist eine Testnachricht' in rendered


@pytest.mark.django_db
def test_alert_dismissible():
    """Test, dass das alert-Tag mit schließbarer Option korrekt gerendert wird."""
    template = Template(
        "{% load insight_tags %}"
        "{% alert message='Dies ist eine Testnachricht' type='warning' dismissible=True %}"
    )
    rendered = template.render(Context({}))
    
    # Überprüfe, ob die Schließen-Schaltfläche vorhanden ist
    assert 'insight-alert--dismissible' in rendered
    assert 'data-insight-dismiss="alert"' in rendered
    assert 'aria-label="Schließen"' in rendered

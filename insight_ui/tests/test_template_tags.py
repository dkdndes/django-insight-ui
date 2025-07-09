"""Tests für Insight UI Template Tags."""

from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils.translation import activate


class TemplateTagsTestCase(TestCase):
    """Basis-Testklasse für Template Tags."""

    def setUp(self):
        """Setup für Tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        activate('de')

    def render_template(self, template_string, context=None):
        """Hilfsmethode zum Rendern von Templates."""
        if context is None:
            context = {}
        template = Template(template_string)
        return template.render(Context(context))


class NavbarTemplateTagTest(TemplateTagsTestCase):
    """Tests für den navbar Template Tag."""

    def test_navbar_basic(self):
        """Test für grundlegende navbar Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% navbar brand="Test App" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('Test App', rendered)

    def test_navbar_with_links(self):
        """Test für navbar mit Links."""
        links = [
            {'url': '/home/', 'title': 'Home', 'active': True},
            {'url': '/about/', 'title': 'About', 'active': False}
        ]
        template_string = """
        {% load insight_tags %}
        {% navbar brand="Test App" links=links %}
        """
        rendered = self.render_template(template_string, {'links': links})
        self.assertIn('Test App', rendered)

    def test_navbar_themes(self):
        """Test für verschiedene navbar Themes."""
        for theme in ['light', 'dark', 'high-contrast']:
            with self.subTest(theme=theme):
                template_string = f"""
                {{% load insight_tags %}}
                {{% navbar brand="Test App" theme="{theme}" %}}
                """
                rendered = self.render_template(template_string)
                self.assertIn('Test App', rendered)


class LiveContentTemplateTagTest(TemplateTagsTestCase):
    """Tests für den live_content Template Tag."""

    def test_live_content_basic(self):
        """Test für grundlegende live_content Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% live_content url="/api/live-data/" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('/api/live-data/', rendered)

    def test_live_content_with_interval(self):
        """Test für live_content mit Intervall."""
        template_string = """
        {% load insight_tags %}
        {% live_content url="/api/live-data/" interval=5000 %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('/api/live-data/', rendered)


class WebsocketTemplateTagTest(TemplateTagsTestCase):
    """Tests für den insight_websocket Template Tag."""

    def test_websocket_basic(self):
        """Test für grundlegende WebSocket Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% insight_websocket ws_url="ws://localhost:8765" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('ws://localhost:8765', rendered)


class InfiniteScrollTemplateTagTest(TemplateTagsTestCase):
    """Tests für den infinite_scroll Template Tag."""

    def test_infinite_scroll_basic(self):
        """Test für grundlegende infinite_scroll Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% infinite_scroll next_url="/api/more-items/" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('/api/more-items/', rendered)


class LanguageSelectorTemplateTagTest(TemplateTagsTestCase):
    """Tests für den language_selector Template Tag."""

    def test_language_selector_basic(self):
        """Test für grundlegende language_selector Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% language_selector current_language="de" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('de', rendered)


class AlertTemplateTagTest(TemplateTagsTestCase):
    """Tests für den alert Template Tag."""

    def test_alert_basic(self):
        """Test für grundlegende alert Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% alert message="Test message" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('Test message', rendered)

    def test_alert_types(self):
        """Test für verschiedene alert Typen."""
        for alert_type in ['info', 'success', 'warning', 'error']:
            with self.subTest(alert_type=alert_type):
                template_string = f"""
                {{% load insight_tags %}}
                {{% alert message="Test message" type="{alert_type}" %}}
                """
                rendered = self.render_template(template_string)
                self.assertIn('Test message', rendered)


class SidebarTemplateTagTest(TemplateTagsTestCase):
    """Tests für den sidebar Template Tag."""

    def test_sidebar_basic(self):
        """Test für grundlegende sidebar Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% sidebar title="Navigation" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('Navigation', rendered)


class BreadcrumbsTemplateTagTest(TemplateTagsTestCase):
    """Tests für den breadcrumbs Template Tag."""

    def test_breadcrumbs_basic(self):
        """Test für grundlegende breadcrumbs Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% breadcrumbs %}
        """
        rendered = self.render_template(template_string)
        self.assertIsNotNone(rendered)


class TableTemplateTagTest(TemplateTagsTestCase):
    """Tests für den table Template Tag."""

    def test_table_basic(self):
        """Test für grundlegende table Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% table %}
        """
        rendered = self.render_template(template_string)
        self.assertIsNotNone(rendered)


class ModalTemplateTagTest(TemplateTagsTestCase):
    """Tests für den modal Template Tag."""

    def test_modal_basic(self):
        """Test für grundlegende modal Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% modal id="test-modal" title="Test Modal" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('test-modal', rendered)
        self.assertIn('Test Modal', rendered)


class CardTemplateTagTest(TemplateTagsTestCase):
    """Tests für den card Template Tag."""

    def test_card_basic(self):
        """Test für grundlegende card Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% card title="Test Card" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('Test Card', rendered)


class FormTemplateTagTest(TemplateTagsTestCase):
    """Tests für den form Template Tag."""

    def test_form_basic(self):
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" %}
        """
        rendered = self.render_template(template_string)
        self.assertIn('Test Form', rendered)


class FooterTemplateTagTest(TemplateTagsTestCase):
    """Tests für den footer Template Tag."""

    def test_footer_basic(self):
        """Test für grundlegende footer Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% footer %}
        """
        rendered = self.render_template(template_string)
        self.assertIsNotNone(rendered)

# Installation

Django Insight UI kann einfach mit UV installiert werden, dem empfohlenen Paketmanager für Python-Projekte.

## Voraussetzungen

- Python 3.8 oder höher
- Django 4.2 oder höher
- UV als Paketmanager

## Installation mit UV

```bash
uv add django-insight-ui
```

## Manuelle Installation

Alternativ können Sie das Paket auch manuell installieren:

1. Klonen Sie das Repository:

```bash
git clone https://github.com/yourusername/django-insight-ui.git
```

2. Installieren Sie das Paket im Entwicklungsmodus:

```bash
cd django-insight-ui
uv add -e .
```

## Django-Konfiguration

1. Fügen Sie 'insight_ui' zu Ihren INSTALLED_APPS in settings.py hinzu:

```python
INSTALLED_APPS = [
    # ...
    'insight_ui',
    # ...
]
```

2. Fügen Sie die Insight UI-Einstellungen zu Ihrer settings.py hinzu (optional):

```python
INSIGHT_UI = {
    "theme": "light",  # 'light', 'dark', oder 'high-contrast'
    "branding": {
        "name": "Meine App",
        "logo": "path/to/logo.svg",
    },
    "features": {
        "theme_toggle": True,
        "language_selector": True,
    },
}
```

3. Führen Sie die Migrationen aus:

```bash
python manage.py migrate
```

4. Sammeln Sie die statischen Dateien:

```bash
python manage.py collectstatic
```

## Nächste Schritte

Nachdem Sie Django Insight UI installiert haben, können Sie mit dem [Schnellstart](quickstart.md) fortfahren, um zu erfahren, wie Sie die Komponenten in Ihren Templates verwenden können.

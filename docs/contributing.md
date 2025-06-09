# Mitwirken

Wir freuen uns über Beiträge zur Verbesserung von Django Insight UI! Diese Anleitung hilft Ihnen, zum Projekt beizutragen.

## Entwicklungsumgebung einrichten

1. Klonen Sie das Repository:

```bash
git clone https://github.com/yourusername/django-insight-ui.git
cd django-insight-ui
```

2. Installieren Sie die Entwicklungsabhängigkeiten:

```bash
uv add --dev -e ".[dev,test,docs]"
```

3. Installieren Sie die Pre-Commit-Hooks:

```bash
pre-commit install
```

## Entwicklungsworkflow

1. Erstellen Sie einen neuen Branch für Ihre Änderungen:

```bash
git checkout -b feature/ihre-feature-beschreibung
```

2. Nehmen Sie Ihre Änderungen vor und stellen Sie sicher, dass die Tests bestehen:

```bash
uv run pytest
```

3. Führen Sie die Linter aus:

```bash
uv run black .
uv run isort .
uv run ruff .
uv run mypy .
```

4. Reichen Sie einen Pull Request ein

## Coderichtlinien

- Folgen Sie dem [PEP 8](https://www.python.org/dev/peps/pep-0008/)-Stilguide für Python-Code
- Schreiben Sie Docstrings im [Google-Stil](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Fügen Sie Typhinweise hinzu
- Schreiben Sie Tests für neue Funktionen
- Halten Sie die Barrierefreiheit aufrecht (WCAG 2.1 AA)

## Tests

Wir verwenden pytest für Tests. Führen Sie die Tests aus mit:

```bash
uv run pytest
```

Für Barrierefreiheitstests:

```bash
uv run pytest tests/accessibility/
```

## Dokumentation

Die Dokumentation wird mit MkDocs erstellt. Um die Dokumentation lokal zu erstellen und anzuzeigen:

```bash
uv run mkdocs serve
```

## Neue Komponenten hinzufügen

1. Erstellen Sie ein Template in `insight_ui/templates/insight_ui/components/`
2. Fügen Sie ein Template-Tag in `insight_ui/templatetags/insight_tags.py` hinzu
3. Fügen Sie CSS in `insight_ui/static/insight_ui/css/insight-ui.css` hinzu
4. Fügen Sie bei Bedarf JavaScript in `insight_ui/static/insight_ui/js/insight-ui.js` hinzu
5. Schreiben Sie Tests für die neue Komponente
6. Dokumentieren Sie die Komponente in `docs/components/`

## Versionshinweise

Wir folgen [Semantic Versioning](https://semver.org/):

- MAJOR: Inkompatible API-Änderungen
- MINOR: Neue Funktionen (abwärtskompatibel)
- PATCH: Bugfixes (abwärtskompatibel)

## Verhaltenskodex

Bitte beachten Sie unseren [Verhaltenskodex](CODE_OF_CONDUCT.md), um eine positive und respektvolle Umgebung für alle Mitwirkenden zu schaffen.

## Lizenz

Durch das Einreichen von Beiträgen erklären Sie sich damit einverstanden, dass Ihre Beiträge unter der [MIT-Lizenz](LICENSE) des Projekts stehen.

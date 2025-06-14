#!/usr/bin/env python
"""
Dieses Skript ist ein Platzhalter für UI-Tests.
"""
import sys

def run_tests():
    """Führt UI-Tests aus (aktuell deaktiviert)."""
    print("UI-Tests mit Playwright sind derzeit deaktiviert.")
    print("Um Playwright-Tests zu aktivieren, führen Sie folgende Befehle aus:")
    print("  uv run playwright install")
    print("  python -m pytest insight_ui/tests/test_ui.py -v")
    print("✅ Keine Tests ausgeführt.")
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())

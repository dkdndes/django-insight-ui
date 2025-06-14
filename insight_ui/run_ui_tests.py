#!/usr/bin/env python
"""
Dieses Skript führt die Playwright-UI-Tests für Django Insight UI aus.
"""
import os
import sys
import subprocess
from pathlib import Path

# Füge das Projektverzeichnis zum Python-Pfad hinzu
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def run_tests():
    """Führt die Playwright-Tests aus."""
    print("Starte UI-Tests mit Playwright...")
    
    # Führe die Tests mit pytest aus
    result = subprocess.run(
        ["pytest", "insight_ui/tests/test_ui.py", "-v"],
        env=os.environ.copy()
    )
    
    if result.returncode == 0:
        print("✅ Alle UI-Tests erfolgreich bestanden!")
    else:
        print("❌ Einige UI-Tests sind fehlgeschlagen.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()

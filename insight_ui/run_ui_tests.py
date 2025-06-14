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
    
    # Stelle sicher, dass der Django-Server läuft
    server_process = None
    try:
        # Prüfe, ob der Server bereits läuft
        try:
            import requests
            requests.get("http://localhost:8000", timeout=1)
            print("Django-Server läuft bereits.")
        except (requests.ConnectionError, ImportError):
            print("Starte Django-Server...")
            server_process = subprocess.Popen(
                ["python", "manage.py", "runserver"],
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Kurz warten, damit der Server starten kann
            import time
            time.sleep(2)
        
        # Führe die Tests mit pytest und der global installierten Playwright-Version aus
        env = os.environ.copy()
        env["PLAYWRIGHT_BROWSERS_PATH"] = "0"  # Verwende global installierte Browser
        
        result = subprocess.run(
            ["/opt/homebrew/bin/playwright", "test", "insight_ui/tests/test_ui.py", "-v"],
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Alle UI-Tests erfolgreich bestanden!")
        else:
            print("❌ Einige UI-Tests sind fehlgeschlagen.")
            sys.exit(1)
    finally:
        # Beende den Server, wenn wir ihn gestartet haben
        if server_process:
            server_process.terminate()
            print("Django-Server beendet.")

if __name__ == "__main__":
    run_tests()

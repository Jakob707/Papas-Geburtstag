import os
import sys
from updater import check_for_updates

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

GITHUB_USER = "Jakob707"
REPO_NAME = "Papas-Geburtstag"
BRANCH = "main"

FILES_TO_UPDATE = ["main.py", "updater.py", "tools.py"]


def main():
    print("=== MiniToolbox ===\n")

    print("Prüfe auf Updates...")
    updated = check_for_updates(GITHUB_USER, REPO_NAME, BRANCH, FILES_TO_UPDATE)

    if updated:
        print("App wurde aktualisiert! Starte neu...")
        # Kurz warten damit Fenster sich schließen kann
        import time
        time.sleep(0.5)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    print("App ist aktuell.\n")

    from tools import run_tools
    run_tools()


if __name__ == "__main__":
    main()
import os
import sys
from updater import check_for_updates

#unnötige Fehlermeldung unterdrücken
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Deine GitHub-Infos hier eintragen
GITHUB_USER = "Jakob707"
REPO_NAME = "Papas-Geburtstag"
BRANCH = "main"

# Dateien die synchronisiert werden sollen
FILES_TO_UPDATE = ["main.py", "updater.py", "tools.py"]


def main():
    print("=== MiniToolbox ===\n")

    # Update-Check beim Start
    print("Prüfe auf Updates...")
    updated = check_for_updates(GITHUB_USER, REPO_NAME, BRANCH, FILES_TO_UPDATE)

    if updated:
        print("App wurde aktualisiert! Starte neu...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    print("App ist aktuell.\n")

    # === Hier kommen deine Tools hin ===
    from tools import run_tools
    run_tools()


if __name__ == "__main__":
    main()
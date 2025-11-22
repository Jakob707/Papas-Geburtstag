import os
import sys
from updater import check_for_updates

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Deine GitHub-Infos
GITHUB_USER = "Jakob707"
REPO_NAME = "Papas-Geburtstag"
BRANCH = "main"
APP_NAME = "MiniToolbox"  # Name deiner .app (ohne .app)


def main():
    print("=== MiniToolbox ===\n")

    print("Prüfe auf Updates...")
    updated = check_for_updates(GITHUB_USER, REPO_NAME, BRANCH, APP_NAME)

    if updated:
        print("Update installiert. Bitte App neu starten.")
        sys.exit(0)

    print("App ist aktuell.\n")

    from tools import run_tools
    run_tools()


if __name__ == "__main__":
    main()
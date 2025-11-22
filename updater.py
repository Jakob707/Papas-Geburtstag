import urllib.request
import os


def get_raw_url(user, repo, branch, filename):
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{filename}"


def get_remote_version(user, repo, branch):
    url = get_raw_url(user, repo, branch, "version.txt")
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode().strip()
    except:
        return None


def get_local_version():
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            return f.read().strip()
    return "0"


def download_file(user, repo, branch, filename):
    url = get_raw_url(user, repo, branch, filename)
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
        with open(filename, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Fehler beim Download von {filename}: {e}")
        return False


def check_for_updates(user, repo, branch, files):
    local_version = get_local_version()
    remote_version = get_remote_version(user, repo, branch)

    if remote_version is None:
        print("Konnte Version nicht prüfen (offline?)")
        return False

    print(f"Lokale Version: {local_version}")
    print(f"Remote Version: {remote_version}")

    if remote_version > local_version:
        print(f"\nNeue Version verfügbar! Lade herunter...")

        for filename in files:
            print(f"  Lade {filename}...")
            download_file(user, repo, branch, filename)

        # Version aktualisieren
        download_file(user, repo, branch, "version.txt")
        print("Update abgeschlossen!")
        return True

    return False
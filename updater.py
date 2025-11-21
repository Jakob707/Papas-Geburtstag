import os
import sys
import requests
import shutil
import zipfile

# -------------------------
# ❶ URLs HIER ANPASSEN
# -------------------------
REMOTE_VERSION_URL = "HIER_VERSION_URL_REIN"  # z.B. https://raw.githubusercontent.com/USER/REPO/main/version.txt
UPDATE_ZIP_URL = "HIER_ZIP_URL_REIN"          # z.B. https://github.com/USER/REPO/raw/main/MeineApp.app.zip
# -------------------------

TMP_ZIP = "/tmp/update.zip"

# Pfad zur .app (funktioniert zuverlässig in PyInstaller)
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
LOCAL_VERSION_PATH = os.path.join(APP_PATH, "Contents/Resources/version.txt")

def get_local_version():
    try:
        with open(LOCAL_VERSION_PATH, "r") as f:
            return f.read().strip()
    except:
        return "0"

def get_remote_version():
    return requests.get(REMOTE_VERSION_URL).text.strip()

def download_update():
    print("📥 Lade Update herunter…")
    r = requests.get(UPDATE_ZIP_URL)
    with open(TMP_ZIP, "wb") as f:
        f.write(r.content)

def install_update():
    print("📦 Entpacke Update…")
    with zipfile.ZipFile(TMP_ZIP, "r") as zip_ref:
        zip_ref.extractall("/tmp/new_app")

    print("🔁 Ersetze alte App…")
    shutil.rmtree(APP_PATH)
    shutil.move("/tmp/new_app/MeineApp.app", APP_PATH)

    print("✔️ Update installiert! Bitte App neu starten.")

def check_for_updates():
    local = get_local_version()
    remote = get_remote_version()

    if local != remote:
        print(f"Neue Version verfügbar: {remote} (du hast {local})")
        download_update()
        install_update()
    else:
        print("App ist aktuell.")

if __name__ == "__main__":
    check_for_updates()

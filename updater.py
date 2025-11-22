import urllib.request
import os
import sys
import zipfile
import shutil
import threading
import customtkinter as ctk


def get_base_path():
    """Gibt den Ordner zurück, in dem die .app liegt"""
    if getattr(sys, 'frozen', False):
        exe_path = os.path.dirname(sys.executable)
        if sys.platform == "darwin":
            # 3 Ebenen hoch: MacOS -> Contents -> .app -> Ordner daneben
            return os.path.dirname(os.path.dirname(os.path.dirname(exe_path)))
        else:
            return exe_path
    else:
        return os.path.dirname(__file__)


def get_app_path():
    """Gibt den Pfad zur .app selbst zurück"""
    if getattr(sys, 'frozen', False) and sys.platform == "darwin":
        exe_path = os.path.dirname(sys.executable)
        # 2 Ebenen hoch: MacOS -> Contents -> .app
        return os.path.dirname(os.path.dirname(exe_path))
    return None


def get_raw_url(user, repo, branch, filename):
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{filename}"


def get_release_url(user, repo, filename):
    """URL für GitHub Release Downloads"""
    return f"https://github.com/{user}/{repo}/releases/latest/download/{filename}"


def get_remote_version(user, repo, branch):
    url = get_raw_url(user, repo, branch, "version.txt")
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode().strip()
    except:
        return None


def get_local_version():
    version_path = os.path.join(get_base_path(), "version.txt")
    if os.path.exists(version_path):
        with open(version_path, "r") as f:
            return f.read().strip()
    return "0"


def download_app_zip(user, repo, zip_name, dest_path):
    """Lädt die neue .app als .zip von GitHub Releases"""
    url = get_release_url(user, repo, zip_name)
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
        with open(dest_path, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Fehler beim Download: {e}")
        return False


class UpdateWindow(ctk.CTk):
    def __init__(self, user, repo, branch, app_name):
        super().__init__()

        self.user = user
        self.repo = repo
        self.branch = branch
        self.app_name = app_name  # z.B. "MeineApp"
        self.update_done = False

        self.title("Update")
        self.geometry("400x180")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Update verfügbar!", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="Starte Download...")
        self.status.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=10)
        self.progress.set(0)

        thread = threading.Thread(target=self.run_update)
        thread.start()

    def run_update(self):
        base_path = get_base_path()
        zip_name = f"{self.app_name}.zip"
        zip_path = os.path.join(base_path, zip_name)

        # 1. ZIP downloaden
        self.status.configure(text="Lade Update herunter...")
        self.progress.set(0.2)

        if not download_app_zip(self.user, self.repo, zip_name, zip_path):
            self.status.configure(text="Download fehlgeschlagen!")
            self.after(2000, self.destroy)
            return

        self.progress.set(0.5)

        # 2. Alte .app löschen
        self.status.configure(text="Installiere Update...")
        old_app = get_app_path()
        if old_app and os.path.exists(old_app):
            shutil.rmtree(old_app)

        self.progress.set(0.7)

        # 3. ZIP entpacken
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_path)

        # 4. ZIP löschen
        os.remove(zip_path)

        # 5. version.txt updaten
        self.status.configure(text="Lade version.txt...")
        version_url = get_raw_url(self.user, self.repo, self.branch, "version.txt")
        version_path = os.path.join(base_path, "version.txt")
        try:
            with urllib.request.urlopen(version_url) as response:
                content = response.read()
            with open(version_path, "wb") as f:
                f.write(content)
        except:
            pass

        self.progress.set(1)
        self.status.configure(text="Update fertig! Bitte App neu starten.")
        self.update_done = True

        self.after(2500, self.destroy)


def check_for_updates(user, repo, branch, app_name):
    """
    app_name = Name der App ohne .app Endung, z.B. "MiniToolbox"
    Auf GitHub Releases muss eine Datei "MiniToolbox.zip" liegen
    """
    local_version = get_local_version()
    remote_version = get_remote_version(user, repo, branch)

    if remote_version is None:
        print("Konnte Version nicht prüfen (offline?)")
        return False

    print(f"Lokale Version: {local_version}")
    print(f"Remote Version: {remote_version}")

    if remote_version > local_version:
        app = UpdateWindow(user, repo, branch, app_name)
        app.mainloop()
        return True

    return False
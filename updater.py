import urllib.request
import os
import sys
import threading
import customtkinter as ctk


def get_base_path():
    if getattr(sys, 'frozen', False):
        # macOS .app Bundle: sys.executable liegt in MeineApp.app/Contents/MacOS/
        # Wir wollen den Ordner NEBEN der .app
        exe_path = os.path.dirname(sys.executable)
        if sys.platform == "darwin":
            # 3 Ebenen hoch: MacOS -> Contents -> .app -> Ordner daneben
            return os.path.dirname(os.path.dirname(os.path.dirname(exe_path)))
        else:
            # Windows .exe
            return exe_path
    else:
        # Normal in PyCharm
        return os.path.dirname(__file__)


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
    version_path = os.path.join(get_base_path(), "version.txt")
    if os.path.exists(version_path):
        with open(version_path, "r") as f:
            return f.read().strip()
    return "0"


def download_file(user, repo, branch, filename):
    url = get_raw_url(user, repo, branch, filename)
    filepath = os.path.join(get_base_path(), filename)
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
        with open(filepath, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Fehler beim Download von {filename}: {e}")
        return False


class UpdateWindow(ctk.CTk):
    def __init__(self, user, repo, branch, files):
        super().__init__()

        self.user = user
        self.repo = repo
        self.branch = branch
        self.files = files
        self.update_done = False

        self.title("Update")
        self.geometry("400x150")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Update verfügbar!", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="Starte Download...")
        self.status.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=10)
        self.progress.set(0)

        # Update in separatem Thread starten
        thread = threading.Thread(target=self.run_update)
        thread.start()

    def run_update(self):
        total = len(self.files) + 1  # +1 für version.txt

        for i, filename in enumerate(self.files):
            self.status.configure(text=f"Lade {filename}...")
            download_file(self.user, self.repo, self.branch, filename)
            self.progress.set((i + 1) / total)

        self.status.configure(text="Lade version.txt...")
        download_file(self.user, self.repo, self.branch, "version.txt")
        self.progress.set(1)

        self.status.configure(text="Update abgeschlossen!")
        self.update_done = True

        self.after(1500, self.destroy)


def check_for_updates(user, repo, branch, files):
    local_version = get_local_version()
    remote_version = get_remote_version(user, repo, branch)

    if remote_version is None:
        print("Konnte Version nicht prüfen (offline?)")
        return False

    print(f"Lokale Version: {local_version}")
    print(f"Remote Version: {remote_version}")

    if remote_version > local_version:
        # GUI starten
        app = UpdateWindow(user, repo, branch, files)
        app.mainloop()
        return True

    return False
import urllib.request
import os
import threading
import customtkinter as ctk


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
            success = download_file(self.user, self.repo, self.branch, filename)
            if success:
                print(f"✓ {filename} aktualisiert")
            self.progress.set((i + 1) / total)

        self.status.configure(text="Lade version.txt...")
        download_file(self.user, self.repo, self.branch, "version.txt")
        self.progress.set(1)

        self.status.configure(text="Update abgeschlossen!")
        self.update_done = True

        self.after(500, self.destroy)


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
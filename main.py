import os
import zipfile
import requests
import shutil
import sys
import tempfile
import customtkinter as ctk


# -----------------------------------------------------
#                 AUTO-UPDATER (OHNE GIT)
# -----------------------------------------------------
def updater():
    current_version = "1.0"   # <--- Hier deine Version eintragen

    GITHUB_OWNER = "Jakob707"
    GITHUB_REPO = "Papas-Geburtstag"

    print("🔍 Suche nach Updates...")

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    r = requests.get(url)

    if r.status_code != 200:
        print("⚠️ Konnte Release nicht abrufen.")
        return

    data = r.json()
    latest_version = data["tag_name"]

    print(f"Aktuelle Version: {current_version}")
    print(f"Neueste Version:  {latest_version}")

    if latest_version == current_version:
        print("✅ Programm ist aktuell.")
        return

    print("⬇️ Update verfügbar! Lade ZIP herunter...")

    asset_url = data["assets"][0]["browser_download_url"]

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "update.zip")

    # ZIP herunterladen
    with requests.get(asset_url, stream=True) as res:
        res.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)

    print("📦 Entpacke Update...")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(temp_dir)

    print("🔁 Überschreibe Dateien...")

    extracted_folder = [
        f for f in os.listdir(temp_dir)
        if f != "update.zip"
    ][0]

    extract_path = os.path.join(temp_dir, extracted_folder)

    # Dateien kopieren
    for root, dirs, files in os.walk(extract_path):
        rel = os.path.relpath(root, extract_path)
        dest = os.path.join(os.getcwd(), rel)

        if not os.path.exists(dest):
            os.makedirs(dest)

        for file in files:
            shutil.copy(os.path.join(root, file), os.path.join(dest, file))

    print("✅ Update installiert!")
    print("🔄 Starte Programm neu...")

    os.execv(sys.executable, [sys.executable] + sys.argv)


# -----------------------------------------------------
#                DEINE GESAMTE CTk-APP
# -----------------------------------------------------
def main_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("800x800")

    # ----------------- Seitenklassen -----------------
    class MainPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            label = ctk.CTkLabel(self, text="Test222???")
            label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            button = ctk.CTkButton(
                self,
                text="Done",
                command=lambda: show_page(end_page)
            )
            button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    class EndPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            label = ctk.CTkLabel(self, text="Test!")
            label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            back_btn = ctk.CTkButton(
                self,
                text="Back",
                command=lambda: show_page(main_page)
            )
            back_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    # ----------------- Seiten erstellen -----------------
    main_page = MainPage(root)
    end_page = EndPage(root)

    for page in (main_page, end_page):
        page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(page):
        page.tkraise()

    show_page(main_page)

    root.mainloop()


# -----------------------------------------------------
#               PROGRAMMSTART
# -----------------------------------------------------
if __name__ == "__main__":
    updater()     # <-- Check & install updates
    main_app()    # <-- Start GUI

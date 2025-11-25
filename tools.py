def run_tools():
    import customtkinter as ctk
    from typing import Union, Callable

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme('blue')

    root = ctk.CTk()
    root.geometry("800x800")
    root.title("MiniToolbox")

    class FloatSpinbox(ctk.CTkFrame):
        def __init__(self, *args,
                     width: int = 100,
                     height: int = 32,
                     step_size: Union[int, float] = 1,
                     command: Callable = None,
                     **kwargs):
            super().__init__(*args, width=width, height=height, **kwargs)

            self.step_size = step_size
            self.command = command

            self.configure(fg_color=("gray78", "gray28"))

            self.grid_columnconfigure((0, 2), weight=0)
            self.grid_columnconfigure(1, weight=1)

            self.subtract_button = ctk.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                           command=self.subtract_button_callback)
            self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

            self.entry = ctk.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
            self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

            self.add_button = ctk.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                                      command=self.add_button_callback)
            self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

            self.entry.insert(0, "0.0")

        def add_button_callback(self):
            if self.command is not None:
                self.command()
            try:
                value = float(self.entry.get()) + self.step_size
                if value > 60:
                    value = 60
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

        def subtract_button_callback(self):
            if self.command is not None:
                self.command()
            try:
                value = float(self.entry.get()) - self.step_size
                if value < 1:
                    value = 1
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

        def get(self) -> Union[float, None]:
            try:
                return float(self.entry.get())
            except ValueError:
                return None

        def set(self, value: float):
            self.entry.delete(0, "end")
            self.entry.insert(0, str(float(value)))

    class MainPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)


            def dateien_card():

                def organize():
                    import shutil
                    import tkinter as tk
                    from tkinter import messagebox, scrolledtext
                    from pathlib import Path

                    quelle_ordner = [
                        Path.home() / "Downloads",
                        Path.home() / "Desktop",
                        Path.home() / "Documents",
                        Path("/Users/krudi/Dokumente Rudi")
                    ]

                    ziel_basisordner = Path("/Users/krudi/Dokumente Rudi")
                    verschiebungen = []

                    bekannte_kategorien = {
                        "Bilder", "Videos", "Code", "ZIPs", "MP3s", "Text", "PKGs", "DMGs", "JARs", "RTFs"
                    }

                    interessante_endungen = {
                        ".png", ".jpg", ".jpeg", ".mov", ".txt", ".jar", ".zip", ".py", ".html",
                        ".css", ".js", ".swift", ".xcodeproj", ".dmg", ".pkg", ".pdf", ".pages",
                        ".yml", ".mp4", ".mp3", ".json", ".rtf"
                    }

                    def zielordner_fuer_endung(endung):
                        if endung in [".png", ".jpg", ".jpeg", ".heic"]:
                            return "Bilder"
                        elif endung in [".mp4", ".mov"]:
                            return "Videos"
                        elif endung in [".txt", ".pdf", ".pages", ".rtf"]:
                            return "Text"
                        elif endung == ".jar":
                            return "JARs"
                        elif endung == ".zip":
                            return "ZIPs"
                        elif endung in [".py", ".html", ".css", ".js", ".swift", ".xcodeproj", ".yml", ".json"]:
                            return "Code"
                        elif endung == ".dmg":
                            return "DMGs"
                        elif endung == ".pkg":
                            return "PKGs"
                        elif endung == ".mp3":
                            return "MP3s"
                        else:
                            return None

                    def log(msg):
                        log_box.insert(tk.END, msg + '\n')
                        log_box.see(tk.END)
                        organize_window.update_idletasks()

                    def sortiere_dateien_in_ordner(ordner: Path):
                        for datei in ordner.rglob("*"):
                            if datei.is_file():
                                zielname = zielordner_fuer_endung(datei.suffix.lower())
                                if zielname:
                                    ziel = ziel_basisordner / zielname
                                    ziel.mkdir(parents=True, exist_ok=True)
                                    zielpfad = ziel / datei.name
                                    verschiebungen.append((zielpfad, datei))
                                    shutil.move(str(datei), str(zielpfad))
                                    log(f"📦 Sortiert: {datei.name} → {ziel}")
                        versuche_ordner_und_leere_eltern_zu_loeschen(ordner)

                    def versuche_ordner_und_leere_eltern_zu_loeschen(ordner: Path):
                        try:
                            while ordner != ordner.parent and not any(ordner.iterdir()):
                                ordner.rmdir()
                                log(f"🗑️  Leerer Ordner gelöscht: {ordner}")
                                ordner = ordner.parent
                        except Exception:
                            pass

                    def verschiebe_ordner(ordner: Path):
                        for eintrag in ordner.iterdir():
                            if eintrag.is_dir():
                                ordnername = eintrag.name
                                ziel = ziel_basisordner / ordnername

                                if ordnername in bekannte_kategorien:
                                    if ziel.exists():
                                        log(f"❗ Zielordner '{ziel}' existiert – übersprungen.")
                                        continue
                                    shutil.move(str(eintrag), str(ziel))
                                    verschiebungen.append((ziel, eintrag))
                                    log(f"📁 Auto-Verschoben: {eintrag} → {ziel}")
                                else:
                                    if not str(eintrag.resolve()).startswith(str(ziel_basisordner)):
                                        zeige_auswahl_dialog(eintrag)

                    def verschiebe_einzeldateien(ordner: Path):
                        for datei in ordner.iterdir():
                            if datei.is_file():
                                zielname = zielordner_fuer_endung(datei.suffix.lower())
                                if zielname:
                                    zielordner = ziel_basisordner / zielname
                                    zielordner.mkdir(parents=True, exist_ok=True)
                                    zielpfad = zielordner / datei.name
                                    verschiebungen.append((zielpfad, datei))
                                    shutil.move(str(datei), str(zielpfad))
                                    log(f"📄 Datei verschoben: {datei.name} → {zielordner}")

                    def rueckgaengig():
                        if not verschiebungen:
                            messagebox.showinfo("Rückgängig", "Keine Verschiebungen rückgängig zu machen.")
                            return
                        for ziel, original in reversed(verschiebungen):
                            if ziel.exists():
                                try:
                                    shutil.move(str(ziel), str(original))
                                    log(f"🔁 Zurück: {ziel.name} → {original}")
                                except Exception as e:
                                    log(f"⚠️ Fehler beim Zurückverschieben: {ziel} → {original} | {e}")
                            versuche_ordner_und_leere_eltern_zu_loeschen(ziel.parent)
                        verschiebungen.clear()
                        log("✅ Alle Verschiebungen rückgängig gemacht.")

                    def alles_starten():
                        log_box.delete(1.0, tk.END)
                        for ordner in quelle_ordner:
                            verschiebe_ordner(ordner)
                            verschiebe_einzeldateien(ordner)
                        log("✅ Sortierung abgeschlossen.")

                    def zeige_auswahl_dialog(eintrag: Path):
                        dialog = tk.Toplevel(organize_window)
                        dialog.title(f"Ordner: {eintrag.name}")
                        tk.Label(dialog, text=f"Was tun mit: {eintrag.name}?").pack(pady=10)

                        def aktion_1():
                            ziel = ziel_basisordner / eintrag.name
                            if ziel.exists():
                                log(f"❗ Ziel '{ziel}' existiert – übersprungen.")
                            else:
                                shutil.move(str(eintrag), str(ziel))
                                verschiebungen.append((ziel, eintrag))
                                log(f"📁 Ordner verschoben: {eintrag} → {ziel}")
                            dialog.destroy()

                        def aktion_2():
                            sortiere_dateien_in_ordner(eintrag)
                            dialog.destroy()

                        def aktion_3():
                            log(f"⏭️  Ordner übersprungen: {eintrag.name}")
                            dialog.destroy()

                        tk.Button(dialog, text="1️⃣ Ordner verschieben", width=30, command=aktion_1).pack(pady=5)
                        tk.Button(dialog, text="2️⃣ Nur Inhalt sortieren", width=30, command=aktion_2).pack(pady=5)
                        tk.Button(dialog, text="3️⃣ Nichts tun", width=30, command=aktion_3).pack(pady=5)

                    organize_window = tk.Tk()
                    organize_window.title("🗂️ Dateien-Organiser")
                    organize_window.geometry("425x280")

                    tk.Button(organize_window, text="🚀 Sortieren starten", command=alles_starten, bg="lightgreen").pack(pady=10)
                    tk.Button(organize_window, text="↩️ Rückgängig", command=rueckgaengig, bg="lightblue").pack(pady=5)

                    log_box = scrolledtext.ScrolledText(organize_window, width=100, height=30)
                    log_box.pack(padx=10, pady=10)

                    organize_window.mainloop()

                card = ctk.CTkFrame(self, corner_radius=10)
                card.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")

                detein_card_label = ctk.CTkLabel(master=card, text="Dateien Sortierer")
                detein_card_label.grid(column=0, row=0, sticky="w", padx=20, pady=10)

                button = ctk.CTkButton(master=card, text="Sortieren!", command=organize)
                button.grid(row=1, column=0, padx=20, pady=5)

            def pass_gen_card():
                import random


                def generate():
                    avalible_characters = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h',
                                           'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O',
                                           'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w',
                                           'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                                           '8', '9', '!', '@', '#', '$', '%', '*', '?', '-', '_', '+', '=', '(', ')']
                    password_list = []

                    import tkinter as tk

                    length = int(pas_length_input.get())

                    for _ in range(length):
                        choice = random.choice(avalible_characters)
                        avalible_characters.remove(choice)
                        password_list.append(choice)

                    password = "".join(password_list)

                    copy = tk.Tk()
                    copy.withdraw()
                    copy.clipboard_clear()
                    copy.clipboard_append(f'{password}')
                    copy.update()
                    copy.destroy()

                card = ctk.CTkFrame(self, corner_radius=10)
                card.grid(column=1, row=0, padx=20, pady=20, sticky="nsew")

                pass_gen_label = ctk.CTkLabel(master=card, text="Passwort Generator")
                pass_gen_label.grid(column=0, row=0, sticky="w", padx=20, pady=10)

                pas_length_input = FloatSpinbox(card, width=150, step_size=1)
                pas_length_input.grid(column=0, row=1, padx=20, pady=5)

                pas_length_input.set(12)

                button = ctk.CTkButton(master=card, text="In Zwischenablage kopieren", command=generate)
                button.grid(column=0, row=2, padx=20, pady=5)

            dateien_card()
            pass_gen_card()

    main_page = MainPage(root)
    main_page.place(relx=0, rely=0, relwidth=1, relheight=1)

    root.mainloop()

run_tools()
# -------------------------
# Updater importieren
# -------------------------
from updater import check_for_updates

# -------------------------
# App starten
# -------------------------
def main_app():
    print("🚀 Starte Hauptprogramm…")

    import customtkinter as ctk

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme('blue')

    root = ctk.CTk()
    root.geometry("800x400")

    class MainPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            label = ctk.CTkLabel(master=self, text="Test!")
            label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            def button_function():
                end_page = EndPage(master)
                end_page.place(relx=0, rely=0, relwidth=1, relheight=1)
                end_page.tkraise()

            button = ctk.CTkButton(master=self, text="Done", command=button_function)
            button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    class EndPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)

            def back():
                end_page = EndPage(master)
                end_page.place(relx=0, rely=0, relwidth=1, relheight=1)
                end_page.tkraise()

            self.welcome_text = ctk.CTkLabel(master=self, text=f"Test!")
            self.welcome_text.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

            self.back_button = ctk.CTkButton(master=self, text="Back", command=back)
            self.back_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    main_page = MainPage(root)
    main_page.place(relx=0, rely=0, relwidth=1, relheight=1)

    root.mainloop()


if __name__ == "__main__":
    # 1️⃣ Prüfe auf Updates
    try:
        check_for_updates()
    except Exception as e:
        print("⚠️ Update konnte nicht geprüft werden:", e)

    # 2️⃣ Starte die eigentliche App
    main_app()

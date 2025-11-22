def run_tools():
    print("Verfügbare Tools:")
    print("1. Beispiel-Tool")
    print("0. Beenden")

    while True:
        choice = input("\nAuswahl: ")

        if choice == "1":
            beispiel_tool()
        elif choice == "0":
            print("Tschüss!")
            break
        else:
            print("Ungültige Auswahl")


def beispiel_tool():
    print("Das ist ein Beispiel-Tool!")
    # Hier deine Logik
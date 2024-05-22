# gui_components.py

from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage
from main_settings import create_einstellungen_window, load_config
from PIL import Image
from pathlib import Path

# Basisordner für die Soundpacks
BASE_FOLDER = Path('./soundpacks')


# Funktion zum Anzeigen des spezifischen Menüs einer Fluggesellschaft
def show_airline_menu(root, main_frame, airline):
    from sound_lufthansa import show_airline_soundpack
    show_airline_soundpack(root, main_frame, BASE_FOLDER, airline)


# Funktion zum Erstellen eines Buttons
def create_button(main_frame, text, function, button_color):
    hover_color = darken_color(button_color)
    button = CTkButton(main_frame, text=text, corner_radius=15, fg_color=button_color, hover_color=hover_color,
                       text_color="#ffffff", width=300, height=50, command=function)
    button.pack(side="top", padx=20, pady=10)
    return button


# Funktion zum Dunkeln einer Farbe
def darken_color(hex_color, amount=0.1):
    """Dunkelt eine Hex-Farbe um den angegebenen Prozentsatz ab."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * (1 - amount))) for c in rgb)
    return f"#{''.join(f'{c:02x}' for c in darkened)}"


# Hauptfenster erstellen
def create_main_window():
    root = CTk()
    root.title("Passenger Announcements")
    root.config(bg="#333333")
    root.geometry("430x650")

    # Haupt-Frame erstellen
    main_frame = CTkFrame(root, bg_color="#333333")
    main_frame.pack(fill="both", expand=True)

    # Benutzerdefinierte Menüleiste erstellen
    menubar_frame = CTkFrame(main_frame, height=30, bg_color="#222222", corner_radius=0)
    menubar_frame.pack(side="top", fill="x")

    # Hauptknöpfe für jede Fluggesellschaft dynamisch erstellen
    config = load_config()
    button_color = config.get("button_color", "#3498DB")
    airlines_dir = BASE_FOLDER
    airline_dirs = [f.name for f in airlines_dir.iterdir() if f.is_dir()]

    buttons = []
    for airline in airline_dirs:
        button = create_button(main_frame, airline.capitalize(),
                               lambda a=airline: show_airline_menu(root, main_frame, a), button_color)
        buttons.append(button)

    # Einstellungsfenster-Button
    einstellungen_button = CTkButton(menubar_frame, text="Einstellungen", fg_color="#222222", hover_color="#444444",
                                     text_color="#ffffff", command=lambda: create_einstellungen_window(buttons),
                                     corner_radius=0)
    einstellungen_button.pack(side="left", padx=2, pady=2)

    # Neues SoundPack Hinzufügen
    soundpack_hinzufuegen_button = CTkButton(menubar_frame, text="Soundpack Hinzufügen", fg_color="#222222",
                                            hover_color="#444444", text_color="#ffffff",
                                            command=lambda: print("Soundpack hinzufügen"), corner_radius=0)
    soundpack_hinzufuegen_button.pack(side="left", padx=2, pady=2)

    # Support-Button
    support_button = CTkButton(menubar_frame, text="Support", fg_color="#222222", hover_color="#444444",
                               text_color="#ffffff", command=lambda: print("Support aufgerufen"), corner_radius=0)
    support_button.pack(side="right", padx=2, pady=2)

    # PNG-Bild am unteren Teil des Hauptfensters hinzufügen
    def add_image(frame, image_path, width, height):
        image = Image.open(image_path).resize((width, height), Image.Resampling.LANCZOS)
        photo = CTkImage(light_image=image, dark_image=image, size=(width, height))
        label = CTkLabel(frame, image=photo, text="")
        label.pack(side="bottom", pady=10)

    # Pfad zur PNG-Datei im selben Verzeichnis wie die main.py und Größe anpassen
    image_path = "./images/hintergrund.png"
    add_image(main_frame, image_path, width=400, height=189)  # Beispielgröße: 300x150

    root.mainloop()


# Beispiel für die Verwendung der Funktion
if __name__ == "__main__":
    create_main_window()

from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage
from main_settings import create_einstellungen_window, load_config
from sound_lufthansa import show_sound_lufthansa
from PIL import Image


def funktion1():
    show_sound_lufthansa(root, main_frame)


def funktion2():
    print("Condor aufgerufen")


def funktion3():
    print("TUI aufgerufen")


def funktion4():
    print("TAP Portugal aufgerufen")


def funktion5():
    print("Eurowings aufgerufen")


def create_button(main_frame, text, function, button_color):
    hover_color = darken_color(button_color)
    button = CTkButton(main_frame, text=text, corner_radius=15, fg_color=button_color, hover_color=hover_color,
                       text_color="#ffffff",
                       width=300, height=50, command=function)
    button.pack(side="top", padx=20, pady=10)
    return button


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

# Hauptknöpfe erstellen
buttons = []
button_texts = ["Lufthansa", "Condor", "TUI", "TAP Portugal", "Eurowings"]
functions = [funktion1, funktion2, funktion3, funktion4, funktion5]

# Konfiguration laden
config = load_config()
button_color = config.get("button_color", "#3498DB")


def darken_color(hex_color, amount=0.1):
    """Dunkelt eine Hex-Farbe um den angegebenen Prozentsatz ab."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * (1 - amount))) for c in rgb)
    return f"#{''.join(f'{c:02x}' for c in darkened)}"


hover_color = darken_color(button_color)

buttons = []
for i in range(5):
    button = create_button(main_frame, button_texts[i], functions[i], button_color)
    buttons.append(button)

# Einstellungsfenster-Button
einstellungen_button = CTkButton(menubar_frame, text="Einstellungen", fg_color="#222222", hover_color="#444444",
                                 text_color="#ffffff",
                                 command=lambda: create_einstellungen_window(buttons), corner_radius=0)
einstellungen_button.pack(side="left", padx=2, pady=2)

# Neues SoundPack Hinzufügen
soundpack_hinzufügen_button = CTkButton(menubar_frame, text="Soundpack Hinzufügen", fg_color="#222222",
                                        hover_color="#444444", text_color="#ffffff",
                                        command=lambda: print("Soundpack hinzufügen"), corner_radius=0)
soundpack_hinzufügen_button.pack(side="left", padx=2, pady=2)

# Support-Button
support_button = CTkButton(menubar_frame, text="Support", fg_color="#222222", hover_color="#444444",
                           text_color="#ffffff",
                           command=lambda: print("Support aufgerufen"), corner_radius=0)
support_button.pack(side="right", padx=2, pady=2)


# PNG-Bild am unteren Teil des Hauptfensters hinzufügen
def add_image(frame, image_path, width, height):
    image = Image.open(image_path).resize((width, height), Image.Resampling.LANCZOS)
    photo = CTkImage(light_image=image, dark_image=image, size=(width, height))
    label = CTkLabel(frame, image=photo, text="")
    label.pack(side="bottom", pady=10)


# Pfad zur PNG-Datei im selben Verzeichnis wie die main.py und Größe anpassen
image_path = "hintergrund.png"
add_image(main_frame, image_path, width=400, height=189)  # Beispielgröße: 300x150

root.mainloop()
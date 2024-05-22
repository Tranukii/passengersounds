import json
from customtkinter import CTkToplevel, CTkLabel, CTkButton, CTkFrame, CTkCheckBox

CONFIG_FILE = "config.json"


# Funktion zum Speichern der Konfiguration in eine Datei
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


# Funktion zum Laden der Konfiguration aus einer Datei
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Initialisiere die Konfiguration
config = load_config()

# Funktion zum Erstellen des Einstellungsfensters
def create_einstellungen_window(main_buttons):
    def on_color_chosen(color):
        config["button_color"] = color
        save_config(config)
        for button in main_buttons:
            button.configure(fg_color=color, hover_color=darken_color(color))
        close_button.configure(fg_color=color, hover_color=darken_color(color))
        print(f"Gewählte Farbe: {color}")

    def darken_color(hex_color, amount=0.1):
        """Dunkelt eine Hex-Farbe um den angegebenen Prozentsatz ab."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (1 - amount))) for c in rgb)
        return f"#{''.join(f'{c:02x}' for c in darkened)}"

    # Moderne Farben
    modern_colors = ["#be2edd", "#FF5733", "#FF8D1A", "#6ab04c", "#3380FF"]

    einstellungsfenster = CTkToplevel()
    einstellungsfenster.attributes("-topmost", True)
    einstellungsfenster.title("Einstellungen")
    einstellungsfenster.geometry("430x200")

    def create_checkboxes(parent_frame):
        checkbox_frame = CTkFrame(parent_frame)

        # Checkbox: Mit Flugsimulator verbinden
        flight_sim_checkbox = CTkCheckBox(checkbox_frame, text="Mit Flugsimulator verbinden")
        flight_sim_checkbox.grid(row=0, column=0, padx=10)

        # Checkbox: Joystickeingaben benutzen
        joystick_checkbox = CTkCheckBox(checkbox_frame, text="Joystickeingaben benutzen")
        joystick_checkbox.grid(row=0, column=1, padx=10)

        return checkbox_frame

    # Checkbox-Frame erstellen
    checkbox_frame = create_checkboxes(einstellungsfenster)
    checkbox_frame.pack(side="bottom", pady=20)


    # Farbauswahl für die Knöpfe
    label = CTkLabel(einstellungsfenster, text="Farbe Auswählen:")
    label.pack(pady=10)

    # Frame für die Farbknöpfe
    colors_frame = CTkFrame(einstellungsfenster)
    colors_frame.pack(pady=10)

    # Erstellen der Knöpfe
    for color in modern_colors:
        button = CTkButton(
            colors_frame,
            width=40,
            height=40,
            fg_color=color,
            text="",
            command=lambda c=color: on_color_chosen(c)
        )
        button.pack(side="left", padx=8, pady=8)

    # Schließen Knopf
    close_button = CTkButton(
        einstellungsfenster,
        text="Schließen",
        command=einstellungsfenster.destroy,
        fg_color=config.get("button_color", "#3498DB"),
        hover_color=darken_color(config.get("button_color", "#3498DB"))
    )
    close_button.pack(pady=20)

    return einstellungsfenster
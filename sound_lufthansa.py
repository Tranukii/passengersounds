import json
from pathlib import Path
import pygame
import tkinter as tk
from tkinter import ttk
from customtkinter import CTkFrame, CTkButton, CTkLabel

from utils.gui_components import darken_color

# Initialisiere pygame für das Abspielen der Sounds
pygame.mixer.init()

# Basisordner für die Soundpacks und Konfigurationsdateien
BASE_FOLDER = Path('./soundpacks')
CONFIG_PATH = Path('./config.json')  # Pfad zur config.json im Hauptverzeichnis


# Farben aus der config.json laden
def load_button_color(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config.get("button_color", "#3380FF")


# Sounddateien aus dem angegebenen Verzeichnis laden
def get_sound_files(base_folder, airline, aircraft_model):
    directory = base_folder / airline / aircraft_model
    if not directory.exists():
        print(f"Directory {directory} does not exist")
        return []
    return [f for f in directory.iterdir() if f.suffix == '.wav']


# Namen aus der spezifischen names.json Datei laden
def load_names(base_folder, airline, aircraft_model):
    names_path = base_folder / airline / aircraft_model / 'names.json'
    if not names_path.exists():
        print(f"Names file {names_path} does not exist")
        return {}
    with open(names_path, 'r') as names_file:
        return json.load(names_file)


def get_aircraft_types(base_folder, airline):
    soundpack_dir = base_folder / airline
    return [f.name for f in soundpack_dir.iterdir() if f.is_dir()]


# Hauptfunktion zum Anzeigen des Airline-Soundpacks
def show_airline_soundpack(root, main_frame, base_folder, airline):
    # Verstecke das Haupt-Frame
    main_frame.pack_forget()

    # Erstelle ein neues Frame für das Menü
    menu_frame = CTkFrame(root, width=800, height=600, corner_radius=15)
    menu_frame.pack(fill="both", expand=True)

    def update_button_color():
        button_color = load_button_color(CONFIG_PATH)
        back_button.configure(fg_color=button_color)
        for button in sound_buttons:
            button.configure(fg_color=button_color)
        root.after(10000, update_button_color)

    def back_to_main():
        menu_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)

    def sound_airline_playbuttons(aircraft_model):
        # Lösche vorhandene Buttons
        for button in sound_buttons:
            button.destroy()
        sound_buttons.clear()

        # Lade die Sounddateien und Namen
        sound_files = get_sound_files(base_folder, airline, aircraft_model)
        names_config = load_names(base_folder, airline, aircraft_model)

        sorted_files = sorted(names_config.items(), key=lambda x: int(x[0]))
        sound_files = [item['filename'] for key, item in sorted_files]
        display_names = [item['display_name'] for key, item in sorted_files]

        col = 0
        row = 0
        max_per_column = 8
        num_columns = (len(sound_files) // max_per_column) + 1
        for index, (sound_file, display_name) in enumerate(zip(sound_files, display_names)):
            if index != 0 and index % max_per_column == 0:
                col += 1
                row = 0
            hover_color = darken_color(load_button_color(CONFIG_PATH))
            button = CTkButton(sound_buttons_frame, text=display_name, fg_color=load_button_color(CONFIG_PATH),
                               hover_color=hover_color, command=lambda sf=sound_file: play_sound(aircraft_model, sf))
            button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            sound_buttons.append(button)
            row += 1

        # Adjust the column weights to be equal, making buttons symmetrically distributed
        for i in range(num_columns):
            sound_buttons_frame.grid_columnconfigure(i, weight=1)

        # Center buttons if only one column
        if num_columns == 1:
            sound_buttons_frame.grid_columnconfigure(0, weight=1)
            sound_buttons_frame.grid_columnconfigure(1, weight=1)

    def play_sound(aircraft_model, sound_file):
        # Hier den Code einfügen, um den entsprechenden Sound abzuspielen
        sound_path = base_folder / airline / aircraft_model / sound_file
        print(f"Playing {sound_path}")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

    def on_aircraft_model_selected(event):
        selected_model = aircraft_combobox.get()
        sound_airline_playbuttons(selected_model)

    # Überschrift
    label = CTkLabel(menu_frame, text=airline.capitalize(), text_color="#ffffff", font=("Open Sans", 24))
    label.pack(pady=20)

    # Frame für das Dropdown-Menü und das Label
    top_frame = CTkFrame(menu_frame)
    top_frame.pack(pady=20)

    # Label: Modell auswählen
    model_label = CTkLabel(top_frame, text="Modell auswählen", text_color="#ffffff")
    model_label.grid(row=0, column=0, padx=10)

    # Dropdown-Menü für die Flugzeugtypen
    aircraft_types = get_aircraft_types(base_folder, airline)
    selected_aircraft = tk.StringVar()
    aircraft_combobox = ttk.Combobox(top_frame, values=aircraft_types, textvariable=selected_aircraft, state="readonly")
    if aircraft_types:
        aircraft_combobox.set(aircraft_types[0])
    aircraft_combobox.grid(row=0, column=1, padx=10)
    aircraft_combobox.bind("<<ComboboxSelected>>", on_aircraft_model_selected)

    # Frame für die Sound-Knöpfe
    sound_buttons_frame = CTkFrame(menu_frame, width=800, height=600, corner_radius=15)
    sound_buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Liste der Sound-Knöpfe für spätere Farbanpassung
    sound_buttons = []

    # Initiale Sound-Knöpfe für das erste Modell
    if aircraft_types:
        sound_airline_playbuttons(aircraft_types[0])

    # Volume Slider


    # Back Button
    hover_color = darken_color(load_button_color(CONFIG_PATH))
    back_button = CTkButton(menu_frame, text="Zurück", command=back_to_main, fg_color=load_button_color(CONFIG_PATH), hover_color=hover_color)
    back_button.pack(side="bottom", pady=10)

    # Dynamische Aktualisierung der Button-Farbe
    root.after(10000, update_button_color)

    root.mainloop()
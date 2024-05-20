import pygame
import time

# Konfigurationsdaten als Python-Dictionary festlegen
config = {
    "10": "Button A",
    "11": "Button B",
    "12": "Button X"
}


def check_joystick(config):
    # Initialisiere Pygame
    pygame.init()

    # Überprüfe die Anzahl der Joysticks
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("Es ist kein Joystick angeschlossen.")
        return

    # Initialisiere den ersten Joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Joystick gefunden und initialisiert.")

    # Verfolge den Zustand der gedrückten Tasten
    button_pressed = {}

    # Kontinuierlich die Tasten überprüfen
    while True:
        pygame.event.pump()

        # Überprüfe die Tasten
        num_buttons = joystick.get_numbuttons()
        for button_id, button_key in config.items():
            if button_id.isdigit() and int(button_id) < num_buttons:
                # Überprüfe, ob die Taste gedrückt ist und sie noch nicht als gedrückt erkannt wurde
                if joystick.get_button(int(button_id)) and not button_pressed.get(button_id):
                    print(f"Taste {button_id} ({button_key}) wurde betätigt.")
                    button_pressed[button_id] = True
                # Überprüfe, ob die Taste nicht mehr gedrückt ist und setze den Zustand zurück
                elif not joystick.get_button(int(button_id)):
                    button_pressed[button_id] = False

        time.sleep(0.5)  # Füge eine kleine Verzögerung ein, um die CPU nicht zu belasten


if __name__ == "__main__":
    check_joystick(config)

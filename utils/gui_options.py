# Hinzufügen von Lautstärkeregler
import pygame
from customtkinter import CTkSlider


# Funktion zum Festlegen der Lautstärke
def set_volume(value):
    volume = int(value) / 100
    pygame.mixer.music.set_volume(value)


# Lautstärkeinstellungen
volume_slider = CTkSlider(master=None, from_=0, to=100, number_of_steps=100, orientation="horizontal", command=set_volume)
volume_slider.set(50)
volume_slider.pack(pady=10, padx=10, fill="x")






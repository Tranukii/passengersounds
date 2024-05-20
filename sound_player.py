# sound_player.py

import pygame
import os

class SoundPlayer:
    def __init__(self, soundpack_path):
        pygame.mixer.init()
        self.soundpack_path = soundpack_path

    def play_sound(self, sound_name):
        sound_path = os.path.join(self.soundpack_path, sound_name)
        if os.path.exists(sound_path):
            pygame.mixer.Sound(sound_path).play()
        else:
            print(f"Sound '{sound_name}' not found.")

    def stop_all_sounds(self):
        pygame.mixer.stop()
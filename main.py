# main.py

from utils.config_loader import load_config
from sound_player import SoundPlayer

def main():
    config = load_config('configs/config.json')
    airline = config.get('current_airline', 'default')
    soundpack_path = f"soundpacks/{airline}/Standard"

    player = SoundPlayer(soundpack_path)
    player.play_sound('sound1.wav')

if __name__ == "__main__":
    main()
import sys
from pathlib import Path
from utils.gui_components import create_main_window

# Füge das Verzeichnis utils zum Python-Pfad hinzu
utils_path = Path(__file__).resolve().parent / 'utils'
sys.path.append(str(utils_path))

if __name__ == "__main__":
    create_main_window()
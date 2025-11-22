import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_FOLDER = os.path.join(BASE_DIR, "audios")

if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
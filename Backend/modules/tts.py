import os
import requests
import uuid
from modules.config import AUDIO_FOLDER

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE_ID = "SmgKjOvC1aIujLWcMzqq"  
ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")

def text_to_speech(text: str) -> str:

    filename = f"{uuid.uuid4()}.mp3"
    output_file = os.path.join(AUDIO_FOLDER, filename)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.90,
            "similarity_boost": 0.81,
            "speed": 1.06
        }
    }

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("Error en ElevenLabs:", response.text)
        return "error"

    with open(output_file, "wb") as f:
        f.write(response.content)

    return filename
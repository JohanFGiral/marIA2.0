import os
import requests

ELEVEN_API_KEY = "sk_3ddf8d54679741a23ed5a259658c1470901f75aa0bd01a79"
VOICE_ID = "SmgKjOvC1aIujLWcMzqq"  
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
AUDIO_FOLDER = os.path.join(BASE_DIR, "audios")  
OUTPUT_FILE = os.path.join(AUDIO_FOLDER, "respuesta.mp3")

def text_to_speech(text):
    
    folder = os.path.dirname(OUTPUT_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

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
        return None

    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)

    return "respuesta.mp3"
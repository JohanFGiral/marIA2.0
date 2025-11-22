from flask import Flask, request, jsonify, send_from_directory
import os
from modules import hugging_face, tts
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audios")

@app.route('/')
def inicio():
    return 'Bienvenido a Flask'

@app.route('/send', methods=['POST'])
def message():
    user_message = request.json.get("mensaje")
    
    if not user_message:
        return jsonify({"Error": "No se envio el mensaje"}), 400
    
    respuesta = hugging_face.send_messages(user_message)
    
    audio_filename = tts.text_to_speech(respuesta)
    host_url = request.host_url
    print("Audio generado:", audio_filename)

    return jsonify({
        "respuesta": respuesta,
        "audio_url": f"{host_url}audio/{audio_filename}"
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    print("Buscando archivo en:", AUDIO_FOLDER, "archivo:", filename)
    return send_from_directory(AUDIO_FOLDER, filename)

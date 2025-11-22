from flask import Flask, request, jsonify, send_from_directory
import os
from modules import hugging_face, tts
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://127.0.0.1:5500",
    "https://marIA2.0.github.io",
    "http://localhost:5500"  # por si usas localhost en vez de 127.0.0.1
])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(BASE_DIR, "audios")
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
# FRONTEND_DIR = carpeta Frontend al mismo nivel que Backend
FRONTEND_DIR = os.path.join(BASE_DIR, '..','..' ,'Frontend')  

@app.route('/')
def inicio():
    html_path = os.path.join(FRONTEND_DIR, 'MarIA.html')
    if not os.path.exists(html_path):
        return f"Archivo no encontrado en: {html_path}", 404
    return send_from_directory(FRONTEND_DIR, 'MarIA.html')

@app.route('/<path:path>')
def frontend_files(path):
    file_path = os.path.join(FRONTEND_DIR, path)
    if not os.path.exists(file_path):
        return f"Archivo no encontrado: {file_path}", 404
    return send_from_directory(FRONTEND_DIR, path)
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

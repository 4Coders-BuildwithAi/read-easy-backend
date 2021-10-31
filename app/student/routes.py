from flask import Blueprint, jsonify, request, abort
from gtts import gTTS
student = Blueprint("student", __name__)

@student.route("/tts", methods=["POST"])
def tts():
    word = request.get_json()["word"]
    # Text to Speech
    
    tts = gTTS(text=word, lang="en")
    tts.save("tts.mp3")
    return jsonify({"message": "success"})
    
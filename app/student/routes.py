from flask import Blueprint, jsonify, request, abort
from gtts import gTTS

import PyPDF2

from app.db.schema import Course 




student = Blueprint("student", __name__)


@student.route("/tts", methods=["POST"])
def tts():
    word = request.get_json()["word"]
    # Text to Speech

    tts = gTTS(text=word, lang="en")
    tts.save("tts.mp3")
    return jsonify({"message": "success"})


@student.route("/getallcourse", methods=["GET"])
def getallcourse():
    result = Course.query.all()
    courses = [course.format_short() for course in result]
    
    return jsonify({"message": "success","courses": courses})


@student.route("/course/<int:id>", methods=["GET"])
def getcourse(id):
    course = Course.query.filter(Course.id == id).first()
    return jsonify({"message": "success","course": course.format()})






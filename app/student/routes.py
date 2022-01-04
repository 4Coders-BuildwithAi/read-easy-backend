from flask import Blueprint, jsonify, request, abort
from gtts import gTTS

import PyPDF2

from app.db.schema import Course 
from werkzeug.utils import secure_filename
import numpy as np
import os

import tensorflow as tf
import tensorflow_datasets as tfds
from PIL import Image , ImageOps




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

@student.route("/ocr", methods=["POST"])
def ocr():
    f = request.files["file"]
        #Save file in a specific folder
        
    f.save(f"app/images/{secure_filename(f.filename)}")
    #open the image
    img_height = 90
    img_width = 90
    class_names=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = tf.keras.models.load_model('ocr')
    img = tf.keras.preprocessing.image.load_img(
    "app/images/{secure_filename(f.filename)}", target_size=(img_height, img_width)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    return jsonify({"message": "success","prediction": class_names[np.argmax(score)]})
    






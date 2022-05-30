from flask import Blueprint, jsonify, request, abort
from gtts import gTTS

import PyPDF2

from app.db.schema import Course 
from werkzeug.utils import secure_filename
import numpy as np
import os
import cv2

import tensorflow as tf

from PIL import Image , ImageOps
from base64 import decodestring




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
    f = request.get_json()
    im = f["image"].split("base64,")[1]

    print(im)
    imgstr = im.encode('utf-8')
    with open("./l.png","wb") as f:
        f.write(decodestring(imgstr))
    imgg = cv2.imread('./l.png', cv2.IMREAD_UNCHANGED)    


    trans_mask = imgg[:,:,3] == 0

    #replace areas of transparency with white and not transparent
    imgg[trans_mask] = [255, 255, 255, 255]

    #new image without alpha channel...
    imgg = cv2.cvtColor(imgg, cv2.COLOR_BGRA2BGR)
    cv2.imwrite("./l.png",imgg)

    img_height = 90
    img_width = 90
    class_names=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = tf.keras.models.load_model('/home/anzar/Desktop/ReadEasy/read-easy-backend/app/student/ocr')
    img = tf.keras.preprocessing.image.load_img(
    "./l.png", target_size=(img_height, img_width)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    print(class_names[np.argmax(score)])
    return jsonify({"message": "success","prediction": class_names[np.argmax(score)]})

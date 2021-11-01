from flask import Flask, Blueprint, jsonify, request, abort, redirect, render_template
from flask import current_app


import docx2txt

from werkzeug.utils import secure_filename

from app.db.schema import Course

teacher = Blueprint("teacher", __name__)


import PyPDF2 


@teacher.route("/upload/<course_id>", methods=["POST"])
def upload_file(course_id):
    if request.method == "POST":
        f = request.files["file"]
        #Save file in a specific folder
        
        f.save(f"app/static/{secure_filename(f.filename)}")
        text = docx2txt.process(f"app/static/{secure_filename(f.filename)}")
        print(course_id)
        course = Course.query.filter(Course.id==course_id).first()
        course.content = text
        course.update()
        return jsonify({"message": "success", "text": text})
    
def readpdf():
    filename = 'sample.pdf'
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    if text != "":
       text = text
    
    # Sanitize the text after pdf extraction
    
    
    return text

@teacher.route("/add-course", methods=["POST"])
def add_course():
    body = request.get_json()
    content=""
    filename=""
    new_course = Course(content, body["title"],filename)
    new_course.insert()
    
    return jsonify({"message": "success","id":new_course.id})
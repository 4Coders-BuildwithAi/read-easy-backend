from flask import Flask, Blueprint, jsonify, request, abort, redirect, render_template

import os

from werkzeug.utils import secure_filename

teacher = Blueprint("teacher", __name__)

# ALLOWED_EXTENSIONS = {'pdf'}
# def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

teacher.config["FILE_UPLOADS"] = "./../static/uploads/pdf"
teacher.config["ALLOWED_EXTENSIONS"] = ["PDF"]

def allowed_files(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".",1)[1]

    if ext.upper() in teacher.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@teacher.route("/uploadMaterial", methods=["POST"])
def uploadMaterial():

    if request.method == "POST":

        if request.files:

            file = request.files["file"]

            if file.filename =="":
                print("Invalid")
                return redirect(request.url)

            if not allowed_files(file.filename):
                print("Invalid File")
                return redirect(request.url)

            else:
                filename = secure_filename(file.filename)
                
                file.save(os.path.join(teacher.config["FILE_UPLOADS"], filename))

            print("File Saved")

            return redirect(request.url)
    #File Uploading

    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         print('File not found.')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     if file.filename == '':
    #         print('No file selected')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename):
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         process_file(os.path.join(app.config['UPLOAD_FOLDER'],filename), filename)
    #         return redirect(url_for('uploaded_file', filename=filename))
    
    return render_template() 
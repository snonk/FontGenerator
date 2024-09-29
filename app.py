import os
from flask import Flask, flash, request, redirect, url_for, render_template 
from flask import send_from_directory

from werkzeug.utils import secure_filename
import image_parser

UPLOAD_FOLDER = 'handwriting'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SECRET_KEY'] = "what"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        print(request.form)
        # if 'text' not in request.form['text']:
        #     flash('No text')
        #     return redirect(request.url)
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['file']
        text = request.form['text']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if text == '':
        #     flash('No text')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            print("working...")
            image_parser.process_document(path)
            print("processed...")
            image_parser.generate_image("file.pil", text)
            print("generated...") 
            return redirect(url_for('download_file', name="out.png"))
    return render_template("page.html")

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(".", name)

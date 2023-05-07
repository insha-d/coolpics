from flask import Flask,render_template,flash,redirect,url_for,session
from flask import request
from imageProcessor import *
import os
from werkzeug.utils import secure_filename
app = Flask(__name__,template_folder='static',static_folder='static',static_url_path='')
app.secret_key="insha"
path = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(path, "static","uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/animate', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # print(request.files)
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            print('no file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('file uploaded')
    return redirect(request.url+'/'+filename)


@app.route("/animate/<id>")
def returnAnimated(id):
    bnw(id)
    paint(id)
    cartoon(id)
    sketch(id)
    return  render_template("result.html",sourceFile=id)
if __name__=='__main__':
    app.run(debug=True,port=8080)
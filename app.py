import os
import urllib.request

import cv2
import imutils
import joblib
import numpy as np
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from keras.models import load_model
from werkzeug.utils import secure_filename

alzheimer_model = load_model('alz_model.h5',compile=False)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def login1():
   return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return render_template("login.html")

@app.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if (username == "AD" and password == "1234"):
            session['email'] = username
            return render_template("homepage.html")
        else:
            msg = "Invalid username or password"
            return render_template("login.html",msg=msg)


@app.route('/homepage')
def home():
    return render_template('homepage.html')


@app.route('/alzheimer')
def alzheimer():
    return render_template('alzheimer.html')


@app.route('/resulta', methods=['GET', 'POST'])
def resulta():
    if request.method == 'POST':
        print(request.url)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            img = cv2.imread('static/uploads/'+filename)
            img = cv2.resize(img, (176, 176))
            img = img.reshape(1, 176, 176, 3)
            img = img/255.0
            pred = alzheimer_model.predict(img)
            pred = pred[0].argmax()
            print(pred)
            return render_template('resulta.html', filename=filename, fn=firstname, ln=lastname, age=age, r=pred, gender=gender)
        else:
            flash('Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)



if __name__ == '__main__':
    app.run(debug=True)

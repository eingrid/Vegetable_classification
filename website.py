UPLOAD_FOLDER = 'static/uploads'

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}




index_to_class = ['apple',
 'banana',
 'beetroot',
 'bell pepper',
 'cabbage',
 'capsicum',
 'carrot',
 'cauliflower',
 'chilli pepper',
 'corn',
 'cucumber',
 'eggplant',
 'garlic',
 'ginger',
 'grapes',
 'jalepeno',
 'kiwi',
 'lemon',
 'lettuce',
 'mango',
 'onion',
 'orange',
 'paprika',
 'pear',
 'peas',
 'pineapple',
 'pomegranate',
 'potato',
 'raddish',
 'soy beans',
 'spinach',
 'sweetcorn',
 'sweetpotato',
 'tomato',
 'turnip',
 'watermelon']


import os

from flask import redirect, render_template, url_for
from flask import Flask, request 
from werkzeug.utils import secure_filename

import numpy as np

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow as tf


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def load_model_from_file():
    myModel = load_model("/mnt/Dev/Study_Mentorship/TASK1/saved_model/model_res50")
    return myModel  

@app.route('/',methods=['GET','POST'])
def upload_file():

    if request.method == 'GET' :
        return render_template('index.html')
    else: 
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('uploaded_file',filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    test_image = image.load_img(UPLOAD_FOLDER +'/'+filename,target_size=(150,150))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image,axis=0)

    myModel = app.config['MODEL']
    
    image_src = '/' + UPLOAD_FOLDER+'/'+filename
    result = myModel.predict(test_image)
    answer = "<div class = 'col text-center'><img width='150' height='150'  src='"+image_src+"' class='img-thumbnail'/><h4>guess:"+" "+str(index_to_class[np.argmax(result)] + f", probability = {np.max(result)}")+ "</h4></div><div class='col'></div><div class='w-100'></div>"
    results.append(answer)
    return render_template('index.html',len=len(results),results = results) 



def main():
    myModel = load_model_from_file()    
    app.config['MODEL'] = myModel
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGHT'] = 16*1024*1024
    app.run()

results = []


main()
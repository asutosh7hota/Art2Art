from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
import json
from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 
import re
#from sklearn.utils import shuffle
import numpy as np
import os
import sounddevice as sd
from scipy.io.wavfile import write

app = Flask(__name__)
Bootstrap(app)
user_list = []

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyse',methods=['POST'])
def analyse():
    if request.method == 'POST':
        rawtext = request.data
        filename = rawtext.decode()
    user_list.append(filename)
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording
    print('recording started')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(filename + '.wav', fs, myrecording)  # Save as WAV file 

    print('Data Sent')
    return render_template('index.html', status = 'File has been saved successfully!')

@app.route('/save',methods=['POST'])
def save():
    if request.method == 'POST':
        rawtext = request.data.decode()
        print('The Json array is:',rawtext)
        print('Type of doc:', type(rawtext))
    filename = user_list[len(user_list)-1]
    
    with open(filename+'.json', 'w') as json_file:
        json.dump(rawtext, json_file)
    
    return render_template('index.html', file = 'Data Collection Complete!')





if __name__ == '__main__':
	app.run(debug=True)
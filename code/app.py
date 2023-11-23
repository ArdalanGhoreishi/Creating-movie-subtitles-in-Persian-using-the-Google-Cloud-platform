from flask import Flask, redirect, render_template, \
    request, url_for, send_from_directory, current_app, send_file
from google.cloud import storage
from werkzeug.utils import secure_filename
import os, shutil
import zmq
import json



os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="your_own_GCP_Key.json"
storage_client = storage.Client.from_service_account_json(
        'your_own_GCP_Key.json')
def uploadtogc(bucket, localfile, bucketfile):
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(bucketfile)
    blob.upload_from_filename(localfile)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'name':'دریافت زیرنویس فارسی'}])

@app.route("/" , methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        if request.form['comp_select'] == 'دریافت زیرنویس فارسی':
            return redirect(url_for('vupload'))
    else:
        return redirect(url_for('index'))



@app.route('/vupload')
def vupload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        uploadtogc(bucket="my-video-buck",
        localfile=f.filename,
        bucketfile="test.mp4")
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:1048")
        socket.send_json("Hello")
        message = socket.recv()
        
        return redirect(url_for('uploads'))
@app.route('/uploads',methods = ['GET'])
def uploads():
    return render_template('download.html')
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    path = filename
    return send_file(path, as_attachment=True)




if __name__=='__main__':
    app.run(debug=True)

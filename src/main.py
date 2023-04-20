from flask import Flask, render_template, flash, request, redirect, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "f2gjdke02984ngnyjok09ewhdbwg2tr4fkrjr"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename: str):
	print(filename.split('.')[-1].lower())
	return filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
	if request.method == 'POST':
		file = request.files['file']
		if file == None:
			flash('No file selected !', 'warning')
		filename = secure_filename(request.form['filename'])
		if not filename:
			flash('No filename entered !', 'warning')
		if file and allowed_file(filename):
			file.save(f'src/files/{filename}')
			flash(f'Uploaded {filename} successfully !', 'message')
			return redirect('/files')
	return redirect('/upload')

@app.route('/files/<path:filename>')
def show(filename):
	return send_from_directory('files', filename)

@app.route('/files')
def files():
	files = os.listdir('src/files')		
	return render_template('library.html', files=files)
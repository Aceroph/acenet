from flask import Flask, render_template, request, redirect, send_from_directory, flash
import os
from github import Github

g = Github(os.environ.get("GIT_TOKEN"))
repo = g.get_repo("Aceroph/acenet")

app = Flask(__name__)
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
		filename = request.form['filename']
		if file and allowed_file(filename):
			repo.create_file(f'src/f/{filename}', 'uploaded file', file.stream.read())
			return redirect('/')
	return redirect('/upload')

@app.route('/f/<path:filename>')
def show(filename):
	return send_from_directory('./f', filename)

from flask import Flask, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename
from github import Github

g = Github(os.environ.get('GIT_TOKEN'))
repo = g.get_repo("acenet")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './f'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename: str):
	return filename.split('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
	if request.method == 'POST':
		if 'file' not in request.files:
			return flash(request.url)
		file = request.files['file']

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			repo.create_file('/', 'uploaded file', str(file))
			return redirect('/')
	return redirect('/')

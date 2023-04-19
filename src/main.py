from flask import Flask, render_template, request, flash, redirect
import os
from github import Github
import base64

g = Github('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')
repo = g.get_repo("Aceroph/acenet")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './f'
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
		if file and allowed_file(file.filename):
			print(file.stream)
			repo.create_file(f'f/{file.filename}', 'uploaded file', base64.b64encode(file.stream.read()))
			print('success')
			return redirect('/')
	return redirect('/upload')

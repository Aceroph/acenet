from flask import Flask, render_template, flash, request, redirect, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "f2gjdke02984ngnyjok09ewhdbwg2tr4fkrjr"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.curdir = 'acenet/'

def allowed_file(filename: str):
	print(filename.split('.')[-1].lower())
	return filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

def uploadfileexists():
	if not os.path.exists('files/'):
		os.mkdir('files')

def findpath(pathA: str, pathB: str):
	e = True
	blacklist = []
	currentpath = pathA
	while e:
		items = os.listdir(currentpath)
		for black in blacklist: items.remove(black) if black in items else items

		if items == []:
			empty = currentpath.split('/')[-1]
			print('empty', empty)
			blacklist.append(empty)
			currentpath = currentpath.replace(f'/{empty}', '')
			print('empty', currentpath)
		else:
			for item in items:
				if os.path.isdir(f'{currentpath}/{item}') and item not in blacklist:
					currentpath += f'/{item}'
					print(currentpath)
					if item == pathB:
						e = False
	
	return currentpath


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
	uploadfileexists()

	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part', 'warning')
		
		file = request.files['file']
		if file.filename =='':
			flash('No file selected !', 'warning')
		
		filename = secure_filename(request.form['filename'])
		if filename == '':
			flash('No filename entered !', 'warning')

		if file and allowed_file(filename):
			file.save(f'files/{filename}')
			flash(f'Uploaded {filename} successfully !', 'message')

	return redirect('/upload')

@app.route('/files/<path:filename>')
def show(filename):
	if os.path.isfile(f'files/{filename}'):
		return send_from_directory('files', filename)
	else:
		items = []	
		path = findpath('files', filename)

		for item in os.listdir(path):
			if os.path.isdir(f'{path}/{item}'):
				items.append(['dir', item])
			else:
				items.append(['file'])

		return render_template('library.html', items=sorted(items))

@app.route('/files')
def files():
	uploadfileexists()

	items = []
	for item in os.listdir('files'):
		if os.path.isdir(f'files/{item}'):
			items.append(['dir', item])
		else:
			items.append(['file', item])

	return render_template('library.html', items=sorted(items))
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/contact')
def contact():
	return '<h1 style="text-align: center;">Contact me pls</h1>'

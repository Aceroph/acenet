from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1 style="text-align: center;">Home Page</h1>'
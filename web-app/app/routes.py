from flask import render_template
from app import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/emoji')
def emoji():
    return render_template('emoji.html', title='Emojifier')


@app.route('/meme')
def meme():
    return render_template('meme.html', title='Meme Classifier')

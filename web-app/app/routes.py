from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import EmojiForm
from app.forms import MemeForm
from .emoji.tfidf_generator import generateEmojipasta


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/emoji', methods=['GET', 'POST'])
def emoji():
    form = EmojiForm()
    if form.validate_on_submit():
        flash('Output: {}'.format(generateEmojipasta(form.input_s.data)))
        return redirect(url_for('emoji_vis'))
    return render_template('emoji.html', title='Emojifier', form=form)


@app.route('/meme', methods=['GET', 'POST'])
def meme():
    form = MemeForm()
    if form.validate_on_submit():
        flash('Output: {}'.format(form.input_s.data))
        return redirect(url_for('meme'))
    return render_template('meme.html', title='Meme Classifier', form=form)


@app.route('/emoji_vis', methods=['GET', 'POST'])
def emoji_vis():
    return render_template('emoji_vis.html', title="Emoji Visualization")


@app.route('/csv/emoji_insights.csv', methods=['GET'])
def emoji_insight():
    with open("./app/csv/emoji_insights.csv", "r") as fp:
        return fp.read()

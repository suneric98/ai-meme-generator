from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import EmojiForm
from app.forms import MemeForm
from .emoji.tfidf_generator import generateEmojipasta
from .meme.tfidf_generator import generateMemePrediction


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
        prediction, url = generateMemePrediction(form.input_s.data)
        flash('Output: {}'.format(prediction))
        flash('URL:  {}'.format(url))
        return redirect(url_for('meme_vis'))
    return render_template('meme.html', title='Meme Classifier', form=form)


@app.route('/emoji_vis', methods=['GET', 'POST'])
def emoji_vis():
    return render_template('emoji_vis.html', title="Emoji Visualization")


@app.route('/meme_vis', methods=['GET', 'POST'])
def meme_vis():
    return render_template('meme_vis.html', title="Meme Visualization")


@app.route('/csv/emoji_insights.csv', methods=['GET'])
def emoji_insight():
    with open("./app/csv/emoji_insights.csv", "r") as fp:
        return fp.read()

@app.route('/csv/emoji_insights.json', methods=['GET'])
def emoji_insight_json():
    with open("./app/csv/emoji_insights.json", "r") as fp:
        return fp.read()

@app.route('/csv/meme_insights.csv', methods=['GET'])
def meme_insight():
    with open("./app/csv/meme_insights.csv", "r") as fp:
        return fp.read()


@app.route('/csv/meme_probability.csv', methods=['GET'])
def meme_probability():
    with open("./app/csv/meme_probability.csv", "r") as fp:
        return fp.read()

@app.route('/csv/meme_insights.json', methods=['GET'])
def meme_insight_json():
    with open("./app/csv/meme_insights.json", "r") as fp:
        return fp.read()


@app.route('/csv/meme_probability.json', methods=['GET'])
def meme_probability_json():
    with open("./app/csv/meme_probability.json", "r") as fp:
        return fp.read()

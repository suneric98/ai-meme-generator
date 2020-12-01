from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import EmojiForm
from app.forms import MemeForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/emoji', methods=['GET', 'POST'])
def emoji():
    form = EmojiForm()
    if form.validate_on_submit():
        flash('Processing input: {}'.format(form.input_s.data))
        return redirect(url_for('home'))
    return render_template('emoji.html', title='Emojifier', form=form)


@app.route('/meme', methods=['GET', 'POST'])
def meme():
    form = MemeForm()
    if form.validate_on_submit():
        flash('Processing input: {}'.format(form.input_s.data))
        return redirect(url_for('home'))
    return render_template('meme.html', title='Meme Classifier', form=form)

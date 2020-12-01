from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class MemeForm(FlaskForm):
    input_s = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Classify Meme')


class EmojiForm(FlaskForm):
    input_s = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Add Emojis')

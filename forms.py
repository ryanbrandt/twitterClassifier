from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class KeywordForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

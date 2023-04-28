from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FolderForm(FlaskForm):
    name = StringField('Название папки', validators=[DataRequired()])
    submit = SubmitField('Добавить')

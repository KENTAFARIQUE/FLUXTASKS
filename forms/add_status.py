from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class StatusForm(FlaskForm):
    name = StringField('Название статуса', validators=[DataRequired()])
    submit = SubmitField('Добавить')

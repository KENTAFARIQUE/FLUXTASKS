from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField('Название задачи', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    status = SelectMultipleField('Укажите статус', choices=[])
    importance = SelectMultipleField('Укажите важность', choices=[])
    folder = SelectMultipleField('Укажите папку', choices=[])
    submit = SubmitField('Добавить')

    def set_status_choices(self, list):
        self.status.choices = list

    def set_importance_choices(self, list):
        self.importance.choices = list

    def set_folder_choices(self, list):
        self.folder.choices = list
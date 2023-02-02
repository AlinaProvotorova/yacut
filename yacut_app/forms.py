from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256), Optional()]
    )
    short = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]

    )
    submit = SubmitField('Создать')

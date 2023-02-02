from .models import URLMap

from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):

    def validate_form_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(
                f'Имя {self.custom_id.data} уже занято!')

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16),
                    Regexp(r'[A-Za-z0-9]', message='Указано недопустимое имя для короткой ссылки'),
                    Optional(),
                    validate_form_custom_id]

    )
    submit = SubmitField('Создать')

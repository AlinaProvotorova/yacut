from .models import URLMap
from .constants import MAX_SIZE_SHORT_FOR_USER, MAX_SIZE_URL, VALID_CHARACTERS

from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

original_link_input = 'Длинная ссылка'
custom_id_input = 'Ваш вариант короткой ссылки'


class URLMapForm(FlaskForm):
    original_link = URLField(
        original_link_input,
        validators=[DataRequired(message='Обязательное поле'),
                    Length(max=MAX_SIZE_URL)]
    )
    custom_id = URLField(
        custom_id_input,
        validators=[Length(max=MAX_SIZE_SHORT_FOR_USER),
                    Optional()]

    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        for char in self.custom_id.data:
            if char not in VALID_CHARACTERS:
                raise ValidationError(
                    message='Указано недопустимое имя для короткой ссылки'
                )
        if self.custom_id.data and URLMap.get_model_from_bd(
                short_id=self.custom_id.data
        ):
            raise ValidationError(
                f'Имя {self.custom_id.data} уже занято!'
            )

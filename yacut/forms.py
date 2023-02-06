from .models import URLMap
from settings import PATTERN_VALID_CHARACTERS, MAX_SIZE_SHORT_FOR_USER

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError, URL

original_link_input = 'Длинная ссылка'
custom_id_input = 'Ваш вариант короткой ссылки'

message_not_url = 'Обязательное поле'
message_invalid_short = (
    'Указано недопустимое имя для короткой ссылки, '
    'имя должно состоять только из латинских букв и цифр'
)
message_non_unique_short = 'Имя {} уже занято!'
message_invalid_url = 'Указано недопустимое имя для длинной ссылки'


class URLMapForm(FlaskForm):
    original_link = URLField(
        original_link_input,
        validators=[DataRequired(message=message_not_url), URL(True, message=message_invalid_url)]
    )
    custom_id = StringField(
        custom_id_input,
        validators=[Length(max=MAX_SIZE_SHORT_FOR_USER),
                    Optional(),
                    Regexp(PATTERN_VALID_CHARACTERS, message=message_invalid_short)]

    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        if self.custom_id.data and URLMap.get_model_from_bd(
                short_id=self.custom_id.data
        ):
            raise ValidationError(
                message_non_unique_short.format(self.custom_id.data)
            )

from .models import URLMap
from settings import (
    PATTERN_VALID_CHARACTERS,
    MAX_SIZE_SHORT_FOR_USER,
    MAX_SIZE_URL)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError,
    URL)

ORIGINAL_LINK_INPUT = 'Длинная ссылка'
CUSTOM_ID_INPUT = 'Ваш вариант короткой ссылки'

MESSAGE_NO_URL = 'Обязательное поле'
MESSAGE_INVALID_SHORT = (
    'Указано недопустимое имя для короткой ссылки, '
    'имя должно состоять только из латинских букв и цифр'
)
MESSAGE_NON_UNIQUE_SHORT = 'Имя {} уже занято!'
MESSAGE_INVALID_URL = 'Указано недопустимое имя для длинной ссылки'
SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = StringField(
        ORIGINAL_LINK_INPUT,
        validators=[DataRequired(message=MESSAGE_NO_URL),
                    URL(True, message=MESSAGE_INVALID_URL),
                    Length(max=MAX_SIZE_URL)]
    )
    custom_id = StringField(
        CUSTOM_ID_INPUT,
        validators=[Length(max=MAX_SIZE_SHORT_FOR_USER),
                    Optional(),
                    Regexp(PATTERN_VALID_CHARACTERS,
                           message=MESSAGE_INVALID_SHORT)]

    )
    submit = SubmitField(SUBMIT)

    def validate_custom_id(self, custom_id):
        if self.custom_id.data and URLMap.get_model_from_bd(
                short_id=self.custom_id.data
        ):
            raise ValidationError(
                MESSAGE_NON_UNIQUE_SHORT.format(self.custom_id.data)
            )

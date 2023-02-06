import re
from datetime import datetime
from random import sample

from flask import url_for

from . import db
from settings import (
    MAX_SIZE_SHORT,
    MAX_COUNT_CREATE_SHORT,
    MAX_SIZE_SHORT_FOR_USER,
    PATTERN_VALID_CHARACTERS,
    PATTERN_VALID_URL,
    VALID_CHARACTERS
)

message_not_new_short = 'Новый уникальнй id не найден'
message_non_body_input = 'Отсутствует тело запроса'
message_non_url = '\"url\" является обязательным полем!'
message_invalid_short = 'Указано недопустимое имя для короткой ссылки'
message_invalid_url = 'Указано недопустимое имя для длинной ссылки'
message_non_unique_short = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(MAX_SIZE_SHORT_FOR_USER), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('new_link_view', short_id=self.short, _external=True)
        )

    def from_dict(self, data: dict):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def create_urlmap(data, custom_id):
        if not custom_id or custom_id is None or len(custom_id) == 0 or custom_id == "":
            custom_id = URLMap.get_unique_short_id()
        urlmap = URLMap()
        data['custom_id'] = custom_id
        urlmap.from_dict(data)
        URLMap.db_commit(urlmap)
        return urlmap

    @staticmethod
    def get_model_from_bd(short_id=None, url=None):
        if short_id is not None:
            return URLMap.query.filter_by(short=short_id).first()
        return URLMap.query.filter_by(original=url).first()

    @staticmethod
    def db_commit(data):
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def get_unique_short_id():
        short_link = ''.join(sample(VALID_CHARACTERS, MAX_SIZE_SHORT))
        for i in range(MAX_COUNT_CREATE_SHORT):
            if URLMap.get_model_from_bd(short_id=short_link) is None:
                return short_link
        else:
            return message_not_new_short

    @staticmethod
    def input_validation(data):
        if data is None:
            raise ValueError(message_non_body_input)
        if 'url' not in data:
            raise ValueError(message_non_url)
        if not re.match(PATTERN_VALID_URL, data['url']):
            raise ValueError(message_invalid_url)
        if 'custom_id' in data:
            if URLMap.get_model_from_bd(short_id=data['custom_id']):
                raise ValueError(message_non_unique_short.format(data['custom_id']))
            if data['custom_id'] is not None \
                    and len(data['custom_id']) > 0 \
                    and data['custom_id'] != "":
                if not re.match(PATTERN_VALID_CHARACTERS, data['custom_id']) \
                        or len(data['custom_id']) > MAX_SIZE_SHORT_FOR_USER:
                    raise ValueError(message_invalid_short)

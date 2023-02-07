import re
import urllib.parse
from datetime import datetime
from random import sample
from urllib.error import URLError

from flask import url_for

from . import db
from settings import (
    MAX_SIZE_SHORT,
    MAX_SIZE_URL,
    MAX_SIZE_SHORT_FOR_USER,
    PATTERN_VALID_CHARACTERS,
    VALID_CHARACTERS,
    _,
)

MESSAGE_NON_NEW_SHORT = 'Новый уникальнй id не найден'
MESSAGE_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
MESSAGE_INVALID_URL = 'Указано недопустимое имя для длинной ссылки'
MESSAGE_NON_UNIQUE_SHORT = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_SIZE_URL), nullable=False)
    short = db.Column(
        db.String(MAX_SIZE_SHORT_FOR_USER), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'new_link_view',
                short_id=self.short,
                _external=True)
        )

    def from_dict(self, data: dict):
        self.original = data['url']
        self.short = data['custom_id']

    @staticmethod
    def create(url, custom_id=None):
        URLMap.url_custom_id_validation(url, custom_id)
        if not custom_id or custom_id is None or custom_id == "":
            data = URLMap.get_model_from_bd(url=url)
            if data is not None:
                return data
            custom_id = URLMap.get_unique_short_id()
        urlmap = URLMap(
            original=url,
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def get_model_from_bd(short_id=None, url=None):
        if short_id is not None:
            return URLMap.query.filter_by(short=short_id).first()
        return URLMap.query.filter_by(original=url).first()

    @staticmethod
    def get_unique_short_id():
        for i in range(_):
            short_link = ''.join(sample(VALID_CHARACTERS, MAX_SIZE_SHORT))
            if URLMap.get_model_from_bd(short_id=short_link) is None:
                return short_link
        raise ValueError(MESSAGE_NON_NEW_SHORT)

    @staticmethod
    def url_custom_id_validation(url, custom_id=None):
        if (len(url) > MAX_SIZE_URL or
                urllib.parse.urlsplit(url).scheme not in ['http', 'https']):
            raise ValueError(MESSAGE_INVALID_URL)
        if custom_id is not None and custom_id != "":
            if (len(custom_id) > MAX_SIZE_SHORT_FOR_USER or
                    not re.match(PATTERN_VALID_CHARACTERS, custom_id)):
                raise ValueError(MESSAGE_INVALID_SHORT)
        if URLMap.get_model_from_bd(short_id=custom_id):
            raise ValueError(MESSAGE_NON_UNIQUE_SHORT.format(custom_id))

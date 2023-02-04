from datetime import datetime
from random import sample

from flask import url_for

from . import db
from .constants import (
    MAX_SIZE_SHORT,
    MAX_SIZE_URL,
    MAX_COUNT,
    MAX_SIZE_SHORT_FOR_USER, VALID_CHARACTERS
)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_SIZE_URL), unique=True, nullable=False)
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
    def get_model_from_bd(short_id=None, url=None):
        if short_id is not None:
            return URLMap.query.filter_by(short=short_id).first()
        return URLMap.query.filter_by(original=url).first()

    @staticmethod
    def db_commit(data):
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def get_unique_short_id(short_link=None):
        if not short_link or short_link is None or len(short_link) == 0 or short_link == "":
            count = 0
            short_link = ''.join(sample(VALID_CHARACTERS, MAX_SIZE_SHORT))
            while URLMap.get_model_from_bd(short_id=short_link) is not None:
                short_link = ''.join(sample(VALID_CHARACTERS, MAX_SIZE_SHORT))
                count += 1
                if count > MAX_COUNT:
                    short_link = None
                    break
        return short_link

    @staticmethod
    def input_validation(data):
        if data is None:
            raise InvalidAPIUsage('Отсутствует тело запроса')
        if 'url' not in data:
            raise InvalidAPIUsage('\"url\" является обязательным полем!')
        if dict(data).get('custom_id') is not None:
            if len(str(data['custom_id'])) > MAX_SIZE_SHORT_FOR_USER:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
            for char in data['custom_id']:
                if char not in VALID_CHARACTERS:
                    raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
            if URLMap.get_model_from_bd(short_id=data['custom_id']):
                raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
        return True

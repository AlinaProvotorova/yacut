import re

from flask import jsonify, request
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import db_commit, validate_short


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


def form_validate(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if dict(data).get('custom_id') is not None:
        if re.compile(r'[^A-Za-z0-9]').search(data['custom_id']) or len(str(data['custom_id'])) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(r'Имя "' + data['custom_id'] + r'" уже занято.')
    return True


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if form_validate(data):
        custom_id = dict(data).setdefault('custom_id')
        urlmap = URLMap()
        if URLMap.query.filter_by(original=data['url']).first() is None:
            data['custom_id'] = validate_short(custom_id)
            urlmap.from_dict(data)
            db_commit(urlmap)
        else:
            urlmap = URLMap.query.filter_by(original=data['url']).first()
        return jsonify({'url': urlmap.to_dict().get('url'),
                        'short_link': urlmap.to_dict().get('short_link')}), 201

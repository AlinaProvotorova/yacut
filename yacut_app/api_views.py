from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/<string:short>/', methods=['GET'])
def get_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'link': url.to_dict()}), 200


@app.route('/api/urls/', methods=['POST'])
def add_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'original' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if len(data['short']) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({'urimap': urlmap.to_dict()}), 201

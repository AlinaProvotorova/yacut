from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.get_model_from_bd(short_id=short_id)
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if URLMap.input_validation(data):
        custom_id = dict(data).setdefault('custom_id')
        urlmap = URLMap.get_model_from_bd(url=data['url'])
        if urlmap is None:
            urlmap = URLMap()
            data['custom_id'] = URLMap.get_unique_short_id(custom_id)
            urlmap.from_dict(data)
            URLMap.db_commit(urlmap)
        return jsonify(urlmap.to_dict()), 201

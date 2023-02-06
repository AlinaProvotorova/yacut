from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

error_not_short = 'Указанный id не найден'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.get_model_from_bd(short_id=short_id)
    if url is None:
        raise InvalidAPIUsage(error_not_short, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    try:
        data = request.get_json()
        URLMap.input_validation(data)
        custom_id = dict(data).setdefault('custom_id')
        urlmap = URLMap.create_urlmap(data, custom_id)
    except ValueError as e:
        raise InvalidAPIUsage(e.__str__())
    return jsonify(urlmap.to_dict()), 201

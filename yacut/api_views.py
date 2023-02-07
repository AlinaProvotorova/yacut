from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

MESSAGE_NOT_SHORT = 'Указанный id не найден'
MESSAGE_NON_BODY_INPUT = 'Отсутствует тело запроса'
MESSAGE_NON_URL = '\"url\" является обязательным полем!'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.get_model_from_bd(short_id=short_id)
    if url is None:
        raise InvalidAPIUsage(MESSAGE_NOT_SHORT, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    json_response = request.get_json()
    if json_response is None:
        raise InvalidAPIUsage(MESSAGE_NON_BODY_INPUT)
    if 'url' not in json_response or type(json_response['url']) != str:
        raise InvalidAPIUsage(MESSAGE_NON_URL)
    try:
        URLMap.json_input_validation(json_response['url'], dict(json_response).setdefault('custom_id'))
        urlmap = URLMap.create_urlmap(json_response['url'], dict(json_response).setdefault('custom_id'))
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(urlmap.to_dict()), 201

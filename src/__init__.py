import json
import os, sys
import logging

from uuid import uuid4
from utils import *
from data_model import Scooter
from flask import Flask
from flask import request, abort
from flask_caching import Cache
from flask_pymongo import PyMongo


app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

app.config.from_pyfile('../config/config.py')
cache = Cache(app)

file_path = f"{os.environ.get('PROJECT_PATH')}/config/app_info.json".replace('\"', '')  # magic with quotes
app.config['MONGO_URI'] = os.environ.get('MONGO_CONNECTION_STR').replace('\"', '')
cache.set('APP_ID2URL', json.load(open(file_path, 'r')))
db = PyMongo(app, ssl=True).db


@cache.cached(timeout=65, key_prefix='all_scooters')
def get_all_scooters():
    scooters = []
    try:
        for app_id, app_url in cache.get('APP_ID2URL').items():
            app_scooters = get_vehicles(app_url)
            for scooter in app_scooters:
                scooter['scooter_id'] = f"{app_id}-{scooter['scooter_id']}"
                scooters.append(scooter)
        scooters: list[Scooter] = [Scooter(data) for data in scooters]
    except ExternalAppError:
        abort(503, 'Scooter service is unavailable')
    return scooters


@app.route("/api")
def hello():
    return {
        "_links": {
            "clients": {"href": "/clients"},
            "scooters": {"href": "/scooters"}
        }
    }


@app.route("/clients")
def new_client():
    client_response = {
        "uuid": str(uuid4()),
        "_links": {
            "self": {"href": "/clients"}
        }}
    add_client(db, client_response['uuid'])  # todo: handle failure
    return client_response


@app.route("/scooters")
def get_scooters():
    scooters = get_all_scooters()
    data = {
        "scooters": [x.to_dict() for x in scooters],
        "_links": {
            "self": {"href": "/scooters"},
            "nearest": {"href": "/scooters/nearest"},
            "book": {"href": "/scooters/{id}/reservations"},
            "unbook": {"href": "/scooters/{id}/reservations"}
        }
    }
    return data


@app.route("/scooters/nearest")
def get_nearest():
    scooters = get_all_scooters()
    lon = request.args.get('lon', '')
    lat = request.args.get('lat', '')
    max_price = request.args.get('max_price', '')
    limit = request.args.get('limit', 5)

    try:
        lon, lat = parse_float(lon), parse_float(lat)
    except ParseError:
        abort(400)

    if max_price:
        try:
            max_price = parse_float(max_price)
        except ParseError:
            abort(400)

    if limit != 5:
        try:
            limit = parse_int(limit)
        except ParseError:
            abort(400)

    scooters_sorted = sorted(scooters, key=lambda x: x.dist((lon, lat)))[:limit]
    if max_price != '':
        scooters_sorted = filter(lambda x: x.price <= max_price, scooters_sorted)
    scooters_serialized = [x.to_dict() for x in scooters_sorted]

    data = {
        "scooters": scooters_serialized,
        "_links": {
            "self": {"href": "/scooters/nearest"},
            "book": {"href": "/scooters/{id}/reservations"},
            "unbook": {"href": "/scooters/{id}/reservations"}
        }
    }
    return data


@app.route("/scooters/<scooter_id>/reservations", methods=['POST', 'DELETE'])
def reservation(scooter_id):
    cur_uuid = request.args.get('uuid', '')
    if cur_uuid == '':
        abort(400, 'No uuid specified.')
    db.clients.find_one_or_404({'uuid': cur_uuid})

    try:
        app_id, scooter_id = parse_scooter_id(scooter_id)
        if app_id not in cache.get('APP_ID2URL'):
            abort(400, 'Wrong scooter_id.')
        url = cache.get('APP_ID2URL')[app_id]
        route = f'/vehicles/{scooter_id}/reservations'

        app_response = requests.post(f"{url}{route}", params={'uuid': cur_uuid}) \
            if request.method == 'POST' \
            else requests.delete(f"{url}{route}", params={'uuid': cur_uuid})

        return '', app_response.status_code

    except ParseError:
        abort(400, 'Wrong scooter id.')


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port)

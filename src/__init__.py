from uuid import uuid4
from utils import *
from data_model import Scooter
from flask import Flask
from flask import request, abort

app = Flask(__name__)


def update_scooters():
    scooters = []
    for app_id, app_url in APP_ID2URL.items():
        for scooter in get_vehicles(app_url):
            print(type(app_id))
            scooter['scooter_id'] = f"{app_id}/{scooter['scooter_id']}"
            scooters.append(scooter)
    scooters: list[Scooter] = [Scooter(data) for data in scooters]
    return scooters

# todo: remove
scooters = update_scooters()


@app.route("/")
def hello():
    param_id = request.args.get('id', '')
    return "Hello World!" + str(param_id) + '\n'


@app.route("/clients")
def new_client():
    new_id = {"uuid": str(uuid4())}
    return new_id


@app.route("/scooters")
def get_scooters():
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
    # todo check cur_uuid in db
    try:
        app_id, scooter_id = parse_scooter_id(scooter_id)
        if app_id not in APP_ID2URL:
            abort(400)
        url = APP_ID2URL[app_id]
        route = f'/vehicles/{scooter_id}/reservations'
        method = request.method
        # todo: make request
    except ParseError:
        abort(400)


if __name__ == "__main__":
    app.run(port=5000)

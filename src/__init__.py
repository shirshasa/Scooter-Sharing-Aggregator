from uuid import uuid4
from utils import *
from data_model import Scooter
from flask import Flask
from flask import request, abort

app = Flask(__name__)

# todo: remove
scooters = []
for app_id, app_url in app_id2url.items():
    for scooter in get_vehicles(app_url):
        print(type(app_id))
        scooter['scooter_id'] = f"{app_id}/{scooter['scooter_id']}"
        scooters.append(scooter)
scooters: list[Scooter] = [Scooter(data) for data in scooters]


@app.route("/")
def hello():
    param_id = request.args.get('id', '')
    return "Hello World!" + str(param_id)


@app.route("/new_client")
def new_client():
    new_id = {"uuid": str(uuid4())}
    return new_id


@app.route("/nearest")
def get_nearest():
    lon = request.args.get('lon', '')
    lat = request.args.get('lat', '')
    max_price = request.args.get('max_price', '')
    limit = int(request.args.get('limit', 5))

    try:
        lon, lat = parse_coordinate(lon), parse_coordinate(lat)
    except ParseError:
        abort(400)

    if max_price:
        pass

    scooters_sorted = sorted(scooters, key=lambda x: x.dist((lon, lat)))[:limit]
    scooters_dict = [x.to_dict() for x in scooters_sorted]
    return {'nearest': scooters_dict}


if __name__ == "__main__":
    app.run()

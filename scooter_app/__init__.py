from flask import Flask
from flask import request, abort
from flask_pymongo import PyMongo
from pymongo import ReturnDocument

from data_model import Scooter


app = Flask(__name__)
app.config.from_pyfile('../config/config.py')
db = PyMongo(app).db


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/vehicles', methods=['GET'])
def vehicles():
    try:
        vehicles = db.scooters.find({'is_booked': False})
        scooters: list[Scooter] = [Scooter(data) for data in vehicles]
    except Exception as e:
        print(e)

    return {'vehicles': [x.to_dict() for x in scooters]}


@app.route('/vehicles/<string:vehicle_id>/reservations', methods=['POST', 'DELETE'])
def book_vehicle(vehicle_id):
    client_id = request.args.get('uuid', '')

    if client_id == '':
        abort(400, 'No uuid specified.')

    response_code = 204

    if request.method == 'POST':
        scooter = db.scooters.find_one_and_update({'scooter_id': vehicle_id},
                                                  {'$set': {"is_booked": True, "client_id": client_id}},
                                                  return_document=ReturnDocument.BEFORE)

        if scooter is None:
            response_code = 404
        elif scooter['is_booked'] is True:
            response_code = 409

    elif request.method == 'DELETE':
        scooter = db.scooters.find_one_and_update({'scooter_id': vehicle_id},
                                                  {'$set': {"is_booked": False}, '$unset': {"client_id": client_id}},
                                                  return_document=ReturnDocument.AFTER)
        if scooter is None:
            response_code = 404

    return '', response_code


if __name__ == "__main__":
    app.run()

import requests


class ParseError(RuntimeError):
  pass


class ExternalAppError(RuntimeError):
    pass


def parse_float(value):
    try:
        return float(value)
    except ValueError:
        raise ParseError()


def parse_int(value):
    try:
        return int(value)
    except ValueError:
        raise ParseError()


def parse_scooter_id(composed_scooter_id):
    if composed_scooter_id.count('-') != 1:
        raise ParseError()
    app_id, scooter_id = composed_scooter_id.split('-')

    return app_id, scooter_id


def get_vehicles(url):
    route = f'/vehicles'
    response = requests.get(f"{url}{route}")
    if response.status_code == 200:
        data = response.json()
        return data['vehicles']
    else:
        raise ExternalAppError()


def add_client(db, new_uuid):
    client_doc = {'uuid': new_uuid}
    return db.clients.insert_one(client_doc)

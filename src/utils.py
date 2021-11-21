import requests


class ParseError(RuntimeError):
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
    if '/' not in composed_scooter_id:
        raise ParseError()
    app_id, scooter_id = composed_scooter_id.split('/')

    return app_id, scooter_id


def get_vehicles(url):
    route = f'/vehicles'
    response = requests.get(f"{url}{route}")
    data = response.json()
    print(data)
    return data['vehicles']

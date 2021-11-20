APP_ID2URL = {
  '1': 'http://1.by',
  '2': 'http://2.by'
}

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
    return [
        {
            "scooter_id": '1009',
            "lon": 10,
            "lat": 40,
            "price": 1
        },
        {
            "scooter_id": '1008',
            "lon": 20,
            "lat": 55,
            "price": 1
        }
    ]

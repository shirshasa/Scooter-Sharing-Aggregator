app_id2url = {
  '1': 'http://1.by',
  '2': 'http://2.by'
}

class ParseError(RuntimeError):
  pass


def parse_coordinate(value):
    try:
        return float(value)
    except ValueError:
        print(value, type(value))
        raise ParseError()


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

from utils import *
from geopy.distance import geodesic


class Scooter:
    def __init__(self, data):
        lon, lat = data.get('lon', ''), data.get('lat', '')
        self.position = parse_float(lon), parse_float(lat)
        self.price = data.get('price')
        self.scooter_id = data.get('scooter_id')

    def dist(self, pos):
        return geodesic(self.position, pos).km

    def to_dict(self):
        return {
            'lon': self.position[0],
            'lat': self.position[1],
            'price': self.price,
            'scooter_id': self.scooter_id
        }

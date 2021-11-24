class Scooter:
    def __init__(self, data):
        lon, lat = data.get('longitude', ''), data.get('latitude', '')
        self.position = float(lon), float(lat)
        self.price = data.get('price')
        self.scooter_id = data.get('scooter_id')

    def to_dict(self):
        return {
            'lon': self.position[0],
            'lat': self.position[1],
            'price': self.price,
            'scooter_id': self.scooter_id
        }


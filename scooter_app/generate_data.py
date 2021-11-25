import random
import string
import secrets

str_len = 24

models = ['Kugoo X1', 'Xiaomi Pro 2', 'Kugoo M4 Pro', 'Ninebot E25', 'GT M4 Pro', 'Kugoo S3', 'Ninebot ES1L']
prices = {'Kugoo X1': 0.99, 'Xiaomi Pro 2': 0.89, 'Kugoo M4 Pro': 2.99, 'Ninebot E25': 1.59, 'GT M4 Pro': 3.09,
          'Kugoo S3': 1.89, 'Ninebot ES1L': 1.09}


def gen_scooters_data(n, collection):
    scooters = []

    for i in range(n):
        scooter_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for x in range(str_len))
        lon = round(random.uniform(0, 90), 1)
        lat = round(random.uniform(0, 90), 1)
        model = random.choice(models)
        price = prices.get(model)

        scooter = {'scooter_id': scooter_id, 'model': model, 'longitude': lon, 'latitude': lat, 'price': price,
                   'is_booked': False}

        # print(scooter)
        scooters.append(scooter)

    x = collection.insert_many(scooters)

from generate_data import gen_scooters_data


auth_url = '' # connection string for MongoDB


def get_database(auth_str):
    from pymongo import MongoClient
    client = MongoClient(auth_str, ssl=True)
    return client.scootersharing


if __name__ == "__main__":
    # Get the database
    dbname = get_database(auth_url)
    collection = dbname["scooters"]
    gen_scooters_data(250, collection)




from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017

SENSOR_DATA = 'sensor-data'

HARPSICHORD_DB = 'harpsichord-database'

CLIENT = MongoClient(HOST, PORT)
MONGO_DB = CLIENT[HARPSICHORD_DB]


def get_most_recent_harpsichord_data():
  sensor_db = MONGO_DB[SENSOR_DATA]
  for doc in sensor_db.find().sort([('timestamp', -1)]).limit(1):
    return doc

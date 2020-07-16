import requests
from pymongo import MongoClient, errors
from datetime import datetime

#Mongo-DB
MONGO_HOST = 'hucserv193'
MONGO_PORT = 8888
MONGO_USERNAME = 'mongoadmin'
MONGO_PASSWORD = 'Ze3cr1t!'

try:
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME,
                         password=MONGO_PASSWORD, serverSelectionTimeoutMS=1)

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)


db = client.airq_db
sensors = db.airq_sensors

start = datetime(2020, 3, 1, 9, 00, 00)
end = datetime(2020, 3, 1, 10, 00, 00)

myquery = {"timestamp" : {'$lt': end, '$gte': start}}

test = sensors.find(myquery)

for x in enumerate(test):
    print(x)


# test = sensors.find(myquery)
# for x in enumerate(test):
#     print(x)



#
# for i, sensor in enumerate(test):
#     lon, lat = sensor["location"]["coordinates"]
#     print("ausgabe: " + str(lon), str(lat))
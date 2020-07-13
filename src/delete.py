import requests
from pymongo import MongoClient, errors

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

myquery = {"location.coordinates" : None}

x = sensors.delete_many(myquery)
print(x.deleted_count, " documents deleted.")


# test = sensors.find(myquery)
# for x in enumerate(test):
#     print(x)



#
# for i, sensor in enumerate(test):
#     lon, lat = sensor["location"]["coordinates"]
#     print("ausgabe: " + str(lon), str(lat))
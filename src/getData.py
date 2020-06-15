import csv
import json
import io
from datetime import datetime
from pymongo import MongoClient, errors
import wget

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

x = {}
sensorList = []

wget.

#sensor_id;sensor_type;location;lat;lon;timestamp;P1;durP1;ratioP1;P2;durP2;ratioP2
with open("data/2020-05_sds011.csv") as csvdatei:
    csv_reader_object = csv.reader(csvdatei, delimiter=';')
    csv_reader_object.__next__()
    for row in csv_reader_object:
        x = {
            "sensor_id": row[0],
            "sensor_type": row[1],
            "location": {
                "type": "point",
                "coordinates": [row[4], row[3]]
            },
            "timestamp": datetime.fromisoformat(row[5]) ,
            "PM1": "",
            "PM4": "",
            "PM2": row[9],
            "PM10": row[6],
            "N10": "",
            "N4": "",
            "N2": "",
            "N1": "",
            "N05": "",
            "TS": ""
        }
        sensorList.append(x)

    #with io.open('2020-06-10_sds011_sensor_10154.json', 'w', encoding='utf8') as outfile:
     #   str_ = json.dumps(sensorList, indent=4, separators=(',', ': '), ensure_ascii=False)
      #  outfile.write(to_unicode(str_))


MONGO_HOST='localhost'
MONGO_PORT=8888
MONGO_USERNAME='mongoadmin'
MONGO_PASSWORD='secret'

maxSevSelDelay=1
print("adsf")

try:
    client = MongoClient(host='localhost', port=8888, username='mongoadmin', password='secret',
                         serverSelectionTimeoutMS=maxSevSelDelay)

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)

db = client.patricksDB2
sensoren = db.sensoren
sensoren.insert_many(documents=sensorList)
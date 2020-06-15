import datetime
import logging
import sys
from datetime import datetime
from pprint import pprint
from bson.son import SON
#sys.path.insert(1, 'd:/Nam/Docs/Uni/3_Semester/Visualisierung/code_project/repo')
sys.path.insert(1, 'd:/Nam/Docs/Uni/3_Semester/Visualisierung/code_project/repo')

from pymongo import MongoClient, errors
from bson.objectid import ObjectId

from src.config import Configuration


MONGO_HOST='localhost'
MONGO_PORT=8888
MONGO_USERNAME='mongoadmin'
MONGO_PASSWORD='secret'

maxSevSelDelay=1


_cfg = Configuration()

try:
    client = MongoClient(host='localhost', port=8888, username='mongoadmin', password='secret',
                         serverSelectionTimeoutMS=maxSevSelDelay)

    #logging.info(client.server_info())
    #logging.info(f"+{str(client.list_database_names())}")

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)

db = client.air_db
sensors = db.airq_data

def test_inserts():
    post = {"author": "ass",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    posts= db.posts
    post_id = posts.insert_one(post).inserted_id

    print(post_id)
    print("asstring "+str(post_id))

    print(db.list_collection_names())
    pprint(posts.find_one({"author": "ass"}))
    a = posts.find({"author": "ass"})

    for item in a:
        print(item)

def myfind():

    #SQL where example.
    #results = sensors.find({"sensor_id": 29175})

    #Nested Attribute Example, Where at least one of the coordinates elements contains 9.00258013
    #results = sensors.find({"location.coordinates": 9.00258013})

    ''' And Query example mit AND als beispiel. Gibt das $and immer an. Kann auch mit $or genutzt werden.
    d = datetime(2020,6,1)
    d = datetime.fromisoformat('2020-06-10')

    results = sensors.find(filter={"$and": [{"location.coordinates": 9.00258013}, {"timestamp": {"$gt": d}} ]})'''


    #Holt sich alle Sensors mit einen bestimmten typ und gibt nur 2 attribute jeweils zurück. Die eigentlichen werte, kp was die bedeuten.
    #results = sensors.find(filter={"sensor_type": 'SPS30'}, projection={"timestamp": -1, "sensor_type": 1})


    ''' Geowithin a Polygon
    results = sensors.find(
        {
        "location":{
            "$geoWithin":
                {"$geometry": {
                    "type": "Polygon", "coordinates": [
                    [ [9.0,48.0],[10.0,48.0],[10.0,50.0],[9.0,50.0],[9.0,48.0]]
                    ]
                    }
                }
            }
        }

    )'''

    results = sensors.find(
        {
            "location": {
                "$geoWithin": {
                    "$box": [
                        [ 10,50],[ 9,48 ]
                        ]
                }
            }
        }
    )
    

    for item in results:
        pprint(item)

myfind()

print("GUTE NACHT IHR MONGOS!")

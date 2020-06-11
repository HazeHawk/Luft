import datetime
import logging
import sys
import pprint
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
print("adsf")

_cfg = Configuration()

try:
    client = MongoClient(host='localhost', port=8888, username='mongoadmin', password='secret',
                         serverSelectionTimeoutMS=maxSevSelDelay)

    logging.info(client.server_info())
    logging.info(f"+{str(client.list_database_names())}")

except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    # tryagain later
    print(err)

db = client.test_database

post = {"author": "ass",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}

posts= db.posts
post_id = posts.insert_one(post).inserted_id

print(post_id)
print("asstring "+str(post_id))

print(db.list_collection_names())
pprint.pprint(posts.find_one({"author": "ass"}))
a = posts.find({"author": "ass"})

for item in a:
    print(item)

print("GUTE NACHT IHR MONGOS!")

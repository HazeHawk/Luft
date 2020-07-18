import threading
import time
from multiprocessing import Pool, Process, Queue, freeze_support
from pprint import pformat
import datetime
import queue

import pymongo as pm
from bson.objectid import ObjectId
from dateutil.relativedelta import *

from config import Configuration, Singleton

_cfg = Configuration()
logger = _cfg.LOGGER
q_logger = _cfg.Q_LOGGER

client = pm.MongoClient(host=_cfg.MONGO_HOST, port=_cfg.MONGO_PORT, username=_cfg.MONGO_USERNAME,
                                 password=_cfg.MONGO_PASSWORD, serverSelectionTimeoutMS=1)

db = client.airq_db
sensor_col = db.airq_sensors

def work_on_q(q):
    working = True
    logger.info("Start QQ")

    while working:
        try:
            sensor_id, start_date = q.get(timeout=100)
            insert_to_db(start_date, sensor_id)
        except queue.Full as e:
            working = False

    logger.info(f"Done QQ at {sensor_id} and {start_date}")

def insert_to_db(start_date: datetime.datetime, sensor_id: int):
    pip = []
    start_date = start_date
    end_date = start_date+relativedelta(hours=1)

    sensor_id_match = {"sensor_id": sensor_id}
    start_match = {"timestamp": {"$gte": start_date}}
    end_match = {"timestamp": {"$lt": end_date}}
    matches = {"$and": [sensor_id_match, start_match, end_match]}
    match = {"$match": matches}

    groups = { "_id": None,
                "sensor_id" : {"$first": "$sensor_id"},
                "sensor_type" : {"$first": "$sensor_type"},
                "location": {"$first": "$location"},
                "PM2": {"$avg": "$PM2"}, "PM10": {"$avg": "$PM10"}
        }
    group = {"$group": groups}

    setter = {"$set": {"timestamp": start_date}}

    unset = {"$unset": "_id"}

    merge = {"$merge": {"into" : "airq_sensors_fixed",
                        "whenMatched": "keepExisting",
                        "whenNotMatched": "insert"
                    }
    }

    stages = [match, group, setter, unset, merge]

    cursor = sensor_col.aggregate(pipeline=stages, allowDiskUse=True)

    for sensor in cursor:
        print(sensor)


def main():
    q = Queue()
    p1 = Process(target=work_on_q, args=(q,), name="NUBKEKS")
    p2 = Process(target=work_on_q, args=(q,), name="DERPKEKS")
    p3 = Process(target=work_on_q, args=(q,), name="dreikeks")
    p4 = Process(target=work_on_q, args=(q,), name="vierkeks")
    p5 = Process(target=work_on_q, args=(q,), name="funfkeks")
    p6 = Process(target=work_on_q, args=(q,), name="sexkeks")
    p7 = Process(target=work_on_q, args=(q,), name="zieppenkeks")
    p8 = Process(target=work_on_q, args=(q,), name="achtkeks")


    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    #p7.start()
    #p8.start()

    broke = 1685
    result = db.airq_sensors_fixed.delete_many({"sensor_id": broke})

    t0 = time.time()
    sensor_id_list = sensor_col.find(projection={"sensor_id":1}).distinct("sensor_id")

    last_date = datetime.datetime(2020,7,1)

    for sensor_id in sensor_id_list:
        if sensor_id < 1685:
            print(f'skip {sensor_id}')
            continue

        if q.qsize > 2000:
            time.sleep(10)
        # query dataset
        print(sensor_id)
        first_date = datetime.datetime(2020,3,1)
        while first_date < last_date:

            #put work to queue
            params = [sensor_id, first_date]
            q.put(params)

            first_date = first_date+relativedelta(hours=1)
    t1 = time.time()

    print(t1-t0)

    q.close()
    q.join_thread()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    #p7.join()
    #p8.join()
    print("Donus maximus")


if __name__ == "__main__":
    freeze_support()
    main()
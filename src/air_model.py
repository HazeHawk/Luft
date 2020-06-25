''' This is the air_model Module
Contains all model classes for DB connects and datahandling.
'''
import datetime
import logging

from dateutil.relativedelta import *
from pymongo import MongoClient, errors

from src.config import Configuration, Singleton

_cfg = Configuration()
class AirModel(Singleton):

    def __init__(self):

        try:
            client = MongoClient(host=_cfg.MONGO_HOST, port=_cfg.MONGO_PORT, username=_cfg.MONGO_USERNAME,
                                 password=_cfg.MONGO_PASSWORD, serverSelectionTimeoutMS=1)
        except errors.ServerSelectionTimeoutError as err:
            logging.error(str(err))

        logging.debug(client.server_info())
        logging.debug(f"{str(client.list_database_names())}")

        self.db = client.air_db
        self.sensors = self.db.airq_data

    def get_db(self):
        return self.db

    def get_sensors(self):
        return self.sensors


    #TODO die GeoQuery sollte direkt nach einem Read ein zu ein, so aufgerufen werden. Also das dict.
    # Überarbeiten wenn das nicht klappt
    def find_sensors_by(self, geometry=None, timestamp=None, day=None, month=None, year=None, timeframe=None):
        '''
            Query Mongo DB for finding sensor data in specific area and timeframe.
            If several parameters are given it will usually interpreted as AND Operator!
            Query Filters are in dictionary format(essentially JSON).
            Checkout PyMongo docs or official MongoDB docs
            (https://docs.mongodb.com/manual/tutorial/query-documents/)
            for more details regarding the matching operators.

            Parameters:
                time-related parameters should be a datetime object.
                timeframe: Tuple with start and ending date (start, end) of type datetimeobj
                day, month, year filter by just 1 month!


            Geometry Example

            geometry = {"$geometry": {"type": "Polygon",
                                    "coordinates": [[9.0,48.0],[10.0,48.0],[10.0,50.0],[9.0,50.0],[9.0,48.0]]
                                    }
                    }
            geometry = {"$box": [[ 10,50],[ 9,48 ]]}

            Timestamp Example

            time = {"$gt": datetime.fromisoformat('2020-06-10')}

            Make sure that the time attribute is an datetime Object.
        '''
        query = []
        start_date, end_date = None, None

        arg_num = list(locals().values()).count(None)
        if all(param is None for param in locals().values()):
            raise(ValueError("At least one argument must be set."))
        time_vars = [day, month, year, timeframe, timestamp]

        if time_vars.count(None)> 1:
            raise(ValueError("Only one timefilter (day, month, year, timeframe, timestamp) can be chosen!"))

        if geometry is not None:
            geo_match = {"location": {"$geoWithin": geometry}}
            query.append(geo_match)

        if not all(item is None for item in time_vars):
            if (timeframe is not None):
                start_date, end_date = timeframe
            elif day is not None:
                start_date = day
                end_date = start_date+relativedelta(day=1)
            elif month is not None:
                start_date = month
                end_date = start_date+relativedelta(months=1)
            elif year is not None:
                start_date = year
                end_date = start_date+relativedelta(years=1)
            time_match = {"timestamp": {"$and": [{"$gte": start_date}, {"$lt": end_date}]}}
            if timestamp is not None:
                time_match = {"timestamp": timestamp}

            query.append(time_match)

        if len(query)==1:
            query = query[0]

        results = self.sensors.find(filter=query)
        return results


    def read(self):
        pass


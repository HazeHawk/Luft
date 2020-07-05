''' This is the air_model Module
Contains all model classes for DB connects and datahandling.
'''
import datetime
import json
import sys
import time
from pprint import pformat

import pymongo as pm
from bson.objectid import ObjectId
from dateutil.relativedelta import *

from src.config import Configuration, Singleton

_cfg = Configuration()
logger = _cfg.LOGGER
q_logger = _cfg.Q_LOGGER

class AirModel(metaclass=Singleton):
    """Docstring Tests
    >>> Rando Docstring
    ``asd``    `aa`wert
    """
    def __init__(self):

        try:
            client = pm.MongoClient(host=_cfg.MONGO_HOST, port=_cfg.MONGO_PORT, username=_cfg.MONGO_USERNAME,
                                 password=_cfg.MONGO_PASSWORD, serverSelectionTimeoutMS=1)
            client.server_info()
        except pm.errors.ServerSelectionTimeoutError as err:
            logger.error(str(err))
            return

        self.db = client.airq_db2
        self.sensors_col = self.db.airq_sensors
        self.areas_col = self.db.areas
        self.smoltest_col = self.db.smoltest
        self.client = client
        self.create_index()

    def create_index(self):
        col1 = self.client.airq_db2.airq_sensors
        col1.create_index(keys=[('timestamp', pm.ASCENDING)], background=True)
        col1.create_index(keys=[("sensor_id", pm.ASCENDING)], background=True)
        col1.create_index(keys=[("sensor_type", pm.ASCENDING)], background=True)
        col1.create_index(keys=[("location", pm.GEOSPHERE)], background=True, name="GEO_INDEXU")
        col1.create_index(keys=[("timestamp", pm.DESCENDING),("location", pm.GEOSPHERE)], background=True)
        col1.create_index(keys=[("sensor_id", pm.ASCENDING), ("timestamp", pm.DESCENDING),("location", pm.GEOSPHERE)], background=True)

        col2 = self.client.airq_db2.areas
        col2.create_index(keys=[('properties.ID_1', pm.ASCENDING)], background=True, name="Bundesland_Index")
        col2.create_index(keys=[('properties.ID_2', pm.ASCENDING)], background=True, name="Bezirk_Index")
        col2.create_index(keys=[("geometry", pm.GEOSPHERE)], background=True, name="GEO_AREA_INDEXU")


    def test_model(self):

        self._test_queries()

    def _test_queries(self):
        geo = self.get_stuttgart_geo()
        day = datetime.datetime(2020,6,1)
        q_logger.debug("Start Testing Queries "+str(datetime.datetime.now().time()))

        #cursor1 = self.find_sensors_by_old(geometry=geo, month=datetime.datetime(2020,6,1))
        #self._explain_query(cursor1)

        cursor2 = self.find_sensors_by(geometry=geo, timeframe=(day, day+relativedelta(days=1)), group_by="sensor_id")

        for i, item in enumerate(cursor2):
            print(item)
            if i == 10:
                break

        print("DONUS MAXIMUS")


    def _explain_query(self, cursor):
        expa = cursor.explain()
        del expa["executionStats"]["allPlansExecution"]
        q_logger.debug("FindQuery")
        #q_logger.debug(f'Query Planner: {pformat(expa["queryPlanner"])}')
        q_logger.debug(f'Executionstats: {pformat(expa["executionStats"])}')
        q_logger.debug("FindQuery DONUS")


    def get_db(self):
        '''Return the database instance 'airq_db' from the MongoDB.'''
        return self.db

    def get_sensors_col(self):
        '''Return the airq_sensors collection from the db.'''
        return self.sensors_col

    def get_areas_col(self):
        '''Return the areas collection from the db.'''
        return self.areas_col

    def get_stuttgart_geo(self):
        '''Return a query filter dict obj ("JSON Format") of the Stuttgart Area'''
        areas = self.db.areas
        area = areas.find_one(filter={"properties.NAME_2": "Stuttgart"}, projection={"geometry":1})
        query_filter = {'$geometry': area['geometry']} # "$geometry"is need for the pymongo Query
        return query_filter

    #TODO die GeoQuery sollte direkt nach einem Read ein zu ein, so aufgerufen werden. Also das dict.
    # Überarbeiten wenn das nicht klappt
    def find_sensors_by_old(self, geometry=None, timestamp=None, day=None, month=None, year=None, timeframe=None):
        ''' Query Mongo DB for finding sensor data in specific area and timeframe.
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

            time = datetime.fromisoformat('2020-06-10')

            Make sure that the time attribute is an datetime Object.
        '''
        params = []
        start_date, end_date = None, None

        arg_num = list(locals().values()).count(None)
        if all(param is None for param in locals().values()):
            raise(ValueError("At least one argument must be set."))
        time_vars = [day, month, year, timeframe, timestamp]

        if time_vars.count(None)<4:
            raise(ValueError("Only one timefilter (day, month, year, timeframe, timestamp) can be chosen!"))

        if geometry is not None:
            geo_match = {"location": {"$geoWithin": geometry}}
            params.append(geo_match)

        if not all(item is None for item in time_vars):
            if (timeframe is not None):
                start_date, end_date = timeframe
            elif day is not None:
                start_date = day
                end_date = start_date+relativedelta(days=1)
            elif month is not None:
                start_date = month
                end_date = start_date+relativedelta(months=1)
            elif year is not None:
                start_date = year
                end_date = start_date+relativedelta(years=1)
            #time_match = {"timestamp": {"$and": [{"$gte": start_date}, {"$lt": end_date}]}}
            time_match = {"$and": [{"timestamp": {"$gte": start_date}}, {"timestamp": {"$lt": end_date}}]}
            #time_match = {"timestamp": {"$gte": start_date}, "timestamp": {"$lt": end_date}}
            if timestamp is not None:
                time_match = {"timestamp": timestamp}

            params.append(time_match)

        if len(params) == 1:
            query = params[0]
        else:
            query = {**geo_match, **time_match}

        #logger.debug(f'QUERY: {query}')
        results = self.sensors_col.find(filter=query)
        return results

    def find_area_by(self, bundesland=None, bezirk=None,  projection={"_id":0, "geometry":1}, as_ft_collection=False):
        ''' Returns cursor object of an area query.
            By default the query return only the geometry of the document.
            For unfiltered document, use projection=None

            Parameters:

                Bundesland - 2 Character String in Options: ['BW','BY','BE','BB','HB','HH','HE','MV','NI','NW','RP','SL','SN','ST','SH','TH']
                https://de.wikipedia.org/wiki/ISO_3166-2%3ADE is the convention for bundesländer abbrevation.

                bezirk - free string e.g. Stuttgart. (CASE SENSITIVE!)
        '''
        BL_OPTIONS= ['BW','BY','BE','BB','HB','HH','HE','MV','NI','NW','RP','SL','SN','ST','SH','TH']
        BL_OPT_DICT = {}
        for val, key in enumerate(BL_OPTIONS, start=1):
            BL_OPT_DICT[key] = val
        if bundesland not in BL_OPTIONS and bundesland is not None:
            raise ValueError(f'bundesland parameter must be in {BL_OPTIONS}')
        if [bundesland, bezirk].count(None) == 2:
            raise ValueError("Please just set one parameter bezirk or bundesland")

        areas = self.areas_col
        bl_query = {"properties.ID_1":BL_OPT_DICT[bundesland]}
        bezirk_query = {"properties.NAME_2": bezirk}
        query_filter = bl_query if not bezirk else bezirk_query
        cursor = areas.find(filter=query_filter, projection=projection)

        if as_ft_collection:
            ft_list = []
            for area in cursor:
                ft_list.append(area)
            feature_collection = {"type": "FeatureCollection",
                                  "features": ft_list
            }
            return feature_collection
        else:
            return cursor

    def find_sensors_by(self, geometry=None, timeframe=(None, None), group_by=None, sort_by=None, projection=None, show_debug=False):
        ''' Sort & projection sind noch nicht implementiert. Ist aber "einfach"
        Geometry, Timeframe und group_by funtionieren.

        Wenn ihr group_by nutzen wollt.
        group_by = sensor_id

        TimeFrame example für Tag
        start_date = day
        end_date = start_date+relativedelta(days=1)

        '''
        match, group, sort = None, None, None
        pip = []
        start_date, end_date = timeframe

        # Matching TODO find data for single sensor
        geo_match = {"location": {"$geoWithin": geometry}} if geometry is not None else None
        start_match = {"timestamp": {"$gte": start_date}} if timeframe is not None else None
        end_match = {"timestamp": {"$lt": end_date}} if timeframe is not None else None
        matches = self._merge_dicts([start_match, end_match, geo_match])
        match = {"$match": matches}


        # Group projection

        #Group_by, maybe prepare some options
        if group_by == 0:
            groups = { "_id": group_by,
                   "PM2_avg": {"$avg": "$PM2"},
                   "PM2_min": {"$min": "$PM2"},
                   "PM2_max": {"$max": "$PM2"},
                   "PM2_std": {"$stdDevPop": "$PM2"},
                   "PM10_avg": {"$avg": "$PM10"},
                   "PM10_min": {"$min": "$PM10"},
                   "PM10_max": {"$max": "$PM10"},
                   "PM10_std": {"$stdDevPop": "$PM10"}
                 }
        elif isinstance(group_by, str):
            groups = { "_id": "$"+group_by,
                    "sensor_type": {"$first": "$sensortype"},
                    "location": {"$first": "$location"},
                    "PM2_avg": {"$avg": "$PM2"},
                    "PM2_min": {"$min": "$PM2"},
                    "PM2_max": {"$max": "$PM2"},
                    "PM2_std": {"$stdDevPop": "$PM2"},
                    "PM10_avg": {"$avg": "$PM10"},
                    "PM10_min": {"$min": "$PM10"},
                    "PM10_max": {"$max": "$PM10"},
                    "PM10_std": {"$stdDevPop": "$PM10"}
                    }

        group = {"$group": groups} if group_by is not None else None

        stages = [match, sort, group]
        for stage in stages:
            if stage is not None:
                pip.append(stage)

        if show_debug:
            #q_logger.debug("Explain Cursor V1 - Nur Queryplan?")
            #explain_cursor = self.db.command('aggregate', 'airq_sensors', pipeline=pip, explain=True, allowDiskUse=True)
            #q_logger.debug(pformat(explain_cursor))
            q_logger.debug(f"ExplainCursor with EXEC - {datetime.datetime.now().time()}")
            explain_aggregate = self.db.command('explain', {'aggregate': 'airq_sensors', 'pipeline': pip, 'cursor': {}}, verbosity='executionStats')
            #del another['queryPlanner']
            q_logger.debug(pformat(explain_aggregate))

        cursor = self.sensors_col.aggregate(pipeline=pip, allowDiskUse=True)
        return cursor



    def _median(self):
        #https://stackoverflow.com/questions/20456095/calculate-the-median-in-mongodb-aggregation-framework
        pass

    def _merge_dicts(self, dicts):
        '''Takes a list of dicts and merges them into a bigger dict.'''
        merged = {}
        for a_dict in dicts:
            if not a_dict:
                continue
            else:
                merged = {**merged, **a_dict}
        return merged



    def read(self):
        pass

     #ID + indexe for the areas is unclear, but because of few query length optimization can be ignored imo.

    def _import_areas(self):
        areas = self.db.areas
        with open('data/areas/bezirke_compact.json', encoding='utf-8') as f:
            json_data = json.load(f)

        areas.insert_many(json_data)

    def __old_examples(self):
        def do_query():
            geo = self.get_stuttgart_geo()

            #cursor = self.find_sensors_by(geometry=geo)
            filteru = {"location": {"$geoWithin": geo}}

            cursor = self.sensors_col.find(filter=filteru)
            q_logger.debug(cursor.explain())

            for item in cursor[:10]:
                print(item)

        def do_query2():

            cursor = self.find_area_by(bundesland='BW', projection={"properties":1})
            q_logger.debug(cursor.explain())

            for item in cursor[:10]:
                print(item)

        def do_query3():
            geo = self.get_stuttgart_geo()
            start_time = datetime.datetime(year=2020, month=6, day=28)
            end_time = start_time+relativedelta(hours=3)

            logger.debug((start_time, end_time))
            #geo = None
            #cursor = self.find_sensors_by(geometry=geo, timeframe=(start_time, end_time))
            cursor = self.find_sensors_by_old(geometry=geo, day=datetime.datetime(2020,6,1))
            day = datetime.datetime(2020,6,1)
            #cursor = self._pipeline(geometry=geo, timeframe=(month, month+relativedelta(days=1)))
            q_logger.debug("Start Testing "+str(datetime.datetime.now().time()))

            self._explain_query(cursor)

            for i, item in enumerate(cursor):
                print(item)
                if i==10:
                    break



if __name__ == 'main':
    model = AirModel()
    model.test_model()


import sys
from datetime import date, datetime
from pprint import pformat

import folium
import pymongo as pm
from dateutil.relativedelta import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QApplication, QWidget

from src.air_model import AirModel
from src.air_view import AirView
from src.config import Configuration

_cfg = Configuration()
logger = _cfg.LOGGER

class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.widget = QWidget()

        self._ui = AirView()
        self._ui.setupUi(self.widget)

        self._homeDateStart = self._ui.homeDateEditStart.date()
        self._homeDateEnd = self._ui.homeDateEditEnd.date()
        self._ui.homeDateEditStart.dateChanged.connect(self.setHomeDateStart)
        self._ui.homeDateEditEnd.dateChanged.connect(self.setHomeDateEnd)

        self.model = AirModel()

    def test(self):
        sensors = self.model.get_sensors()
        jan = datetime(year=2020,month=1,day=1)
        cursor = self.model.find_sensors_by_old(day=jan)
        print(cursor.explain())

    def run(self):

        self.widget.show()
        self.load_home_data()
        self.load_test_circles()
        logger.info("Running Over is dono")

    def load_home_data(self, timeframe=None):

        if not timeframe:
            d = date.today()
            today = datetime(d.year, d.month, d.day)

            today = datetime(2020,6,1) # tmp

            start_time = today
            end_time = today+relativedelta(hours=1)

        stuttgart_geo = self.model.get_stuttgart_geo()

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})
        areas = self.model.find_area_by(bundesland="BW", projection=None)
        list = []

        for area in areas:
            print(pformat(area))
            geo = {'$geometry': area['geometry']}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by=0)


            for i, sensor in enumerate(cursor):
                if i == 5:
                    break
                sensor['NAME_2'] = area["properties"]["NAME_2"]
                logger.debug(pformat(sensor))
                list.append({"ID": sensor["NAME_2"], "AVG": sensor['PM2_avg']})

        self.choroplethTest(geometry=areas, data=list)



    def load_test_circles(self):
        self.setFoliumCircle(48.780, 9.175, "murks")
        self.setFoliumCircle(48.785, 9.175, "marks")
        self.setFoliumCircle(48.775, 9.175, "merks")
        self.setFoliumCircle(48.780, 9.180, "mirks")
        self.setFoliumCircle(48.780, 9.170, "morks")

    def get_popup_str(self):
        pass

    def choroplethTest(self, geometry, data):
        folium.Choropleth(
            geo_data=geometry,
            name='choropleth',
            data=data,
            columns=['State', 'Unemployment'],
            key_on='feature.properties.NAME_2',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Unemployment Rate (%)'
        ).add_to(self._ui.m)

        self._ui.homeWidgetMap.setHtml(self._ui.saveFoliumToHtml().getvalue().decode())

        self._ui.homeWidgetMap.update()

    def setFoliumCircle(self, lat:float, long:float, popup:str):
        folium.Circle(
            location=[lat, long],
            radius=20,
            popup=popup,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(self._ui.m)


    def _refresh_home_map(self):
        self._ui.homeWidgetMap.setHtml(self._ui.saveFoliumToHtml().getvalue().decode())
        self._ui.homeWidgetMap.update()


    def setHomeDateStart(self):
        logger.debug(self._ui.homeDateEditStart.date())
        self._homeDateStart = self._ui.homeDateEditStart.date()

    def getHomeDateStart(self):
        return self._homeDateStart

    def setHomeDateEnd(self):
        logger.debug(self._ui.homeDateEditEnd.date())
        self._homeDateEnd = self._ui.homeDateEditEnd.date()

    def getHomeDateEnd(self):
        return self._homeDateEnd

    def setLabelMedian(self, median: str):
        self._ui.homeLabelMedian.setText(median)

    def setLabelMaximum(self, maximum: str):
        self._ui.homeLabelMaximal.setText(maximum)

    def setLabelMinimum(self, minimum: str):
        self._ui.homeLabelMinimal.setText(minimum)

    def setLabelAverag(self, average:str):
        self._ui.homeLabelAverage.setText(average)

    def setLabelSensorCount(self, sensorCount: str):
        self._ui.homeLabelSencorCount.setText(sensorCount)
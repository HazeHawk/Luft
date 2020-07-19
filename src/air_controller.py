import time
import json
import statistics
import sys
import threading
from datetime import date, datetime
from pprint import pformat

import altair.vegalite.v3 as alt
import folium
import numpy as np
import pandas as pd
from dateutil.relativedelta import *
from folium.plugins import MarkerCluster
from opencage.geocoder import OpenCageGeocode
from PySide2.QtCharts import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from src.air_model import AirModel
from src.air_view import AirView
from src.config import Configuration
from src.qthread_data import QThreadData

_cfg = Configuration()
logger = _cfg.LOGGER

class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        self.widget = QWidget()

        self._ui = AirView()
        self._ui.setupUi(self.widget)
        self._ui.homeLineEditPosition.returnPressed.connect(self.gethomeLineEditPosition)

        self._ui.homeDateEditStart.setMinimumDate(QDate(2020, 3, 1))
        self._ui.homeDateEditStart.setMaximumDate(QDate(2020, 6, 30))
        self._ui.homeDateEditStart.setDate(QDate(2020, 3, 1))
        self._homeDateStart = self._ui.homeDateEditStart.date()
        self._ui.homeDateEditStart.dateChanged.connect(self.setHomeDateStart)

        self._homeTimeStart = self._ui.homeTimeEditStart.time()

        self._ui.homeDateEditEnd.setMinimumDate(QDate(2020, 3, 1))
        self._ui.homeDateEditEnd.setMaximumDate(QDate(2020, 6, 30))
        self._ui.homeDateEditEnd.setDate(QDate(2020, 3, 1))
        self._homeDateEnd = self._ui.homeDateEditEnd.date()
        self._ui.homeDateEditEnd.dateChanged.connect(self.setHomeDateEnd)

        self._homeTimeEnd = self._ui.homeTimeEditEnd.time()

        self._ui.homeButtonSendData.clicked.connect(self.homeButtonSendClicked)

        self.location = [48.77915707462204, 9.175987243652344]

        self.messageBox = QMessageBox()
        self.messageBox.setIcon(QMessageBox.Information)
        self.messageBox.setWindowTitle("Warning!")
        self.messageBox.setText("The input position is non existent!")
        self.messageBox.setInformativeText("Please enter a valid location.")
        self.messageBox.setStandardButtons(QMessageBox.Ok)

        self.choropleth = None
        self.clusterPoints = None
        self.singlePoints = None

        self.model = AirModel()

    def run(self):
        self.widget.show()
        self._ui.homeButtonSendData.setEnabled(False)
        self.load_view_util()

        logger.info("Running Over is dono")

    def load_view_util(self):
        self.home_loading_start()

        tasks = [self.load_home_data, self.load_cluster_circle_home, self.load_single_circle_home]
        #tasks = [self.load_home_data]
        #tasks = [self.load_single_circle_home]
        self.thread = QThreadData(tasks)
        self.thread.start()
        self._ui.connect(self.thread, SIGNAL("finished()"), self.refresh_home_util)
        self.thread.exit()

    def load_home_data(self):

        start_time, end_time = self.getTimeframe()

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})
        #areas = self.model.find_area_by(bundesland="BW", projection=None, as_ft_collection=True)

        with open('data/areas/bezirke.json', encoding='utf-8') as f:
            areas = json.load(f)

        listID = []
        listAVG = []

        for area in areas["features"]:
            geo = {"$geometry": area["geometry"]}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by=0)

            for i, sensor in enumerate(cursor):
                sensor['NAME_2'] = area["properties"]["NAME_2"]
                #logger.debug(pformat(sensor))
                listID.append(area["properties"]["NAME_2"])
                listAVG.append(sensor['PM2_avg'])

        data = {'AVG': listAVG, 'ID': listID}

        self.load_analysis(listID, listAVG)
        self.load_highlights(listID, listAVG)

        dataFrameData = pd.DataFrame.from_dict(data)
        self.choropleth = self.choroplethTest(geometry=areas, data=dataFrameData)

    def load_single_circle_home(self):
        start_time, end_time = self.getTimeframe()

        fg = folium.FeatureGroup(name="Single Circles")
        sfgList = []

        sensorCount = 0
        pm2_avgList = []

        self.popup_list = []

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})
        with open('data/areas/bezirke.json', encoding='utf-8') as f:
            areas = json.load(f)

        for area in areas["features"]:
            geo = {'$geometry': area['geometry']}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by='sensor_id')

            sfg = folium.plugins.FeatureGroupSubGroup(fg, name="Single points " + area["properties"]["NAME_2"])

            for i, sensor in enumerate(cursor):
                #t0 = time.time()
                lon, lat = sensor["location"]["coordinates"]
                if False:
                    popup = self.get_sensor_popup(sensor_id=sensor["_id"],
                                              timeframe=(start_time, end_time), time_group="h")
                else:
                    data = {"Bundesland":area["properties"]["NAME_2"],**sensor}
                    data['location'] = str(data['location']['coordinates'])
                    df = pd.DataFrame(data, index=[0])
                    html = df.to_html(classes='table table-striped table-hover table-condensed table-responsive')
                    popup = folium.Popup(html)
                self.popup_list.append(popup)

                if sensor["PM2_avg"] is not None and 0 < sensor["PM2_avg"] < 999:
                    pm2_avgList.append(sensor["PM2_avg"])

                self.setFoliumCircle(lat=lat, long=lon, popup=popup).add_to(sfg)
                sensorCount += 1
                #t1 = time.time()
                #logger.debug(f"{sensor['_id']} took {t1-t0} s")

            sfgList.append(sfg)

        for item in sfgList:
            fg.add_child(item)
        self.singlePoints = fg

        self.setLabelSensorCount(str(sensorCount))
        self.setLabelMinimum(str(round(min(pm2_avgList), 4)))
        self.setLabelMaximum(str(round(max(pm2_avgList), 4)))
        self.setLabelAverag(str(round(sum(pm2_avgList)/len(pm2_avgList), 4)))

        pm2_avgList.sort()
        self.setLabelMedian(str(round(statistics.median(pm2_avgList), 4)))

    def load_cluster_circle_home(self):
        start_time, end_time = self.getTimeframe()

        with open('data/areas/bezirke.json', encoding='utf-8') as f:
            areas = json.load(f)

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})

        fg = folium.FeatureGroup(name="Cluster Circles")
        sfgList = []

        for area in areas["features"]:
            location_list = []
            popup_list = []

            geo = {'$geometry': area['geometry']}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by='sensor_id')

            for i, sensor in enumerate(cursor):
                lon, lat = sensor["location"]["coordinates"]
                data = {"Bundesland":area["properties"]["NAME_2"],**sensor}
                data['location'] = str(data['location']['coordinates'])
                df = pd.DataFrame(data, index=[0])
                html = df.to_html(classes='table table-striped table-hover table-condensed table-responsive')
                popup = folium.Popup(html)

                location_list.append([lat, lon])
                popup_list.append(popup)

            sfg = folium.plugins.FeatureGroupSubGroup(fg, name=area["properties"]["NAME_2"])

            cluster = self.setFoliumMarkerCluster(coordinates=location_list, popup=popup_list)
            cluster.add_to(sfg)

            sfgList.append(sfg)

        for item in sfgList:
            fg.add_child(item)
        self.clusterPoints = fg

    def getTimeframe(self):

        start_time = self.getHomeDateStart().toPython()
        start_time = start_time + relativedelta(
            hours=self.getHomeTimeStart().hour(),
            minutes=self.getHomeTimeStart().minute(),
            seconds=self.getHomeTimeStart().second()
        )

        end_time = self.getHomeDateEnd().toPython()
        end_time = end_time + relativedelta(
            hours=self.getHomeTimeEnd().hour(),
            minutes=self.getHomeTimeEnd().minute(),
            seconds=self.getHomeTimeEnd().second()
        )

        return start_time, end_time

    def load_analysis(self, listID:list, listAVG:list):

        listID = listID[:4]
        listAVG = listAVG[:4]

        dataSet2 = QtCharts.QBarSet("PM2_avg")
        for item in listAVG:
            dataSet2.append(item)

        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(listID)

        axisY = QtCharts.QValueAxis()
        min = 0
        max = 0
        for item in listAVG:
            if min>item:
                min=item
            if max<item:
                max=item

        axisY.setRange(min, max)

        dataSeries = QtCharts.QBarSeries()
        dataSeries.append(dataSet2)
        dataSeries.attachAxis(axisX)
        dataSeries.attachAxis(axisY)

        self._ui.analysisChart.addAxis(axisX, Qt.AlignBottom)
        self._ui.analysisChart.addAxis(axisY, Qt.AlignLeft)

        self._ui.analysisChart.addSeries(dataSeries)
        self._ui.analysisChart.legend().setVisible(True)
        self._ui.analysisChart.legend().setAlignment(Qt.AlignBottom)
        self._ui.analysisChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)

    def load_highlights(self, listID: list, listAVG: list):

        series = QtCharts.QPieSeries()

        for itemID, itemAVG in zip(listID, listAVG):
            series.append(itemID, itemAVG)

        slice = QtCharts.QPieSlice()

        for i in range(0, series.count()):
            slice = series.slices()[i]
            slice.setLabelVisible(True)

        self._ui.highlightsQChart.legend().setVisible(True)
        self._ui.highlightsQChart.legend().setAlignment(Qt.AlignBottom)
        self._ui.highlightsQChart.addSeries(series)
        self._ui.highlightsQChart.createDefaultAxes()
        self._ui.highlightsQChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self._ui.highlightsQChart.setTitle("Pie Chart Example")

    def get_popup_str(self):
        pass

    def setFoliumMarkerCluster(self, coordinates:list, popup:list):
        options_dict = {"showCoverageOnHover":True, "removeOutsideVisibleBounds":False,
                        "spiderfyOnMaxZoom":True, "maxClusterRadius":80}
        #cluster = folium.plugins.FastMarkerCluster(data=coordinates, popups=popup, name="SensorClusterLayer")

        cluster = MarkerCluster(locations=coordinates, popups=popup)

        return cluster
        pass

    def get_sensor_popup(self, sensor_id, timeframe, time_group, as_html):
        """Return a `folium.Popup` Object, which has a multiline lineplot for a single sensor.

        group_by
            - Must be in ["y","m","d","h"] """
        t0 = time.time()
        cursor = self.model.find_single_sensor(sensor_id=sensor_id, timeframe=timeframe, group_by=time_group)
        data = []
        t1 = time.time()
        for item in cursor:
            item['date'] = item['_id']
            del item['_id']
            del item['sensor_id']
            data.append(item)
        t2 = time.time()

        df = pd.DataFrame(data)
        df = df.melt('date', var_name='PM_category', value_name='concentration')  #µg_per_m3

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=['date'], empty='none')

        # The basic line
        line = alt.Chart(df).mark_line(interpolate='basis').encode(
            x='date:O',
            y='concentration:Q',
            color='PM_category:N'
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(df).mark_point().encode(
            x='date:O',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'concentration:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='date:O',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        layered = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=500, height=300
        )

        chart_json = layered.to_json()
        vega = folium.VegaLite(chart_json, width=650)
        popup = folium.Popup()
        vega.add_to(popup)
        t_end= time.time()

        """ Takes about 0.3 seconds to build plot
        logger.debug(f"t1 took {t1-t0} s")
        logger.debug(f"t2 took {t2-t1} s")
        logger.debug(f"t2 end took {t_end-t2} s")
        logger.debug(f"t1 took {t_end-t0} s")
        """
        return popup


    def choroplethTest(self, geometry, data):
        choro = folium.Choropleth(
            geo_data=geometry,
            name='choropleth',
            data=data,
            columns=['ID', 'AVG'],
            key_on='feature.properties.NAME_2',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Average PM2'
        )

        style_function = "font-size: 15px; font-weight: bold"
        choro.geojson.add_child(folium.GeoJsonTooltip(["NAME_2"], style=style_function, labels=False))

        return choro

        #WTF Warum geht das hier fürs choro und sonst nirgends?
        #folium.LayerControl().add_to(self._ui.m)

        #self._ui.homeWidgetMap.setHtml(self._ui.saveFoliumToHtml().getvalue().decode())

        #self._ui.homeWidgetMap.update()

    def setFoliumCircle(self, lat:float, long:float, popup:str):
        return folium.Circle(
            location=[lat, long],
            radius=50,
            popup=popup,
            color='blue',
            fill=True,
            fill_color='blue'
        )

    def refresh_home_util(self):
        tasks = [self.buildFoliumMap]
        self.thread = QThreadData(tasks)
        self.thread.start()
        self._ui.connect(self.thread, SIGNAL("finished()"), self.refresh_home_map)
        self.thread.exit()

    def refresh_home_map(self):
        self._ui.homeWidgetMap.reload()
        self._ui.homeWidgetMap.update()
        self.home_loading_end()

    def buildFoliumMap(self):

        map = folium.Map(location=self.location, tiles="Stamen Toner", zoom_start=12)

        if self.choropleth is not None:
            map.add_child(self.choropleth)

        if self.clusterPoints is not None:
            map.add_child(self.clusterPoints)

        if self.singlePoints is not None:
            map.add_child(self.singlePoints)

        folium.LayerControl().add_to(map)

        map.save('./data/html/map.html', close_file=False)

    def home_loading_start(self):
        self._ui.homeButtonSendData.setEnabled(False)
        self._ui.homeLineEditPosition.setEnabled(False)
        self._ui.homeLoadingLabel.show()
        self._ui.homeLoadingMovie.start()

    def home_loading_end(self):
        self._ui.homeLoadingLabel.hide()
        self._ui.homeLoadingMovie.stop()
        self._ui.homeLineEditPosition.setEnabled(True)
        self._ui.homeButtonSendData.setEnabled(True)

    def homeButtonSendClicked(self):
        self._ui.homeButtonSendData.setEnabled(False)

        self.setHomeTimeStart()
        self.setHomeTimeEnd()

        self.load_view_util()
        #self.thread_test()

    def setHomeDateStart(self):
        logger.debug(self._ui.homeDateEditStart.date())
        self._homeDateStart = self._ui.homeDateEditStart.date()
        self._ui.homeDateEditEnd.setMinimumDate(self._ui.homeDateEditStart.date())

    def getHomeDateStart(self):
        return self._homeDateStart

    def setHomeDateEnd(self):
        logger.debug(self._ui.homeDateEditEnd.date())
        self._homeDateEnd = self._ui.homeDateEditEnd.date()

    def getHomeDateEnd(self):
        return self._homeDateEnd

    def setHomeTimeStart(self):
        logger.debug(self._ui.homeTimeEditStart.time())
        self._homeTimeStart = self._ui.homeTimeEditStart.time()

    def getHomeTimeStart(self):
        return self._homeTimeStart

    def setHomeTimeEnd(self):
        logger.debug(self._ui.homeTimeEditEnd.time())

        if (self._homeTimeStart.toPython() > self._ui.homeTimeEditEnd.time().toPython()):
            self._homeTimeEnd = self._homeTimeStart.addSecs(3600)
            self._ui.homeTimeEditEnd.setTime(self._homeTimeStart.addSecs(3600))
        else:
            self._homeTimeEnd = self._ui.homeTimeEditEnd.time()

    def getHomeTimeEnd(self):
        return self._homeTimeEnd

    def setLabelMedian(self, median: str):
        self._ui.homeLabelMedian.setText("Median: " + median)

    def setLabelMaximum(self, maximum: str):
        self._ui.homeLabelMaximal.setText("Maximum: " + maximum)

    def setLabelMinimum(self, minimum: str):
        self._ui.homeLabelMinimal.setText("Minimum: " + minimum)

    def setLabelAverag(self, average:str):
        self._ui.homeLabelAverage.setText("Average: " + average)

    def setLabelSensorCount(self, sensorCount:str):
        self._ui.homeLabelSencorCount.setText("Sensor Count: " + sensorCount)

    def getCoordinates(self, name):
        key = "3803f50ca47344bf87e9c165d4e7fa94"
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(name)
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return [lat, lng];

    def gethomeLineEditPosition(self):
        self.home_loading_start()
        try:
            city = self._ui.homeLineEditPosition.text()
            coordinates = self.getCoordinates(city)
            #self._ui.m.location = [48.77915707462204, -9.175987243652344]
            self.location = coordinates
            self.refresh_home_util()
        except:
            self.home_loading_end()
            self.messageBox.show()

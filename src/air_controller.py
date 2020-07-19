import sys
from datetime import date, datetime
from pprint import pformat
import json
import folium
import altair.vegalite.v3 as alt
from altair_saver import save as altSave
from chromedriver_py import binary_path
from folium.plugins import MarkerCluster
from PySide2.QtCharts import *
from PySide2.QtCore import *
from dateutil.relativedelta import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pandas as pd
from opencage.geocoder import OpenCageGeocode
from src.air_model import AirModel
from src.air_view import AirView
from src.config import Configuration
from src.qthread_data import QThreadData
import statistics


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
        self._ui.highlightsCompareButton.clicked.connect(self.reload_linechart)

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
        self.singlePointsO500 = None

        self.dateaxis = QtCharts.QDateTimeAxis()
        self.value_axis = QtCharts.QValueAxis()
        self.anaaxisX = QtCharts.QBarCategoryAxis()
        self.anaaxisY = QtCharts.QValueAxis()
        self.scattervalue_axis = QtCharts.QValueAxis()
        self.scattervalue_axisbot = QtCharts.QValueAxis()
        self.scattervalue_axis2 = QtCharts.QValueAxis()
        self.scattervalue_axisbot2 = QtCharts.QValueAxis()

        self.model = AirModel()

    def test(self):
        sensors = self.model.get_sensors()
        jan = datetime(year=2020,month=1,day=1)
        cursor = self.model.find_sensors_by_old(day=jan)
        print(cursor.explain())

    def run(self):

        self.widget.show()

        self._ui.homeButtonSendData.setEnabled(False)
        self.load_view_util()

        logger.info("Running Over is dono")

    def load_view_util(self):
        self.home_loading_start()

        self.clear_diagramms()

        tasks = [self.load_home_data, self.load_cluster_circle_home, self.load_single_circle_home, self.load_line_chart]
        self.thread = QThreadData(tasks)
        self.thread.start()
        self._ui.connect(self.thread, SIGNAL("finished()"), self.refresh_home_util)
        self.thread.exit()

    def clear_diagramms(self):
        self._ui.analysisChart.removeAllSeries()
        self._ui.analysisChart.removeAxis(self.anaaxisY)
        self._ui.analysisChart.removeAxis(self.anaaxisX)

        self._ui.highlightsBWAVG.removeAllSeries()
        self._ui.highlightsBWAVG.removeAxis(self.dateaxis)
        self._ui.highlightsBWAVG.removeAxis(self.value_axis)

        self._ui.highlightsScatterChart.removeAllSeries()
        self._ui.highlightsScatterChart.removeAxis(self.scattervalue_axis)
        self._ui.highlightsScatterChart.removeAxis(self.scattervalue_axisbot)

        self._ui.highlightsScatterChart250.removeAllSeries()
        self._ui.highlightsScatterChart250.removeAxis(self.scattervalue_axis2)
        self._ui.highlightsScatterChart250.removeAxis(self.scattervalue_axisbot2)

        self._ui.highlightsQChart.removeAllSeries()

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

        fg = folium.FeatureGroup(name="Single Sensors", show=False)
        fgO500 = folium.FeatureGroup(name="Single Sensors over PM2 AVG 500", show=False)

        sfgList = []
        sfgList0500 = []

        sensorCount = 0
        sensorCountFiltered = 0
        pm2_avgList = []

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})
        with open('data/areas/bezirke.json', encoding='utf-8') as f:
            areas = json.load(f)

        for area in areas["features"]:
            geo = {'$geometry': area['geometry']}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by='sensor_id')

            sfg = folium.plugins.FeatureGroupSubGroup(fg, name="Single Sensors " + area["properties"]["NAME_2"])
            sfgo500 = folium.plugins.FeatureGroupSubGroup(fgO500, name="Single Sensors over 500 " + area["properties"]["NAME_2"])

            for i, sensor in enumerate(cursor):
                lon, lat = sensor["location"]["coordinates"]
                popup = pformat({"Bezirk":area["properties"]["NAME_2"],**sensor})

                self.setFoliumCircle(lat=lat, long=lon, popup=popup, color='blue').add_to(sfg)

                # Roter Kreis wenn PM2_avg wert über 500
                if sensor["PM2_avg"] is not None and sensor["PM2_avg"] > 500:
                    self.setFoliumCircle(lat=lat, long=lon, popup=popup, color='red').add_to(sfgo500)

                sensorCount += 1

                if sensor["PM2_avg"] is not None and 0 < sensor["PM2_avg"] < 999:
                    pm2_avgList.append(sensor["PM2_avg"])
                    sensorCountFiltered += 1

            sfgList.append(sfg)
            sfgList0500.append(sfgo500)

        for item in sfgList:
            fg.add_child(item)
        self.singlePoints = fg

        for item in sfgList0500:
            fgO500.add_child(item)
        self.singlePointsO500 = fgO500

        self.setLabelSensorCount(str(sensorCount))
        self.setLabelSensorCountFiltered(str(sensorCountFiltered))
        self.setLabelMinimum(str(round(min(pm2_avgList), 3)))
        self.setLabelMaximum(str(round(max(pm2_avgList), 3)))
        self.setLabelAverag(str(round(sum(pm2_avgList)/len(pm2_avgList), 3)))

        pm2_avgList.sort()
        self.setLabelMedian(str(round(statistics.median(pm2_avgList), 3)))

    def load_cluster_circle_home(self):
        start_time, end_time = self.getTimeframe()

        with open('data/areas/bezirke.json', encoding='utf-8') as f:
            areas = json.load(f)

        #areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})

        fg = folium.FeatureGroup(name="Clustered Sensors", show=False)
        sfgList = []

        listpm2max = []
        listpm2min = []
        listbezirk = []

        for area in areas["features"]:
            location_list = []
            popup_list = []

            geo = {'$geometry': area['geometry']}
            cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by='sensor_id')

            for i, sensor in enumerate(cursor):
                lon, lat = sensor["location"]["coordinates"]
                popup = pformat({"Bundesland":area["properties"]["NAME_2"],**sensor})

                location_list.append([lat, lon])
                popup_list.append(popup)

                #scatter plot daten
                if sensor is not None and area["properties"]["NAME_2"] is not None:
                    listpm2min.append(sensor["PM2_min"])
                    listpm2max.append(sensor["PM2_max"])
                    listbezirk.append(str(area["properties"]["NAME_2"]))

            sfg = folium.plugins.FeatureGroupSubGroup(fg, name=area["properties"]["NAME_2"])

            cluster = self.setFoliumMarkerCluster(coordinates=location_list, popup=popup_list)
            cluster.add_to(sfg)

            sfgList.append(sfg)

        data = {
            'PM2MAX': listpm2max,
            'PM2MIN': listpm2min,
            'Bezirk': listbezirk
        }

        self.scatter_plot_all_sensors(data)

        for item in sfgList:
            fg.add_child(item)
        self.clusterPoints = fg

    def load_line_chart(self):
        start_time = self.getHomeDateStart().toPython()
        start_time = start_time + relativedelta(
            hour=0,
            minute=0,
            second=0
        )

        d2 = datetime(2020, 6, 30, 0, 0, 0)

        if start_time > d2:
            start_time = d2

        pMax = 0

        self._ui.highlightsBWAVG.setTitle('Compare Countrie Average ' + str(start_time.date()))
        series = QtCharts.QLineSeries()

        #BL_OPTIONS = ['BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'MV', 'NI', 'NW', 'RP', 'SL', 'SN', 'ST', 'SH', 'TH']

        # areas = self.model.find_area_by(bundesland="BW", projection={"_id":0, "properties.NAME_2":1,"geometry":1})
        bulas = [self._ui.highlightsCompareCombo1.currentText(), self._ui.highlightsCompareCombo2.currentText()]

        for bula in bulas:
            series = QtCharts.QLineSeries()
            series.setName(bula)
            listID = []
            listAVG = []
            areas = self.model.find_area_by(bundesland=bula, projection=None, as_ft_collection=True)

            for i in range(1, 26):

                end_time = start_time + relativedelta(hours=1)
                pAvg = 0
                count = 0

                for area in areas["features"]:
                    geo = {"$geometry": area["geometry"]}
                    cursor = self.model.find_sensors_by(geometry=geo, timeframe=(start_time, end_time), group_by=0)

                    for sensor in cursor:
                        pAvg += sensor['PM2_avg']

                count += 1

                listID.append(start_time)
                listAVG.append(pAvg/4)

                if pMax < pAvg/count:
                    pMax = pAvg/count

                start_time = start_time + relativedelta(hours=1)

            for date, avg in zip(listID, listAVG):
                series.append(float(QDateTime(date.year, date.month, date.day, date.hour, 0, 0).toMSecsSinceEpoch()), avg)

            self._ui.highlightsBWAVG.addSeries(series)

        self.dateaxis = QtCharts.QDateTimeAxis()
        self.dateaxis.setTickCount(13)
        self.dateaxis.setTitleText('Hour')
        self.dateaxis.setFormat('hh:mm:ss')
        self._ui.highlightsBWAVG.addAxis(self.dateaxis, Qt.AlignBottom)
        series.attachAxis(self.dateaxis)

        self.value_axis = QtCharts.QValueAxis()
        self.value_axis.setRange(0, round(pMax, 0))
        self.value_axis.setTickCount(5)
        self.value_axis.setTitleText('PM2 Average')
        self._ui.highlightsBWAVG.addAxis(self.value_axis, Qt.AlignLeft)

        self._ui.highlightsBWAVG.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)

    def reload_linechart(self):
        self._ui.highlightsBWAVG.removeAllSeries()
        self._ui.highlightsBWAVG.removeAxis(self.dateaxis)
        self._ui.highlightsBWAVG.removeAxis(self.value_axis)
        self.thread2 = QThreadData([self.load_line_chart])
        self.thread2.start()
        self.thread2.exit()

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

    def scatter_plot_all_sensors(self, data:dict):

        series = QtCharts.QScatterSeries()
        series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(15)

        for pm2min, pm2max in zip(data['PM2MIN'], data['PM2MAX']):
            if pm2min is not None and pm2max is not None:
                series.append(pm2min, pm2max)

        self._ui.highlightsScatterChart.addSeries(series)
        self._ui.highlightsScatterChart.setTitle('Scatter of all Sensors PM2 min/max')
        self._ui.highlightsScatterChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)

        self.scattervalue_axis = QtCharts.QValueAxis()
        self.scattervalue_axis.setRange(0, 1000)
        self.scattervalue_axis.setTickCount(5)
        self.scattervalue_axis.setTitleText('PM2 maximal')

        self._ui.highlightsScatterChart.addAxis(self.scattervalue_axis, Qt.AlignLeft)

        self.scattervalue_axisbot = QtCharts.QValueAxis()
        self.scattervalue_axisbot.setRange(0, 1000)
        self.scattervalue_axisbot.setTickCount(5)
        self.scattervalue_axisbot.setTitleText('PM2 minimal')

        self._ui.highlightsScatterChart.addAxis(self.scattervalue_axisbot, Qt.AlignBottom)

        #250
        series = QtCharts.QScatterSeries()
        series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(15)

        for pm2min, pm2max in zip(data['PM2MIN'], data['PM2MAX']):
            if pm2min is not None and pm2min < 250 and pm2max is not None and pm2max < 250:
                series.append(pm2min, pm2max)

        self._ui.highlightsScatterChart250.addSeries(series)
        self._ui.highlightsScatterChart250.setTitle('Scatter of all Sensors PM2 min/max lower than 250')
        self._ui.highlightsScatterChart250.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)

        self.scattervalue_axis2 = QtCharts.QValueAxis()
        self.scattervalue_axis2.setRange(0, 250)
        self.scattervalue_axis2.setTickCount(5)
        self.scattervalue_axis2.setTitleText('PM2 maximal')

        self._ui.highlightsScatterChart250.addAxis(self.scattervalue_axis2, Qt.AlignLeft)

        self.scattervalue_axisbot2 = QtCharts.QValueAxis()
        self.scattervalue_axisbot2.setRange(0, 250)
        self.scattervalue_axisbot2.setTickCount(5)
        self.scattervalue_axisbot2.setTitleText('PM2 minimal')

        self._ui.highlightsScatterChart250.addAxis(self.scattervalue_axisbot2, Qt.AlignBottom)

    def load_analysis(self, listID:list, listAVG:list):
        listID = listID[:4]
        listAVG = listAVG[:4]

        dataSet2 = QtCharts.QBarSet("PM2_avg")
        for item in listAVG:
            dataSet2.append(item)

        self.anaaxisX = QtCharts.QBarCategoryAxis()
        self.anaaxisX.append(listID)

        self.anaaxisY = QtCharts.QValueAxis()
        min = 0
        max = 0
        for item in listAVG:
            if min>item:
                min=item
            if max<item:
                max=item

        self.anaaxisY.setRange(min, max)

        dataSeries = QtCharts.QBarSeries()
        dataSeries.append(dataSet2)
        dataSeries.attachAxis(self.anaaxisX)
        dataSeries.attachAxis(self.anaaxisY)

        self._ui.analysisChart.addAxis(self.anaaxisX, Qt.AlignBottom)
        self._ui.analysisChart.addAxis(self.anaaxisY, Qt.AlignLeft)

        self._ui.analysisChart.addSeries(dataSeries)
        self._ui.analysisChart.legend().setVisible(True)
        self._ui.analysisChart.legend().setAlignment(Qt.AlignBottom)
        self._ui.analysisChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self._ui.analysisChart.setTitle("Averages in Baden-Würtemberg")

    def load_highlights(self, listID: list, listAVG: list):

        lavg, lbez = zip(*sorted(zip(listAVG, listID)))

        series = QtCharts.QPieSeries()

        for itemID, itemAVG in zip(lbez[:10], lavg[:10]):
            series.append(itemID + ' ' + str(round(itemAVG, 3)), itemAVG)

        for i in range(0, series.count()):
            slice = series.slices()[i]
            slice.setLabelVisible(True)

        self._ui.highlightsQChart.legend().setVisible(False)
        self._ui.highlightsQChart.legend().setAlignment(Qt.AlignBottom)
        self._ui.highlightsQChart.addSeries(series)
        self._ui.highlightsQChart.createDefaultAxes()
        self._ui.highlightsQChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self._ui.highlightsQChart.setTitle("The 10 Highest PM2 Averages")

    def get_popup_str(self):
        pass

    def setFoliumMarkerCluster(self, coordinates:list, popup:list):
        options_dict = {"showCoverageOnHover":True, "removeOutsideVisibleBounds":False,
                        "spiderfyOnMaxZoom":True, "maxClusterRadius":80}
        #cluster = folium.plugins.FastMarkerCluster(data=coordinates, popups=popup, name="SensorClusterLayer")

        cluster = MarkerCluster(locations=coordinates, popups=popup)

        return cluster
        pass

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

    def setFoliumCircle(self, lat:float, long:float, popup:str, color:str):
        return folium.Circle(
            location=[lat, long],
            radius=50,
            popup=popup,
            color=color,
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

        if self.singlePointsO500 is not None:
            map.add_child(self.singlePointsO500)

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

    def setLabelSensorCountFiltered(self, sensorCountf: str):
        self._ui.homeLabelSencorCountfiltered.setText("Sensor Count Filtered: " + sensorCountf)

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













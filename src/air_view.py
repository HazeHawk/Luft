import io
import sys
import time

import folium
import pyqtgraph

from PySide2.QtCharts import *
from PySide2.QtCore import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWidgets import *
from src.config import Configuration

_cfg = Configuration()

logger = _cfg.LOGGER

class AirView(object):
    def __init__(self):
        self.foliumStandardLocation()
        pass

    def setupUi(self, Form):
        Form.resize(900, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowTitle("Airgoogle")

        gridLayoutTabWidget = QGridLayout(Form)
        tabWidget = QTabWidget(Form)

        #Home Tab
        self.widgetHome = QWidget()
        tabWidget.addTab(self.buildHome(self.widgetHome), "Home")

        #Analysis tab
        self.widgetAnalysis = QWidget()
        tabWidget.addTab(self.buildAnalysis(self.widgetAnalysis), "Analysis")

        # Highlights tab
        self.widgetHighlights = QWidget()
        tabWidget.addTab(self.buildHighlights(self.widgetHighlights), "Highlights")

        #Forecast Tab
        self.widgetForecast = QWidget()
        tabWidget.addTab(self.buildForecast(self.widgetForecast), "Forecast")

        #Info Tab
        self.widgetInfo = QWidget()
        tabWidget.addTab(self.buildInfo(self.widgetInfo), "Info")

        gridLayoutTabWidget.addWidget(tabWidget, 0, 0, 1, 1)

        tabWidget.setCurrentIndex(0)


    def foliumStandardLocation(self):
        self.m = folium.Map(
            location=[48.77915707462204, 9.175987243652344], tiles="Stamen Toner", zoom_start=12
        )

    def saveFoliumToHtml(self):
        data = io.BytesIO()

        self.m.save(data, close_file=False)

        return data


    def buildHome(self, home):
        horizontalLayout = QHBoxLayout(home)

        # Kontrollfeld links
        widgetMenu = QWidget(home)
        verticalLayoutWidgetMenu = QVBoxLayout(widgetMenu)

        widgetMenuTop = QWidget(widgetMenu)
        verticalLayoutWidgetMenuTop = QVBoxLayout(widgetMenuTop)

        widgetMenuBottom = QWidget(widgetMenu)
        verticalLayoutWidgetMenuBottom = QVBoxLayout(widgetMenuBottom)

        # Top
        inputPositionLable = QLabel()
        inputPositionLable.setText("Input Your Position")
        verticalLayoutWidgetMenuTop.addWidget(inputPositionLable)

        inputPosition = QLineEdit()
        verticalLayoutWidgetMenuTop.addWidget(inputPosition)
        self.homeLineEditPosition = inputPosition

        medianLabel = QLabel()
        medianLabel.setText("Median:")
        verticalLayoutWidgetMenuTop.addWidget(medianLabel)
        self.homeLabelMedian = medianLabel

        minimalLabel = QLabel()
        minimalLabel.setText("Minimal:")
        verticalLayoutWidgetMenuTop.addWidget(minimalLabel)
        self.homeLabelMinimal = minimalLabel

        maximalLabel = QLabel()
        maximalLabel.setText("Maximal:")
        verticalLayoutWidgetMenuTop.addWidget(maximalLabel)
        self.homeLabelMaximal = maximalLabel

        averageLabel = QLabel()
        averageLabel.setText("Average:")
        verticalLayoutWidgetMenuTop.addWidget(averageLabel)
        self.homeLabelAverage = averageLabel

        sensorCountLabel = QLabel()
        sensorCountLabel.setText("Sensor Count:")
        verticalLayoutWidgetMenuTop.addWidget(sensorCountLabel)
        self.homeLabelSencorCount = sensorCountLabel

        # Bottom
        configurationTitle = QLabel()
        configurationTitle.setText("Configuration:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitle)

        startLabel = QLabel()
        startLabel.setText("Start:")
        verticalLayoutWidgetMenuBottom.addWidget(startLabel)

        dateEditStart = QDateEdit()
        dateEditStart.setCalendarPopup(True)
        dateEditStart.setDateTime(QDateTime.currentDateTime())
        verticalLayoutWidgetMenuBottom.addWidget(dateEditStart)
        self.homeDateEditStart = dateEditStart

        endLabel = QLabel()
        endLabel.setText("End:")
        verticalLayoutWidgetMenuBottom.addWidget(endLabel)

        dateEditEnd = QDateEdit()
        dateEditEnd.setCalendarPopup(True)
        dateEditEnd.setDateTime(QDateTime.currentDateTime())
        verticalLayoutWidgetMenuBottom.addWidget(dateEditEnd)
        self.homeDateEditEnd = dateEditEnd

        verticalLayoutWidgetMenu.addWidget(widgetMenuTop)
        verticalLayoutWidgetMenu.setStretch(0,1)

        emptyWidget = QWidget()
        verticalLayoutWidgetMenu.addWidget(emptyWidget)
        verticalLayoutWidgetMenu.setStretch(1,1)

        verticalLayoutWidgetMenu.addWidget(widgetMenuBottom)
        verticalLayoutWidgetMenu.setStretch(2,1)

        horizontalLayout.addWidget(widgetMenu)

        mapWidget = QWidget(home)
        verticalLayout = QVBoxLayout(mapWidget)

        widgetMap = QWebEngineView(mapWidget)
        self.foliumStandardLocation()
        widgetMap.setHtml(self.saveFoliumToHtml().getvalue().decode())
        self.homeWidgetMap = widgetMap

        verticalLayout.addWidget(widgetMap)

        # Kontrollfeld unten
        widgetMapControlls = QWidget(mapWidget)
        verticalLayoutMapControlls = QVBoxLayout(widgetMapControlls)

        slider = QSlider(Qt.Horizontal)
        verticalLayoutMapControlls.addWidget(slider)
        self.homeSlider = slider

        verticalLayout.addWidget(widgetMapControlls)

        verticalLayout.setStretch(0, 5)
        verticalLayout.setStretch(1, 1)

        horizontalLayout.addWidget(mapWidget)

        horizontalLayout.setStretch(1, 4)

        return home


    def buildAnalysis(self, analysis):

        horizontalLayout_2 = QHBoxLayout(analysis)

        widgetAnalysisControls = QWidget(analysis)

        vBox3 = QVBoxLayout()
        '''
        #controlls
        configurationTitleAnalysis = QLabel()
        configurationTitleAnalysis.setText("Configuration:")
        vBox3.addWidget(configurationTitleAnalysis)

        startLabel = QLabel()
        startLabel.setText("Start:")
        vBox3.addWidget(startLabel)

        dateEditStart = QDateEdit()
        dateEditStart.setCalendarPopup(True)
        dateEditStart.setDateTime(QDateTime.currentDateTime())
        vBox3.addWidget(dateEditStart)
        self.analysisDateEditStart = dateEditStart

        endLabel = QLabel()
        endLabel.setText("End:")
        vBox3.addWidget(endLabel)

        dateEditEnd = QDateEdit()
        dateEditEnd.setCalendarPopup(True)
        dateEditEnd.setDateTime(QDateTime.currentDateTime())
        vBox3.addWidget(dateEditEnd)
        self.analysisDateEditEnd = dateEditEnd

        widgetAnalysisControls.setLayout(vBox3)

        horizontalLayout_2.addWidget(widgetAnalysisControls)
        '''
        '''widgetAnalysis = pyqtgraph.PlotWidget(analysis)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        widgetAnalysis.plot(hour, temperature)
        '''

        self.analysisChart = QtCharts.QChart()


        widgetAnalysis = QtCharts.QChartView(self.analysisChart)


        self.analysisPlotWidget = widgetAnalysis

        horizontalLayout_2.addWidget(widgetAnalysis)

        horizontalLayout_2.setStretch(0, 1)
        horizontalLayout_2.setStretch(1, 4)


        return analysis


    def buildHighlights(self, highlights):
        scroll = QScrollArea()
        highlightsWidget = QWidget()
        vBox = QGridLayout()

        self.highlightsQChart = QtCharts.QChart()

        chartview = QtCharts.QChartView(self.highlightsQChart)
        vBox.addWidget(chartview)
        '''
        for i in range(1, 10):
            object = pyqtgraph.PlotWidget(highlights)
            hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
            object.plot(hour, temperature)
            vBox.setRowMinimumHeight(i - 1, 500)
            vBox.addWidget(object)
        '''
        highlightsWidget.setLayout(vBox)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(highlightsWidget)

        vBox2 = QVBoxLayout()
        vBox2.addWidget(scroll)

        highlights.setLayout(vBox2)

        return highlights


    def buildForecast(self, forecast):

        horizontalLayout_4 = QHBoxLayout(forecast)

        widgetForecastMenu = QWidget(forecast)

        horizontalLayout_4.addWidget(widgetForecastMenu)

        widget_3 = QWidget(forecast)

        verticalLayout_2 = QVBoxLayout(widget_3)

        widgetForecastMap = QWebEngineView(widget_3)
        widgetForecastMap.setHtml(self.saveFoliumToHtml().getvalue().decode())

        verticalLayout_2.addWidget(widgetForecastMap)

        widgetForecastMapControlls = QWidget(widget_3)


        verticalLayout_2.addWidget(widgetForecastMapControlls)

        verticalLayout_2.setStretch(0, 3)
        verticalLayout_2.setStretch(1, 1)

        horizontalLayout_4.addWidget(widget_3)

        horizontalLayout_4.setStretch(0, 1)
        horizontalLayout_4.setStretch(1, 4)

        return forecast

    def buildInfo(self, info):
        horizontalLayout_5 = QVBoxLayout(info)

        widgetInfoMenu = QWidget(info)

       # horizontalLayout_5.addWidget(widgetInfoMenu)

        widget_3 = QWidget(info)

        verticalLayout_2 = QVBoxLayout(widget_3)

        inputPositionLable1 = QLabel()
        inputPositionLable1.setText("This program visualizes sensor data from Luftdaten.info."
        " Luftdaten.info is a community project that follows the determination of the fine dust content in Stuttgart. In the meantime, the sensors can also be found outside Stuttgart."
        " Users build themselves a measuring station with the ability to measure particulate emissions. In addition, temperature, humidity and air pressure can also be measured.However, these options are optional and it is up to the builder to implement them. In this project only the fine dust content is visualized."
        " The project started in 2015 and there are now over 12000 active measuring stations. The measuring stations measure every 2.5 minutes and transmit the current values to the server."
        " There are different sensors. The SDS011 and the SPS30 are responsible for the fine dust."
        " For more information feel free to visit the Website luftdaten.info and have a look.")
        inputPositionLable1.setAlignment(Qt.AlignLeft)
        inputPositionLable1.setWordWrap(True);
        horizontalLayout_5.addWidget(inputPositionLable1)

        inputPositionLable2 = QLabel()
        inputPositionLable2.setText('''<a href='http://luftdaten.info'>luftdaten.info</a>''')
        inputPositionLable2.setAlignment(Qt.AlignCenter)
        inputPositionLable2.setOpenExternalLinks(True)
        horizontalLayout_5.addWidget(inputPositionLable2)

        return info

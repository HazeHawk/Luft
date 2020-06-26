import io
import folium
import pyqtgraph

from PySide2.QtCore import (Qt, QDateTime)
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWidgets import *
from src.config import Configuration

_cfg = Configuration()

class AirView(object):
    def __init__(self):
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

        gridLayoutTabWidget.addWidget(tabWidget, 0, 0, 1, 1)

        tabWidget.setCurrentIndex(0)


    def foliumMapData(self):
        m = folium.Map(
            location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13
        )

        data = io.BytesIO()
        m.save(data, close_file=False)

        return data

    # retranslateUi

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
        self.lineEditPosition = inputPosition

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
        verticalLayoutWidgetMenu.addWidget(widgetMenuBottom)

        horizontalLayout.addWidget(widgetMenu)

        mapWidget = QWidget(home)
        verticalLayout = QVBoxLayout(mapWidget)

        widgetMap = QWebEngineView(mapWidget)
        widgetMap.setHtml(self.foliumMapData().getvalue().decode())

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

        widgetAnalysis = pyqtgraph.PlotWidget(analysis)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        widgetAnalysis.plot(hour, temperature)
        self.analysisPlotWidget = widgetAnalysis

        horizontalLayout_2.addWidget(widgetAnalysis)

        horizontalLayout_2.setStretch(0, 1)
        horizontalLayout_2.setStretch(1, 4)

        return analysis


    def buildHighlights(self, highlights):
        scroll = QScrollArea()
        highlightsWidget = QWidget()
        vBox = QGridLayout()

        for i in range(1, 10):
            object = pyqtgraph.PlotWidget(highlights)
            hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
            object.plot(hour, temperature)
            vBox.setRowMinimumHeight(i - 1, 500)
            vBox.addWidget(object)

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
        widgetForecastMap.setHtml(self.foliumMapData().getvalue().decode())

        verticalLayout_2.addWidget(widgetForecastMap)

        widgetForecastMapControlls = QWidget(widget_3)


        verticalLayout_2.addWidget(widgetForecastMapControlls)

        verticalLayout_2.setStretch(0, 3)
        verticalLayout_2.setStretch(1, 1)

        horizontalLayout_4.addWidget(widget_3)

        horizontalLayout_4.setStretch(0, 1)
        horizontalLayout_4.setStretch(1, 4)

        return forecast




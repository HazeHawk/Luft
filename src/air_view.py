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
        horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        widgetAnalysisControls = QWidget(analysis)
        widgetAnalysisControls.setObjectName(u"widgetAnalysisControls")

        vBox3 = QVBoxLayout()

        configurationTitleAnalysis = QLabel()
        configurationTitleAnalysis.setText("Configuration:")
        vBox3.addWidget(configurationTitleAnalysis)

        configurationTitleAnalysisYear = QLabel()
        configurationTitleAnalysisYear.setText("Year:")
        vBox3.addWidget(configurationTitleAnalysisYear)

        comboBoxConfigurationAnalysisYear = QComboBox()
        comboBoxConfigurationAnalysisYear.addItem("2020")
        comboBoxConfigurationAnalysisYear.addItem("2019")
        comboBoxConfigurationAnalysisYear.addItem("2018")
        comboBoxConfigurationAnalysisYear.addItem("2017")
        comboBoxConfigurationAnalysisYear.addItem("2016")
        comboBoxConfigurationAnalysisYear.addItem("2015")
        vBox3.addWidget(comboBoxConfigurationAnalysisYear)

        configurationTitleAnalysisMonth = QLabel()
        configurationTitleAnalysisMonth.setText("Month:")
        vBox3.addWidget(configurationTitleAnalysisMonth)

        comboBoxConfigurationAnalysisMonth = QComboBox()
        comboBoxConfigurationAnalysisMonth.addItem("January")
        comboBoxConfigurationAnalysisMonth.addItem("February")
        comboBoxConfigurationAnalysisMonth.addItem("March")
        comboBoxConfigurationAnalysisMonth.addItem("May")
        comboBoxConfigurationAnalysisMonth.addItem("April")
        comboBoxConfigurationAnalysisMonth.addItem("June")
        comboBoxConfigurationAnalysisMonth.addItem("July")
        comboBoxConfigurationAnalysisMonth.addItem("August")
        comboBoxConfigurationAnalysisMonth.addItem("September")
        comboBoxConfigurationAnalysisMonth.addItem("October")
        comboBoxConfigurationAnalysisMonth.addItem("November")
        comboBoxConfigurationAnalysisMonth.addItem("December")
        vBox3.addWidget(comboBoxConfigurationAnalysisMonth)

        configurationTitleAnalysisDay = QLabel()
        configurationTitleAnalysisDay.setText("Day:")
        vBox3.addWidget(configurationTitleAnalysisDay)

        comboBoxConfigurationAnalysisDay = QComboBox()
        comboBoxConfigurationAnalysisDay.addItem("1")
        comboBoxConfigurationAnalysisDay.addItem("2")
        comboBoxConfigurationAnalysisDay.addItem("3")
        comboBoxConfigurationAnalysisDay.addItem("4")
        comboBoxConfigurationAnalysisDay.addItem("5")
        comboBoxConfigurationAnalysisDay.addItem("6")
        comboBoxConfigurationAnalysisDay.addItem("7")
        comboBoxConfigurationAnalysisDay.addItem("8")
        comboBoxConfigurationAnalysisDay.addItem("9")
        comboBoxConfigurationAnalysisDay.addItem("10")
        comboBoxConfigurationAnalysisDay.addItem("11")
        comboBoxConfigurationAnalysisDay.addItem("12")
        comboBoxConfigurationAnalysisDay.addItem("13")
        comboBoxConfigurationAnalysisDay.addItem("14")
        comboBoxConfigurationAnalysisDay.addItem("15")
        comboBoxConfigurationAnalysisDay.addItem("16")
        comboBoxConfigurationAnalysisDay.addItem("17")
        comboBoxConfigurationAnalysisDay.addItem("18")
        comboBoxConfigurationAnalysisDay.addItem("19")
        comboBoxConfigurationAnalysisDay.addItem("20")
        comboBoxConfigurationAnalysisDay.addItem("21")
        comboBoxConfigurationAnalysisDay.addItem("22")
        comboBoxConfigurationAnalysisDay.addItem("23")
        comboBoxConfigurationAnalysisDay.addItem("24")
        comboBoxConfigurationAnalysisDay.addItem("25")
        comboBoxConfigurationAnalysisDay.addItem("26")
        comboBoxConfigurationAnalysisDay.addItem("27")
        comboBoxConfigurationAnalysisDay.addItem("28")
        comboBoxConfigurationAnalysisDay.addItem("29")
        comboBoxConfigurationAnalysisDay.addItem("30")
        comboBoxConfigurationAnalysisDay.addItem("31")
        vBox3.addWidget(comboBoxConfigurationAnalysisDay)

        widgetAnalysisControls.setLayout(vBox3)

        horizontalLayout_2.addWidget(widgetAnalysisControls)

        widgetAnalysis = pyqtgraph.PlotWidget(analysis)
        widgetAnalysis.setObjectName(u"widgeAnalysis")

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        widgetAnalysis.plot(hour, temperature)

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
        horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        widgetForecastMenu = QWidget(forecast)
        widgetForecastMenu.setObjectName(u"widgetForecastMenu")

        horizontalLayout_4.addWidget(widgetForecastMenu)

        widget_3 = QWidget(forecast)
        widget_3.setObjectName(u"widget_3")
        verticalLayout_2 = QVBoxLayout(widget_3)
        verticalLayout_2.setObjectName(u"verticalLayout_2")
        widgetForecastMap = QWebEngineView(widget_3)
        widgetForecastMap.setObjectName(u"widgetForecastMap")
        widgetForecastMap.setHtml(self.foliumMapData().getvalue().decode())

        verticalLayout_2.addWidget(widgetForecastMap)

        widgetForecastMapControlls = QWidget(widget_3)
        widgetForecastMapControlls.setObjectName(u"widgetForecastMapControlls")

        verticalLayout_2.addWidget(widgetForecastMapControlls)

        verticalLayout_2.setStretch(0, 3)
        verticalLayout_2.setStretch(1, 1)

        horizontalLayout_4.addWidget(widget_3)

        horizontalLayout_4.setStretch(0, 1)
        horizontalLayout_4.setStretch(1, 4)

        return forecast




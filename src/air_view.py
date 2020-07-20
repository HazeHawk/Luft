import io
import sys
import time

import folium
import pyqtgraph

from PySide2.QtCharts import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWidgets import *
from src.config import Configuration

_cfg = Configuration()

logger = _cfg.LOGGER

class AirView(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.foliumStandardLocation()
        self.saveFoliumToHtmlInDirectory()
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

        # Highlights tab
        self.widgetHighlights = QWidget()
        tabWidget.addTab(self.buildHighlights(self.widgetHighlights), "Highlights")

        #Info Tab
        self.widgetInfo = QWidget()
        tabWidget.addTab(self.buildInfo(self.widgetInfo), "Info")

        gridLayoutTabWidget.addWidget(tabWidget, 0, 0, 1, 1)

        tabWidget.setCurrentIndex(0)


    def foliumStandardLocation(self):
        self.m = folium.Map(
            location=[48.77915707462204, 9.175987243652344], tiles="Stamen Toner", zoom_start=12
        )

    def saveFoliumToHtmlInDirectory(self):
        self.m.save('./data/html/map.html', close_file=False)


    def buildHome(self, home):
        horizontalLayout = QHBoxLayout(home)

        # Kontrollfeld links
        widgetMenu = QWidget(home)
        verticalLayoutWidgetMenu = QVBoxLayout(widgetMenu)

        widgetMenuTop = QWidget(widgetMenu)
        verticalLayoutWidgetMenuTop = QVBoxLayout(widgetMenuTop)

        widgetMenuMiddle = QWidget(widgetMenu)
        verticalLayoutWidgetMenuMiddle = QVBoxLayout(widgetMenuMiddle)

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
        medianLabel.setText("PM2 Value")
        verticalLayoutWidgetMenuTop.addWidget(medianLabel)

        medianLabel = QLabel()
        medianLabel.setText("Median:")
        verticalLayoutWidgetMenuTop.addWidget(medianLabel)
        self.homeLabelMedian = medianLabel

        averageLabel = QLabel()
        averageLabel.setText("Average:")
        verticalLayoutWidgetMenuTop.addWidget(averageLabel)
        self.homeLabelAverage = averageLabel

        minimalLabel = QLabel()
        minimalLabel.setText("Minimal:")
        verticalLayoutWidgetMenuTop.addWidget(minimalLabel)
        self.homeLabelMinimal = minimalLabel

        maximalLabel = QLabel()
        maximalLabel.setText("Maximal:")
        verticalLayoutWidgetMenuTop.addWidget(maximalLabel)
        self.homeLabelMaximal = maximalLabel

        sensorCountLabel = QLabel()
        sensorCountLabel.setText("Sensor Count:")
        verticalLayoutWidgetMenuTop.addWidget(sensorCountLabel)
        self.homeLabelSencorCount = sensorCountLabel

        sensorCountLabelf = QLabel()
        sensorCountLabelf.setText("Sensor Count Filtered:")
        verticalLayoutWidgetMenuTop.addWidget(sensorCountLabelf)
        self.homeLabelSencorCountfiltered = sensorCountLabelf

        loading = QLabel()
        movie = QMovie('./data/gif/ajax-loader.gif')
        loading.setMovie(movie)
        verticalLayoutWidgetMenuMiddle.addWidget(loading)
        loading.hide()
        self.homeLoadingLabel = loading
        self.homeLoadingMovie = movie

        # Bottom
        configurationTitle = QLabel()
        configurationTitle.setText("Configuration:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitle)

        startLabel = QLabel()
        startLabel.setText("Start Date:")
        verticalLayoutWidgetMenuBottom.addWidget(startLabel)

        dateEditStart = QDateEdit()
        dateEditStart.setCalendarPopup(True)
        dateEditStart.setDateTime(QDateTime.currentDateTime())
        verticalLayoutWidgetMenuBottom.addWidget(dateEditStart)
        self.homeDateEditStart = dateEditStart

        startTimeLabel = QLabel()
        startTimeLabel.setText("Start Time:")
        verticalLayoutWidgetMenuBottom.addWidget(startTimeLabel)

        timeEditStart = QTimeEdit()
        timeEditStart.setTime(QTime(6, 0, 0))
        verticalLayoutWidgetMenuBottom.addWidget(timeEditStart)
        self.homeTimeEditStart = timeEditStart

        endLabel = QLabel()
        endLabel.setText("End Date:")
        verticalLayoutWidgetMenuBottom.addWidget(endLabel)

        dateEditEnd = QDateEdit()
        dateEditEnd.setCalendarPopup(True)
        dateEditEnd.setDateTime(QDateTime.currentDateTime())
        verticalLayoutWidgetMenuBottom.addWidget(dateEditEnd)
        self.homeDateEditEnd = dateEditEnd

        endTimeLabel = QLabel()
        endTimeLabel.setText("End Time:")
        verticalLayoutWidgetMenuBottom.addWidget(endTimeLabel)

        timeEditEnd = QTimeEdit()
        timeEditEnd.setTime(QTime(18, 0, 0))
        verticalLayoutWidgetMenuBottom.addWidget(timeEditEnd)
        self.homeTimeEditEnd = timeEditEnd

        button = QPushButton()
        button.setText('Click Me')
        verticalLayoutWidgetMenuBottom.addWidget(button)
        self.homeButtonSendData = button

        verticalLayoutWidgetMenu.addWidget(widgetMenuTop)
        verticalLayoutWidgetMenu.setStretch(0,1)

        verticalLayoutWidgetMenu.addWidget(widgetMenuMiddle)
        verticalLayoutWidgetMenu.setStretch(1,1)

        verticalLayoutWidgetMenu.addWidget(widgetMenuBottom)
        verticalLayoutWidgetMenu.setStretch(2,1)

        horizontalLayout.addWidget(widgetMenu)

        mapWidget = QWidget(home)
        verticalLayout = QVBoxLayout(mapWidget)

        widgetMap = QWebEngineView(mapWidget)
        self.foliumStandardLocation()
        widgetMap.load(QUrl('file:/data/html/map.html'))
        self.homeWidgetMap = widgetMap

        verticalLayout.addWidget(widgetMap)

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




        return analysis


    def buildHighlights(self, highlights):
        highlightsWidget = QWidget()
        vBox = QGridLayout()

        #Compare Chart
        compareChart = QWidget()
        verLay = QVBoxLayout(compareChart)
        compareChart.setLayout(verLay)

        controlls = QWidget()
        horiLay = QHBoxLayout(controlls)
        controlls.setLayout(horiLay)

        BL_OPTIONS = ['BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'MV', 'NI', 'NW', 'RP', 'SL', 'SN', 'ST', 'SH', 'TH']
        cb1 = QComboBox(controlls)
        cb1.addItems(BL_OPTIONS)
        self.highlightsCompareCombo1 = cb1

        horiLay.addWidget(cb1)

        button = QPushButton()
        button.setText("Compare")
        self.highlightsCompareButton = button
        horiLay.addWidget(button)

        cb2 = QComboBox(controlls)
        cb2.addItems(BL_OPTIONS)
        self.highlightsCompareCombo2 = cb2

        horiLay.addWidget(cb2)

        verLay.addWidget(controlls)

        self.highlightsBWAVG = QtCharts.QChart()
        chartviewbwavg = QtCharts.QChartView(self.highlightsBWAVG)
        verLay.addWidget(chartviewbwavg)

        vBox.addWidget(compareChart)

        #Scatter Chart
        self.highlightsScatterChart = QtCharts.QChart()
        chartviewsc = QtCharts.QChartView(self.highlightsScatterChart)
        vBox.addWidget(chartviewsc)

        self.highlightsScatterChart250 = QtCharts.QChart()
        chartviewsc250 = QtCharts.QChartView(self.highlightsScatterChart250)
        vBox.addWidget(chartviewsc250)

        self.highlightsQChart = QtCharts.QChart()
        chartview = QtCharts.QChartView(self.highlightsQChart)
        vBox.addWidget(chartview)

        self.analysisChart = QtCharts.QChart()
        widgetAnalysis = QtCharts.QChartView(self.analysisChart)
        vBox.addWidget(widgetAnalysis)

        for i in range(0, vBox.rowCount()):
            vBox.setRowMinimumHeight(i, 700)

        highlightsWidget.setLayout(vBox)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(highlightsWidget)

        vBox2 = QVBoxLayout()
        vBox2.addWidget(scroll)

        highlights.setLayout(vBox2)

        return highlights

    def buildInfo(self, info):
        widgetInfoMenu = QWidget()
        vLayout_5 = QVBoxLayout(widgetInfoMenu)


        font = QFont("Open Sans", 12)
        generalLabel = QLabel()
        generalLabel.setText("General:\n"
            "This program visualizes sensor data from Luftdaten.info."
            " Luftdaten.info is a community project that follows the determination of the particle matter concentration in Stuttgart."
            " In the meantime, the sensors can also be found outside Stuttgart."
            " Based on a given blueprint users build themselves a measuring station with the ability to measure particulate emissions."
            " In addition, temperature, humidity and air pressure can also be measured."
            " However, these options are optional and it is up to the builder to implement them. The subject of this project is the particle matter emissions."
            " The project started in 2015 and there are now over 14000 active measuring stations. The measuring stations measure every 2.5 minutes and transmit the current values to the server."
            " There are different sensors and for this dataset primarily the SDS011 SPS30 are analyzed."
            " Due to data loading issues, we include only data inbetween the 01.03.2020 and 30.06.2020."
            " For more information feel free to visit the Website luftdaten.info and have a look.")
        generalLabel.setAlignment(Qt.AlignLeft)
        generalLabel.setWordWrap(True)
        generalLabel.setFont(font)
        vLayout_5.addWidget(generalLabel)

        inputPositionLable2 = QLabel()
        inputPositionLable2.setText('''<a href='http://luftdaten.info'>luftdaten.info</a>''')
        inputPositionLable2.setAlignment(Qt.AlignCenter)
        inputPositionLable2.setOpenExternalLinks(True)
        inputPositionLable2.setMaximumHeight(15)
        vLayout_5.addWidget(inputPositionLable2)

        pmLabel = QLabel()
        pmLabel.setText(
            "Particulate Matter:\n"
            "Patriculate Matter (PM) originates from the american Environmental Protection Agency (EPA)."
            " With PM the goverment can categorize the emissions from industry etc. and keep an eye on the air pollution."
            " PM_10 means that the value includes any particulate matter which is less or equal than 10µm."
            " Likewise PM_2 or rather PM_2.5 contains any matter which is smaller than 2.5µm."
            " The daily limit value is 50 µg/m3"
            " and must not be exceeded more than 35 times a year. The permitted annual mean value"
            " is 40 µg/m3. For the even smaller particles PM2.5, a target value of 25 µg/m3 as"
            " an annual average has been in force throughout Europe since 2008 and is to be"
            " complied with from 1 January 2010. Since 1 January 2015, this value is mandatory."
            " In order to get a better grasp we provide this table which contains the relevant values, which are defined"
            " by the Common Air Quality Index (CAQI) in Europe.")
        pmLabel.setFont(font)
        pmLabel.setAlignment(Qt.AlignLeft)
        pmLabel.setWordWrap(True)
        vLayout_5.addWidget(pmLabel)

        pixmap = QPixmap('data/caqi.png')
        inputPositionLable3 = QLabel()
        inputPositionLable3.setPixmap(pixmap)
        inputPositionLable3.show()
        inputPositionLable3.setAlignment(Qt.AlignCenter)
        vLayout_5.addWidget(inputPositionLable3)

        imgsourceLabel = QLabel()
        imgsourceLabel.setText('''<a href='https://env.kernelit.gr/2019/02/23/making-sense-of-the-data-air-quality-index-aqi/'>Bildquelle aufgerufen am 20.07.2020</a>''')
        imgsourceLabel.setAlignment(Qt.AlignCenter)
        imgsourceLabel.setOpenExternalLinks(True)
        vLayout_5.addWidget(imgsourceLabel)

        caqiLinkLabel = QLabel()
        caqiLinkLabel.setText('''Mehr Informationen finden sie unter <a href='http://www.airqualitynow.eu/index.php'>http://www.airqualitynow.eu/index.php</a>''')
        caqiLinkLabel.setAlignment(Qt.AlignCenter)
        caqiLinkLabel.setOpenExternalLinks(True)
        caqiLinkLabel.setFixedHeight(15)
        vLayout_5.addWidget(caqiLinkLabel)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widgetInfoMenu)

        parentLayout = QVBoxLayout()
        parentLayout.addWidget(scroll)

        info.setLayout(parentLayout)


        return info

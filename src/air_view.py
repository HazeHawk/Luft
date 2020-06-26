import io
import folium
import pyqtgraph
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, Qt, QTime, QUrl)

from PySide2.QtWebEngineWidgets import *
from PySide2.QtWidgets import *

from src.config import Configuration

_cfg = Configuration()

class AirView(object):
    def __init__(self):
        pass

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)

        self.gridLayout_1 = QGridLayout(Form)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")

        #Home Tab
        self.home = QWidget()
        self.home.setObjectName(u"home")

        self.tabWidget.addTab(self.buildHome(self.home), "")


        #Analysis tab
        self.analysis = QWidget()
        self.analysis.setObjectName(u"analysis")

        self.tabWidget.addTab(self.buildAnalysis(self.analysis), "")


        # Highlights tab
        self.highlights = QWidget()
        self.highlights.setObjectName(u"highlights")

        self.tabWidget.addTab(self.buildHighlights(self.highlights), "")


        #Forecast Tab
        self.forecast = QWidget()
        self.forecast.setObjectName(u"forecast")

        self.tabWidget.addTab(self.buildForecast(self.forecast), "")


        self.gridLayout_1.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(4)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def foliumMapData(self):
        m = folium.Map(
            location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13
        )

        data = io.BytesIO()
        m.save(data, close_file=False)

        return data

    # retranslateUi



    def buildHome(self, home):

        # Home Tab
        horizontalLayout = QHBoxLayout(home)
        horizontalLayout.setObjectName(u"horizontalLayout")

        # Kontrollfeld links
        widgetMenu = QWidget(home)
        widgetMenu.setObjectName(u"widgetMenu")
        widgetMenu.setStyleSheet(u"")

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

        medianLabel = QLabel()
        medianLabel.setText("Median:")
        verticalLayoutWidgetMenuTop.addWidget(medianLabel)

        minimalLabel = QLabel()
        minimalLabel.setText("Minimal:")
        verticalLayoutWidgetMenuTop.addWidget(minimalLabel)

        maximalLabel = QLabel()
        maximalLabel.setText("Maximal:")
        verticalLayoutWidgetMenuTop.addWidget(maximalLabel)

        averageLabel = QLabel()
        averageLabel.setText("Average:")
        verticalLayoutWidgetMenuTop.addWidget(averageLabel)

        sensorCountLabel = QLabel()
        sensorCountLabel.setText("Sensor Count:")
        verticalLayoutWidgetMenuTop.addWidget(sensorCountLabel)

        # Bottom
        configurationTitle = QLabel()
        configurationTitle.setText("Configuration:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitle)

        configurationTitleYear = QLabel()
        configurationTitleYear.setText("Year:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitleYear)

        comboBoxConfigurationYear = QComboBox()
        comboBoxConfigurationYear.addItem("2020")
        comboBoxConfigurationYear.addItem("2019")
        comboBoxConfigurationYear.addItem("2018")
        comboBoxConfigurationYear.addItem("2017")
        comboBoxConfigurationYear.addItem("2016")
        comboBoxConfigurationYear.addItem("2015")
        verticalLayoutWidgetMenuBottom.addWidget(comboBoxConfigurationYear)

        configurationTitleMonth = QLabel()
        configurationTitleMonth.setText("Month:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitleMonth)

        comboBoxConfigurationMonth = QComboBox()
        comboBoxConfigurationMonth.addItem("January")
        comboBoxConfigurationMonth.addItem("February")
        comboBoxConfigurationMonth.addItem("March")
        comboBoxConfigurationMonth.addItem("May")
        comboBoxConfigurationMonth.addItem("April")
        comboBoxConfigurationMonth.addItem("June")
        comboBoxConfigurationMonth.addItem("July")
        comboBoxConfigurationMonth.addItem("August")
        comboBoxConfigurationMonth.addItem("September")
        comboBoxConfigurationMonth.addItem("October")
        comboBoxConfigurationMonth.addItem("November")
        comboBoxConfigurationMonth.addItem("December")
        verticalLayoutWidgetMenuBottom.addWidget(comboBoxConfigurationMonth)

        configurationTitleDay = QLabel()
        configurationTitleDay.setText("Day:")
        verticalLayoutWidgetMenuBottom.addWidget(configurationTitleDay)

        comboBoxConfigurationDay = QComboBox()
        comboBoxConfigurationDay.addItem("1")
        comboBoxConfigurationDay.addItem("2")
        comboBoxConfigurationDay.addItem("3")
        comboBoxConfigurationDay.addItem("4")
        comboBoxConfigurationDay.addItem("5")
        comboBoxConfigurationDay.addItem("6")
        comboBoxConfigurationDay.addItem("7")
        comboBoxConfigurationDay.addItem("8")
        comboBoxConfigurationDay.addItem("9")
        comboBoxConfigurationDay.addItem("10")
        comboBoxConfigurationDay.addItem("11")
        comboBoxConfigurationDay.addItem("12")
        comboBoxConfigurationDay.addItem("13")
        comboBoxConfigurationDay.addItem("14")
        comboBoxConfigurationDay.addItem("15")
        comboBoxConfigurationDay.addItem("16")
        comboBoxConfigurationDay.addItem("17")
        comboBoxConfigurationDay.addItem("18")
        comboBoxConfigurationDay.addItem("19")
        comboBoxConfigurationDay.addItem("20")
        comboBoxConfigurationDay.addItem("21")
        comboBoxConfigurationDay.addItem("22")
        comboBoxConfigurationDay.addItem("23")
        comboBoxConfigurationDay.addItem("24")
        comboBoxConfigurationDay.addItem("25")
        comboBoxConfigurationDay.addItem("26")
        comboBoxConfigurationDay.addItem("27")
        comboBoxConfigurationDay.addItem("28")
        comboBoxConfigurationDay.addItem("29")
        comboBoxConfigurationDay.addItem("30")
        comboBoxConfigurationDay.addItem("31")
        verticalLayoutWidgetMenuBottom.addWidget(comboBoxConfigurationDay)

        verticalLayoutWidgetMenu.addWidget(widgetMenuTop)
        verticalLayoutWidgetMenu.addWidget(widgetMenuBottom)

        horizontalLayout.addWidget(widgetMenu)

        widget_2 = QWidget(home)
        widget_2.setObjectName(u"widget_2")
        verticalLayout = QVBoxLayout(widget_2)
        verticalLayout.setObjectName(u"verticalLayout")
        widgetMap = QWebEngineView(widget_2)
        widgetMap.setObjectName(u"widgetMap")
        widgetMap.setHtml(self.foliumMapData().getvalue().decode())

        verticalLayout.addWidget(widgetMap)

        widgetMapControlls = QWidget(widget_2)
        widgetMapControlls.setObjectName(u"widgetMapControlls")
        widgetMapControlls.setStyleSheet(u"")

        # Kontrollfeld unten
        verticalLayoutMapControlls = QVBoxLayout(widgetMapControlls)
        slider = QSlider(Qt.Horizontal)
        verticalLayoutMapControlls.addWidget(slider)

        verticalLayout.addWidget(widgetMapControlls)

        verticalLayout.setStretch(0, 3)
        verticalLayout.setStretch(1, 1)

        horizontalLayout.addWidget(widget_2)

        horizontalLayout.setStretch(0, 1)
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



    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home), QCoreApplication.translate("Form", u"Home", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analysis),
                                  QCoreApplication.translate("Form", u"Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.highlights),
                                  QCoreApplication.translate("Form", u"Highlights", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.forecast),
                                  QCoreApplication.translate("Form", u"Forecast", None))


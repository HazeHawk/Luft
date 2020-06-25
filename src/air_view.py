import io
import logging
import sys
import time

import folium
import numpy
import pandas
import pyqtgraph
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, Qt, QTime, QUrl)
from PySide2.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon,
    QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap,
    QRadialGradient)
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


        # Home Tab
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.horizontalLayout = QHBoxLayout(self.home)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # Kontrollfeld links
        self.widgetMenu = QWidget(self.home)
        self.widgetMenu.setObjectName(u"widgetMenu")
        self.widgetMenu.setStyleSheet(u"")

        self.verticalLayoutWidgetMenu = QVBoxLayout(self.widgetMenu)
        self.widgetMenuTop = QWidget(self.widgetMenu)
        self.verticalLayoutWidgetMenuTop = QVBoxLayout(self.widgetMenuTop)
        self.widgetMenuBottom = QWidget(self.widgetMenu)
        self.verticalLayoutWidgetMenuBottom = QVBoxLayout(self.widgetMenuBottom)

        #Top
        self.inputPositionLable = QLabel()
        self.inputPositionLable.setText("Input Your Position")
        self.verticalLayoutWidgetMenuTop.addWidget(self.inputPositionLable)

        self.inputPosition = QLineEdit()
        self.verticalLayoutWidgetMenuTop.addWidget(self.inputPosition)

        self.medianLabel = QLabel()
        self.medianLabel.setText("Median:")
        self.verticalLayoutWidgetMenuTop.addWidget(self.medianLabel)

        self.minimalLabel = QLabel()
        self.minimalLabel.setText("Minimal:")
        self.verticalLayoutWidgetMenuTop.addWidget(self.minimalLabel)

        self.maximalLabel = QLabel()
        self.maximalLabel.setText("Maximal:")
        self.verticalLayoutWidgetMenuTop.addWidget(self.maximalLabel)

        self.averageLabel = QLabel()
        self.averageLabel.setText("Average:")
        self.verticalLayoutWidgetMenuTop.addWidget(self.averageLabel)

        self.sensorCountLabel = QLabel()
        self.sensorCountLabel.setText("Sensor Count:")
        self.verticalLayoutWidgetMenuTop.addWidget(self.sensorCountLabel)

        #Bottom
        self.configurationTitle = QLabel()
        self.configurationTitle.setText("Configuration:")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.configurationTitle)

        self.configurationTitleYear = QLabel()
        self.configurationTitleYear.setText("Year:")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.configurationTitleYear)

        self.comboBoxConfigurationYear = QComboBox()
        self.comboBoxConfigurationYear.addItem("2020")
        self.comboBoxConfigurationYear.addItem("2019")
        self.comboBoxConfigurationYear.addItem("2018")
        self.comboBoxConfigurationYear.addItem("2017")
        self.comboBoxConfigurationYear.addItem("2016")
        self.comboBoxConfigurationYear.addItem("2015")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.comboBoxConfigurationYear)

        self.configurationTitleMonth = QLabel()
        self.configurationTitleMonth.setText("Month:")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.configurationTitleMonth)

        self.comboBoxConfigurationMonth = QComboBox()
        self.comboBoxConfigurationMonth.addItem("January")
        self.comboBoxConfigurationMonth.addItem("February")
        self.comboBoxConfigurationMonth.addItem("March")
        self.comboBoxConfigurationMonth.addItem("May")
        self.comboBoxConfigurationMonth.addItem("April")
        self.comboBoxConfigurationMonth.addItem("June")
        self.comboBoxConfigurationMonth.addItem("July")
        self.comboBoxConfigurationMonth.addItem("August")
        self.comboBoxConfigurationMonth.addItem("September")
        self.comboBoxConfigurationMonth.addItem("October")
        self.comboBoxConfigurationMonth.addItem("November")
        self.comboBoxConfigurationMonth.addItem("December")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.comboBoxConfigurationMonth)

        self.configurationTitleDay = QLabel()
        self.configurationTitleDay.setText("Day:")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.configurationTitleDay)

        self.comboBoxConfigurationDay = QComboBox()
        self.comboBoxConfigurationDay.addItem("1")
        self.comboBoxConfigurationDay.addItem("2")
        self.comboBoxConfigurationDay.addItem("3")
        self.comboBoxConfigurationDay.addItem("4")
        self.comboBoxConfigurationDay.addItem("5")
        self.comboBoxConfigurationDay.addItem("6")
        self.comboBoxConfigurationDay.addItem("7")
        self.comboBoxConfigurationDay.addItem("8")
        self.comboBoxConfigurationDay.addItem("9")
        self.comboBoxConfigurationDay.addItem("10")
        self.comboBoxConfigurationDay.addItem("11")
        self.comboBoxConfigurationDay.addItem("12")
        self.comboBoxConfigurationDay.addItem("13")
        self.comboBoxConfigurationDay.addItem("14")
        self.comboBoxConfigurationDay.addItem("15")
        self.comboBoxConfigurationDay.addItem("16")
        self.comboBoxConfigurationDay.addItem("17")
        self.comboBoxConfigurationDay.addItem("18")
        self.comboBoxConfigurationDay.addItem("19")
        self.comboBoxConfigurationDay.addItem("20")
        self.comboBoxConfigurationDay.addItem("21")
        self.comboBoxConfigurationDay.addItem("22")
        self.comboBoxConfigurationDay.addItem("23")
        self.comboBoxConfigurationDay.addItem("24")
        self.comboBoxConfigurationDay.addItem("25")
        self.comboBoxConfigurationDay.addItem("26")
        self.comboBoxConfigurationDay.addItem("27")
        self.comboBoxConfigurationDay.addItem("28")
        self.comboBoxConfigurationDay.addItem("29")
        self.comboBoxConfigurationDay.addItem("30")
        self.comboBoxConfigurationDay.addItem("31")
        self.verticalLayoutWidgetMenuBottom.addWidget(self.comboBoxConfigurationDay)


        self.verticalLayoutWidgetMenu.addWidget(self.widgetMenuTop)
        self.verticalLayoutWidgetMenu.addWidget(self.widgetMenuBottom)


        self.horizontalLayout.addWidget(self.widgetMenu)

        self.widget_2 = QWidget(self.home)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widgetMap = QWebEngineView(self.widget_2)
        self.widgetMap.setObjectName(u"widgetMap")
        self.widgetMap.setHtml(self.foliumMapData().getvalue().decode())

        self.verticalLayout.addWidget(self.widgetMap)

        self.widgetMapControlls = QWidget(self.widget_2)
        self.widgetMapControlls.setObjectName(u"widgetMapControlls")
        self.widgetMapControlls.setStyleSheet(u"")

        #Kontrollfeld unten
        self.verticalLayoutMapControlls = QVBoxLayout(self.widgetMapControlls)
        self.slider = QSlider(Qt.Horizontal)
        self.verticalLayoutMapControlls.addWidget(self.slider)

        self.verticalLayout.addWidget(self.widgetMapControlls)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.widget_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.tabWidget.addTab(self.home, "")


        #Analysis tab
        self.analysis = QWidget()
        self.analysis.setObjectName(u"analysis")
        self.horizontalLayout_2 = QHBoxLayout(self.analysis)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widgetAnalysisControls = QWidget(self.analysis)
        self.widgetAnalysisControls.setObjectName(u"widgetAnalysisControls")

        self.vBox3 = QVBoxLayout()

        self.configurationTitleAnalysis = QLabel()
        self.configurationTitleAnalysis.setText("Configuration:")
        self.vBox3.addWidget(self.configurationTitleAnalysis)

        self.configurationTitleAnalysisYear = QLabel()
        self.configurationTitleAnalysisYear.setText("Year:")
        self.vBox3.addWidget(self.configurationTitleAnalysisYear)

        self.comboBoxConfigurationAnalysisYear = QComboBox()
        self.comboBoxConfigurationAnalysisYear.addItem("2020")
        self.comboBoxConfigurationAnalysisYear.addItem("2019")
        self.comboBoxConfigurationAnalysisYear.addItem("2018")
        self.comboBoxConfigurationAnalysisYear.addItem("2017")
        self.comboBoxConfigurationAnalysisYear.addItem("2016")
        self.comboBoxConfigurationAnalysisYear.addItem("2015")
        self.vBox3.addWidget(self.comboBoxConfigurationAnalysisYear)

        self.configurationTitleAnalysisMonth = QLabel()
        self.configurationTitleAnalysisMonth.setText("Month:")
        self.vBox3.addWidget(self.configurationTitleAnalysisMonth)

        self.comboBoxConfigurationAnalysisMonth = QComboBox()
        self.comboBoxConfigurationAnalysisMonth.addItem("January")
        self.comboBoxConfigurationAnalysisMonth.addItem("February")
        self.comboBoxConfigurationAnalysisMonth.addItem("March")
        self.comboBoxConfigurationAnalysisMonth.addItem("May")
        self.comboBoxConfigurationAnalysisMonth.addItem("April")
        self.comboBoxConfigurationAnalysisMonth.addItem("June")
        self.comboBoxConfigurationAnalysisMonth.addItem("July")
        self.comboBoxConfigurationAnalysisMonth.addItem("August")
        self.comboBoxConfigurationAnalysisMonth.addItem("September")
        self.comboBoxConfigurationAnalysisMonth.addItem("October")
        self.comboBoxConfigurationAnalysisMonth.addItem("November")
        self.comboBoxConfigurationAnalysisMonth.addItem("December")
        self.vBox3.addWidget(self.comboBoxConfigurationAnalysisMonth)

        self.configurationTitleAnalysisDay = QLabel()
        self.configurationTitleAnalysisDay.setText("Day:")
        self.vBox3.addWidget(self.configurationTitleAnalysisDay)

        self.comboBoxConfigurationAnalysisDay = QComboBox()
        self.comboBoxConfigurationAnalysisDay.addItem("1")
        self.comboBoxConfigurationAnalysisDay.addItem("2")
        self.comboBoxConfigurationAnalysisDay.addItem("3")
        self.comboBoxConfigurationAnalysisDay.addItem("4")
        self.comboBoxConfigurationAnalysisDay.addItem("5")
        self.comboBoxConfigurationAnalysisDay.addItem("6")
        self.comboBoxConfigurationAnalysisDay.addItem("7")
        self.comboBoxConfigurationAnalysisDay.addItem("8")
        self.comboBoxConfigurationAnalysisDay.addItem("9")
        self.comboBoxConfigurationAnalysisDay.addItem("10")
        self.comboBoxConfigurationAnalysisDay.addItem("11")
        self.comboBoxConfigurationAnalysisDay.addItem("12")
        self.comboBoxConfigurationAnalysisDay.addItem("13")
        self.comboBoxConfigurationAnalysisDay.addItem("14")
        self.comboBoxConfigurationAnalysisDay.addItem("15")
        self.comboBoxConfigurationAnalysisDay.addItem("16")
        self.comboBoxConfigurationAnalysisDay.addItem("17")
        self.comboBoxConfigurationAnalysisDay.addItem("18")
        self.comboBoxConfigurationAnalysisDay.addItem("19")
        self.comboBoxConfigurationAnalysisDay.addItem("20")
        self.comboBoxConfigurationAnalysisDay.addItem("21")
        self.comboBoxConfigurationAnalysisDay.addItem("22")
        self.comboBoxConfigurationAnalysisDay.addItem("23")
        self.comboBoxConfigurationAnalysisDay.addItem("24")
        self.comboBoxConfigurationAnalysisDay.addItem("25")
        self.comboBoxConfigurationAnalysisDay.addItem("26")
        self.comboBoxConfigurationAnalysisDay.addItem("27")
        self.comboBoxConfigurationAnalysisDay.addItem("28")
        self.comboBoxConfigurationAnalysisDay.addItem("29")
        self.comboBoxConfigurationAnalysisDay.addItem("30")
        self.comboBoxConfigurationAnalysisDay.addItem("31")
        self.vBox3.addWidget(self.comboBoxConfigurationAnalysisDay)

        self.widgetAnalysisControls.setLayout(self.vBox3)

        self.horizontalLayout_2.addWidget(self.widgetAnalysisControls)

        self.widgetAnalysis = pyqtgraph.PlotWidget(self.analysis)
        self.widgetAnalysis.setObjectName(u"widgeAnalysis")

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        self.widgetAnalysis.plot(hour, temperature)


        self.horizontalLayout_2.addWidget(self.widgetAnalysis)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.tabWidget.addTab(self.analysis, "")


        # Highlights tab
        self.highlights = QWidget()
        self.highlights.setObjectName(u"highlights")

        self.scroll = QScrollArea()
        self.highlightsWidget = QWidget()
        self.vBox = QGridLayout()

        for i in range(1, 10):
            object = pyqtgraph.PlotWidget(self.analysis)
            hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
            object.plot(hour, temperature)
            self.vBox.setRowMinimumHeight(i-1, 500)
            self.vBox.addWidget(object)


        self.highlightsWidget.setLayout(self.vBox)



        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.highlightsWidget)

        self.vBox2 = QVBoxLayout()
        self.vBox2.addWidget(self.scroll)

        self.highlights.setLayout(self.vBox2)

        self.tabWidget.addTab(self.highlights, "")


        #Forecast Tab
        self.forecast = QWidget()
        self.forecast.setObjectName(u"forecast")
        self.horizontalLayout_4 = QHBoxLayout(self.forecast)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widgetForecastMenu = QWidget(self.forecast)
        self.widgetForecastMenu.setObjectName(u"widgetForecastMenu")

        self.horizontalLayout_4.addWidget(self.widgetForecastMenu)

        self.widget_3 = QWidget(self.forecast)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widgetForecastMap = QWebEngineView(self.widget_3)
        self.widgetForecastMap.setObjectName(u"widgetForecastMap")
        self.widgetForecastMap.setHtml(self.foliumMapData().getvalue().decode())

        self.verticalLayout_2.addWidget(self.widgetForecastMap)

        self.widgetForecastMapControlls = QWidget(self.widget_3)
        self.widgetForecastMapControlls.setObjectName(u"widgetForecastMapControlls")

        self.verticalLayout_2.addWidget(self.widgetForecastMapControlls)

        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_4.addWidget(self.widget_3)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 4)

        self.tabWidget.addTab(self.forecast, "")


        # Personalisation Tab
        self.personalization = QWidget()
        self.personalization.setObjectName(u"personalization")
        self.horizontalLayout_5 = QHBoxLayout(self.personalization)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widgetPersonalization = QWidget(self.personalization)
        self.widgetPersonalization.setObjectName(u"widgetPersonalization")

        self.horizontalLayout_5.addWidget(self.widgetPersonalization)

        self.tabWidget.addTab(self.personalization, "")

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

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home), QCoreApplication.translate("Form", u"Home", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analysis),
                                  QCoreApplication.translate("Form", u"Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.highlights),
                                  QCoreApplication.translate("Form", u"Highlights", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.forecast),
                                  QCoreApplication.translate("Form", u"Forecast", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.personalization),
                                  QCoreApplication.translate("Form", u"Personalization", None))


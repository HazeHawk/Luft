import sys
import io
import folium

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import *

class Ui_Form(object):
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
        self.widgetMap.setHtml(self.foluimMapData().getvalue().decode())

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

        self.horizontalLayout_2.addWidget(self.widgetAnalysisControls)

        self.widgeAnalysis = QWidget(self.analysis)
        self.widgeAnalysis.setObjectName(u"widgeAnalysis")

        self.horizontalLayout_2.addWidget(self.widgeAnalysis)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.tabWidget.addTab(self.analysis, "")


        # Highlights tab
        self.highlights = QWidget()
        self.highlights.setObjectName(u"highlights")

        self.scroll = QScrollArea()
        self.highlightsWidget = QWidget()
        self.vBox = QVBoxLayout()

        for i in range(1, 50):
            object = QLabel("Diagramm")
            self.vBox.addWidget(object)


        self.highlightsWidget.setLayout(self.vBox)



        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        self.widgetForecastMap.setHtml(self.foluimMapData().getvalue().decode())

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

    def foluimMapData(self):
        m = folium.Map(
            location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13
        )

        data = io.BytesIO()
        m.save(data, close_file=False)

        return data

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
        # retranslateUi

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = QWidget()

    ui = Ui_Form()
    ui.setupUi(widget)

    widget.show()

    sys.exit(app.exec_())

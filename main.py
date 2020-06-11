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
        Form.resize(900, 599)
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

        self.inputPositionLable = QLabel()
        self.inputPositionLable.setText("Input Your Position")
        self.verticalLayoutWidgetMenu.addWidget(self.inputPositionLable)

        self.inputPosition = QLineEdit()
        self.verticalLayoutWidgetMenu.addWidget(self.inputPosition)

        self.medianLabel = QLabel()
        self.medianLabel.setText("Median:")
        self.verticalLayoutWidgetMenu.addWidget(self.medianLabel)

        self.minimalLabel = QLabel()
        self.minimalLabel.setText("Minimal:")
        self.verticalLayoutWidgetMenu.addWidget(self.minimalLabel)

        self.maximalLabel = QLabel()
        self.maximalLabel.setText("Maximal:")
        self.verticalLayoutWidgetMenu.addWidget(self.maximalLabel)

        self.averageLabel = QLabel()
        self.averageLabel.setText("Average:")
        self.verticalLayoutWidgetMenu.addWidget(self.averageLabel)

        self.sensorCountLabel = QLabel()
        self.sensorCountLabel.setText("Sensor Count:")
        self.verticalLayoutWidgetMenu.addWidget(self.sensorCountLabel)

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
        self.horizontalLayout_3 = QHBoxLayout(self.highlights)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widgetHighlights = QWidget(self.highlights)
        self.widgetHighlights.setObjectName(u"widgetHighlights")

        self.horizontalLayout_3.addWidget(self.widgetHighlights)

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

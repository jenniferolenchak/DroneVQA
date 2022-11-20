# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LaunchScreen.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(502, 463)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(40, 330, 421, 101))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonAlreadyLaunchedAirsim = QPushButton(self.gridLayoutWidget)
        self.buttonAlreadyLaunchedAirsim.setObjectName(u"buttonAlreadyLaunchedAirsim")

        self.gridLayout.addWidget(self.buttonAlreadyLaunchedAirsim, 2, 0, 1, 1)

        self.labelVirtualEnvSelectPrompt = QLabel(self.gridLayoutWidget)
        self.labelVirtualEnvSelectPrompt.setObjectName(u"labelVirtualEnvSelectPrompt")
        self.labelVirtualEnvSelectPrompt.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelVirtualEnvSelectPrompt, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonLaunchDevMap = QPushButton(self.gridLayoutWidget)
        self.buttonLaunchDevMap.setObjectName(u"buttonLaunchDevMap")

        self.gridLayout_2.addWidget(self.buttonLaunchDevMap, 0, 1, 1, 1)

        self.buttonLaunchCityMap = QPushButton(self.gridLayoutWidget)
        self.buttonLaunchCityMap.setObjectName(u"buttonLaunchCityMap")

        self.gridLayout_2.addWidget(self.buttonLaunchCityMap, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 0, 191, 91))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 80, 471, 51))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.buttonAlreadyLaunchedAirsim.setText(QCoreApplication.translate("Form", u"[I have already launched AirSim myself]", None))
        self.labelVirtualEnvSelectPrompt.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Select A Virtual  Environment To Explore:</span></p></body></html>", None))
        self.buttonLaunchDevMap.setText(QCoreApplication.translate("Form", u"Launch Dev Map", None))
        self.buttonLaunchCityMap.setText(QCoreApplication.translate("Form", u"Launch City Map", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:28pt; font-weight:700; color:#000000;\">DroneVQA</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:16pt; color:#1315a6;\">Utilizing Artifical Intelligence For Visual Question Anwering With Sumulated Drones</span></p></body></html>", None))
    # retranslateUi


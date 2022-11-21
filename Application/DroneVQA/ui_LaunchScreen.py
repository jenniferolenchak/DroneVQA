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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(502, 481)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(40, 300, 421, 101))
        self.gridLayout_SelectVirtalEnvArea = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_SelectVirtalEnvArea.setObjectName(u"gridLayout_SelectVirtalEnvArea")
        self.gridLayout_SelectVirtalEnvArea.setContentsMargins(0, 0, 0, 0)
        self.button_AlreadyLaunched = QPushButton(self.gridLayoutWidget)
        self.button_AlreadyLaunched.setObjectName(u"button_AlreadyLaunched")

        self.gridLayout_SelectVirtalEnvArea.addWidget(self.button_AlreadyLaunched, 2, 0, 1, 1)

        self.label_VirtualEnvSelectPrompt = QLabel(self.gridLayoutWidget)
        self.label_VirtualEnvSelectPrompt.setObjectName(u"label_VirtualEnvSelectPrompt")
        self.label_VirtualEnvSelectPrompt.setAlignment(Qt.AlignCenter)

        self.gridLayout_SelectVirtalEnvArea.addWidget(self.label_VirtualEnvSelectPrompt, 0, 0, 1, 1)

        self.gridLayout_EnvLaunchButtons = QGridLayout()
        self.gridLayout_EnvLaunchButtons.setObjectName(u"gridLayout_EnvLaunchButtons")
        self.button_LaunchTestMap = QPushButton(self.gridLayoutWidget)
        self.button_LaunchTestMap.setObjectName(u"button_LaunchTestMap")

        self.gridLayout_EnvLaunchButtons.addWidget(self.button_LaunchTestMap, 0, 1, 1, 1)

        self.button_LaunchCityMap = QPushButton(self.gridLayoutWidget)
        self.button_LaunchCityMap.setObjectName(u"button_LaunchCityMap")

        self.gridLayout_EnvLaunchButtons.addWidget(self.button_LaunchCityMap, 0, 0, 1, 1)


        self.gridLayout_SelectVirtalEnvArea.addLayout(self.gridLayout_EnvLaunchButtons, 1, 0, 1, 1)

        self.label_LaunchScreenTitle = QLabel(Form)
        self.label_LaunchScreenTitle.setObjectName(u"label_LaunchScreenTitle")
        self.label_LaunchScreenTitle.setGeometry(QRect(150, 0, 191, 91))
        self.label_LaunchScreenDescription = QLabel(Form)
        self.label_LaunchScreenDescription.setObjectName(u"label_LaunchScreenDescription")
        self.label_LaunchScreenDescription.setGeometry(QRect(20, 80, 471, 61))
        self.label_LaunchScreenDescription.setAlignment(Qt.AlignCenter)
        self.label_LaunchScreenDescription.setWordWrap(True)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(80, 420, 331, 48))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_FurtherLaunchInstruction = QLabel(self.verticalLayoutWidget)
        self.label_FurtherLaunchInstruction.setObjectName(u"label_FurtherLaunchInstruction")

        self.verticalLayout.addWidget(self.label_FurtherLaunchInstruction)

        self.button_StartVQA = QPushButton(self.verticalLayoutWidget)
        self.button_StartVQA.setObjectName(u"button_StartVQA")

        self.verticalLayout.addWidget(self.button_StartVQA)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_AlreadyLaunched.setText(QCoreApplication.translate("Form", u"[I have already launched AirSim myself]", None))
        self.label_VirtualEnvSelectPrompt.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Select A Virtual  Environment To Explore:</span></p></body></html>", None))
        self.button_LaunchTestMap.setText(QCoreApplication.translate("Form", u"Launch Test Map", None))
        self.button_LaunchCityMap.setText(QCoreApplication.translate("Form", u"Launch City Map", None))
        self.label_LaunchScreenTitle.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:28pt; font-weight:700; color:#000000;\">DroneVQA</span></p></body></html>", None))
        self.label_LaunchScreenDescription.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:16pt; color:#1315a6;\">Utilizing Artifical Intelligence For Visual Question Anwering With Sumulated Drones</span></p></body></html>", None))
        self.label_FurtherLaunchInstruction.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" color:#740000;\">Click </span><span style=\" font-style:italic; color:#740000;\">&quot;No&quot;</span><span style=\" color:#740000;\"> in AirSim to select quadrotor drone , then click here:</span></p></body></html>", None))
        self.button_StartVQA.setText(QCoreApplication.translate("Form", u"Start VQA", None))
    # retranslateUi


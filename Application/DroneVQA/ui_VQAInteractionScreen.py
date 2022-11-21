# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VQAInteractionScreen.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QHBoxLayout,
    QLCDNumber, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1246, 608)
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(310, 20, 636, 82))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 130, 241, 116))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_2.addWidget(self.pushButton_2, 1, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_2.addWidget(self.pushButton_3, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_2.addWidget(self.pushButton_4, 0, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_2.addWidget(self.pushButton_5, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(360, 130, 391, 142))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSlider_3 = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider_3, 2, 1, 1, 1)

        self.label_7 = QLabel(self.verticalLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_8 = QLabel(self.verticalLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)

        self.horizontalSlider_2 = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider_2, 1, 1, 1, 1)

        self.label_6 = QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_5 = QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider, 0, 1, 1, 1)

        self.horizontalSlider_4 = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider_4, 3, 1, 1, 1)

        self.lcdNumber = QLCDNumber(self.verticalLayoutWidget_2)
        self.lcdNumber.setObjectName(u"lcdNumber")

        self.gridLayout_3.addWidget(self.lcdNumber, 0, 2, 1, 1)

        self.lcdNumber_2 = QLCDNumber(self.verticalLayoutWidget_2)
        self.lcdNumber_2.setObjectName(u"lcdNumber_2")

        self.gridLayout_3.addWidget(self.lcdNumber_2, 1, 2, 1, 1)

        self.lcdNumber_3 = QLCDNumber(self.verticalLayoutWidget_2)
        self.lcdNumber_3.setObjectName(u"lcdNumber_3")

        self.gridLayout_3.addWidget(self.lcdNumber_3, 2, 2, 1, 1)

        self.lcdNumber_4 = QLCDNumber(self.verticalLayoutWidget_2)
        self.lcdNumber_4.setObjectName(u"lcdNumber_4")

        self.gridLayout_3.addWidget(self.lcdNumber_4, 3, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.verticalLayoutWidget_3 = QWidget(Form)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(840, 130, 391, 142))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSlider_5 = QSlider(self.verticalLayoutWidget_3)
        self.horizontalSlider_5.setObjectName(u"horizontalSlider_5")
        self.horizontalSlider_5.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_5, 2, 1, 1, 1)

        self.label_9 = QLabel(self.verticalLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_10 = QLabel(self.verticalLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 3, 0, 1, 1)

        self.horizontalSlider_6 = QSlider(self.verticalLayoutWidget_3)
        self.horizontalSlider_6.setObjectName(u"horizontalSlider_6")
        self.horizontalSlider_6.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_6, 1, 1, 1, 1)

        self.label_11 = QLabel(self.verticalLayoutWidget_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_12 = QLabel(self.verticalLayoutWidget_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)

        self.horizontalSlider_7 = QSlider(self.verticalLayoutWidget_3)
        self.horizontalSlider_7.setObjectName(u"horizontalSlider_7")
        self.horizontalSlider_7.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_7, 0, 1, 1, 1)

        self.horizontalSlider_8 = QSlider(self.verticalLayoutWidget_3)
        self.horizontalSlider_8.setObjectName(u"horizontalSlider_8")
        self.horizontalSlider_8.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_8, 3, 1, 1, 1)

        self.lcdNumber_5 = QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_5.setObjectName(u"lcdNumber_5")

        self.gridLayout_4.addWidget(self.lcdNumber_5, 0, 2, 1, 1)

        self.lcdNumber_6 = QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_6.setObjectName(u"lcdNumber_6")

        self.gridLayout_4.addWidget(self.lcdNumber_6, 1, 2, 1, 1)

        self.lcdNumber_7 = QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_7.setObjectName(u"lcdNumber_7")

        self.gridLayout_4.addWidget(self.lcdNumber_7, 2, 2, 1, 1)

        self.lcdNumber_8 = QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_8.setObjectName(u"lcdNumber_8")

        self.gridLayout_4.addWidget(self.lcdNumber_8, 3, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_4)

        self.verticalLayoutWidget_4 = QWidget(Form)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(30, 320, 481, 201))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.verticalLayoutWidget_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_15)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton_6 = QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_2.addWidget(self.pushButton_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_13 = QLabel(self.verticalLayoutWidget_4)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout.addWidget(self.label_13)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout.addWidget(self.lineEdit_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_14 = QLabel(self.verticalLayoutWidget_4)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_14)

        self.textEdit = QTextEdit(self.verticalLayoutWidget_4)
        self.textEdit.setObjectName(u"textEdit")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.textEdit)


        self.verticalLayout_5.addLayout(self.formLayout_3)

        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(650, 320, 479, 22))
        self.label_16.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:28pt; font-weight:700; color:#0021b6;\">DroneVQA: AirSim Interaction Menu</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Drone Flight Control</span></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Left", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Right", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"Up", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Down", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Weather Control</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Dust", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Fog", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Snow", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Rain", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Environment Control</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Maple Leaves", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Dust", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Road Snow", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Road Wetness", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Ask A Question</span></p></body></html>", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Enter Question Here...", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"Ask", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Answer: ", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Details:", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Result Visualization</span></p></body></html>", None))
    # retranslateUi


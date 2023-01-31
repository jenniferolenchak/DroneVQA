# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoadScreen.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form_LoadScreen(object):
    def setupUi(self, Form_LoadScreen):
        if not Form_LoadScreen.objectName():
            Form_LoadScreen.setObjectName(u"Form_LoadScreen")
        Form_LoadScreen.setEnabled(True)
        Form_LoadScreen.resize(500, 500)
        Form_LoadScreen.setMinimumSize(QSize(500, 500))
        Form_LoadScreen.setMaximumSize(QSize(500, 500))
        font = QFont()
        font.setFamilies([u"Arial"])
        Form_LoadScreen.setFont(font)
        Form_LoadScreen.setStyleSheet(u"background-color: white;")
        self.verticalLayout = QVBoxLayout(Form_LoadScreen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(Form_LoadScreen)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u"Images/Logos/Logo_DroneOnly_ScaledDown.png"))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.progressBar_OverallProgress = QProgressBar(Form_LoadScreen)
        self.progressBar_OverallProgress.setObjectName(u"progressBar_OverallProgress")
        self.progressBar_OverallProgress.setMaximum(100)
        self.progressBar_OverallProgress.setValue(0)
        self.progressBar_OverallProgress.setInvertedAppearance(False)
        self.progressBar_OverallProgress.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout.addWidget(self.progressBar_OverallProgress)

        self.label = QLabel(Form_LoadScreen)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(Form_LoadScreen)

        QMetaObject.connectSlotsByName(Form_LoadScreen)
    # setupUi

    def retranslateUi(self, Form_LoadScreen):
        Form_LoadScreen.setWindowTitle(QCoreApplication.translate("Form_LoadScreen", u"Form_LoadScreen", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("Form_LoadScreen", u"<html><head/><body><p><span style=\" font-size:20pt; color:#1315a6;\">Loading...</span></p></body></html>", None))
    # retranslateUi


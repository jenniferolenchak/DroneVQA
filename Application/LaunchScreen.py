# This Python file uses the following encoding: utf-8

import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import QScreen, QIcon
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader

class LaunchScreen(QWidget):
    def __init__(self, app, stackedWidget, threadManager, VQAScreen, controller, parent=None):
        super().__init__(parent)
        self.app = app
        self.stackedWidget = stackedWidget
        self.threadManager = threadManager
        self.VQAScreen = VQAScreen
        self.controller = controller
        self.load_ui()

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "LaunchScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.resize(500, 625)

        # Connect button action to method
        self.ui.button_InitializeClient.clicked.connect(self.startVQA)

    def navToVQAScreen(self):
        '''Initialize VQA interaction screen and set at the active stacked frame'''
        self.stackedWidget.hide()
        self.stackedWidget.setCurrentWidget(self.VQAScreen)
        self.stackedWidget.resize(1500, 850)
        self.stackedWidget.show()

        # Set window position
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.stackedWidget.frameGeometry()
        geo.moveCenter(center)
        self.stackedWidget.move(geo.topLeft())
        #stackedWidget.setWindowState(Qt.WindowStates.WindowMaximized)

        # Start Camera
        self.VQAScreen.setupCamera()

    def startVQA(self):
        '''Initialize AirSim client, setup camera feed, and change window display to VQA Interaction Window'''
        # Logic to verify the success of initializeAirSimClient() and setupCamera() before switching to the VQA screen
        self.ui.button_InitializeClient.setText("Initializing Client...")
        self.app.processEvents()
        try:
            self.controller.initializeAirSimClient()
            self.navToVQAScreen()
        except:
            errorBox = QMessageBox(self.ui)
            errorBox.setText("""<p>Error initializing the client. 
                Before initializing the client, please ensure that you have launched the AirSim Unreal Engine Environment and that the quadrotor drone is loaded completely. 
                Select 'Retry Client Initialization' to try again.</p>""")
            errorBox.setStyleSheet("""* { background: white; color: #0d0f75; font-family: Arial; font-size: 13px; font-weight: 400; } 
                QPushButton{ background-color: rgb(13, 15, 117); color: white; border-color: blue; border-radius: 5px; padding: 10px 20px; }""")
            errorBox.setWindowTitle("Error")
            errorBox.setWindowIcon(QIcon("Images/Logos/logo_drone_only.png"))
            errorBox.show()
            errorBox.move(errorBox.pos().x()+10, errorBox.pos().y())
            errorBox.exec()
            self.ui.button_InitializeClient.setText("Retry Client Initialization")




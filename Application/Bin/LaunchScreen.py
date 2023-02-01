# This Python file uses the following encoding: utf-8

import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QScreen
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader

class LaunchScreen(QWidget):
    def __init__(self, stackedWidget, threadManager, VQAScreen, controller, parent=None):
        super().__init__(parent)
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

        # Connect button actions to methods
        self.ui.button_AlreadyLaunched.clicked.connect(self.showFurtherInstructions)
        self.ui.button_InitializeClient.clicked.connect(self.startVQA)
        self.ui.button_LaunchCityMap.clicked.connect(lambda: self.launchAirSimEnv("..\\Environments\\CityEnvironment\\CityEnviron.exe"))

        # Initially hide further user instructions
        self.ui.button_InitializeClient.hide()
        self.ui.label_AirSimLaunchInstruction.hide()

    def launchAirSimEnv(self, relativePath):
        '''Launch AirSim environment executable and display further instructions to user'''
        projectPath = os.path.dirname(__file__)
        mapPath = os.path.join(projectPath, relativePath)
        self.runningSimulation = os.startfile(mapPath)
        self.showFurtherInstructions()

    def showFurtherInstructions(self):
        '''Display VQA initilaization button and instruction to click button'''
        self.ui.label_AirSimLaunchInstruction.show()
        self.ui.button_InitializeClient.show()

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

    @Slot()
    def startVQA(self):
        '''Initialize AirSim client, setup camera feed, and change window display to VQA Interaction Window'''
        self.controller.initializeAirSimClient()
        self.VQAScreen.setupCamera()
        self.navToVQAScreen()


# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

import airsim
#import cv2
#import numpy as np
#from transformers import ViltForQuestionAnswering, ViltProcessor
#import torch

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, Qt, QThreadPool, Slot
from PySide6.QtUiTools import QUiLoader

class LaunchScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

        self.threadManager = QThreadPool()

        # Connect button actions to methods
        self.ui.button_AlreadyLaunched.clicked.connect(self.showFurtherInstructions)
        self.ui.button_StartVQA.clicked.connect(self.startVQA)
        self.ui.button_LaunchCityMap.clicked.connect(lambda: self.launchAirSimEnv("..\\CityEnvironment\\CityEnviron.exe"))
        #self.ui.button_LaunchTestMap.clicked.connect(lambda: self.launchAirSimEnv("..\\TestEnvironment\\TestEnviron.exe"))

        # Initially hide further user instructions
        self.ui.button_StartVQA.hide()
        self.ui.label_AirSimLaunchInstruction.hide()

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "LaunchScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def launchAirSimEnv(self, relativePath):
        '''Launch AirSim environment executable and display further instructions to user'''
        projectPath = os.path.dirname(__file__)
        mapPath = os.path.join(projectPath, relativePath)
        self.runningSimulation = os.startfile(mapPath)
        self.showFurtherInstructions()

    def showFurtherInstructions(self):
        '''Display "Start VQA" button and instruction to select No in AirSim'''
        self.ui.label_AirSimLaunchInstruction.show()
        self.ui.button_StartVQA.show()

    def navToVQAScreen(self):
        '''Initialize VQA interaction screen and set at the active stacked frame'''
        widget2 = VQAInteractionScreen()
        stackedWidget.addWidget(widget2)
        stackedWidget.setCurrentWidget(widget2)
        stackedWidget.setMinimumHeight(1000)
        stackedWidget.setMinimumWidth(1000)
        stackedWidget.setWindowState(Qt.WindowStates.WindowMaximized)

    @Slot()
    def startVQA(self):
        '''Initialize AirSim client and change window display to VQA Interaction Window'''
        self.navToVQAScreen()
        self.threadManager.start(self.initilizeAirSimClient)
        print(self.threadManager.activeThreadCount())

    @Slot()
    def initilizeAirSimClient(self):
        '''Initialize AirSim client'''
        client = airsim.MultirotorClient()
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)

        # Enable Weather Options
        client.simEnableWeather(True)

        # Async methods returns Future. Call join() to wait for task to complete.
        client.takeoffAsync().join()
        client.moveToPositionAsync(-10, 10, -10, 5).join()

        print("Finished Moving")



class VQAInteractionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "VQAInteractionScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    stackedWidget = QStackedWidget()
    stackedWidget.setMinimumHeight(500)
    stackedWidget.setMinimumWidth(500)
    stackedWidget.setWindowTitle("DroneVQA")
    stackedWidget.setWindowIcon(QIcon("logo_drone_only.png"))

    # Initialize global variables
    CAMERA_NAME = '0'
    IMAGE_TYPE = airsim.ImageType.Scene
    DECODE_EXTENSION = '.png'
    record = True

    launchScreen = LaunchScreen()
    stackedWidget.addWidget(launchScreen)

    stackedWidget.show()

    sys.exit(app.exec())

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

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "LaunchScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Connect button actions to methods
        self.ui.button_AlreadyLaunched.clicked.connect(self.showFurtherInstructions)
        self.ui.button_InitializeClient.clicked.connect(self.startVQA)
        self.ui.button_LaunchCityMap.clicked.connect(lambda: self.launchAirSimEnv("..\\CityEnvironment\\CityEnviron.exe"))
        #self.ui.button_LaunchTestMap.clicked.connect(lambda: self.launchAirSimEnv("..\\TestEnvironment\\TestEnviron.exe"))

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
        '''Display "Start VQA" button and instruction to select No in AirSim'''
        self.ui.label_AirSimLaunchInstruction.show()
        self.ui.button_InitializeClient.show()

    def navToVQAScreen(self):
        '''Initialize VQA interaction screen and set at the active stacked frame'''
        stackedWidget.setCurrentWidget(widget2)
        stackedWidget.setMinimumHeight(1000)
        stackedWidget.setMinimumWidth(1500)
        #stackedWidget.setWindowState(Qt.WindowStates.WindowMaximized)

    @Slot()
    def startVQA(self):
        '''Initialize AirSim client and change window display to VQA Interaction Window'''
        self.navToVQAScreen()
        threadManager.start(controller.initializeAirSimClient)

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

        # Set button icons
        self.ui.button_Up.setIcon(QIcon("arrow_up.png"))
        self.ui.button_Down.setIcon(QIcon("arrow_down.png"))
        self.ui.button_Left.setIcon(QIcon("arrow_left.png"))
        self.ui.button_Right.setIcon(QIcon("arrow_right.png"))
        self.ui.button_RotateRight.setIcon(QIcon("arrow_rotate_right.png"))
        self.ui.button_RotateLeft.setIcon(QIcon("arrow_rotate_left.png"))

        # Connect drone navigation button actions to methods
        self.ui.button_Up.pressed.connect(lambda: controller.startDroneMovementThread("up"))
        self.ui.button_Down.pressed.connect(lambda: controller.startDroneMovementThread("down"))
        self.ui.button_Left.pressed.connect(lambda: controller.startDroneMovementThread("left"))
        self.ui.button_Right.pressed.connect(lambda: controller.startDroneMovementThread("right"))
        self.ui.button_RotateRight.pressed.connect(lambda: controller.startDroneMovementThread("rotate right"))
        self.ui.button_RotateLeft.pressed.connect(lambda: controller.startDroneMovementThread("rotate left"))

        # Connect weather and environment sliders to methods
        self.ui.horizontalSlider_Rain.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Rain, self.ui.lcdNumber_Rain, self.ui.horizontalSlider_Rain.value()))
        self.ui.horizontalSlider_Snow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Snow, self.ui.lcdNumber_Snow, self.ui.horizontalSlider_Snow.value()))
        self.ui.horizontalSlider_Dust.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Dust, self.ui.lcdNumber_Dust, self.ui.horizontalSlider_Dust.value()))
        self.ui.horizontalSlider_Fog.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Fog, self.ui.lcdNumber_Fog, self.ui.horizontalSlider_Fog.value()))
        self.ui.horizontalSlider_RoadWetness.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Roadwetness, self.ui.lcdNumber_RoadWetness, self.ui.horizontalSlider_RoadWetness.value()))
        self.ui.horizontalSlider_RoadSnow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.RoadSnow, self.ui.lcdNumber_RoadSnow, self.ui.horizontalSlider_RoadSnow.value()))
        self.ui.horizontalSlider_MapleLeaves.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.MapleLeaf, self.ui.lcdNumber_MapleLeaves, self.ui.horizontalSlider_MapleLeaves.value()))


    def changeWeather(self, command, lcd, sliderVal):
        '''Updates the lcd number next to slider and passes updated weather values to air sim control'''
        lcd.display(sliderVal)

        # Convert slider value from [0-100] to [0.00-1.00] range equivalent & pass to AirSim controller
        decSliderVal = sliderVal / 100
        controller.updateAirSimWeather(command, decSliderVal)


class AirSimControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set initial flight coordinates
        self.x = -10
        self.y = 10
        self.z = -10

    @Slot()
    def initializeAirSimClient(self):
        '''Initializes AirSim client'''
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        # Enable Weather Options
        self.client.simEnableWeather(True)

        # Async methods returns Future. Call join() to wait for task to complete.
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(self.x, self.y, self.z, 5).join()

    #@Slot()
    def threadedDroneMovement(self, command):
        print(str(threadManager.activeThreadCount()) + "" + command)
        '''Moves quadcopter drone based on direction command'''
        if (command == "rotate left"):
            self.client.moveByAngleRatesThrottleAsync(0, 0, 1, 0.2, 0.5).join()
        elif (command == "rotate right"):
            self.client.moveByAngleRatesThrottleAsync(0, 0, -1, 0.2, 0.5).join()
        elif (command == "up"):
            self.x+=1
        elif (command == "down"):
            self.x-=1
        elif (command == "left"):
            self.y+=1
        elif (command == "right"):
            self.y+=1

        print("x: " + str(self.x) + "y: " + str(self.y) + "z: " + str(self.z))

        self.client.moveToPositionAsync(self.x, self.y, self.z, 10)


    #@Slot()
    def startDroneMovementThread(self, command):
        #threadManager.start(self.threadedDroneMovement(command))
        #print(threadManager.activeThreadCount())
        self.threadedDroneMovement(command)


    def updateAirSimWeather(self, parameter, value):
        self.client.simSetWeatherParameter(parameter, value)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = AirSimControl()
    threadManager = QThreadPool()

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
    widget2 = VQAInteractionScreen()
    stackedWidget.addWidget(launchScreen)
    stackedWidget.addWidget(widget2)
    stackedWidget.setCurrentWidget(launchScreen)

    stackedWidget.show()

    sys.exit(app.exec())

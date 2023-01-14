import os
from pathlib import Path
import sys

import airsim

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap, QScreen
from PySide6.QtCore import QFile, Qt, QThreadPool, Slot
from PySide6.QtUiTools import QUiLoader

class AirSimControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set default movement velocity
        self.movementVelocity = 20

        # Set initial flight coordinates
        self.x = 0
        self.y = 0
        self.z = -3

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


    def startDroneMovement(self, command):
        if (command == "up"):
            self.client.moveByVelocityAsync(0, 0, 0-self.movementVelocity, 1)
        elif (command == "down"):
            self.client.moveByVelocityAsync(0, 0, self.movementVelocity, 1)
        elif (command == "left"):
            self.client.moveByVelocityAsync(0, 0-self.movementVelocity, 0, 1)
        elif (command == "right"):
            self.client.moveByVelocityAsync(0, self.movementVelocity, 0, 1)
        elif (command == "forward"):
            self.client.moveByVelocityAsync(self.movementVelocity, 0, 0, 1)
        elif (command == "backward"):
            self.client.moveByVelocityAsync(0-self.movementVelocity, 0, 0, 1)

    def stopDroneMovement(self, command):
        self.client.moveByVelocityAsync(0, 0, 0, 3)

    def resetDrone(self, command):
        self.client.reset()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(self.x, self.y, self.z, 5).join()

    def updateAirSimWeather(self, parameter, value):
        self.client.simSetWeatherParameter(parameter, value)

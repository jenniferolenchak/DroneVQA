import os
from pathlib import Path
import sys

from threading import Timer

import airsim
from airsim.types import YawMode, KinematicsState, Pose

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap, QScreen
from PySide6.QtCore import QFile, Qt, QThreadPool, Slot
from PySide6.QtUiTools import QUiLoader

class AirSimControl(QWidget):

    # Camera Variables
    CAMERA_NAME = '0'
    IMAGE_TYPE = airsim.ImageType.Scene

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set default movement velocity
        self.movementVelocity = 20

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

        # Create second AirSim client for image threading
        self.image_client = airsim.MultirotorClient()

        print("AirSim Client Initialized")

    def startDroneMovement(self, command, moveButtons):
        # Disable movement until current movement is finished
        for button in moveButtons:
            button.setEnabled(False)

        if (command == "up"):
            self.client.moveByVelocityBodyFrameAsync(0, 0, 0-self.movementVelocity, 1)
        elif (command == "down"):
            self.client.moveByVelocityBodyFrameAsync(0, 0, self.movementVelocity, 1)
        elif (command == "left"):
            self.client.moveByVelocityBodyFrameAsync(0, 0-self.movementVelocity, 0, 1)
        elif (command == "right"):
            self.client.moveByVelocityBodyFrameAsync(0, self.movementVelocity, 0, 1)
        elif (command == "forward"):
            self.client.moveByVelocityBodyFrameAsync(self.movementVelocity, 0, 0, 1)
        elif (command == "backward"):
            self.client.moveByVelocityBodyFrameAsync(0-self.movementVelocity, 0, 0, 1)
        elif (command == 'rotate_right'):
            self.client.moveByVelocityBodyFrameAsync(0, 0, 0, 1, drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,  yaw_mode=YawMode(True, abs(0-self.movementVelocity)))
        elif (command == 'rotate_left'):
            self.client.moveByVelocityBodyFrameAsync(0, 0, 0, 1, drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,  yaw_mode=YawMode(True, -abs(0-self.movementVelocity)))

        Timer(1.5, self.stopDroneMovement, [moveButtons]).start()
        

    def stopDroneMovement(self, moveButtons):
        self.client.moveByVelocityAsync(0, 0, 0, 3)
        # Enable movement after stopping current movement
        for button in moveButtons:
            button.setEnabled(True)


    def resetDrone(self, command):
        self.client.reset()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()

    def updateAirSimWeather(self, parameter, value):
        self.client.simSetWeatherParameter(parameter, value)

    def getCurrentDroneImage(self, cameraName = CAMERA_NAME, imageType = IMAGE_TYPE):
        return self.image_client.simGetImage(cameraName, imageType)
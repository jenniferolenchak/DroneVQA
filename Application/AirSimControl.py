import os
from pathlib import Path
import sys

import airsim
from airsim.types import YawMode

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap, QScreen
from PySide6.QtCore import QFile, Qt, QThreadPool, Slot
from PySide6.QtUiTools import QUiLoader

class AirSimControl(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set default movement velocity
        self.movementVelocity = 20

        # Set default camera type to scene
        self.imageType = airsim.ImageType.Scene
        
        # Set camera name value
        self.CAMERA_NAME = '0'

    def setCameraType(self, cameraIndex):
        # Types of AirSim cameras available
        CAMERA_TYPE = [airsim.ImageType.Scene, airsim.ImageType.DepthPlanar, airsim.ImageType.DepthPerspective, airsim.ImageType.DepthVis, airsim.ImageType.DisparityNormalized, airsim.ImageType.Segmentation, airsim.ImageType.SurfaceNormals, airsim.ImageType.Infrared, airsim.ImageType.OpticalFlow, airsim.ImageType.OpticalFlowVis]
        self.imageType = CAMERA_TYPE[cameraIndex]

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

    def startDroneMovement(self, command):
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

    def stopDroneMovement(self, command):
        self.client.moveByVelocityAsync(0, 0, 0, 3)

    def resetDrone(self, command):
        self.client.reset()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()

    def updateAirSimWeather(self, parameter, value):
        self.client.simSetWeatherParameter(parameter, value)

    def getCurrentDroneImage(self):
        return self.image_client.simGetImage(self.CAMERA_NAME, self.imageType)
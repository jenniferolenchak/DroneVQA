# This Python file uses the following encoding: utf-8
from pathlib import Path
import sys

import airsim

from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThreadPool

from LaunchScreen import LaunchScreen
from VQAInteractionScreen import VQAInteractionScreen
from AirSimControl import AirSimControl
from utils import setupViltTransformer, setupLxmertTransformer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = AirSimControl()
    threadManager = QThreadPool()

    stackedWidget = QStackedWidget()
    stackedWidget.setMinimumHeight(625)
    stackedWidget.setMinimumWidth(500)
    stackedWidget.setWindowTitle("DroneVQA")
    stackedWidget.setWindowIcon(QIcon("Images/Logos/logo_drone_only.png"))

    # Initialize global variables
    CAMERA_NAME = '0'
    IMAGE_TYPE = airsim.ImageType.Scene
    DECODE_EXTENSION = '.png'
    record = True

    # Setup Models 
    # TODO: setup models in separate threads/processes for startup performance
    print("Initializing Models")
    models = []
    models.append((setupViltTransformer()))
    models.append((setupLxmertTransformer()))
    print("Model's Initialized")

    VQAScreen = VQAInteractionScreen(threadManager, controller, models)
    launchScreen = LaunchScreen(stackedWidget, threadManager, VQAScreen, controller)
    
    stackedWidget.addWidget(launchScreen)
    stackedWidget.addWidget(VQAScreen)
    stackedWidget.setCurrentWidget(launchScreen)

    stackedWidget.show()

    sys.exit(app.exec())

# This Python file uses the following encoding: utf-8
from pathlib import Path
import sys
import os

from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThreadPool
from LoadScreen import LoadScreen

def ImportGlobalModules(loadScreen):
    loadScreen.updateLoadStatus(percentComplete=5, statusText="Importing AirSim")
    global airsim
    import airsim

    loadScreen.updateLoadStatus(percentComplete=15, statusText="Importing LaunchScreen")
    global LaunchScreen
    from LaunchScreen import LaunchScreen

    loadScreen.updateLoadStatus(percentComplete=20, statusText="Importing VQAInteractionScreen")
    global VQAInteractionScreen
    from VQAInteractionScreen import VQAInteractionScreen

    loadScreen.updateLoadStatus(percentComplete=30, statusText="Importing AirSimControl")
    global AirSimControl
    from AirSimControl import AirSimControl

    loadScreen.updateLoadStatus(percentComplete=40, statusText="Importing setupViltTransformer")
    global setupViltTransformer
    from utils import setupViltTransformer

    loadScreen.updateLoadStatus(percentComplete=50, statusText="Importing setupLxmertTransformer")
    global setupLxmertTransformer
    from utils import setupLxmertTransformer


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stackedWidget = QStackedWidget()
    stackedWidget.resize(500, 500)
    stackedWidget.setWindowTitle("DroneVQA")
    stackedWidget.setWindowIcon(QIcon("Images/Logos/logo_drone_only.png"))


    # Display the load screen until the initialization processes are done
    loadScreen = LoadScreen(app, stackedWidget)
    stackedWidget.addWidget(loadScreen)
    stackedWidget.setCurrentWidget(loadScreen)
    stackedWidget.resize(600,600)
    stackedWidget.show()

    # Update App To Display Loading Screen
    app.processEvents()

    # Import modules while the loading screen  is displaying
    ImportGlobalModules(loadScreen)

    loadScreen.updateLoadStatus(percentComplete=55, statusText="Initializing AirSimControl")
    controller = AirSimControl()

    loadScreen.updateLoadStatus(percentComplete=60, statusText="Initializing QThreadPool")
    threadManager = QThreadPool()

    # Initialize global variables
    loadScreen.updateLoadStatus(percentComplete=65, statusText="Initializing global camera variables")
    CAMERA_NAME = '0'
    IMAGE_TYPE = airsim.ImageType.Scene
    DECODE_EXTENSION = '.png'
    record = True

    # Setup Models 
    loadScreen.updateLoadStatus(percentComplete=65, statusText="Beginning to set up models...")
    models = []
    loadScreen.updateLoadStatus(percentComplete=60, statusText="Initializing Vilt model\nThis step will take longer the first time this application loads.")
    models.append((setupViltTransformer()))
    loadScreen.updateLoadStatus(percentComplete=80, statusText="Initializing LxMERT model\nThis step will take longer the first time this application loads.")
    models.append((setupLxmertTransformer()))
    loadScreen.updateLoadStatus(percentComplete=95, statusText="Switching to launch screen...")

    # Switch to the launch screen
    VQAScreen = VQAInteractionScreen(threadManager, controller, models)
    launchScreen = LaunchScreen(stackedWidget, threadManager, VQAScreen, controller)
    stackedWidget.addWidget(launchScreen)
    stackedWidget.addWidget(VQAScreen)
    stackedWidget.resize(500, 625)
    stackedWidget.setCurrentWidget(launchScreen)

    sys.exit(app.exec())


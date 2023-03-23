# This Python file uses the following encoding: utf-8
from pathlib import Path
import sys
import os
import time

from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThreadPool
from LoadScreen import LoadScreen
from app_setup_worker import App_Setup_Worker

# Global Variable Setup
app = None
threadManager = None
stackedWidget = None
loadScreen = None

def ImportGlobalModules():
    global airsim
    import airsim

def setupModels(progress_callback):
    progress_callback.emit((1, "Importing LaunchScreen"))
    global LaunchScreen
    from LaunchScreen import LaunchScreen

    progress_callback.emit((5, "Importing VQAInteractionScreen"))
    global VQAInteractionScreen
    from VQAInteractionScreen import VQAInteractionScreen

    progress_callback.emit((10, "Initializing AirSim Controller"))
    time.sleep(1)

    global AirSimControl
    from AirSimControl import AirSimControl

    airsim_controller = AirSimControl()

    progress_callback.emit((15, "Importing Model Setup"))
    time.sleep(1)

    global setupViltTransformer
    from ModelPredictionUtils import setupViltTransformer
    
    global setupFineViltTransformer
    from ModelPredictionUtils import setupFineViltTransformer

    global setupLxmertTransformer
    from ModelPredictionUtils import setupLxmertTransformer

    global setupLxmertTransformer_finetuned
    from ModelPredictionUtils import setupLxmertTransformer_finetuned

    models = []
    progress_callback.emit((25, "Initializing Vilt model\nThis step will take longer the first time this application loads."))
    models.append((setupViltTransformer()))

    progress_callback.emit((40, "Initializing fine-tuned Vilt model\nThis step will take longer the first time this application loads."))
    models.append((setupFineViltTransformer()))

    progress_callback.emit((60, "Initializing base LxMERT model\nThis step will take longer the first time this application loads."))
    models.append((setupLxmertTransformer()))

    progress_callback.emit((80, "Initializing fine-tuned LxMERT model\nThis step will take longer the first time this application loads."))
    models.append((setupLxmertTransformer_finetuned()))

    progress_callback.emit((100, "Switching to launch screen..."))
    time.sleep(1)
    return [VQAInteractionScreen, LaunchScreen, airsim_controller, models]

def switchToLaunchScreen(threadManager, stackedWidget, VQAInteractionScreen, LaunchScreen, controller, final_models):
    # Switch to the launch screen
    VQAScreen = VQAInteractionScreen(threadManager, controller, final_models)
    launchScreen = LaunchScreen(app, stackedWidget, threadManager, VQAScreen, controller)
    stackedWidget.addWidget(launchScreen)
    stackedWidget.addWidget(VQAScreen)
    stackedWidget.resize(500, 625)
    stackedWidget.setCurrentWidget(launchScreen)

def finalizeModels(setupResults):
    switchToLaunchScreen(threadManager, stackedWidget, setupResults[0], setupResults[1], setupResults[2], setupResults[3])

def updateLoadScreenProgress(percentComplete):
    loadScreen.updateLoadStatus(percentComplete=percentComplete[0], statusText=percentComplete[1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    threadManager = QThreadPool()

    stackedWidget = QStackedWidget()
    stackedWidget.resize(500, 500)
    stackedWidget.setWindowTitle("DroneVQA")
    stackedWidget.setWindowIcon(QIcon("Images/Logos/logo_drone_only.png"))

    # Display the load screen until the initialization processes are done
    loadScreen = LoadScreen(stackedWidget)
    stackedWidget.addWidget(loadScreen)
    stackedWidget.setCurrentWidget(loadScreen)
    stackedWidget.resize(600,600)
    stackedWidget.show()

    # Start loading screen process and update App
    loadScreen.updateLoadStatus(percentComplete=0, statusText="Starting Application")
    app.processEvents()

    # Import modules while the loading screen is displaying
    ImportGlobalModules()


    # Initialize global variables
    CAMERA_NAME = '0'
    IMAGE_TYPE = airsim.ImageType.Scene
    DECODE_EXTENSION = '.png'
    record = True

    # Update App with modules after initialization
    app.processEvents()

    # Setup Models 
    worker = App_Setup_Worker(setupModels)
    worker.signals.result.connect(finalizeModels)
    worker.signals.progress.connect(updateLoadScreenProgress)
    threadManager.start(worker)

    sys.exit(app.exec())


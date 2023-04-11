# This Python file uses the following encoding: utf-8
from pathlib import Path

import sys
import airsim
import cv2
import numpy as np

from PySide6.QtWidgets import QWidget, QRadioButton, QLabel, QToolBar
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader

import random
import time
import os
from threading import Timer, main_thread

from docx import Document
from docx.shared import Inches, Pt

from worker import Worker
from ModelPredictionUtils import PredictionResults, predictVilt, predictLxmert

from ExportUtils import ExportUtils
from video_stream_worker import Video_Stream_Worker

class VQAInteractionScreen(QWidget):
    def __init__(self, threadManager, controller, models, parent=None):
        super().__init__(parent)
        self.threadManager = threadManager
        self.controller = controller
        self.models = models
        self.currentImage = None
        self.predictionResult = None
        self.current_model_details = ""
        self.visuals = []
        self.cameraEffect = "None"
        # Position in array corresponds to airsim command value
        # Rain: 0, Road Wetness: 1, Snow: 2, Road Snow: 3
        # Maple Leaves: 4, Road Leaves (Unused): 5,
        # Dust: 6, Fog: 7
        self.weatherEffects = [ ["Rain", 0.0], ["Road Wetness", 0.0],
                                ["Snow", 0.0], ["Road Snow", 0.0], 
                                ["Maple Leaves", 0.0], ["Road Leaves", 0.0], 
                                ["Dust", 0.0], ["Fog", 0.0]
                            ]
        self.ExportResults = ExportUtils()
        # Values for controlling video feed
        self.run_video_stream = True
        self.pause_video_stream = False
        self.load_ui()
      
    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "VQAInteractionScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Create movement button array for enabling/disabling if necessary
        moveButtons = [self.ui.button_Up, self.ui.button_Down, self.ui.button_Left, self.ui.button_Right, self.ui.button_Forward, self.ui.button_Backward, self.ui.button_rotate_right, self.ui.button_rotate_left]

        # Connect drone navigation button actions to methods
        self.ui.button_Up.pressed.connect(lambda: self.controller.startDroneMovement("up"))
        self.ui.button_Down.pressed.connect(lambda: self.controller.startDroneMovement("down"))
        self.ui.button_Left.pressed.connect(lambda: self.controller.startDroneMovement("left"))
        self.ui.button_Right.pressed.connect(lambda: self.controller.startDroneMovement("right"))
        self.ui.button_Forward.pressed.connect(lambda: self.controller.startDroneMovement("forward"))
        self.ui.button_Backward.pressed.connect(lambda: self.controller.startDroneMovement("backward"))
        self.ui.button_rotate_right.pressed.connect(lambda: self.controller.startDroneMovement("rotate_right"))
        self.ui.button_rotate_left.pressed.connect(lambda: self.controller.startDroneMovement("rotate_left"))

        self.ui.button_Up.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Down.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Left.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Right.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Forward.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Backward.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_rotate_right.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_rotate_left.released.connect(lambda: self.controller.stopDroneMovement)

        # Camera setting combo box drop-down value changed (camera view and type fields) to methods
        self.ui.comboBox_CameraView.currentIndexChanged.connect(lambda: self.controller.setCameraView(self.ui.comboBox_CameraView.currentIndex()))

        # Connect weather and environment sliders to methods
        self.ui.horizontalSlider_Rain.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Rain, self.ui.label_RainVal, self.ui.horizontalSlider_Rain.value()))
        self.ui.horizontalSlider_Snow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Snow, self.ui.label_SnowVal, self.ui.horizontalSlider_Snow.value()))
        self.ui.horizontalSlider_Dust.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Dust, self.ui.label_DustVal, self.ui.horizontalSlider_Dust.value()))
        self.ui.horizontalSlider_Fog.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Fog, self.ui.label_FogVal, self.ui.horizontalSlider_Fog.value()))
        self.ui.horizontalSlider_RoadWetness.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Roadwetness, self.ui.label_RoadWetnessVal, self.ui.horizontalSlider_RoadWetness.value()))
        self.ui.horizontalSlider_RoadSnow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.RoadSnow, self.ui.label_RoadSnowVal, self.ui.horizontalSlider_RoadSnow.value()))
        self.ui.horizontalSlider_MapleLeaves.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.MapleLeaf, self.ui.label_MapleLeavesVal, self.ui.horizontalSlider_MapleLeaves.value()))

        self.ui.horizontalSlider_MovementVelocity.valueChanged.connect(self.changeMovementVelocity)

        self.ui.comboBox_Visualizations.currentTextChanged.connect(lambda: self.displayVisualization(self.ui.comboBox_Visualizations.currentIndex()))

        self.ui.pushButton_ViewExpandedVisualization.clicked.connect(lambda: self.displayExpandedVisualization(self.ui.comboBox_Visualizations.currentIndex()))

        # Re-initialize AirSim client
        self.ui.pushButton_RestartAirSimClient.clicked.connect(self.controller.initializeAirSimClient)

        # Reset Drone Location Button
        self.ui.button_ResetDrone.clicked.connect(self.controller.resetDrone)

        # Reset Camera Button
        self.ui.pushButton_RestartCamera.clicked.connect(self.restartCamera)

        # Freeze Frame Button Clicked
        self.ui.pushButton_FreezeUnfreezeFrame.clicked.connect(self.freezeUnfreezeCamera)

        # Take a Snapshot Button Clicked
        self.ui.pushButton_TakeASnapshot.clicked.connect(lambda: self.ExportResults.takeSnapshot(self.ui.pushButton_TakeASnapshot, self.currentImage))

        # Ask Question Button
        self.ui.pushButton_Ask.clicked.connect(self.askQuestion)
        self.ui.lineEdit_Question.returnPressed.connect(self.askQuestion)

    def changeWeather(self, command, valLabel, sliderVal):
        '''Updates the lcd number next to slider and passes updated weather values to air sim control'''
        valLabel.setText(str(sliderVal))

        self.weatherEffects[command][1] = sliderVal

        # Convert slider value from [0-100] to [0.00-1.00] range equivalent & pass to AirSim controller
        decSliderVal = sliderVal / 100
        self.controller.updateAirSimWeather(command, decSliderVal)

    def changeMovementVelocity(self, value):
        '''Sets the AirSim controller's movementVelocity variable based on the GUI slider value (horizontalSlider_MovementVelocity)'''
        self.controller.movementVelocity = self.ui.horizontalSlider_MovementVelocity.value()

    def setupCamera(self):
        """
        Initialize camera.
        """
        self.run_video_stream = True
        self.threadCamera()
            
    def threadCamera(self):
        """
        Thread camera to free main thread for increased GUI performance
        Camera thread ends on exiting main thread through exception
        """
        # Setup long running thread to display image stream
        video_stream_worker = Video_Stream_Worker(self.get_video_stream)

        # Use progress callback to send image to main thread
        video_stream_worker.signals.progress.connect(self.display_video_stream)

        # When 'Restart Camera' button is pressed
        # exit current thread and automatically create new thread
        video_stream_worker.signals.finished.connect(self.setupCamera)

        self.threadManager.start(video_stream_worker)

    def restartCamera(self):
        # Stop video stream loop ending camera thread
        self.run_video_stream = False

    def get_video_stream(self, progress_callback):
        """
        Get frame from AirSim controller, apply camera effects, and resize for displaying
        Send frame back to main thread through progress callback
        """
        while(self.run_video_stream):
            # Exit from thread if main thread is terminated
            if (not main_thread().is_alive()):
                sys.exit()
                
            while(not self.pause_video_stream and self.run_video_stream):
                # Exit from thread if main thread is terminated
                if (not main_thread().is_alive()):
                    sys.exit()
                
                # Get frame from AirSim
                response_image = self.controller.getCurrentDroneImage()

                np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
                frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)        
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Get user-selected camera effect text
                self.cameraEffect = str(self.ui.comboBox_CameraEffect.currentText())

                # Apply effect to the frame, if applicable. "None" selection has no effect.
                if (self.cameraEffect == "Black Screen"):
                    frame[frame != 0] = 0
                elif (self.cameraEffect == "Lens Blur"):
                    frame = cv2.GaussianBlur(frame, (15,15), cv2.BORDER_DEFAULT)
                elif (self.cameraEffect == "Pixel Corruption"):
                    frame_dim = frame.shape
                    for i in range(1000):
                        frame[random.randint(0, frame_dim[0] - 1), random.randint(0, frame_dim[1] - 1)] = 0

                self.currentImage = frame
                
                # Resize Image for Display
                dim = (self.ui.label_CameraFeed.width(),self.ui.label_CameraFeed.height())
                frame = cv2.resize(frame, dim)
                
                # Return current frame back to main
                progress_callback.emit(frame)

            # Return paused status back to main
            progress_callback.emit("Video Stream Paused.")
       
    def display_video_stream(self, frame):
        # Check if the video stream is paused
        if (frame == "Video Stream Paused."):
            return
        
        # Set global current image to be used as VQA image
        self.currentImage = frame

        # Display Image by repainting QLabel widget
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format_RGB888)
        self.ui.label_CameraFeed.setPixmap(QPixmap.fromImage(image))

    def freezeUnfreezeCamera(self):
        if self.ui.pushButton_FreezeUnfreezeFrame.isChecked():
            self.pause_video_stream = True
            self.ui.pushButton_FreezeUnfreezeFrame.setText("Unfreeze Frame")
        else:
            self.pause_video_stream = False
            self.ui.pushButton_FreezeUnfreezeFrame.setText("Freeze Frame")
    
    def askQuestion(self):
        # Hide any existing displayed visualization
        self.ui.label_ResultVisualization.hide()

        # Remove previous results
        self.ui.lineEdit_Answer.setText("")
        self.ui.textEdit_Details.setText("")

        # Disable question asking options while model is running
        self.ui.radioButton_ViltFineTuned.setEnabled(False)
        self.ui.radioButton_ViltBase.setEnabled(False)
        self.ui.radioButton_LxmertFineTuned.setEnabled(False)
        self.ui.radioButton_LxmertBase.setEnabled(False)
        self.ui.lineEdit_Question.setEnabled(False)
        self.ui.checkBox_ExportResults.setEnabled(False)

        # Change text/color/state of ask button to reflect that a model is running and results are loading
        self.ui.pushButton_Ask.setEnabled(False)
        self.ui.pushButton_Ask.setText("Loading...")
        self.ui.pushButton_Ask.setStyleSheet("* { background-color: DarkSalmon; color: black; }\n\nQPushButton {\nborder-radius: 4px;\npadding: 4px 0;\n}")

        # Obtain the desired model for prediction
        question = self.ui.lineEdit_Question.text()
        image = self.currentImage.copy()

        model_index = 0
        # ViLT (Base) Model
        if self.ui.radioButton_ViltBase.isChecked():
            model_index = 0
            model = self.models[model_index]
            worker = Worker(predictVilt, model[0], model[1], question, image) 
       #Fine Tuned ViLT
        elif self.ui.radioButton_ViltFineTuned.isChecked():
            model_index = 1
            model = self.models[model_index]
            worker = Worker(predictVilt, model[0], model[1], question, image) 
        # LXMERT (Base) Model
        elif self.ui.radioButton_LxmertBase.isChecked():
            model_index = 2
            model = self.models[model_index]
            worker = Worker(predictLxmert, model[0], model[1], model[2], model[3], model[4], question, image)
        #Fine Tuned LXMERT
        elif self.ui.radioButton_LxmertFineTuned.isChecked():
            model_index = 3
            model = self.models[model_index]
            worker = Worker(predictLxmert, model[0], model[1], model[2], model[3], model[4], question, image)

        def completed():
            # Enable question asking options now that model is complete
            self.ui.radioButton_ViltFineTuned.setEnabled(True)
            self.ui.radioButton_ViltBase.setEnabled(True)
            self.ui.radioButton_LxmertFineTuned.setEnabled(True)
            self.ui.radioButton_LxmertBase.setEnabled(True)
            self.ui.lineEdit_Question.setEnabled(True)
            self.ui.checkBox_ExportResults.setEnabled(True)

            # Set ask button active and change text/color back to user ask prompt
            self.ui.pushButton_Ask.setEnabled(True)
            self.ui.pushButton_Ask.setText("Ask")
            self.ui.pushButton_Ask.setStyleSheet("* { background-color: lightgrey; color: black; }\n\nQPushButton {\nborder-radius: 4px;\npadding: 4px 0;\n}")

        worker.signals.result.connect(self.showResults)
        worker.signals.finished.connect(completed)
        #worker.signals.progress.connect(self.progress_fn)

        self.threadManager.start(worker)

    def displayVisualization(self, imageIndex):
        """
        Sets the visualization image in the 'Model Visualization' area
        """

        # Get visualization based on index
        image = self.predictionResult.visualizations[imageIndex]

        # Resize Image for Display
        dim = (self.ui.label_ResultVisualization.width(),self.ui.label_ResultVisualization.height())
        frame = cv2.resize(image, dim)

        # Display Image
        image = QImage(frame, frame.shape[1], frame.shape[0],
                    frame.strides[0], QImage.Format_RGB888)
        self.ui.label_ResultVisualization.setPixmap(QPixmap.fromImage(image))
        self.ui.label_ResultVisualization.hide()
        self.ui.label_ResultVisualization.show()

    def displayExpandedVisualization(self, imageIndex):
        """
        Launches a separate window with a larger version of the selected visualization
        """

        # Get visualization based on index
        image = self.predictionResult.visualizations[imageIndex]

        # Set pixel expansion factor
        pixelExpansion = 600

        # Set the expansion size to the current pixel dimensions + the pixel expansion factor (retains current aspect ratio)
        dim = (self.ui.label_ResultVisualization.width()+pixelExpansion,self.ui.label_ResultVisualization.height()+pixelExpansion)
        frame = cv2.resize(image, dim)

        # Display Image
        self.miniWindow = QLabel("Expanded Visualization")
        image = QImage(frame, frame.shape[1], frame.shape[0],
                    frame.strides[0], QImage.Format_RGB888)
        self.miniWindow.setPixmap(QPixmap.fromImage(image))

        self.miniWindow.show()



    def showResults(self, results: PredictionResults):
        # Store prediction results (for showing more visualization images later)
        self.predictionResult = results

        self.ui.lineEdit_Answer.clear()
        self.ui.lineEdit_Answer.setText(results.prediction)

        # Show top predictions
        detailsBox = self.ui.textEdit_Details
        detailsBox.clear()
        details = []
        self.current_model_details = ""
        for prediction, prob in results.top_predictions:
            details.append(f"{prediction}\t{prob:.5f}\n")
        self.current_model_details = "".join(details)
        detailsBox.setText(self.current_model_details)

        # Clear the old visualization dropdown options
        self.ui.comboBox_Visualizations.clear()

        # Show the new visualization options in the dropdown box
        numVisuals = len(self.predictionResult.visualizations)

        if numVisuals:
            for i in range(numVisuals):
                # Note: The visualization names list is the same length as the visualization list
                self.ui.comboBox_Visualizations.addItem(f"{self.predictionResult.visualization_names[i]}")

            # Show the 1st vizualization as a default
            defaultImageIndex = 0
            self.ui.comboBox_Visualizations.setCurrentIndex(defaultImageIndex);
            self.displayVisualization(defaultImageIndex)
        
        if (self.ui.checkBox_ExportResults.isChecked()):
            self.ExportResults.exportResults(self.predictionResult, self.current_model_details, 
                                             self.cameraEffect, self.weatherEffects, 
                                             self.ui.checkBox_ExportResults)

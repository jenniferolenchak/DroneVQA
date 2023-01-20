
# This Python file uses the following encoding: utf-8
from pathlib import Path

import airsim
import cv2
import numpy as np

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader

import random

from worker import Worker
from utils import PredictionResults, predictVilt, predictLxmert

class VQAInteractionScreen(QWidget):
    def __init__(self, threadManager, controller, models, parent=None):
        super().__init__(parent)
        self.threadManager = threadManager
        self.controller = controller
        self.models = models
        self.currentImage = None
        self.predictionResult = None
        self.load_ui()
      
    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "VQAInteractionScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Connect drone navigation button actions to methods
        self.ui.button_Up.pressed.connect(lambda: self.controller.startDroneMovement("up"))
        self.ui.button_Down.pressed.connect(lambda: self.controller.startDroneMovement("down"))
        self.ui.button_Left.pressed.connect(lambda: self.controller.startDroneMovement("left"))
        self.ui.button_Right.pressed.connect(lambda: self.controller.startDroneMovement("right"))
        self.ui.button_Forward.pressed.connect(lambda: self.controller.startDroneMovement("forward"))
        self.ui.button_Backward.pressed.connect(lambda: self.controller.startDroneMovement("backward"))
        self.ui.button_Up.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Down.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Left.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Right.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Forward.released.connect(lambda: self.controller.stopDroneMovement)
        self.ui.button_Backward.released.connect(lambda: self.controller.stopDroneMovement)

        # Connect weather and environment sliders to methods
        self.ui.horizontalSlider_Rain.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Rain, self.ui.lcdNumber_Rain, self.ui.horizontalSlider_Rain.value()))
        self.ui.horizontalSlider_Snow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Snow, self.ui.lcdNumber_Snow, self.ui.horizontalSlider_Snow.value()))
        self.ui.horizontalSlider_Dust.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Dust, self.ui.lcdNumber_Dust, self.ui.horizontalSlider_Dust.value()))
        self.ui.horizontalSlider_Fog.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Fog, self.ui.lcdNumber_Fog, self.ui.horizontalSlider_Fog.value()))
        self.ui.horizontalSlider_RoadWetness.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.Roadwetness, self.ui.lcdNumber_RoadWetness, self.ui.horizontalSlider_RoadWetness.value()))
        self.ui.horizontalSlider_RoadSnow.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.RoadSnow, self.ui.lcdNumber_RoadSnow, self.ui.horizontalSlider_RoadSnow.value()))
        self.ui.horizontalSlider_MapleLeaves.valueChanged.connect(lambda: self.changeWeather(airsim.WeatherParameter.MapleLeaf, self.ui.lcdNumber_MapleLeaves, self.ui.horizontalSlider_MapleLeaves.value()))

        self.ui.horizontalSlider_MovementVelocity.valueChanged.connect(self.changeMovementVelocity)

        # Connect reset button to action method
        self.ui.button_ResetDrone.clicked.connect(self.controller.resetDrone)

        # Start Camera Button
        self.ui.pushButton_StartCamera.clicked.connect(self.setupCamera)

        # Freeze Frame Button Clicked
        self.ui.pushButton_FreezeFrame.clicked.connect(self.freezeCamera)

        # Ask Question Button
        self.ui.pushButton_Ask.clicked.connect(self.askQuestion)

    def changeWeather(self, command, lcd, sliderVal):
        '''Updates the lcd number next to slider and passes updated weather values to air sim control'''
        lcd.display(sliderVal)

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
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(100)

    def display_video_stream(self):
        """
        Read frame from camera and repaint QLabel widget.
        """
        # Get Feed From AirSim
        response_image = self.controller.getCurrentDroneImage()

        


        np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
        frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # TODO: Add in the camera effects...
        if (self.ui.radioButton_BlackScreen.isChecked()):
            frame[frame != 0] = 0;
        
        if (self.ui.radioButton_LensBlur.isChecked()):
            frame = cv2.GaussianBlur(frame, (5,5), 10.0)

        if (self.ui.radioButton_PixelCorruption.isChecked()):
            frame_dim = frame.shape
            for i in range(1000):
                frame[random.randint(0, frame_dim[0] - 1), random.randint(0, frame_dim[1] - 1)] = 0
            
        self.currentImage = frame
        
        # Resize Image for Display
        dim = (self.ui.label_CameraFeed.width(),self.ui.label_CameraFeed.height())
        frame = cv2.resize(frame, dim)

        # Display Image
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format_RGB888)
        self.ui.label_CameraFeed.setPixmap(QPixmap.fromImage(image))

    def freezeCamera(self):
        self.timer.stop()

    def askQuestion(self):
        # Obtain the desired model for prediction
        question = self.ui.lineEdit_Question.text()
        image = self.currentImage.copy()

        model_index = 0
        # ViLT Model
        if self.ui.radioButton_Model1.isChecked():
            model_index = 0
            model = self.models[model_index]
            worker = Worker(predictVilt, model[0], model[1], question, image) 
        # LXMERT
        elif self.ui.radioButton_Model2.isChecked():
            model_index = 1
            model = self.models[model_index]
            worker = Worker(predictLxmert, model[0], model[1], model[2], model[3], model[4], question, image)
        elif self.ui.radioButton_Model3.isChecked():
            model_index = 2
        elif self.ui.radioButton_Model4.isChecked():
            model_index = 3

        def completed():
            print(f"Completed Prediction")

        worker.signals.result.connect(self.showResults)
        worker.signals.finished.connect(completed)
        #worker.signals.progress.connect(self.progress_fn)

        self.threadManager.start(worker)

    def showResults(self, results: PredictionResults):
        # Store prediction results (for showing more visualization images later)
        self.predictionResult = results

        self.ui.lineEdit_Answer.clear()
        self.ui.lineEdit_Answer.setText(results.prediction)

        # Show top predictions
        detailsBox = self.ui.textEdit_Details
        detailsBox.clear()
        details = []
        for prediction, prob in results.top_predictions:
            details.append(f"{prediction}\t{prob:.5f}\n")
        detailsBox.setText("".join(details))

        # Show the first visualization on screen
        if len(results.visualizations):

            # Set visualization radio box
            self.ui.radioButton_Visualization1.click()

            # Resize Image for Display
            dim = (self.ui.label_ResultVisualization.width(),self.ui.label_ResultVisualization.height())
            frame = cv2.resize(results.visualizations[0], dim)

            # Display Image
            image = QImage(frame, frame.shape[1], frame.shape[0], 
                        frame.strides[0], QImage.Format_RGB888)
            self.ui.label_ResultVisualization.setPixmap(QPixmap.fromImage(image))
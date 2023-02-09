# This Python file uses the following encoding: utf-8
from pathlib import Path

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
from threading import Timer

from docx import Document
from docx.shared import Inches, Pt

from worker import Worker
from utils import PredictionResults, predictVilt, predictLxmert

class VQAInteractionScreen(QWidget):
    def __init__(self, threadManager, controller, models, parent=None):
        super().__init__(parent)
        self.threadManager = threadManager
        self.controller = controller
        self.models = models
        self.currentImage = None
        self.currentQuestion = ""
        self.currentModelImage = None
        self.predictionResult = None
        self.exported_dir = "Exports and Snapshots/"
        self.snapshot_dir = "Exports and Snapshots/Snapshots/"
        self.model_dir = "Exports and Snapshots/Model Results/"
        self.current_doc_name = ""
        self.current_model_details = ""
        self.visuals = []
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
        self.ui.pushButton_RestartCamera.clicked.connect(self.setupCamera)

        # Freeze Frame Button Clicked
        self.ui.pushButton_FreezeUnfreezeFrame.clicked.connect(self.freezeUnfreezeCamera)

        # Take a Snapshot Button Clicked
        self.ui.pushButton_TakeASnapshot.clicked.connect(self.takeSnapshot)

        # Ask Question Button
        self.ui.pushButton_Ask.clicked.connect(self.askQuestion)

    def changeWeather(self, command, valLabel, sliderVal):
        '''Updates the lcd number next to slider and passes updated weather values to air sim control'''
        valLabel.setText(str(sliderVal))

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

    def freezeUnfreezeCamera(self):
        if self.ui.pushButton_FreezeUnfreezeFrame.isChecked():
            self.timer.stop()
            self.ui.pushButton_FreezeUnfreezeFrame.setText("Unfreeze Frame")
        else:
            self.timer.start(100)
            self.ui.pushButton_FreezeUnfreezeFrame.setText("Freeze Frame")
    
    def getCurrentFormattedTime(self): 
        current_time = time.localtime()
        formatted_time = time.strftime("%b-%d-%H-%M-%S", current_time)
        return formatted_time

    def checkExportDir(self):
        try:
            if (not os.path.exists(self.exported_dir)):
                os.mkdir(self.exported_dir)
            
            if (not os.path.exists(self.snapshot_dir)):
                os.mkdir(self.snapshot_dir)
            
            if (not os.path.exists(self.model_dir)):
                os.mkdir(self.model_dir)
            
            return True
        except:
            return False


    def takeSnapshot(self):
        self.ui.pushButton_TakeASnapshot.setText("Capturing")
        self.ui.pushButton_TakeASnapshot.setEnabled(False)

        formatted_time = self.getCurrentFormattedTime()
        filename = formatted_time + ".png"
        
        if (not self.checkExportDir()):
            print("Could not save snapshot")
            return
        
        try: 
            cv2.imwrite(self.snapshot_dir + filename, cv2.cvtColor(self.currentImage, cv2.COLOR_RGB2BGR))
            print("Snapshot saved to: " + self.snapshot_dir + filename)

            self.ui.pushButton_TakeASnapshot.setText("Captured")
            Timer(2, self.resetTakeSnapshot).start()
        except:
            print("Could not save snapshot")
        
    
    def resetTakeSnapshot(self):
        self.ui.pushButton_TakeASnapshot.setText("Take a Snapshot")
        self.ui.pushButton_TakeASnapshot.setEnabled(True)


    def askQuestion(self):
        # Hide any existing displayed visualization
        self.ui.label_ResultVisualization.hide()

        # Set ask button inactive and change text/color to loading while the model is running
        self.ui.pushButton_Ask.setEnabled(False)
        self.ui.pushButton_Ask.setText("Loading...")
        self.ui.pushButton_Ask.setStyleSheet("* { background-color: DarkSalmon; color: black; }\n\nQPushButton {\nborder-radius: 4px;\npadding: 4px 0;\n}")

        # Obtain the desired model for prediction
        question = self.ui.lineEdit_Question.text()
        self.currentQuestion = question
        image = self.currentImage.copy()
        self.currentModelImage = image

        model_index = 0
        # ViLT (Base) Model
        if self.ui.radioButton_ViltBase.isChecked():
            model_index = 0
            model = self.models[model_index]
            worker = Worker(predictVilt, model[0], model[1], question, image) 
        # LXMERT (Base) Model
        elif self.ui.radioButton_LxmertBase.isChecked():
            model_index = 1
            model = self.models[model_index]
            worker = Worker(predictLxmert, model[0], model[1], model[2], model[3], model[4], question, image)

        def completed():
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
                self.ui.comboBox_Visualizations.addItem(f"Visualization {i+1}")

            # Show the 1st vizualization as a default
            defaultImageIndex = 0
            self.ui.comboBox_Visualizations.setCurrentIndex(defaultImageIndex);
            self.displayVisualization(defaultImageIndex)
        
        if (self.ui.checkBox_ExportResults.isChecked()):
            self.exportResults()

    def resetExportText(self):
        self.ui.checkBox_ExportResults.setText("Export Results")

    def exportResults(self):

            if (not self.checkExportDir()):
                print("Could not save snapshot")
                return

            try: 
                document = Document()
                formatted_time = self.getCurrentFormattedTime()

                result_dir = self.model_dir + formatted_time + "/"

                os.mkdir(result_dir)

                self.current_doc_name = self.model_dir + formatted_time + "/Results_" + formatted_time + ".docx"

                document.add_heading("Question and Model Prediction")

                question_paragraph = document.add_paragraph()
                question_format = question_paragraph.paragraph_format
                question_format.left_indent = Inches(0.5)

                question_run = question_paragraph.add_run("Question Asked: " + self.currentQuestion)
                question_font = question_run.font
                question_font.name = 'Calibri'
                question_font.size = Pt(12)

                answer_paragraph = document.add_paragraph()
                answer_format = answer_paragraph.paragraph_format
                answer_format.left_indent = Inches(0.5)

                answer_run = answer_paragraph.add_run("Prediction: " + self.predictionResult.prediction)
                answer_font = answer_run.font
                answer_font.name = 'Calibri'
                answer_font.size = Pt(12)

                if (self.current_model_details != ""):
                    document.add_heading("Prediction Details")
                    details_paragraph = document.add_paragraph()
                    details_format = details_paragraph.paragraph_format
                    details_format.left_indent = Inches(0.5)

                    details_run = details_paragraph.add_run(self.current_model_details)
                    details_font = details_run.font
                    details_font.name = 'Calibri'
                    details_font.size = Pt(12)

                document.add_heading("Base Image")
                cv2.imwrite(result_dir + "base_image.png", cv2.cvtColor(self.currentModelImage, cv2.COLOR_RGB2BGR))
                document.add_picture(result_dir + "base_image.png", width=Inches(6.0))

                numVisuals = len(self.predictionResult.visualizations)
                if numVisuals:
                    document.add_heading("Model Visualizations")
                    # Export each visual
                    for i in range(numVisuals):
                        # Resize Image for Export (uses size from GUI)
                        dim = (self.ui.label_ResultVisualization.width(),self.ui.label_ResultVisualization.height())
                        export_frame = cv2.resize(self.predictionResult.visualizations[i], dim)

                        visual_filename = f"Visualization_{i+1}.png"
                        cv2.imwrite(result_dir + visual_filename, cv2.cvtColor(export_frame, cv2.COLOR_RGB2BGR))
                        
                        document.add_heading(f"Visualization_{i+1}.png", level=2)
                        document.add_picture(result_dir + visual_filename, width=Inches(6.0))
                

                document.save(self.current_doc_name)
                print("results exported to: " + self.current_doc_name)

                self.ui.checkBox_ExportResults.setText("Exported")
                Timer(2, self.resetExportText).start()
            except:
                print("Could not export results")
                self.ui.checkBox_ExportResults.setText("Could Not Export")
                Timer(2, self.resetExportText).start()


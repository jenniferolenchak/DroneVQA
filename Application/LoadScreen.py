# This Python file uses the following encoding: utf-8

import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QScreen
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

class LoadScreen(QWidget):
    def __init__(self, app, stackedWidget, parent=None):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
        self.app = app
        self.load_ui()

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "LoadScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def updateLoadStatus(self, percentComplete, statusText):
        '''Update the progress bar and status message of the loading page'''
        self.ui.progressBar.setValue(percentComplete)
        self.ui.label_StatusText.setText(statusText)
        self.app.processEvents()

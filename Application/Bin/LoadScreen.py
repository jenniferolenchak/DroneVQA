# This Python file uses the following encoding: utf-8

from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QFile


class LoadScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        '''Translate .ui design file to python equivalent and load'''
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "LoadScreen.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def switchVisibleWidget(self, widgetToDisplay):
        '''Initialize VQA interaction screen and set at the active stacked frame'''
        self.stackedWidget.setCurrentWidget(self.widgetToDisplay)

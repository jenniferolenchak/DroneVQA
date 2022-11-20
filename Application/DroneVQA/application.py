# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


class LaunchScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()
        self.ui.button1.clicked.connect(self.navToVQAScreen)

    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "form.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def navToVQAScreen(self):
        widget2 = VQAInteractionScreen()
        stacked.addWidget(widget2)
        stacked.setCurrentWidget(widget2)


class VQAInteractionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()
        self.ui.button1.clicked.connect(self.navToLaunchScreen)

    def load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "second.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def navToLaunchScreen(self):
        stacked.setCurrentWidget(launchScreen)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked = QStackedWidget()
    stacked.setMinimumHeight(500)
    stacked.setMinimumWidth(500)
    stacked.setWindowTitle("DroneVQA")
    stacked.setWindowIcon(QIcon("logo_drone_only.png"))

    launchScreen = LaunchScreen()
    stacked.addWidget(launchScreen)

    stacked.show()

    sys.exit(app.exec())

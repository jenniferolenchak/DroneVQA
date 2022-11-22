import time

from PyQt5.QtCore import pyqtSlot, QThreadPool, QTimer
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QAction,
)
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setFixedSize(500, 500)
        self.setWindowTitle("DroneVQA")

        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.thread_manager = QThreadPool()

        # Add sample button
        self.multiThreadTestButton = QPushButton("Multithread test")
        self.multiThreadTestLabel = QLabel()

        self.layout.addWidget(self.multiThreadTestButton)
        self.layout.addWidget(self.multiThreadTestLabel)

        self.multiThreadTestButton.pressed.connect(self.threadedExitCall)


        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # SET UP MENU BAR:
        # Create new action
        newAction = QAction(QIcon('new.png'), '&New', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.threadedExitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

    def openCall(self):
        print('Open')

    def newCall(self):
        print('New')

    @pyqtSlot()
    def closeWindow(self):
        self.close()

    @pyqtSlot()
    def threadedExitCall(self):
        self.thread_manager.start(self.closeWindow)


if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec()
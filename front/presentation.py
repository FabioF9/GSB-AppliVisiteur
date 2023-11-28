import sys
import typing
import requests
import json
from datetime import date
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow
)

class Screen2(QMainWindow):
    """docstring for Screen2"""
    def __init__(self):
        super().__init__()
        self.tokaccess = ""
        super(Screen2, self).__init__()
        loadUi("test.ui", self)

app = QApplication(sys.argv)

app.setStyleSheet("""
    Qwidget {
                  background-color: "#8797AF";
    }

    QPushButton{
                  background-color: "#7AA095";
                  border-radius: 5px;
    }
    

 """)


widget = QtWidgets.QStackedWidget()
menu = Screen2()
widget.addWidget(menu)

widget.show()
sys.exit(app.exec())
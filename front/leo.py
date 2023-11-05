import sys
import typing
import requests
import json
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Galaxy Swiss Bourdin")
        self.setLayout(layout)
        # Dimensionnez la fenêtre en pixels (largeur, hauteur)
        self.resize(400, 200)

        title = QLabel("Login Form :")
        layout.addWidget(title, 0, 1)

        user = QLabel("Username :")
        layout.addWidget(user, 1, 0)

        pwd = QLabel("Password :")
        layout.addWidget(pwd, 2, 0)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1)

        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1)

        button1 = QPushButton("Login")
        button1.clicked.connect(self.login)
        layout.addWidget(button1, 3, 1)


    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def login(self):
        dico = {
        'snack':'chibre',
        'carton':'papier',
        'fabio':'triplemonstre'
        }

        login   = self.input1.text()
        mdp     = self.input2.text()
        logedin = False

        for user in dico:
            if user == login and mdp == dico[user]:
                logedin = True
                self.gotoscreen2()
                break

        if logedin:
            print('Username & Password are corrects !')
        else:
            print('Username or Password are wrong !')

    # def login(self):
    #     dico = {
    #     'snack':'00',
    #     'carton':'papier'
    #     }

    #     for user in dico:
    #         if user == self.input1.text():
    #             if self.input2.text() == dico[user]:
    #                 print("Username & Password are corrects !");
    #                 break
    #         else:
    #             print("Username or Password are wrong !")
    


class Screen2(QMainWindow):
    """docstring for Screen2"""
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("main.ui", self)
        # fake = ['Dr.chibre','Dr.castor','Dr.carpe','Dr.MacOs']
        # jason = {''}
        x = requests.get('http://127.0.0.1:8000/medecins')
        jason = x.json()
        fake = json.dumps(jason)
        self.List.addItem(fake)
        self.button1.clicked.connect(self.createDr)
    def createDr(self):
        nom   = self.dr_nom.text()
        spe   = self.dr_spe.text()
        ville = self.dr_ville.text()
        x = requests.post(f'http://127.0.0.1:8000/create_medecin', json={
            "nom":nom,
            "spe":spe,
            "ville":ville
            })
        self.List.repaint()

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
login = Window()
menu = Screen2()
widget.addWidget(login)
widget.addWidget(menu)

widget.show()
sys.exit(app.exec())
h
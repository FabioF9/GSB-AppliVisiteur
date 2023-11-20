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
        # self.tokaccess = " test "
        self.access_token = ""
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Galaxy Swiss Bourdin")
        self.setLayout(layout)
        self.access_token = ""
        # Dimensionnez la fenêtre en pixels (largeur, hauteur)
        self.resize(400, 200)

        title = QLabel("Login Form :")
        layout.addWidget(title, 0, 1)

        user = QLabel("Username :")
        layout.addWidget(user, 1, 0)

        pwd = QLabel("Password :")
        layout.addWidget(pwd, 2, 0)

        self.input1 = QLineEdit()
        self.input1.returnPressed.connect(self.login)
        layout.addWidget(self.input1, 1, 1)

        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        self.input2.returnPressed.connect(self.login)
        layout.addWidget(self.input2, 2, 1)

        button1 = QPushButton("Login")
        button1.clicked.connect(self.login)
        layout.addWidget(button1, 3, 1)


    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        # menu.get_token(self.tokaccess)

    def login(self):
        # print(self.tokaccess)

        login   = self.input1.text()
        mdp     = self.input2.text()
        logedin = False

        x = requests.post(f'http://127.0.0.1:8000/login',
        data={
            "grant_type":"",
            "username":login,
            "password":mdp,
            "scope":"",
            "client_id":"",
            "client_secret":""
            })

        if x.status_code==200:
            logedin = True
            # self.tokaccess = x.json().get("access_token")
            # print(self.tokaccess)
            self.gotoscreen2()
        else:
            print('Username or Password are wrong !')    


class Screen2(QMainWindow):
    """docstring for Screen2"""
    def __init__(self, login):
        super().__init__()
        self.tokaccess = ""
        super(Screen2, self).__init__()
        loadUi("main.ui", self)
        # self.access_token = Window.access_token
        # print(self.access_token)
        # headers = {"Authorization": f"Bearer {access_token}"}
        # x = requests.get('http://127.0.0.1:8000/medecins', headers=headers)
        self.set_list()
        self.index_button_create.clicked.connect(self.createDr)
        self.index_button_update.clicked.connect(self.updateDr)
        self.index_button_delete.clicked.connect(self.deleteDr)
        self.index_button_read.clicked.connect(self.gotoCpRendu)
        self.calendar.setGridVisible(True);

    def set_list(self):
        x = requests.get('http://127.0.0.1:8000/medecins')
        jason = x.json()
        fake = json.dumps(jason)
        self.List.clear()
        self.List.setText(fake)  

    def gotoCpRendu(self):
        widget.setCurrentIndex(widget.currentIndex()+1)


    def createDr(self):
        # print(f"Window token = {login.tokaccess}")
        # print(f"Screen 2 token = {self.tokaccess}")
        nom   = self.dr_nom.text()
        spe   = self.dr_spe.text()
        ville = self.dr_ville.text()
        x = requests.post(f'http://127.0.0.1:8000/create_medecin', json={
            "nom":nom,
            "spe":spe,
            "ville":ville
            })
        self.set_list()


    def updateDr(self):
        id_dr = self.dr_id.text()
        nom   = self.dr_nom.text()
        spe   = self.dr_spe.text()
        ville = self.dr_ville.text()
        x = requests.put(f'http://127.0.0.1:8000/update_medecin/{id_dr}', json={
            "nom":nom,
            "spe":spe,
            "ville":ville
            })
        self.set_list()

    def deleteDr(self):
        id_dr = self.dr_id.text()
        x = requests.delete(f'http://127.0.0.1:8000/delete_medecin/{id_dr}')
        self.set_list()




class CpRendu(QMainWindow):
    """docstring for CpRendu"""
    def __init__(self):
        super().__init__()
        self.tokaccess = ""
        super(CpRendu, self).__init__()
        loadUi("CpRendu.ui", self)
        self.insert_medecins()
        self.bouton_retour.clicked.connect(self.retour_acceuil)
        
    def insert_medecins(self):
        x = requests.get('http://127.0.0.1:8000/medecins')
        jason = x.json()
        for i in jason:
            self.CpRendu_medecins.addItem(i['nom'])

    def retour_acceuil(self):
        widget.setCurrentIndex(widget.currentIndex()-1)


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
menu = Screen2(login)
CpRendu = CpRendu()
widget.addWidget(login)
widget.addWidget(menu)
widget.addWidget(CpRendu)

widget.show()
sys.exit(app.exec())
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

class Login_page(QtWidgets.QWidget):
    def __init__(self):
        super(Login_page, self).__init__()
        self.tokaccess = " test "
        self.access_token = ""
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
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
        layout.addWidget(self.input1, 1, 1)

        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1)

        self.button1 = QPushButton("Login")
        layout.addWidget(self.button1, 3, 1)

     def login(self):
        print(self.tokaccess)

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
            self.tokaccess = x.json().get("access_token")
            print(self.tokaccess)
            self.gotoscreen2()
        else:
            print('Username or Password are wrong !')


class Index_page(QtWidgets.QWidget):
    def __init__(self):
        super(Index_page, self).__init__()
        # ...
        self.prevButton = QtWidgets.QPushButton('Previous')
        self.doSomething()

    def doSomething(self):
        ""


    """docstring for Index_page"""
    # def __init__(self):
    #     super(Index_page, self).__init__()

        # self.tokaccess = ""
        # # super(Index_page, self).__init__()
        # loadUi("main.ui", self)
        # self.access_token = Window.access_token
        # print(self.access_token)
        # headers = {"Authorization": f"Bearer {access_token}"}
        # x = requests.get('http://127.0.0.1:8000/medecins', headers=headers)
        # x = requests.get('http://127.0.0.1:8000/medecins')
        # jason = x.json()
        # fake = json.dumps(jason)
        # self.List.addItem(fake)        
        # self.button1.clicked.connect(self.createDr)


class Stack(QtWidgets.QStackedWidget):
    def __init__(self):
        super(Stack, self).__init__()
        self.login = Login_page()
        self.login.button1.clicked.connect(self.goNext)
        self.addWidget(self.login)
        self.currentChanged.connect(self.initCurrent)

    def goNext(self):
        

    def goPrev(self):
        self.set_current_screen()

    def initCurrent():
        if self.currentWidget():
            self.currentWidget().doSomethingNext()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    appStack = Stack()
    appStack.show()
    sys.exit(app.exec())
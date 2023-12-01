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


# Index 0
class Login_page(QtWidgets.QWidget):
    def __init__(self):
        super(Login_page, self).__init__()
        loadUi("new_login.ui", self)
        self.tokaccess = " tokaccess "
        self.access_token = ""
        self.login_button1.clicked.connect(self.login)

    def login(self):
        print(f'le token au début : {self.tokaccess}')

        login   = self.login_input1.text()
        mdp     = self.login_input2.text()
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
            self.tokaccess = x.json()[0]['access_token']
            print(f'le token au apres une réussite : {self.tokaccess}')
            appStack.setCurrentWidget(appStack.index_page)
        else:
            print('Username or Password are wrong !')

    def doSomethingNext(self):
        print("début de l'application")

# Index 1
class Index_page(QtWidgets.QWidget):
    def __init__(self):
        super(Index_page, self).__init__()
        

    def doSomethingNext(self):
        print("mon fiak")


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
        # Index 0
        self.login_page = Login_page()
        # Index 1
        self.index_page = Index_page()
        self.addWidget(self.login_page)
        self.addWidget(self.index_page)
        self.currentChanged.connect(self.initCurrent)

    def goNext(self, target):
        print(target)

    # def goPrev(self):
    #     self.set_current_screen()

    def initCurrent(self):
        if self.currentWidget():
            self.currentWidget().doSomethingNext()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    appStack = Stack()
    appStack.show()
    sys.exit(app.exec())
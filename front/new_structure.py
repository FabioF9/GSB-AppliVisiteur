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

class User():
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.id = user_id

    def getUserDatas(self):
        x.requests.get(f'http://127.0.0.1:8000/user/{self.id}')


# Index 0
class Login_page(QtWidgets.QWidget):
    def __init__(self):
        super(Login_page, self).__init__()
        loadUi("ui/new_login.ui", self)
        self.login_button1.clicked.connect(self.login)

    def login(self):
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
            # appStack.setCurrentWidget(appStack.index_page)
            appStack.launchIndex(self.tokaccess,x.json()[1])
        else:
            print('Username or Password are wrong !')

    def doSomethingNext(self):
        print("début de l'application")

# Index 1
class Index_page(QtWidgets.QWidget):
    def __init__(self):
        super(Index_page, self).__init__()
        loadUi("ui/new_index.ui", self)
        self.index_to_rapport.clicked.connect(self.goToRapport)

    def doSomethingNext(self):
        self.setRapportList()

    def setRapportList(self):
        print( requests.get(f'http://127.0.0.1:8000/rapports').json())
        print( requests.get(f'http://127.0.0.1:8000/rapport/visiteur/1').json())
        # all_rapports = request.json()
        # print(all_rapports)
        # for rapport in all_rapports:
        #     self.index_tableau_rapports.insertRow(self.index_tableau_rapports.rowCount())                
        #     self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 0, QtWidgets.QTableWidgetItem(rapport['RAP_DATE']))
        #     self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 1, QtWidgets.QTableWidgetItem(rapport['RAP_COMMENTAIRE']))
        #     self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 2, QtWidgets.QTableWidgetItem(rapport['RAP_MOTIF']))
        #     self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 3, QtWidgets.QTableWidgetItem(rapport['RAP_BILAN']))
        #     self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 4, QtWidgets.QTableWidgetItem('OWO'))

    def goToRapport(self):
        appStack.setCurrentWidget(appStack.Rapport_page)

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

class Rapport_page(QtWidgets.QWidget):
    def __init__(self):
        super(Index_page, self).__init__()
        loadUi("ui/new_rapport.ui", self)


class Stack(QtWidgets.QStackedWidget):
    def __init__(self):
        super(Stack, self).__init__()
        # Index 0
        self.login_page = Login_page()
        # Index 1
        # self.index_page = Index_page()
        self.addWidget(self.login_page)
        # self.addWidget(self.index_page)
        self.initCurrent()
        self.currentChanged.connect(self.initCurrent)

    def goNext(self, target):
        print(target)

    # def goPrev(self):
    #     self.set_current_screen()

    def initCurrent(self):
        if self.currentWidget():
            self.currentWidget().doSomethingNext()

    def launchIndex(self,access_token,id_user):
        self.user = User(access_token,id_user)
        self.index_page = Index_page()
        # self.rapport_page = Rapport_page()
        self.addWidget(self.index_page)
        # self.addWidget(self.Rapport_page)
        self.setCurrentWidget(self.index_page)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    appStack = Stack()
    appStack.show()
    sys.exit(app.exec())
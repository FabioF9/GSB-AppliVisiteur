import sys
import typing
import requests
import json
from datetime import date
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow, QToolButton
)

class User():
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.id = user_id
        self.headers = {"Authorization": f"Bearer {self.access_token}"} 

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

    def caca(self):
        print("caca")

    def setRapportList(self):
        from pdf.pdf import CreerPresentation
        while self.index_tableau_rapports.rowCount() > 0:
            self.index_tableau_rapports.removeRow(0)
        request = requests.get(f'http://127.0.0.1:8000/rapport/visiteur/{appStack.user.id}',headers=appStack.user.headers)
        all_rapports = request.json()
        print(all_rapports)
        button_dict = {}
        suppr_dict = {}
        for rapport in all_rapports:
            button_dict[f'index_button{rapport["RAP_NUM"]}'] = QPushButton("afficher")
            suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] = QPushButton("supprimer")
            # test_dict[f'index_test{rapport["RAP_NUM"]}'] = QPushButton("supprimer")
            self.index_tableau_rapports.insertRow(self.index_tableau_rapports.rowCount())                
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 0, QtWidgets.QTableWidgetItem(rapport['RAP_DATE']))
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 1, QtWidgets.QTableWidgetItem(rapport['RAP_COMMENTAIRE']))
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 2, QtWidgets.QTableWidgetItem(rapport['RAP_MOTIF']))
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 3, QtWidgets.QTableWidgetItem(rapport['RAP_BILAN']))
            self.index_tableau_rapports.setCellWidget(self.index_tableau_rapports.rowCount()-1, 4, button_dict[f'index_button{rapport["RAP_NUM"]}'])
            self.index_tableau_rapports.setCellWidget(self.index_tableau_rapports.rowCount()-1, 5, suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'])
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 6, QtWidgets.QTableWidgetItem(str(rapport["RAP_NUM"])))
            currentButton = suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] 
            currentButton.clicked.connect(lambda _, id_RAP=rapport["RAP_NUM"]: self.suppr(id_RAP))


            # button_dict[f'index_button{rapport["RAP_NUM"]}'].clicked.connect(CreerPresentation("test","test2"))

        # for boutton in button_dict:
        #     button_dict[boutton].clicked.connect(self.caca)
            # print(boutton)


    def goToRapport(self):
        appStack.setCurrentWidget(appStack.rapport_page)

    def suppr(self,id_RAP):
        # print("test")
        delete_RAP = requests.delete(f'http://127.0.0.1:8000/delete_rapport/{id_RAP}',headers=appStack.user.headers)
        self.setRapportList()



class Rapport_page(QtWidgets.QWidget):
    def __init__(self):
        super(Rapport_page, self).__init__()
        loadUi("ui/new_rapport.ui", self)
        self.rapport_to_index.clicked.connect(self.goToIndex)
        self.rapport_datas.clicked.connect(self.sendRapport)

    def doSomethingNext(self):
        queryMedecins = requests.get("http://127.0.0.1:8000/medecins", headers=appStack.user.headers)
        jsonMedecins = queryMedecins.json()
        for medecin in jsonMedecins:
            self.rapport_medecins.addItem(medecin['MED_NOM']+' '+medecin['MED_PRENOM'],medecin['MED_ID'])

    def goToIndex(self):
        appStack.setCurrentWidget(appStack.index_page)

    def sendRapport(self):
        print(str(self.rapport_medecins.currentText()))
        med_id = self.rapport_medecins.itemData(self.rapport_medecins.currentIndex())
        if self.rapport_motif.currentText() == "Autre":
           motif = self.rapport_motif_autre.text()
           print("le motif actuel : "+self.rapport_motif_autre.text())
        else:
            motif = self.rapport_motif.currentText()
            print("le motif actuel : "+self.rapport_motif.currentText())
        commentaire = self.rapport_comm.toPlainText()
        bilan = self.rapport_bilan.currentText()
        print(commentaire)
        print("la date actuel : "+todayFr)

        create_rapport = requests.post('http://127.0.0.1:8000/create_rapport', json={
            "RAP_DATE":todayFr,
            "RAP_BILAN":bilan,
            "RAP_MOTIF":motif,
            "RAP_COMMENTAIRE":commentaire,
            "MED_ID": med_id,
            "VIS_MATRICULE": appStack.user.id
            },headers=appStack.user.headers)     

        print("fnct sendRapport")


    # def test(self):
    #     print("l'index actuel : "+str(self.CpRendu_medecins.currentIndex()))
    #     print("le nom actuel  : "+self.CpRendu_medecins.currentText())
    #     if self.CpRendu_motif.currentText() == "Autre":
    #        motif = self.CpRendu_motif_autre.text()
    #        print("le motif actuel : "+self.CpRendu_motif_autre.text())
    #     else:
    #         motif = self.CpRendu_motif.currentText()
    #         print("le motif actuel : "+self.CpRendu_motif.currentText())
    #     commentaire = self.CpRendu_commentaire.toPlainText()
    #     print("le commentaire actuel : "+self.CpRendu_commentaire.toPlainText())
    #     print("la date actuel : "+todayFr)
    #     titre = motif+" de "+self.CpRendu_medecins.currentText()+" le "+todayFr
    #     print("motif = "+motif+" de "+self.CpRendu_medecins.currentText()+" le "+todayFr)
    #     x = requests.post('http://127.0.0.1:8000/create_rapport', json={
    #         "RAP_DATE":todayFr,
    #         "RAP_BILAN":titre,
    #         "RAP_MOTIF":motif,
    #         "RAP_COMMENTAIRE":commentaire
    #         })

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
        self.rapport_page = Rapport_page()
        # self.rapport_page = Rapport_page()
        self.addWidget(self.index_page)
        self.addWidget(self.rapport_page)
        self.setCurrentWidget(self.index_page)

if __name__ == "__main__":
    

    today = date.today()
    todayFr = today.strftime("%Y-%m-%d")
    app = QApplication(sys.argv)
    appStack = Stack()
    appStack.show()
    sys.exit(app.exec())
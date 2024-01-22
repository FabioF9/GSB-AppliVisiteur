import sys
import typing
import requests
import json
from datetime import date
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6 import QtGui  

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow, QToolButton
)

class User():
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.id = user_id
        self.headers = {"Authorization": f"Bearer {self.access_token}"} 
        self.admin = False
        self.getUserDatas()

    def getUserDatas(self):
        userdatas = (requests.get(f'http://127.0.0.1:8000/visiteur/{self.id}')).json()
        self.admin = userdatas["VIS_ADMIN"]


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
        if x.status_code == 200:
            logedin = True
            self.tokaccess = x.json()[0]['access_token']
            appStack.launchIndex(self.tokaccess,x.json()[1])
        else:
            print('Username or Password are wrong !')

    def doSomethingNext(self):
        print("début de l'application")


class Index_page(QtWidgets.QWidget):
    def __init__(self):
        from pdf.pdf import CreerPresentation
        super(Index_page, self).__init__()
        loadUi("ui/new_index.ui", self)
        self.index_to_rapport.clicked.connect(self.goToRapport)
        self.index_bouton_deconnection.clicked.connect(appStack.deconnection)
        self.setUserDatas()
        self.index_to_admin.clicked.connect(self.goToAdmin)
        if not appStack.user.admin:
            self.index_to_admin.hide()

    def goToAdmin(self):
        appStack.setCurrentWidget(appStack.admin_page)


    def doSomethingNext(self):
        self.setRapportList()

    def setUserDatas(self):
        request = requests.get(f'http://127.0.0.1:8000/visiteur/{appStack.user.id}',headers=appStack.user.headers)
        infoUser = request.json()
        self.index_label_titre.setText(f' Bienvenue {infoUser["LOG_LOGIN"]} {infoUser["VIS_NOM"]} ')


    def setRapportList(self):
        from pdf.pdf import CreerPresentation
        while self.index_tableau_rapports.rowCount() > 0:
            self.index_tableau_rapports.removeRow(0)
        request = requests.get(f'http://127.0.0.1:8000/rapport/visiteur/{appStack.user.id}',headers=appStack.user.headers)
        all_rapports = request.json()
        button_dict = {}
        suppr_dict = {}
        edit_dict = {}
        for rapport in all_rapports:
            button_dict[f'index_button{rapport["RAP_NUM"]}'] = QPushButton("afficher")
            suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] = QPushButton("supprimer")
            edit_dict[f'index_edit{rapport["RAP_NUM"]}'] = QPushButton("éditer")
            self.index_tableau_rapports.insertRow(self.index_tableau_rapports.rowCount())                
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 0, QtWidgets.QTableWidgetItem(rapport['RAP_DATE']))
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 1, QtWidgets.QTableWidgetItem(rapport['affiliate_med']['MED_NOM']))
            self.index_tableau_rapports.setItem(self.index_tableau_rapports.rowCount()-1, 2, QtWidgets.QTableWidgetItem(rapport['RAP_MOTIF']))
            self.index_tableau_rapports.setCellWidget(self.index_tableau_rapports.rowCount()-1, 3, button_dict[f'index_button{rapport["RAP_NUM"]}'])
            self.index_tableau_rapports.setCellWidget(self.index_tableau_rapports.rowCount()-1, 4, suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'])
            self.index_tableau_rapports.setCellWidget(self.index_tableau_rapports.rowCount()-1, 5, edit_dict[f'index_edit{rapport["RAP_NUM"]}'])

            currentButton = button_dict[f'index_button{rapport["RAP_NUM"]}'] 
            currentButton.clicked.connect(lambda _, id_rapport=rapport["RAP_NUM"]: CreerPresentation(id_rapport))

            currentButtonSuppr = suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] 
            currentButtonSuppr.clicked.connect(lambda _, id_RAP=rapport["RAP_NUM"]: self.suppr(id_RAP))

            currentButtonEdit = edit_dict[f'index_edit{rapport["RAP_NUM"]}'] 
            currentButtonEdit.clicked.connect(lambda _, RAP_NUM=rapport["RAP_NUM"]: self.editRapport(RAP_NUM))

    def editRapport(self,RAP_NUM):
        # {'RAP_DATE': '2023-12-18', 'RAP_BILAN': 'Acheté', 'RAP_MOTIF': 'Visite', 'RAP_COMMENTAIRE': '"tgrty', 'MED_ID': 1, 'VIS_MATRICULE': 1}
        rapport_query = requests.get(f'http://127.0.0.1:8000/rapport/{RAP_NUM}',headers=appStack.user.headers)
        rapport_infos = rapport_query.json()
        index_medecin = appStack.rapport_page.rapport_medecins.findData(rapport_infos['MED_ID'])
        if ( index_medecin != -1 ):
            appStack.rapport_page.rapport_medecins.setCurrentIndex(index_medecin)
        appStack.rapport_page.rapport_comm.setText(rapport_infos['RAP_COMMENTAIRE'])
        self.goToRapport()
 
    def goToRapport(self):
        appStack.setCurrentWidget(appStack.rapport_page)

    def suppr(self,id_RAP):
        delete_RAP = requests.delete(f'http://127.0.0.1:8000/delete_rapport/{id_RAP}',headers=appStack.user.headers)
        self.setRapportList()

class Admin_page(QtWidgets.QWidget):
    def __init__(self):
        super(Admin_page, self).__init__()
        loadUi("ui/new_admin.ui", self)
        self.admin_to_index.clicked.connect(self.goToIndex)

    def goToIndex(self):
        appStack.setCurrentWidget(appStack.index_page)        

    def doSomethingNext(self):
        sousFifre = (requests.get(f'http://127.0.0.1:8000/visiteurgroup/{appStack.user.id}',headers=appStack.user.headers)).json()
        self.admin_vis1_nom.setText(sousFifre[0]["VIS_NOM"])
        self.admin_vis1_prenom.setText(sousFifre[0]["LOG_LOGIN"])
        # self.admin_vis1_prenom.setText(sousFifre[0]["LOG_LOGIN"])
        self.admin_vis2_nom.setText(sousFifre[1]["VIS_NOM"])
        self.admin_vis2_prenom.setText(sousFifre[1]["LOG_LOGIN"])
        # self.admin_vis2_count.setText(sousFifre[1]["LOG_LOGIN"])
        self.admin_vis3_nom.setText(sousFifre[2]["VIS_NOM"])
        self.admin_vis3_prenom.setText(sousFifre[2]["LOG_LOGIN"])
        # self.admin_vis3_count.setText(sousFifre[2]["LOG_LOGIN"])

    def setVisRapports(self,id_vis):
        from pdf.pdf import CreerPresentation
        while self.admin_tableau_rapport.rowCount() > 0:
            self.admin_tableau_rapports.removeRow(0)
        rapportsVis = (requests.get(f'http://127.0.0.1:8000/rapport/visiteur{id_vis}',headers=appStack.user.headers)).json()
        button_dict = {}
        suppr_dict = {}
        edit_dict = {}
        for rapport in rapportsVis:
            
            

class Rapport_page(QtWidgets.QWidget):
    def __init__(self):
        super(Rapport_page, self).__init__()
        loadUi("ui/new_rapport.ui", self)
        self.rapport_to_index.clicked.connect(self.goToIndex)
        self.rapport_datas.clicked.connect(self.sendRapport)
        self.setMedecins()
        self.rapport_medecins.currentIndexChanged.connect(self.setRapportResume)
        self.rapport_motif.currentIndexChanged.connect(self.setRapportResume)

    def setRapportResume(self):
        self.rapport_label2_medecin.setText(self.rapport_medecins.currentText())
        self.rapport_label2_motif.setText(self.rapport_motif.currentText())


    def setMedecins(self):
        queryMedecins = requests.get("http://127.0.0.1:8000/medecins", headers=appStack.user.headers)
        jsonMedecins = queryMedecins.json()
        i = 0
        for medecin in jsonMedecins:
            self.rapport_medecins.addItem(medecin['MED_NOM']+' '+medecin['MED_PRENOM'],medecin['MED_ID'])
            i += 1

    def doSomethingNext(self):
        return False

    def goToIndex(self):
        appStack.setCurrentWidget(appStack.index_page)

    def sendRapport(self):
        med_id = self.rapport_medecins.itemData(self.rapport_medecins.currentIndex())
        if self.rapport_motif.currentText() == "Autre":
           motif = self.rapport_motif_autre.text()
        else:
            motif = self.rapport_motif.currentText()
            
        commentaire = self.rapport_comm.toPlainText()
        bilan = self.rapport_bilan.currentText()
        
        

        create_rapport = requests.post('http://127.0.0.1:8000/create_rapport', json={
            "RAP_DATE":todayFr,
            "RAP_BILAN":bilan,
            "RAP_MOTIF":motif,
            "RAP_COMMENTAIRE":commentaire,
            "MED_ID": med_id,
            "VIS_MATRICULE": appStack.user.id
            },headers=appStack.user.headers)     


        self.goToIndex()

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
        self.setWindowIcon(QtGui.QIcon('ui/logoGSB.png'))
        self.setWindowTitle("AppliVisiteur")

    def deconnection(self):
        self.setCurrentWidget(appStack.login_page)
        del self.user
        del self.index_page
        del self.rapport_page
        del self.admin_page

    def initCurrent(self):
        if self.currentWidget():
            self.currentWidget().doSomethingNext()

    def launchIndex(self,access_token,id_user):
        self.user = User(access_token,id_user)
        self.admin_page = Admin_page()
        self.index_page = Index_page()
        self.rapport_page = Rapport_page()
        # self.rapport_page = Rapport_page()
        self.addWidget(self.admin_page)
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
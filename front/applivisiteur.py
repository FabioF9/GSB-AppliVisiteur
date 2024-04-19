import sys
import typing
import requests
import json
from datetime import date
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
import applivisiteur_config

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMainWindow, QToolButton
)

config_local = False

if config_local:
    API_LINK = "http://127.0.0.1:8000/"
else:
    API_LINK = "http://192.168.1.119:8000/" 


class User():
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.id = user_id
        self.headers = {"Authorization": f"Bearer {self.access_token}"} 
        self.admin = False
        self.getUserDatas()

    def getUserDatas(self):
        """
        Récupère et set les donnée du visiteurs

        Envoie une requête à la L'API " /visiteur/{id} "
        """
        userdatas = requests.get(f'{API_LINK}visiteur/{self.id}',headers=self.headers)
        userdatas = userdatas.json()
        if userdatas["VIS_ADMIN"] :
            self.admin = True

class Login_page(QtWidgets.QWidget):
    def __init__(self):
        super(Login_page, self).__init__()
        loadUi("ui/login.ui", self)
        self.login_button1.clicked.connect(self.login)

    def login(self):
        """
        Connexion à l'application

        Vérifie les informations rentrées dans le formamulaire de connexion

        Envoie l'identifiant et le mot de passe rentré à l'API " /login/{json} ",
        Si code retour = 200 : récupération du token de connexion et initialisation des fenêtres de l'application
        Sinon : erreur

        """
        login   = self.login_input1.text()
        mdp     = self.login_input2.text()

        x = requests.post(f'{API_LINK}login',
        data={
            "grant_type":"",
            "username":login,
            "password":mdp,
            "scope":"",
            "client_id":"",
            "client_secret":""
            })
        if x.status_code == 200:
            self.tokaccess = x.json()[0]['access_token']
            appStack.launchIndex(self.tokaccess,x.json()[1])
            return x.status_code
        else:
            return x.status_code

    def doSomethingNext(self):
        """
        Méthode au lancement de la page 

        Affiche un message de bienvenue
        """
        print("début de l'application")

class Index_page(QtWidgets.QWidget):
    def __init__(self):
        from pdf.pdf import CreerPresentation
        super(Index_page, self).__init__()
        loadUi("ui/index.ui", self)
        self.index_to_rapport.clicked.connect(self.goToRapport)
        self.index_bouton_deconnection.clicked.connect(appStack.deconnection)
        self.setUserDatas()
        self.index_to_admin.clicked.connect(self.goToAdmin)
        if not appStack.user.admin:
            self.index_to_admin.hide()

    def goToAdmin(self):
        """
        Affiche la fenêtre "Admin"
        """
        appStack.setCurrentWidget(appStack.admin_page)


    def doSomethingNext(self):
        """
        Méthode au lancement de la page

        Lance la méthode "setRapportList()"
        """
        self.setRapportList()

    def setUserDatas(self):
        """
        Affiche le nom et prénom du visiteur sur l'application

        Effectue une requête pour récupérer les données du visiteur 
        Change le texte du label "index_label_titre"
        """
        request = requests.get(f'{API_LINK}visiteur/{appStack.user.id}',headers=appStack.user.headers)
        infoUser = request.json()
        self.index_label_titre.setText(f' Bienvenue {infoUser["LOG_LOGIN"]} {infoUser["VIS_NOM"]} ')


    def setRapportList(self):
        """
        Ajoute les lignes des rapports du visiteur dans un tableau

        Importe la bibliothèque pdf
        Enlève toutes les lignes déjà présentes dans le tableau
        Effectue une requête à l'API "/rapport/visiter/{id}"
        Boucle sur le json contenant les rapports du vissiteur
        Ajoute les informations des rapports dans les lignes ["Date","Medecin","Motif","Voir","Supprimer","Editer"]
            Définie la fontion des boutons
            ( les colonnes "Voir","Supprimer","Editer" sont complété avec des bouttons qui ont une fonctionnalité en accord avec leur appelation )
        """
        from pdf.pdf import CreerPresentation
        while self.index_tableau_rapports.rowCount() > 0:
            self.index_tableau_rapports.removeRow(0)
        request = requests.get(f'{API_LINK}rapport/visiteur/{appStack.user.id}',headers=appStack.user.headers)
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
            currentButton.clicked.connect(lambda _, id_rapport=rapport["RAP_NUM"]: CreerPresentation(id_rapport, appStack.user.headers))
            currentButton.setIcon(QIcon('ui/eye.png'))

            currentButtonSuppr = suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] 
            currentButtonSuppr.clicked.connect(lambda _, id_RAP=rapport["RAP_NUM"]: self.suppr(id_RAP))
            currentButtonSuppr.setIcon(QIcon('ui/trash-can.png'))

            currentButtonEdit = edit_dict[f'index_edit{rapport["RAP_NUM"]}'] 
            currentButtonEdit.clicked.connect(lambda _, RAP_NUM=rapport["RAP_NUM"]: self.editRapport(RAP_NUM))
            currentButtonEdit.setIcon(QIcon('ui/office-material.png'))

    def editRapport(self,RAP_NUM):
        """
        Éditer un rapport

        Ouvre la page d'édition des rapport avec les données du rapport sélectionné
        """
        # {'RAP_DATE': '2023-12-18', 'RAP_BILAN': 'Acheté', 'RAP_MOTIF': 'Visite', 'RAP_COMMENTAIRE': '"tgrty', 'MED_ID': 1, 'VIS_MATRICULE': 1}
        rapport_query = requests.get(f'{API_LINK}rapport/{RAP_NUM}',headers=appStack.user.headers)
        rapport_infos = rapport_query.json()
        index_medecin = appStack.rapport_page.rapport_medecins.findData(rapport_infos['MED_ID'])
        if ( index_medecin != -1 ):
            appStack.rapport_page.rapport_medecins.setCurrentIndex(index_medecin)
        appStack.rapport_page.rapport_comm.setText(rapport_infos['RAP_COMMENTAIRE'])
        self.goToRapport()
 
    def goToRapport(self):
        """
        Affiche la page "Rapport"
        """
        appStack.setCurrentWidget(appStack.rapport_page)

    def suppr(self,id_RAP):
        """
        Supprime un rapport

        Supprime dans la base de donnée le rapport sélectionnée à l'aide d'une requête à l'API "/delete_rapport"
        """
        delete_RAP = requests.delete(f'{API_LINK}delete_rapport/{id_RAP}',headers=appStack.user.headers)
        self.setRapportList()

class Admin_page(QtWidgets.QWidget):
    def __init__(self):
        super(Admin_page, self).__init__()
        loadUi("ui/admin.ui", self)
        self.admin_to_index.clicked.connect(self.goToIndex)

    def goToIndex(self):
        """
        Affiche la page "Index"
        """
        appStack.setCurrentWidget(appStack.index_page)        

    def doSomethingNext(self):
        """
        Méthode au lancement de la page

        Récupére les informations des visiteur en charge du visiteur connecté (Svst) et les set
    
        """
        sousVisiteur = requests.get(f'{API_LINK}visiteurgroup/{appStack.user.id}',headers=appStack.user.headers)
        sousVisiteur = sousVisiteur.json()
        self.admin_vis1_nom.setText(sousVisiteur[0]["VIS_NOM"])
        self.admin_vis1_prenom.setText(sousVisiteur[0]["LOG_LOGIN"])
        self.admin_vis1_count.setText(str(sousVisiteur[0]["RAPPORT_COUNT"]))
        self.admin_boutton_vis1.clicked.connect(lambda _, id_vis=int(sousVisiteur[0]["VIS_MATRICULE"]): self.setVisRapports(id_vis))
        self.admin_boutton_vis1.setIcon(QIcon('ui/eye.png'))
        self.admin_vis2_nom.setText(sousVisiteur[1]["VIS_NOM"])
        self.admin_vis2_prenom.setText(sousVisiteur[1]["LOG_LOGIN"])
        self.admin_vis2_count.setText(str(sousVisiteur[1]["RAPPORT_COUNT"]))
        self.admin_boutton_vis2.clicked.connect(lambda _, id_vis=int(sousVisiteur[1]["VIS_MATRICULE"]): self.setVisRapports(id_vis))
        self.admin_boutton_vis2.setIcon(QIcon('ui/eye.png'))
        self.admin_vis3_nom.setText(sousVisiteur[2]["VIS_NOM"])
        self.admin_vis3_prenom.setText(sousVisiteur[2]["LOG_LOGIN"])
        self.admin_vis3_count.setText(str(sousVisiteur[2]["RAPPORT_COUNT"]))
        self.admin_boutton_vis3.clicked.connect(lambda _, id_vis=int(sousVisiteur[2]["VIS_MATRICULE"]): self.setVisRapports(id_vis))
        self.admin_boutton_vis3.setIcon(QIcon('ui/eye.png'))

    def setVisRapports(self,id_vis):
        """
        Ajoute les lignes des rapports du visiteur dans un tableau

        Importe la bibliothèque pdf
        Enlève toutes les lignes déjà présentes dans le tableau
        Effectue une requête à l'API "/rapport/visiter/{id}"
        Boucle sur le json contenant les rapports du vissiteur
        Ajoute les informations des rapports dans les lignes ["Date","Medecin","Motif","Voir","Supprimer","Editer"]
            Définie la fontion des boutons
            ( les colonnes "Voir","Supprimer","Editer" sont complété avec des bouttons qui ont une fonctionnalité en accord avec leur appelation )
        """
        from pdf.pdf import CreerPresentation
        while self.admin_tableau_rapports.rowCount() > 0:
            self.admin_tableau_rapports.removeRow(0)
        rapportsVis = (requests.get(f'{API_LINK}rapport/visiteur/{id_vis}',headers=appStack.user.headers)).json()
        button_dict = {}
        suppr_dict = {}
        edit_dict = {}
        for rapport in rapportsVis:
            button_dict[f'index_button{rapport["RAP_NUM"]}'] = QPushButton("afficher")
            suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] = QPushButton("supprimer")
            edit_dict[f'index_edit{rapport["RAP_NUM"]}'] = QPushButton("éditer")
            self.admin_tableau_rapports.insertRow(self.admin_tableau_rapports.rowCount())                
            self.admin_tableau_rapports.setItem(self.admin_tableau_rapports.rowCount()-1, 0, QtWidgets.QTableWidgetItem(rapport['RAP_DATE']))
            self.admin_tableau_rapports.setItem(self.admin_tableau_rapports.rowCount()-1, 1, QtWidgets.QTableWidgetItem(rapport['affiliate_med']['MED_NOM']))
            self.admin_tableau_rapports.setItem(self.admin_tableau_rapports.rowCount()-1, 2, QtWidgets.QTableWidgetItem(rapport['RAP_MOTIF']))
            self.admin_tableau_rapports.setCellWidget(self.admin_tableau_rapports.rowCount()-1, 3, button_dict[f'index_button{rapport["RAP_NUM"]}'])
            self.admin_tableau_rapports.setCellWidget(self.admin_tableau_rapports.rowCount()-1, 4, suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'])
            self.admin_tableau_rapports.setCellWidget(self.admin_tableau_rapports.rowCount()-1, 5, edit_dict[f'index_edit{rapport["RAP_NUM"]}'])

            currentButton = button_dict[f'index_button{rapport["RAP_NUM"]}'] 
            currentButton.clicked.connect(lambda _, id_rapport=rapport["RAP_NUM"]: CreerPresentation(id_rapport))
            currentButton.setIcon(QIcon('ui/eye.png'))

            currentButtonSuppr = suppr_dict[f'index_suppr{rapport["RAP_NUM"]}'] 
            currentButtonSuppr.clicked.connect(lambda _, id_RAP=rapport["RAP_NUM"]: self.suppr(id_RAP))
            currentButtonSuppr.setIcon(QIcon('ui/trash-can.png'))

            currentButtonEdit = edit_dict[f'index_edit{rapport["RAP_NUM"]}'] 
            currentButtonEdit.clicked.connect(lambda _, RAP_NUM=rapport["RAP_NUM"]: self.editRapport(RAP_NUM))
            currentButtonEdit.setIcon(QIcon('ui/office-material.png'))

    def suppr(self,id_RAP):
        """
        Supprime un rapport

        Supprime dans la base de donnée le rapport sélectionnée à l'aide d'une requête à l'API "/delete_rapport"
        """        
        delete_RAP = requests.delete(f'{API_LINK}delete_rapport/{id_RAP}',headers=appStack.user.headers)
        self.setVisRapports()

    def goToRapport(self):
        """
        Affiche la page "Rapport"
        """
        appStack.setCurrentWidget(appStack.rapport_page)        

    def editRapport(self,RAP_NUM):
        """
        Éditer un rapport

        Ouvre la page d'édition des rapport avec les données du rapport sélectionné
        """        
        # {'RAP_DATE': '2023-12-18', 'RAP_BILAN': 'Acheté', 'RAP_MOTIF': 'Visite', 'RAP_COMMENTAIRE': '"tgrty', 'MED_ID': 1, 'VIS_MATRICULE': 1}
        rapport_query = requests.get(f'{API_LINK}rapport/{RAP_NUM}',headers=appStack.user.headers)
        rapport_infos = rapport_query.json()
        index_medecin = appStack.rapport_page.rapport_medecins.findData(rapport_infos['MED_ID'])
        if ( index_medecin != -1 ):
            appStack.rapport_page.rapport_medecins.setCurrentIndex(index_medecin)
        appStack.rapport_page.rapport_comm.setText(rapport_infos['RAP_COMMENTAIRE'])
        self.goToRapport()

class Rapport_page(QtWidgets.QWidget):
    def __init__(self):
        super(Rapport_page, self).__init__()
        loadUi("ui/rapport.ui", self)
        self.rapport_to_index.clicked.connect(self.goToIndex)
        self.rapport_envoyer.clicked.connect(self.sendRapport)
        self.setMedecins()
        self.rapport_medecins.currentIndexChanged.connect(self.setRapportResume)
        self.rapport_motif.currentIndexChanged.connect(self.setRapportResume)
        self.setMedicaments()

    def setRapportResume(self):
        """
        Récupére les données sélectionnée dans les champs "médecin"
        """        
        # self.rapport_label2_medecin.setText(self.rapport_medecins.currentText())
        # self.rapport_label2_motif.setText(self.rapport_motif.currentText())


    def setMedecins(self):
        """
        Set la liste des médecins dans une liste déroulante
        """
        queryMedecins = requests.get(f"{API_LINK}medecins", headers=appStack.user.headers)
        jsonMedecins = queryMedecins.json()
        for medecin in jsonMedecins:
            nomMed = str(medecin['MED_NOM'])+' '+str(medecin['MED_PRENOM'])
            self.rapport_medecins.addItem(nomMed,medecin['MED_ID'])

        

    def setMedicaments(self):
        """
        Set la liste des médicaments dans une liste déroulante
        """
        queryMedicaments = requests.get(f"{API_LINK}medicaments", headers=appStack.user.headers)
        medicaments = queryMedicaments.json()
        for medicament in medicaments:
            # self.rapport_echantillon1.addItem(medicament['MEDI_LABEL'], medicament['MEDI_ID'])
            self.rapport_echantillon1.addItem(medicament['MEDI_LABEL'], medicament['MEDI_ID'])
            self.rapport_echantillon2.addItem(medicament['MEDI_LABEL'], medicament['MEDI_ID'])

    def doSomethingNext(self):
        """
        Méthode au lancement de la page
        """
        return False

    def goToIndex(self):
        """
        Affiche la page "Index"
        """
        appStack.setCurrentWidget(appStack.index_page)

    def sendRapport(self):
        """
        Envoie les informations renseigné dans le formulaire de rapport
        """

        med_id = self.rapport_medecins.itemData(self.rapport_medecins.currentIndex())

        if self.rapport_motif.currentText() == "Autre":
           motif = self.rapport_motif_autre.text()
        else:
            motif = self.rapport_motif.currentText()
            
        commentaire = self.rapport_datas.toPlainText()
        listeMedicaments = []
        
        if self.rapport_echantillon1.currentText() != 'Aucun':
            listeMedicaments.append({'med':1,'id':self.rapport_echantillon1.itemData(self.rapport_echantillon1.currentIndex()),'nbr':self.rapport_echantillon1_compteur.value()})

        if self.rapport_echantillon2.currentText() != 'Aucun':
            listeMedicaments.append({'med':2,'id':self.rapport_echantillon2.itemData(self.rapport_echantillon2.currentIndex()),'nbr':self.rapport_echantillon2_compteur.value()})


        create_rapport = requests.post(f'{API_LINK}create_rapport', json={
            "RAP_DATE":todayFr,
            "RAP_BILAN":'bilan',
            "RAP_MOTIF":motif,
            "RAP_COMMENTAIRE":commentaire,
            "MED_ID": med_id,
            "VIS_MATRICULE": appStack.user.id
            },headers=appStack.user.headers) 
        getLastRapp = (requests.get(f'{API_LINK}maxrapport', headers=appStack.user.headers)).json()
        for medicament in listeMedicaments:
            if medicament['med'] != 0:
                json ={
                      "ECH_NOMBRE": medicament['nbr'],
                      "RAP_NUM": getLastRapp,
                      "MEDI_ID": medicament['id']
                    } 
                requests.post(f'{API_LINK}add_echantillon', json={
                      "ECH_NOMBRE": medicament['nbr'],
                      "RAP_NUM": getLastRapp,
                      "MEDI_ID": medicament['id']
                    } ,headers=appStack.user.headers)

        # self.goToIndex()

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
        """
        Déconnecte l'utilisateur
        """
        self.setCurrentWidget(appStack.login_page)
        del self.user
        del self.index_page
        del self.rapport_page
        del self.admin_page

    def initCurrent(self):
        if self.currentWidget():
            self.currentWidget().doSomethingNext()

    def launchIndex(self,access_token,id_user):
        """
        Initie les pages de l'application
        """
        self.user = User(access_token,id_user)
        self.admin_page = Admin_page()
        self.index_page = Index_page()
        self.rapport_page = Rapport_page()
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
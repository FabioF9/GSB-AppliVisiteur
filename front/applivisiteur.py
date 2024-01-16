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

class Window(QWidget):
    def __init__(self):
        # self.tokaccess = " test "
        self.access_token = ""
        super().__init__()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("Galaxy Swiss Bourdin")
        layout = QGridLayout()
        self.setLayout(layout)
        button1 = QPushButton("Login")
        layout.addWidget(button1)




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
        loadUi("ui/main.ui", self)
        # self.access_token = Window.access_token
        # print(self.access_token)
        # headers = {"Authorization": f"Bearer {access_token}"}
        # x = requests.get('http://127.0.0.1:8000/medecins', headers=headers)
        self.set_list()
        self.index_button_create.clicked.connect(self.createDr)
        self.index_button_update.clicked.connect(self.updateDr)
        self.index_button_delete.clicked.connect(self.deleteDr)
        self.index_button_read.clicked.connect(self.gotoCpRendu)
        self.index_button_view.clicked.connect(self.gotoView)
        self.calendar.setGridVisible(True);

    def set_list(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        x = requests.get('http://127.0.0.1:8000/medecins')
        lstMedecins = x.json()        
        for medecin in lstMedecins:
                self.tableWidget.insertRow(self.tableWidget.rowCount())                
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 0, QtWidgets.QTableWidgetItem(medecin['nom']))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 1, QtWidgets.QTableWidgetItem(medecin['spe']))
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, 2, QtWidgets.QTableWidgetItem(medecin['nom']))


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

    def gotoView(self):
        widget.setCurrentIndex(widget.currentIndex()+2)




class CpRendu(QMainWindow):
    """docstring for CpRendu"""
    def __init__(self):
        super().__init__()
        self.tokaccess = ""
        super(CpRendu, self).__init__()
        loadUi("ui/CpRendu.ui", self)
        self.insert_medecins()
        self.CpRendu_test.clicked.connect(self.test)
        self.bouton_retour.clicked.connect(self.retour_acceuil)
        
    def insert_medecins(self):
        x = requests.get('http://127.0.0.1:8000/medecins')
        jason = x.json()
        for i in jason:
            self.CpRendu_medecins.addItem(i['nom'])

    def retour_acceuil(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def test(self):
        print("l'index actuel : "+str(self.CpRendu_medecins.currentIndex()))
        print("le nom actuel  : "+self.CpRendu_medecins.currentText())
        if self.CpRendu_motif.currentText() == "Autre":
           motif = self.CpRendu_motif_autre.text()
           print("le motif actuel : "+self.CpRendu_motif_autre.text())
        else:
            motif = self.CpRendu_motif.currentText()
            print("le motif actuel : "+self.CpRendu_motif.currentText())
        commentaire = self.CpRendu_commentaire.toPlainText()
        print("le commentaire actuel : "+self.CpRendu_commentaire.toPlainText())
        print("la date actuel : "+todayFr)
        titre = motif+" de "+self.CpRendu_medecins.currentText()+" le "+todayFr
        print("motif = "+motif+" de "+self.CpRendu_medecins.currentText()+" le "+todayFr)
        x = requests.post('http://127.0.0.1:8000/create_rapport', json={
            "RAP_DATE":todayFr,
            "RAP_BILAN":titre,
            "RAP_MOTIF":motif,
            "RAP_COMMENTAIRE":commentaire,
            "MED_ID":
            })

        
class ViewPdf(QMainWindow):
    """docstring for CpRendu"""
    def __init__(self):
        super().__init__()
        self.tokaccess = ""
        super(ViewPdf, self).__init__()
        loadUi("ui/ViewRapport.ui", self)
        self.view_retour.clicked.connect(self.retour_acceuil)
    
    def retour_acceuil(self):
        widget.setCurrentIndex(widget.currentIndex()-2)



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


today = date.today()
todayFr = today.strftime("%d/%m/%Y")


widget = QtWidgets.QStackedWidget()
login = Window()
menu = Screen2(login)
CpRendu = CpRendu()
View = ViewPdf()
widget.addWidget(login)
widget.addWidget(menu)
widget.addWidget(CpRendu)
widget.addWidget(View)

widget.show()
sys.exit(app.exec())
h
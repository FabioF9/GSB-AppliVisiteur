import os
import subprocess

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.uic import loadUi
from datetime import date
import logging
import json
import sys
import requests
import re
import configparser

visiteur = None


class Visiteur:
    """
        class utilisee pour contenir les informations du visiteur connecté

        ...

        Attributes
        ----------
        id : int
           contient l'id du visiteur
        nom : str
           contient le nom du visiteur
        prenom : str
           contient le prenom du visiteur
        secteur : int
           contient le secteur du visiteur
        token : str
           contient le token de session du visiteur

    """

    def __init__(self, id, nom, prenom, secteur, token):
        """
            constructeur des attributs de l'objet Visiteur
        """
        super(Visiteur, self).__init__()

        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.secteur = secteur
        self.token = token


class FenetreMaitresse(QMainWindow):
    """
        class utilisée pour contenir les autres objets Fenetre

        ...

        Attributes
        ----------
        stackedWidget : obj
            un objet enfant permettant de contenir des objets (ici des fenêtres)

    """

    def __init__(self):
        """
            constructeur des attributs de l'objet FenetreMaitresse
        """
        super(FenetreMaitresse, self).__init__()
        try:
            loadUi("UI/fenetre_maitresse.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        fenetre_connexion = FenetreConnexion()
        self.stackedWidget.addWidget(fenetre_connexion)
        self.stackedWidget.setCurrentWidget(fenetre_connexion)


class FenetreConnexion(QDialog):
    """
        class qui crée une fenêtre pour se connecter a l'application

        ...

        Attributes
        ----------
        champsLogin : obj
            un champ de saisie pour le login du visiteur
        champsMDP : obj
            un champ de saisie pour le mot de passe du visiteur
        loginBouton : obj
            un bouton pour permettre de se connecter

        Methods
        -------
        connexion (self) :
            methode permettant d'initialiser la connexion avec l'api
        @staticmethod
        aller_vers_fenetre_principale () :
            methode permettant de transitionner de fenetre vers fenetre_principale
    """

    def __init__(self):
        """
            constructeur des attributs de l'objet FenetreConnexion
        """
        super(FenetreConnexion, self).__init__()
        try:
            loadUi("UI/fenetre_connexion.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        self.champsLogin.returnPressed.connect(self.connexion)
        self.champsMDP.returnPressed.connect(self.connexion)
        self.loginBouton.clicked.connect(self.connexion)

    def connexion(self):
        """
            Fonction de connexion à l'API

            Returns
            -------
            None
        """
        global visiteur

        login = Utils.nettoyage_str(self.champsLogin.text(), 1, 0, 1)
        mdp = Utils.nettoyage_str(self.champsMDP.text(), 1, 0, 1)
        if login == 'swiss':

            login_json = {"login": login, "password": mdp}
            try:
                requete = requests.get(
                    Utils.url_api() + '/GSB/connexion',
                    json=login_json,
                    headers={'Content-Type': 'application/json'})

                if Utils.check_code_status(requete.status_code)['status']:

                    Utils.popup("Bravo, la connexion avec l'api est possible !", 'Information')

            except Exception as e:
                logging.exception(e)

        elif login != '' or mdp != '':
            # je construis un dictionnaire pour l'envoyer sous format Json
            login_json = {"login": login, "password": mdp}
            try:
                requete = requests.get(
                    Utils.url_api() + '/GSB/connexion',
                    json=login_json,
                    headers={'Content-Type': 'application/json'})
            except Exception as e:
                logging.exception(e)

            if Utils.check_code_status(requete.status_code)['status']:

                infos_visiteur = json.loads(requete.text)

                visiteur = Visiteur(infos_visiteur['id'], infos_visiteur['nom'], infos_visiteur['prenom'],
                                    infos_visiteur['secteur'], requete.cookies['session'])

                self.aller_vers_fenetre_principale()

            else:
                print(requete.status_code)
                self.champsMDP.setText('')

    # la méthode statique permet de prévenir la fonction d'altérer la class
    @staticmethod
    def aller_vers_fenetre_principale():
        """
            Fonction de redirection vers la fenetre principale

            Returns
            -------
            None
        """
        fenetre_principale = FenetrePrincipale()
        win.stackedWidget.addWidget(fenetre_principale)
        win.stackedWidget.setCurrentWidget(fenetre_principale)

        return None


class FenetrePresentation(QDialog):
    def __init__(self):
        super(FenetrePresentation, self).__init__()
        loadUi("UI/fenetre_saisie_présentation.ui", self)

        self.BoutonFormulaire.clicked.connect(self.creer_presentation)
        self.AccueilBouton.clicked.connect(self.fermer_fenetre)

        # dictionnaire des praticiens et des médicaments
        self.praticiens = dict()
        self.medicaments = dict()

        # requete pour obtenir les medecins
        requete = requests.get(
            Utils.url_api() + '/GSB/medecins',
            cookies=dict(session=visiteur.token))

        if Utils.check_code_status(requete.status_code)['status']:

            medecins_json = json.loads(requete.text)
            del requete

            # creation d'un dictionnaire pour lier les noms des praticiens avec leur id
            for i in range(len(medecins_json)):
                nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
                self.praticiens[nom_total] = {"Id": medecins_json[i]['Id'],
                                              "Secteur_id": medecins_json[i]['Secteur_id']}

            # j'ordonne les noms des praticiens par ordre alphabetique
            self.praticiens_ordonnes = sorted(self.praticiens.keys(), key=lambda x: x.lower())

            # j'ajoute les praticiens ordonnés en fonction du secteur du visiteur
            for nom_praticien in self.praticiens_ordonnes:
                if int(self.praticiens[nom_praticien].get('Secteur_id')) == int(visiteur.secteur):
                    self.SelectionPraticiens.addItem(nom_praticien)

        else:
            pass

        self.SelectionMedicamentNom.addItem("-Aucun-")
        self.SelectionMedicamentNom_2.addItem("-Aucun-")

        # requete pour obtenir les médicaments
        requete = requests.get(
            Utils.url_api() + '/GSB/medicaments',
            cookies=dict(session=visiteur.token))

        if Utils.check_code_status(requete.status_code)['status']:

            medicaments_json = json.loads(requete.text)
            del requete

            # creation d'un dictionnaire pour lier les noms des médicaments avec leur nombre
            for j in range(len(medicaments_json)):
                self.medicaments[medicaments_json[j]["Label"]] = medicaments_json[j]["Id"]

            # j'ordonne les noms des médicaments par ordre alphabetique
            self.medicaments_ordonnes = sorted(self.medicaments.keys(), key=lambda x: x.lower())
            for nom_medicaments in self.medicaments_ordonnes:
                self.SelectionMedicamentNom.addItem(nom_medicaments)
                self.SelectionMedicamentNom_2.addItem(nom_medicaments)

    def creer_presentation(self):
        if self.SelectionMedicamentNom.currentText() != '-Aucun-' and self.SelectionMedicamentNom_2.currentText() != '-Aucun-':
            from pdf.pdf import CreerPresentation
            # requete pour obtenir les médicaments
            requete_med1 = requests.get(
                Utils.url_api() + '/GSB/medicament/' + str(self.medicaments[self.SelectionMedicamentNom.currentText()]),
                cookies=dict(session=visiteur.token))

            # requete pour obtenir les médicaments
            requete_med2 = requests.get(
                Utils.url_api() + '/GSB/medicament/' + str(self.medicaments[self.SelectionMedicamentNom_2.currentText()]),
                cookies=dict(session=visiteur.token))

            if Utils.check_code_status(requete_med1.status_code)['status'] and Utils.check_code_status(requete_med2.status_code)['status']:
                med1_json = json.loads(requete_med1.text)
                med2_json = json.loads(requete_med2.text)
                file = CreerPresentation(self.SelectionPraticiens.currentText(),
                                  med1_json,
                                  med2_json)
                subprocess.Popen(file,shell=True)

        else:
            Utils.popup('Veuillez choisir les deux échantillons !', 'Warning')


    # fonction pour détruire la page
    def fermer_fenetre(self):
        """
            Fonction de fermeture de la fenetre

            Returns
            -------
            None
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

        return None

class FenetreStatistiques(QDialog):
    def __init__(self):
        super(FenetreStatistiques, self).__init__()
        loadUi("UI/fenetre_statistiques.ui", self)
        self.Visiteurs.clicked.connect(self.stat_visiteurs)
        self.CR.clicked.connect(self.stat_CR)
        self.echantillons.clicked.connect(self.stat_echantillons)
        self.medicaments.clicked.connect(self.stat_medicaments)
        self.Praticiens.clicked.connect(self.stat_praticiens)
        self.AccueilBouton.clicked.connect(self.fermer_fenetre)

    def stat(self, valeurs_json):

        while (self.TableauStats.rowCount() > 0):
                self.TableauStats.removeRow(0)
        while (self.TableauStats.columnCount() > 0):
                self.TableauStats.removeColumn(0)


        colonnes = list(valeurs_json[0].keys())

        for colonne in colonnes :
            self.TableauStats.insertColumn(self.TableauStats.columnCount())
           
        self.TableauStats.setHorizontalHeaderLabels(colonnes)
        for stat in valeurs_json:
            self.TableauStats.insertRow(self.TableauStats.rowCount())
            i = 0
            for colonne in colonnes:
                self.TableauStats.setItem(self.TableauStats.rowCount() - 1, i,QTableWidgetItem(str(stat[colonne])))
                i+=1

        self.TableauStats.resizeColumnsToContents()

    def stat_medicaments(self):
        requete = requests.get(Utils.url_api() + '/stats/medicaments', cookies=dict(session=visiteur.token))

        visiteur_json = json.loads(requete.text)
        del requete

        self.stat(visiteur_json)

    def stat_praticiens(self):
        requete = requests.get(Utils.url_api() + '/stats/praticiens', cookies=dict(session=visiteur.token))

        visiteur_json = json.loads(requete.text)
        del requete

        self.stat(visiteur_json)

    def stat_visiteurs(self):
        requete = requests.get(Utils.url_api() + '/stats/visiteurs', cookies=dict(session=visiteur.token))

        visiteur_json = json.loads(requete.text)
        del requete

        self.stat(visiteur_json)

    def stat_CR(self):
        requete = requests.get(Utils.url_api() + '/stats/CR', cookies=dict(session=visiteur.token))

        visiteur_json = json.loads(requete.text)
        del requete

        self.stat(visiteur_json)

    def stat_echantillons(self):
        requete = requests.get(Utils.url_api() + '/stats/echantillons', cookies=dict(session=visiteur.token))

        visiteur_json = json.loads(requete.text)
        del requete

        self.stat(visiteur_json)
        
        
        
        

        
        
        # self.TableauStats.insertRow(self.TableauOffreMedicaments.rowCount())

        #                                              QTableWidgetItem(self.SelectionMedicamentNom.currentText()))
        # self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 1,
        #                                              QTableWidgetItem(self.SelectionMedicamentQuantite.text()))



    # fonction pour détruire la page
    def fermer_fenetre(self):
        """
            Fonction de fermeture de la fenetre

            Returns
            -------
            None
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

        return None


class FenetrePrincipale(QDialog):
    """
        class pour créer une fenêtre pour se connecter a l'application

        ...

        Attributes
        ----------
        NomVisiteur : obj
            une ligne de texte affichant le nom du visiteur
        SaisieBouton : obj
            un bouton pour permettre de saisir un rapport
        ConsultationBouton : obj
            un bouton pour permettre de consulter les rapport
        DeconnexionBouton : obj
            un bouton pour permettre de se déconnecter
        InformationsBouton : obj
            un bouton pour permettre d'afficher les informations praticiens/médicamments

        Methods
        -------
        @staticmethod
        aller_vers_fenetre_saisie () :
            methode permettant de transitionner de fenetre vers fenetre_saisie
        @staticmethod
        aller_vers_fenetre_connexion () :
            methode permettant de transitionner de fenetre vers fenetre_connexion
        @staticmethod
        aller_vers_fenetre_consultation () :
            methode permettant de transitionner de fenetre vers fenetre_consultation
        @staticmethod
        aller_vers_fenetre_information () :
            methode permettant de transitionner de fenetre vers fenetre_information
    """

    def __init__(self):
        """
            constructeur des attributs de l'objet FenetrePrincipale
        """
        super(FenetrePrincipale, self).__init__()
        try:
            loadUi("UI/fenetre_principale.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        self.NomVisiteur.setText(visiteur.nom + ' ' + visiteur.prenom)
        self.SaisieBouton.clicked.connect(self.aller_vers_fenetre_saisie)
        self.ConsultationBouton.clicked.connect(self.aller_vers_fenetre_consultation)
        self.DeconnexionBouton.clicked.connect(self.aller_vers_fenetre_connexion)
        self.InformationsBouton.clicked.connect(self.aller_vers_fenetre_information)
        self.PresentationBouton.clicked.connect(self.aller_vers_fenetre_presentation)
        self.StatistiquesBouton.clicked.connect(self.aller_vers_fenetre_statistiques)

    @staticmethod
    def aller_vers_fenetre_saisie():
        """
            Fonction de redirection vers la fenetre saisie

            Returns
            -------
            None
        """
        fenetre_saisie = FenetreSaisie()
        win.stackedWidget.addWidget(fenetre_saisie)
        win.stackedWidget.setCurrentWidget(fenetre_saisie)

        return None

    @staticmethod
    def aller_vers_fenetre_statistiques():
        """
            Fonction de redirection vers la fenetre saisie

            Returns
            -------
            None
        """
        fenetre_stat = FenetreStatistiques()
        win.stackedWidget.addWidget(fenetre_stat)
        win.stackedWidget.setCurrentWidget(fenetre_stat)

        return None

    @staticmethod
    def aller_vers_fenetre_connexion():
        """
            Fonction de redirection vers la fenetre connexion

            Returns
            -------
            None
        """
        fenetre_connexion = FenetreConnexion()
        win.stackedWidget.addWidget(fenetre_connexion)
        win.stackedWidget.setCurrentWidget(fenetre_connexion)

        return None

    @staticmethod
    def aller_vers_fenetre_consultation():
        """
            Fonction de redirection vers la fenetre consultation

            Returns
            -------
            None
        """
        fenetre_consultation = FenetreConsultation()
        win.stackedWidget.addWidget(fenetre_consultation)
        win.stackedWidget.setCurrentWidget(fenetre_consultation)

        return None

    @staticmethod
    def aller_vers_fenetre_information():
        """
            Fonction de redirection vers la fenetre information

            Returns
            -------
            None
        """
        fenetre_information = FenetreInformation()
        win.stackedWidget.addWidget(fenetre_information)
        win.stackedWidget.setCurrentWidget(fenetre_information)

        return None

    @staticmethod
    def aller_vers_fenetre_presentation():
        """
            Fonction de redirection vers la fenetre saisie

            Returns
            -------
            None
        """
        fenetre_presentation = FenetrePresentation()
        win.stackedWidget.addWidget(fenetre_presentation)
        win.stackedWidget.setCurrentWidget(fenetre_presentation)

        return None


class FenetreInformation(QDialog):
    """
        class pour creer une fenetre qui affiche les informations des médecins

        ...

        Attributes
        ----------
        SelectionInfo : obj
            un objet menu déroulant permettant de choisir entre les infos praticiens et médicamments
        listWidgetInfo : obj
            un objet liste permettant de choisir entre les différentes infos praticiens et médicamments
        RetourInformation : obj
            un objet bouton permettant de fermer la fenetre

        Methods
        -------
        sur_changement (self) :
            Change la liste listWidgetInfo avec la bonne table d'informations sélectionnée dans SelectionInfo
        fermer_fenetre (self) :
            Ferme la fenetre la plus récente
        afficher_informations (self) :
            Affiche les informations des praticiens et des médicamments
    """
    def __init__(self):
        """
            constructeur des attributs de l'objet FenetreInformation
        """
        super(FenetreInformation, self).__init__()
        try:
            loadUi("UI/fenetre_information.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        self.RetourInformation.clicked.connect(self.fermer_fenetre)

        self.SelectionInfo.addItem('-Praticiens-')
        self.SelectionInfo.addItem('-Médicaments-')

        self.sur_changement()
        self.SelectionInfo.currentTextChanged.connect(self.sur_changement)
        self.listWidgetInfo.itemClicked.connect(self.afficher_informations)

    def sur_changement(self):
        """
            Fonction de sélection de l'information demandée

            Returns
            -------
            None
        """

        self.listWidgetInfo.clear()

        if self.SelectionInfo.currentText() == '-Praticiens-':

            self.infoPraticiens = {}

            requete_info = requests.get(
                Utils.url_api() + '/GSB/medecins',
                cookies=dict(session=visiteur.token))

            if Utils.check_code_status(requete_info.status_code)['status']:

                medecins_json = json.loads(requete_info.text)

                for i in range(len(medecins_json)):
                    nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
                    self.infoPraticiens[nom_total] = medecins_json[i]

                # j'ordonne les noms des praticiens par ordre alphabetique
                infos_praticiens_ordonnes = sorted(self.infoPraticiens.keys(), key=lambda x: x.lower())

                for nom_praticien in infos_praticiens_ordonnes:
                    self.listWidgetInfo.addItem(nom_praticien)

            else:
                pass

        if self.SelectionInfo.currentText() == '-Médicaments-':

            self.infoMedicament = {}

            requete_info = requests.get(
                Utils.url_api() + '/GSB/medicaments',
                cookies=dict(session=visiteur.token))

            if Utils.check_code_status(requete_info.status_code)['status']:

                medicaments_json = json.loads(requete_info.text)

                for i in range(len(medicaments_json)):
                    self.infoMedicament[str(medicaments_json[i]['Label'])] = medicaments_json[i]

                # j'ordonne les noms des praticiens par ordre alphabetique
                infos_medicament_ordonnes = sorted(self.infoMedicament.keys(), key=lambda x: x.lower())

                for nom_medicament in infos_medicament_ordonnes:
                    self.listWidgetInfo.addItem(nom_medicament)

            else:
                pass

        return None

    # fonction pour détruire la page
    def fermer_fenetre(self):
        """
            Fonction de fermeture de la fenetre

            Returns
            -------
            None
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

        return None

    def afficher_informations(self):
        """
            Fonction d'affichage des informations médecins/médicaments

            Returns
            -------
            None
        """

        if self.SelectionInfo.currentText() == '-Praticiens-':

            widget_info_medecin = loadUi("UI/widgets/widget_info_medecin.ui")
            self.StackedWidgetInfo.addWidget(widget_info_medecin)
            self.StackedWidgetInfo.setCurrentWidget(widget_info_medecin)

            if self.listWidgetInfo.count() is not None:
                widget_info_medecin.InfoPrenomPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Prenom']))
                widget_info_medecin.InfoNomPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Nom']))
                widget_info_medecin.InfoCvPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Civilite']))
                widget_info_medecin.InfoAdressePraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Adresse']))
                widget_info_medecin.InfoCPPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['CP']))
                widget_info_medecin.InfoVillePraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Ville']))
                widget_info_medecin.InfoCNPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['CoefNotoriete']))
                widget_info_medecin.InfoSecteurPraticien.setText(
                    str(self.infoPraticiens[self.listWidgetInfo.currentItem().text()]['Secteur_id']))

        if self.SelectionInfo.currentText() == '-Médicaments-':

            widget_info_medicament = loadUi("UI/widgets/widget_info_medicament.ui")
            self.StackedWidgetInfo.addWidget(widget_info_medicament)
            self.StackedWidgetInfo.setCurrentWidget(widget_info_medicament)

            if self.listWidgetInfo.count() is not None:
                widget_info_medicament.InfoLabelPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Label']))
                widget_info_medicament.InfoDatePraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Date']))
                widget_info_medicament.InfoCompPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Composition']))
                widget_info_medicament.InfoEffetPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Effets']))
                widget_info_medicament.InfoCIPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['ContreIndic']))
                widget_info_medicament.InfoPrixPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Prix']))
                widget_info_medicament.InfoStockPraticien.setText(
                    str(self.infoMedicament[self.listWidgetInfo.currentItem().text()]['Stock']))

        return None


class FenetreSaisie(QDialog):
    """
        class pour creer une fenetre qui permet de saisir un compte rendu

        ...

        Attributes
        ----------
        praticiens : dict
            un dictionnaire de praticiens
        medicaments : dict
            un dictionnaire de medicaments
        SelectionPraticiens : obj
            Liste déroulante pour sélectionner les praticiens

        Methods
        -------
        fermer_fenetre (self) :
            Ferme la fenetre la plus récente
        ajouter_medicament (self) :
            Permet d'ajouter un médicament sélectionné dans la liste TableauOffreMedicaments
        envoyer_rapport (self) :
            Permet d'envoyer toutes les informations sélectionnées a l'API
    """
    def __init__(self):
        """
            constructeur des attributs de l'objet FenetreSaisie
        """
        super(FenetreSaisie, self).__init__()
        try:
            loadUi("UI/fenetre_saisie_rapport.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        self.AccueilBouton.clicked.connect(self.fermer_fenetre)

        # dictionnaire des praticiens et des médicaments
        self.praticiens = dict()
        self.medicaments = dict()

        # requete pour obtenir les medecins
        requete = requests.get(
            Utils.url_api() + '/GSB/medecins',
            cookies=dict(session=visiteur.token))

        if Utils.check_code_status(requete.status_code)['status']:

            medecins_json = json.loads(requete.text)
            del requete

            # creation d'un dictionnaire pour lier les noms des praticiens avec leur id
            for i in range(len(medecins_json)):
                nom_total = str(medecins_json[i]['Prenom'] + ' ' + medecins_json[i]['Nom'])
                self.praticiens[nom_total] = {"Id": medecins_json[i]['Id'],
                                              "Secteur_id": medecins_json[i]['Secteur_id']}

            # j'ordonne les noms des praticiens par ordre alphabetique
            self.praticiens_ordonnes = sorted(self.praticiens.keys(), key=lambda x: x.lower())

            # j'ajoute les praticiens ordonnés en fonction du secteur du visiteur
            for nom_praticien in self.praticiens_ordonnes:
                if int(self.praticiens[nom_praticien].get('Secteur_id')) == int(visiteur.secteur):
                    self.SelectionPraticiens.addItem(nom_praticien)

        else:
            pass

        self.SelectionMedicamentNom.addItem("-Aucun-")

        # requete pour obtenir les médicaments
        requete = requests.get(
            Utils.url_api() + '/GSB/medicaments',
            cookies=dict(session=visiteur.token))

        if Utils.check_code_status(requete.status_code)['status']:

            medicaments_json = json.loads(requete.text)
            del requete

            # creation d'un dictionnaire pour lier les noms des médicaments avec leur nombre
            for j in range(len(medicaments_json)):
                self.medicaments[medicaments_json[j]["Label"]] = medicaments_json[j]["Id"]

            # j'ordonne les noms des médicaments par ordre alphabetique
            self.medicaments_ordonnes = sorted(self.medicaments.keys(), key=lambda x: x.lower())
            for nom_medicaments in self.medicaments_ordonnes:
                self.SelectionMedicamentNom.addItem(nom_medicaments)

            # mise a jour de la date à la date du jour
            aujourdhui = date.today()
            aujourdhui_formate = aujourdhui.strftime("%d/%m/%Y")
            qdate_aujourdhui_formate = QDate.fromString(aujourdhui_formate, "dd/MM/yyyy")
            self.DateRapport.setDate(qdate_aujourdhui_formate)

            self.BoutonAjouterMedicament.clicked.connect(self.ajouter_medicament)

            # attribut bouton pour valider ou non le formulaire
            self.BoutonFormulaire.accepted.connect(self.envoyer_rapport)
            self.BoutonFormulaire.rejected.connect(self.fermer_fenetre)

        else:
            pass

    # fonction pour détruire la page
    def fermer_fenetre(self):
        """
            Fonction de fermeture de la fenetre

            Returns
            -------
            None
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

        return None

    # fonction pour ajouter des medicaments a la liste
    def ajouter_medicament(self):
        """
            Fonction d'ajout de médicament dans le rapport'

            Returns
            -------
            None
        """
        # si il y a des éléments de sélectionnés
        if self.SelectionMedicamentNom.currentText() != "-Aucun-" and self.SelectionMedicamentQuantite.text() != "":

            # je crée un dictionnaire contenant tous les médicaments choisis
            liste_medicament_enregistre = {}
            for i in range(0, self.TableauOffreMedicaments.rowCount()):
                liste_medicament_enregistre[self.TableauOffreMedicaments.item(i, 0).text()] = i

            # si le médicament n'a pas déjà été entré, je l'intègre
            if self.SelectionMedicamentNom.currentText() not in liste_medicament_enregistre.keys():
                self.TableauOffreMedicaments.insertRow(self.TableauOffreMedicaments.rowCount())

                self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 0,
                                                     QTableWidgetItem(self.SelectionMedicamentNom.currentText()))
                self.TableauOffreMedicaments.setItem(self.TableauOffreMedicaments.rowCount() - 1, 1,
                                                     QTableWidgetItem(self.SelectionMedicamentQuantite.text()))

            # sinon je modifie la valeur de la quantité
            else:
                self.TableauOffreMedicaments.item(
                    liste_medicament_enregistre[self.SelectionMedicamentNom.currentText()], 1) \
                    .setText(self.SelectionMedicamentQuantite.text())
            del liste_medicament_enregistre
        else:
            print("il manque des informations pour pouvoir ajouter un échantillon")

        return None

    # fonction qui va envoyer les informations validées du formulaire
    def envoyer_rapport(self):
        """
            Fonction d'envoi du rapport

            Returns
            -------
            None
        """
        # je collecte l'ensemble des médicaments
        liste_offre_medicaments = {}
        for i in range(self.TableauOffreMedicaments.rowCount()):
            liste_offre_medicaments[
                self.medicaments[self.TableauOffreMedicaments.item(i, 0).text()]] = self.TableauOffreMedicaments.item(i,
                                                                                                                      1).text()

        # je construis un dictionnaire pour l'envoyer sous format Json
        rapport_json = {"Medecin": self.praticiens[self.SelectionPraticiens.currentText()]['Id'],
                        "Date": self.DateRapport.text(),
                        "Motif": self.Motif.text(),
                        "Bilan": self.Bilan.toPlainText(),
                        "Medoc": liste_offre_medicaments}

        requests.post(
            Utils.url_api() + '/GSB/CR/Insert',
            json=rapport_json,
            headers={'Content-Type': 'application/json'},
            cookies=dict(session=visiteur.token))

        self.fermer_fenetre()

        return None


class FenetreConsultation(QDialog):
    """
        class pour creer une fenetre qui permet de saisir un compte rendu

        ...

        Attributes
        ----------
        validerIdRapport : obj
            un bouton de validation du rapport
        retourConsultation : dict
            un bouton de fermeture de la fenetre retourConsultation

        Methods
        -------
        fermer_fenetre (self) :
            Ferme la fenetre la plus récente
        valider_rapport (self) :
            Permet d'afficher toutes les informations du rapport
    """

    def __init__(self):
        """
            constructeur des attributs de l'objet FenetreConsultation
        """
        super(FenetreConsultation, self).__init__()
        try:
            loadUi("UI/fenetre_consultation_rapport.ui", self)
        except Exception as e:
            logging.exception(e)
            exit()

        # je fais une requete pour obtenir les id des rapports
        url = Utils.url_api() + '/GSB/CR/visiteur'
        requete = requests.get(
            url,
            cookies=dict(session=visiteur.token))

        if Utils.check_code_status(requete.status_code)['status']:

            rapports_json = json.loads(requete.text)
            for id_rapport in rapports_json.keys():
                self.idRapport.addItem(str(id_rapport))

        self.validerIdRapport.clicked.connect(lambda: self.valider_rapport(rapports_json))
        self.retourConsultation.clicked.connect(self.fermer_fenetre)
        self.AccueilBouton.clicked.connect(self.fermer_fenetre)

    def fermer_fenetre(self):
        """
            Fonction de fermeture de la fenetre

            Returns
            -------
            None
        """
        win.stackedWidget.removeWidget(self)
        self.reject()

        return None

    def valider_rapport(self, rapports_json):
        """
            Fonction d'affichage du rapport

            Returns
            -------
            None
        """

        rapport_json = rapports_json[self.idRapport.currentText()]

        # j'attribut les valeurs aux champs adéquats
        self.selectionPraticien.setText(rapport_json['Medecin'])
        self.dateRapport.setText(rapport_json["Date"])
        self.motif.setText(rapport_json["Motif"])
        self.bilan.setPlainText(rapport_json["Bilan"])

        self.tableauOffreMedicaments.setRowCount(0)
        # je remplis la liste des médicaments avec les données du JSON
        for i in range(0, len(rapport_json["Medoc"])):

            self.tableauOffreMedicaments.insertRow(self.tableauOffreMedicaments.rowCount())
            self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 0,
                                                 QTableWidgetItem(rapport_json["Medoc"][i]["Label"]))
            self.tableauOffreMedicaments.setItem(self.tableauOffreMedicaments.rowCount() - 1, 1,
                                                 QTableWidgetItem(str(rapport_json["Medoc"][i]["Nombre"])))


        return None


class Utils:

    @staticmethod
    def url_api():

        # variable contenant l'url de connexion
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
        except Exception as e:
            logging.exception(e)
            exit()

        serveur = config['SERVEUR']
        url = serveur['protocole'] + '://' + serveur['host'] + ':' + serveur['port']

        return url

    @staticmethod
    def check_code_status(status_code):
        """
            Fonction de nettoyage des chaines de caractères

            Si la code correspond a une confirmation,
            alors on retourne un booléen True
            sinon on retourne un booléen False avec un message d'erreur

            Parameters
            ----------
            status_code : int
                code que renvoie la api

            Returns
            -------
            liste_retournee
        """
        liste_retournee = dict()

        if status_code == 200:
            liste_retournee['status'] = True
        elif status_code == 201:
            liste_retournee['status'] = True
        elif status_code == 401:
            liste_retournee['status'] = False
            liste_retournee['error'] = 'Authentification échouée, mauvais identifiants'
        elif status_code == 404:
            liste_retournee['status'] = False
            liste_retournee['error'] = "La ressource n'existe pas"
        elif status_code == 500:
            liste_retournee['status'] = False
            liste_retournee['error'] = "Erreur interne"
        else:
            liste_retournee['status'] = False
            liste_retournee['error'] = "Code de status inconnu"

        return liste_retournee

    @staticmethod
    def nettoyage_str(texte, escape=False, lower=False, alphanum=False):
        """
            Fonction de nettoyage des chaines de caractères

            Si escape, lower et alphanum sont placés en paramètre,
            alors les différentes opérations de nettoyage associées seront appliquées

            Parameters
            ----------
            texte : str, optional
                Texte cible du nettoyage
            escape : str, optional
                Option pour enlever les échappements
            lower : str, optional
                Option pour mettre le texte en minuscule
            alphanum : str, optional
                Option pour enlever tous les caractères qui ne sont pas du type alphanumérique

            Returns
            -------
            texte
        """
        if escape:
            # nettoyage simple des caractères vides et d'échappements
            texte = texte.strip()

        elif lower:
            # nettoyage des caractères vides et d'échappements ainsi que la mise en minuscule
            texte = texte.lower()

        elif alphanum:
            # nettoyage alphanumérique uniquement
            modele = re.compile('[\W_]+')
            texte = modele.sub('', texte)

        else:
            return False

        return texte

    @staticmethod
    def popup(texte, niveau='Information'):

        msg = QMessageBox()
        msg.setWindowTitle(win.windowTitle())
        msg.setText(texte)
        msg.setWindowIcon(win.windowIcon())
        if niveau == 'Information':
            msg.setIcon(QMessageBox.Information)
        elif niveau == 'Question':
            msg.setIcon(QMessageBox.Question)
        elif niveau == 'Warning':
            msg.setIcon(QMessageBox.Warning)
        elif niveau == 'Critical':
            msg.setIcon(QMessageBox.Critical)
        msg.exec_()


app = QApplication(sys.argv)

win = FenetreMaitresse()

# je renome la fenetre
win.setWindowTitle("AppliVisiteur")

win.setWindowIcon(QIcon('imageS/favicon.ico'))

win.show()

if __name__ == '__main__':
    try:
        sys.exit(app.exec_())
    finally:
        print("sortie")

import sys
import unittest
from PyQt6.QtWidgets import QApplication
from applivisiteur import User, Login_page, Index_page, Admin_page, Rapport_page, Stack 
 
class TestApplivisiteur(unittest.TestCase):
	def test_login(self):
		identifiants = [{"statut":200,"login":"admin","mdp":"password"},{"statut":200,"login":"demo","mdp":"password"},{"statut":404,"login":"demoD","mdp":"timentibus3"}] 
		for test in identifiants:
			appStack.login_page.login_input1.setText(test["login"])
			appStack.login_page.login_input2.setText(test["mdp"])
			self.assertEqual(appStack.login_page.login(),test["statut"])

	def test_index(self):

if __name__ == '__main__':
	app = QApplication(sys.argv)
	appStack = Stack()
	unittest.main()



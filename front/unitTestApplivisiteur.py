import sys
import unittest
from PyQt6.QtWidgets import QApplication
from unittest.mock import patch
from applivisiteur import Login_page, Index_page, Rapport_page, Stack, User





class TestApp(unittest.TestCase):
	def __init__():
		super(TestApp, self).__init__()
		self.app = QApplication(sys.argv)
		self.stack = Stack()

	def testLogin(self):
		self.identifiants = [{"statut":200,"login":"pascal","mdp":"password"},{"statut":200,"login":"demo","mdp":"password"},{"statut":404,"login":"demoD","mdp":"timentibus3"}] 
		for test in self.identifiants:
			stack.login_page.login_input1.setText(test["login"])
			stack.login_page.login_input1.setText(test["mdp"])
			self.assertEqual(stack.login_page.login(),test["statut"])

	def tearDown(self):
		del self.stack
		del self.app

if __name__ == '__main__':
    unittest.main()



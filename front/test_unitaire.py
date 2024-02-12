# import unittest
# from unittest.mock import MagicMock, patch
# import requests
# from PyQt6.QtWidgets import QApplication
# from applivisiteur import User, Index_page

# class TestUser(unittest.TestCase):
#     @patch('requests.get')
#     def testgetUserDatas(self, mockget):
#         # Setup
#         mockresponse = MagicMock()
#         mock_response.json.return_value = {"VIS_ADMIN": True, "LOG_LOGIN": "test", "VIS_NOM": "User"}
#         mock_get.return_value = mock_response

#         # Test
#         user = User("access_token", 1)
#         user.getUserDatas()

#         # Assertions
#         self.assertTrue(user.admin)
#         self.assertEqual(user.id, 1)

# class TestIndexPage(unittest.TestCase):
#     @patch('requests.get')
#     def test_setUserDatas(self, mock_get):
#         # Setup
#         mock_response = MagicMock()
#         mock_response.json.return_value = {"LOG_LOGIN": "test", "VIS_NOM": "User"}
#         mock_get.return_value = mock_response

#         app = QApplication([])  # Necessary for widget testing
#         index_page = Index_page()

#         # Mocking user object
#         index_page.appStack = MagicMock()
#         index_page.appStack.user.id = 1
#         index_page.appStack.user.headers = {"Authorization": "Bearer access_token"}

#         # Test
#         index_page.setUserDatas()

#         # Assertions
#         self.assertEqual(index_page.index_label_titre.text(), " Bienvenue test User ")

# if __name__ == '__main__':
#     unittest.main()


 # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 

# import sys
# import unittest
# from PyQt6.QtWidgets import QApplication
from applivisiteur import Login_page, Index_page, Rapport_page, Stack, User

# class TestApp(unittest.TestCase):

#     def setUp(self):
#         self.app = QApplication(sys.argv)
#         self.stack = Stack()

#     def test_login(self):
#         login_page = self.stack.Login_page()
#         login_page.login_input1.setText("pascal")
#         login_page.login_input2.setText("password")
#         login_page.login()
#         # Assert that after login, the current widget is changed
#         self.assertIsInstance(self.stack.currentWidget(), Index_page)
#         # Add more assertions to test the login process

#     def test_index_page(self):
#         # Simulate login first
#         self.stack.launchIndex(access_token="your_access_token", id_user="your_user_id")
#         index_page = self.stack.index_page
#         # Add assertions here to test the index page
#         self.assertEqual(index_page.index_label_titre.text(), "Expected welcome message")
#         # Add more assertions to test the index page

#     def test_rapport_page(self):
#         # Simulate login first
#         self.stack.launchIndex(access_token="your_access_token", id_user="your_user_id")
#         rapport_page = self.stack.rapport_page
#         # Add assertions here to test the rapport page
#         # Example assertion to test if widgets are initialized correctly
#         self.assertEqual(rapport_page.rapport_medecins.count(), 0)  # Expected count of medecins
#         # Add more assertions to test the rapport page

#     def tearDown(self):
#         del self.stack
#         del self.app

# if __name__ == '__main__':
#     unittest.main()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 

# import sys
# import unittest
# from PyQt6.QtWidgets import QApplication
# from unittest.mock import patch


# class TestApp(unittest.TestCase):

#     def setUp(self):
#         self.app = QApplication(sys.argv)
#         self.stack = Stack()

#     @patch('applivisiteur.requests.post')
#     def test_login(self, mock_post):
#         # Mocking the response of the POST request
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.side_effect = [
#             [{"access_token": "your_access_token"}],
#             {"id": "your_user_id"}
#         ]

#         login_page = self.stack.login_page
#         login_page.login_input1.setText("your_username")
#         login_page.login_input2.setText("your_password")
#         login_page.login()

#         # Assertions
#         self.assertIsInstance(self.stack.user, User)
#         self.assertEqual(self.stack.user.access_token, "your_access_token")
#         self.assertEqual(self.stack.user.id, "your_user_id")

#     def tearDown(self):
#         del self.stack
#         del self.app

# if __name__ == '__main__':
#     unittest.main()

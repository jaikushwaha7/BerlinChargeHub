from unittest import TestCase
from unittest.mock import patch, MagicMock

import src.application.login as login_module


class TestHandleLogin(TestCase):
    @patch('src.application.login.st.text_input')
    @patch('src.application.login.st.button')
    @patch('src.application.login.check_credentials')
    def test_handle_login_successful(self, mock_check_credentials, mock_button, mock_text_input):
        # Arrange
        mock_button.return_value = True
        mock_text_input.side_effect = ["test_user", "test_password"]
        mock_check_credentials.return_value = True

        # Act
        result = login_module.handle_login()

        # Assert
        mock_text_input.assert_any_call("Username:", "")
        mock_text_input.assert_any_call("Password:", "", type="password")
        mock_button.assert_called_once_with("Login")
        mock_check_credentials.assert_called_once_with("test_user", "test_password")
        self.assertTrue(result)

    @patch('src.application.login.st.text_input')
    @patch('src.application.login.st.button')
    @patch('src.application.login.check_credentials')
    def test_handle_login_invalid_credentials(self, mock_check_credentials, mock_button, mock_text_input):
        # Arrange
        mock_button.return_value = True
        mock_text_input.side_effect = ["test_user", "wrong_password"]
        mock_check_credentials.return_value = False

        # Act
        result = login_module.handle_login()

        # Assert
        mock_text_input.assert_any_call("Username:", "")
        mock_text_input.assert_any_call("Password:", "", type="password")
        mock_button.assert_called_once_with("Login")
        mock_check_credentials.assert_called_once_with("test_user", "wrong_password")
        self.assertFalse(result)

    @patch('src.application.login.st.text_input')
    @patch('src.application.login.st.button')
    def test_handle_login_no_button_pressed(self, mock_button, mock_text_input):
        # Arrange
        mock_button.return_value = False
        mock_text_input.side_effect = ["test_user", "test_password"]

        # Act
        result = login_module.handle_login()

        # Assert
        mock_text_input.assert_any_call("Username:", "")
        mock_text_input.assert_any_call("Password:", "", type="password")
        mock_button.assert_called_once_with("Login")
        self.assertTrue(result)

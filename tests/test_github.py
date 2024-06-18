import os
import unittest
import requests
from unittest.mock import patch, Mock
from src.github import get_github_user_info

class TestGithub(unittest.TestCase):

    @patch('src.github.requests.get')
    def test_get_github_user_info(self, mock_get):
        github_user_info = {
            "login": "tranculent",
            "id": 45804656,
            "name": "Yanko Mirov",
            "blog": "https://javatutorial.net/author/ym_coding"
        }
        mock_response = Mock()
        mock_response.json.return_value = github_user_info
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_github_user_info("tranculent")
        self.assertEqual(result['name'], 'Yanko Mirov')
        self.assertEqual(result['id'], 45804656)
        self.assertEqual(result['blog'], "https://javatutorial.net/author/ym_coding")

        mock_get.assert_called_once_with(
            'https://api.github.com/users/tranculent',
            headers={'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
        )

    @patch('src.github.requests.get')
    def test_get_github_user_info_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
    
        with self.assertRaises(Exception):
            get_github_user_info("nonexistent_user")

    @patch('src.github.requests.get')
    def test_get_github_user_info_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_github_user_info("tranculent")

if __name__ == '__main__':
    unittest.main()


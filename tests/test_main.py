import os
import unittest
from unittest.mock import patch, Mock
from requests.auth import HTTPBasicAuth
from src.main import create_or_update_freshdesk_contact, get_github_user_info
from src.utils import map_github_user_to_freshdesk_contact

class TestMain(unittest.TestCase):
    def test_get_github_user_info(self):
        github_user_info = get_github_user_info("tranculent")
        self.assertEqual(github_user_info['name'], 'Yanko Mirov')
        self.assertEqual(github_user_info['id'], 45804656)
        self.assertEqual(github_user_info['blog'], "https://javatutorial.net/author/ym_coding")

    def test_map_github_user_to_freshdesk_contact(self):
        github_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "company": "ExampleCorp",
            "twitter_username": "john_doe",
            "id": 123,
            "bio": "A GitHub user"
        }
        expected_contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "job_title": "ExampleCorp",
            "twitter_id": "john_doe",
            "unique_external_id": 123,
            "description": "A GitHub user"
        }
        result = map_github_user_to_freshdesk_contact(github_user)
        self.assertEqual(result, expected_contact)

    # Mock all request functions
    @patch('src.main.requests.post')
    @patch('src.main.requests.put')
    @patch('src.main.requests.get')
    def test_create_or_update_freshdesk_contact(self, mock_get, mock_put, mock_post):
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "unique_external_id": 123
        }
        freshdesk_subdomain = "example"
        freshdesk_token = os.getenv('FRESHDESK_TOKEN')
        
        # Simulate no existing contact
        mock_search_response = Mock()
        mock_search_response.json.return_value = {"total": 0}
        mock_search_response.status_code = 200  # Set status code for successful response
        mock_get.return_value = mock_search_response

        mock_post_response = Mock()
        mock_post_response.json.return_value = {"id": 1}
        mock_post_response.status_code = 201  # Set status code for successful creation
        mock_post.return_value = mock_post_response

        result = create_or_update_freshdesk_contact(freshdesk_subdomain, contact)
        self.assertEqual(result, {"id": 1})

        # Assert GET request for search
        mock_get.assert_called_once_with(
            f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/search/contacts?query="email:{contact["email"]}"',
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(freshdesk_token, 'X')
        )

        # Assert POST request for creating contact
        mock_post.assert_called_once_with(
            f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts',
            json=contact,
            auth=HTTPBasicAuth(freshdesk_token, 'X'),
            headers={'Content-Type': 'application/json'}
        )

        # Simulate existing contact
        mock_search_response.json.return_value = {"total": 1, "results": [{"id": 1}]}
        mock_put_response = Mock()
        mock_put_response.json.return_value = {"id": 1}
        mock_put_response.status_code = 200  # Set status code for successful update
        mock_put.return_value = mock_put_response

        result = create_or_update_freshdesk_contact(freshdesk_subdomain, contact)
        self.assertEqual(result, {"id": 1})

        # Assert PUT request for updating contact
        mock_put.assert_called_once_with(
            f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts/1',
            json=contact,
            auth=HTTPBasicAuth(freshdesk_token, 'X'),
            headers={'Content-Type': 'application/json'}
        )

    @patch('src.main.requests.get')
    def test_get_github_user_info_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_github_user_info("nonexistent_user")
    
    @patch('src.main.requests.get')
    def test_get_github_user_info_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_github_user_info("tranculent")

    @patch('src.main.requests.post')
    @patch('src.main.requests.put')
    @patch('src.main.requests.get')
    def test_create_or_update_freshdesk_contact_no_token(self, mock_get, mock_put, mock_post):
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "unique_external_id": 123
        }
        freshdesk_subdomain = "example"
        
        with patch.dict('os.environ', {'FRESHDESK_TOKEN': ''}):
            with self.assertRaises(SystemExit):
                create_or_update_freshdesk_contact(freshdesk_subdomain, contact)

    @patch('src.main.requests.post')
    @patch('src.main.requests.put')
    @patch('src.main.requests.get')
    def test_create_or_update_freshdesk_contact_search_error(self, mock_get, mock_put, mock_post):
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "unique_external_id": 123
        }
        freshdesk_subdomain = "example"

        mock_search_response = Mock()
        mock_search_response.status_code = 500
        mock_get.return_value = mock_search_response

        with self.assertRaises(SystemExit):
            create_or_update_freshdesk_contact(freshdesk_subdomain, contact)

    @patch('src.main.requests.post')
    @patch('src.main.requests.put')
    @patch('src.main.requests.get')
    def test_create_or_update_freshdesk_contact_create_error(self, mock_get, mock_put, mock_post):
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "unique_external_id": 123
        }
        freshdesk_subdomain = "example"

        mock_search_response = Mock()
        mock_search_response.json.return_value = {"total": 0}
        mock_search_response.status_code = 200
        mock_get.return_value = mock_search_response

        mock_post_response = Mock()
        mock_post_response.status_code = 500
        mock_post.return_value = mock_post_response

        with self.assertRaises(SystemExit):
            create_or_update_freshdesk_contact(freshdesk_subdomain, contact)

    @patch('src.main.requests.post')
    @patch('src.main.requests.put')
    @patch('src.main.requests.get')
    def test_create_or_update_freshdesk_contact_update_error(self, mock_get, mock_put, mock_post):
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "unique_external_id": 123
        }
        freshdesk_subdomain = "example"
        freshdesk_token = os.getenv('FRESHDESK_TOKEN')

        mock_search_response = Mock()
        mock_search_response.json.return_value = {"total": 1, "results": [{"id": 1}]}
        mock_search_response.status_code = 200
        mock_get.return_value = mock_search_response

        mock_put_response = Mock()
        mock_put_response.status_code = 500
        mock_put.return_value = mock_put_response

        with self.assertRaises(SystemExit):
            create_or_update_freshdesk_contact(freshdesk_subdomain, contact)

if __name__ == '__main__':
    unittest.main()

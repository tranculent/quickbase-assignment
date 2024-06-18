import os
import unittest
import requests
from unittest.mock import patch, Mock
from requests.auth import HTTPBasicAuth
from src.freshdesk import create_or_update_freshdesk_contact
#from requests.exceptions import Exception

class TestFreshdesk(unittest.TestCase):

    @patch('src.freshdesk.requests.post')
    @patch('src.freshdesk.requests.put')
    @patch('src.freshdesk.requests.get')
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
        mock_search_response.status_code = 200
        mock_get.return_value = mock_search_response

        mock_post_response = Mock()
        mock_post_response.json.return_value = {"id": 1}
        mock_post_response.status_code = 201
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
        mock_put_response.status_code = 200
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

    @patch('src.freshdesk.requests.post')
    @patch('src.freshdesk.requests.put')
    @patch('src.freshdesk.requests.get')
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
    
    @patch('src.freshdesk.requests.post')
    @patch('src.freshdesk.requests.put')
    @patch('src.freshdesk.requests.get')
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

    @patch('src.freshdesk.requests.post')
    @patch('src.freshdesk.requests.put')
    @patch('src.freshdesk.requests.get')
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

    @patch('src.freshdesk.requests.post')
    @patch('src.freshdesk.requests.put')
    @patch('src.freshdesk.requests.get')
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


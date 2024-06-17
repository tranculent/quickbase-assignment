import unittest
from unittest.mock import patch, Mock
import src.main as main

class TestMain(unittest.TestCase):

    # @patch('src.main.requests.get')
    def test_get_github_user_info(self):
        '''mock_response = Mock()
        mock_response.json.return_value = {
            "name": "Yanko Mirov",
            "email": "yanicha93@gmail.com",
            "twitter_username": "john_doe",
            "id": 123,
            "bio": "Software engineer @ Cern"
        }
        mock_get.return_value = mock_response
'''
        github_user_info = main.get_github_user_info("tranculent")
        self.assertEqual(github_user_info['name'], 'Yanko Mirov')
        self.assertEqual(github_user_info['id'], 45804656)
        self.assertEqual(github_user_info['blog'], "https://javatutorial.net/author/ym_coding")
'''
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
        result = main.map_github_user_to_freshdesk_contact(github_user)
        self.assertEqual(result, expected_contact)

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
        freshdesk_token = "fake_token"

        # Simulate no existing contact
        mock_search_response = Mock()
        mock_search_response.json.return_value = {"total": 0}
        mock_search_response.raise_for_status = Mock()
        mock_get.return_value = mock_search_response

        mock_post_response = Mock()
        mock_post_response.json.return_value = {"id": 1}
        mock_post_response.raise_for_status = Mock()
        mock_post.return_value = mock_post_response

        result = main.create_or_update_freshdesk_contact(contact, freshdesk_subdomain, freshdesk_token)
        self.assertEqual(result, {"id": 1})
        mock_post.assert_called_once_with(
            f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts',
            json=contact,
            auth=main.HTTPBasicAuth(freshdesk_token, 'X'),
            headers={'Content-Type': 'application/json'}
        )

        # Simulate existing contact
        mock_search_response.json.return_value = {"total": 1, "results": [{"id": 1}]}
        mock_put_response = Mock()
        mock_put_response.json.return_value = {"id": 1}
        mock_put_response.raise_for_status = Mock()
        mock_put.return_value = mock_put_response

        result = main.create_or_update_freshdesk_contact(contact, freshdesk_subdomain, freshdesk_token)
        self.assertEqual(result, {"id": 1})
        mock_put.assert_called_once_with(
            f'https://{freshdesk_subdomain}.freshdesk.com/api/v2/contacts/1',
            json=contact,
            auth=main.HTTPBasicAuth(freshdesk_token, 'X'),
            headers={'Content-Type': 'application/json'}
        )
'''
if __name__ == '__main__':
    unittest.main()

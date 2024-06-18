import unittest
from src.utils import map_github_user_to_freshdesk_contact

class TestUtils(unittest.TestCase):

    def test_map_github_user_to_freshdesk_contact(self):
        github_user = {
            "id": 12345,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "bio": "Software Developer",
            "twitter_username": "johndoe",
            "company": "Example Inc."
        }

        expected_contact = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "unique_external_id": 12345,
            "description": "Software Developer",
            "twitter_id": "johndoe",
            "job_title": "Example Inc."
        }

        result = map_github_user_to_freshdesk_contact(github_user)
        self.assertEqual(result, expected_contact)

if __name__ == '__main__':
    unittest.main()


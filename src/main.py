import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from src.utils import map_github_user_to_freshdesk_contact

def get_github_user_info(username):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': f'token {github_token}'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
       raise Exception(f"Failed to fetch GitHub user data: {response.status_code} {response.text}")
       sys.exit(1)

    return response.json()

def create_or_update_freshdesk_contact(subdomain, contact_data):
    freshdesk_token = os.getenv('FRESHDESK_TOKEN')
    if not freshdesk_token:
        print("Error: FRESHDESK_TOKEN environment variable not set.")
        sys.exit(1)

    url = f'https://{subdomain}.freshdesk.com/api/v2/contacts'

    # Content type is specified because we are passing request body (the freshdesk contact's data)
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(freshdesk_token, 'X')
    
    # Check if contact exists
    search_url = f'https://{subdomain}.freshdesk.com/api/v2/search/contacts?query="email:{contact_data["email"]}"'
    search_response = requests.get(search_url, headers=headers, auth=auth)
    if search_response.status_code != 200:
        print(f"Error: Unable to search Freshdesk contact (status code {search_response.status_code})")
        sys.exit(1)

    search_results = search_response.json()
    if search_results['total'] > 0:
        print(f'Updating user {contact_data["email"]}..')
        contact_id = search_results['results'][0]['id']
        update_url = f'{url}/{contact_id}'
        response = requests.put(update_url, json=contact_data, headers=headers, auth=auth)
    else:
        print(f'Creating user {contact_data["email"]}..')
        response = requests.post(url, json=contact_data, headers=headers, auth=auth)

    if response.status_code not in [200, 201]:
        print(f"Error: Unable to create/update Freshdesk contact (status code {response.status_code})")
        sys.exit(1)

    return response.json()

def main():
    if len(sys.argv) != 3:
        print("Usage: github_to_freshdesk <github_username> <freshdesk_subdomain>")
        sys.exit(1)

    github_username = sys.argv[1]
    freshdesk_subdomain = sys.argv[2]

    try:
        github_user = get_github_user_info(github_username)
        contact_data = map_github_user_to_freshdesk_contact(github_user)
        result = create_or_update_freshdesk_contact(freshdesk_subdomain, contact_data)
        print("Contact created/updated successfully:", result)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

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


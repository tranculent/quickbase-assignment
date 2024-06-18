import os
import sys
import requests

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


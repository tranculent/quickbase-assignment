import os
import sys
from src.github import get_github_user_info
from src.freshdesk import create_or_update_freshdesk_contact
from src.utils import map_github_user_to_freshdesk_contact

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <github_username> <freshdesk_subdomain>")
        sys.exit(1)

    github_username = sys.argv[1]
    freshdesk_subdomain = sys.argv[2]

    github_user_info = get_github_user_info(github_username)
    contact_data = map_github_user_to_freshdesk_contact(github_user_info)

    result = create_or_update_freshdesk_contact(freshdesk_subdomain, contact_data)
    print("Operation successful. Contact ID:", result.get("id"))

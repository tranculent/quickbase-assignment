def map_github_user_to_freshdesk_contact(github_user):
    contact = {
        "name": github_user.get("name"),
        "email": github_user.get("email"),
        "job_title": github_user.get("company"),
        "twitter_id": github_user.get("twitter_username"),
        "unique_external_id": github_user.get("id"),
        "description": github_user.get("bio")
    }
    return {k: v for k, v in contact.items() if v}


def map_github_user_to_freshdesk_contact(github_user):
    return {
        "name": github_user.get("name"),
        "email": github_user.get("email"),
        "unique_external_id": github_user.get("id"),
        "description": github_user.get("bio"),
        "twitter_id": github_user.get("twitter_username"),
        "job_title": github_user.get("company"),
    }


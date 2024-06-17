
# GitHub to Freshdesk Contact Sync

This command-line Python program retrieves information about a GitHub user and creates or updates a corresponding contact in Freshdesk.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies using pip:
4. Set environment variables by navigating to the root directory and running `set_env.bat`. Make sure you replace the 'your_github_token' and 'your_freshdesk_token' with your personal tokens. Please note this will only set them during this session so it has to be run every time you want to run the program. You can also permanently set them via adding them as keys (GITHUB_TOKEN & FRESHDESK_TOKEN) in Environment Variables in the `User variables` section.

```sh
pip install -r requirements.txt


# GitHub to Freshdesk Contact Sync

This command-line Python program retrieves information about a GitHub user and creates or updates a corresponding contact in Freshdesk.

## Requirements

- Python 3.x
- `requests` library

To install all requirements, run:

```sh
pip install -r requirements.txt
```

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies using pip:
4. Set environment variables by navigating to the root directory and running `set_env.bat`. Make sure you replace the 'your_github_token' and 'your_freshdesk_token' with your personal tokens. Please note this will only set them during this session so it has to be run every time you want to run the program. You can also permanently set them via adding them as keys (GITHUB_TOKEN & FRESHDESK_TOKEN) in Environment Variables in the `User variables` section.

## setup.py
`setup.py` provides metadata about the package and defines (using basic rules) how it should be packaged and distributed. It installs all dependencies automatically when the package is installed.

### Method 1: Run as Administrator (Windows)

1. Open Command Prompt as Administrator:
    - Right-click on the Command Prompt icon.
    - Select "Run as administrator".

2. Run the installation command:
    ```sh
    python setup.py install
    ```

### Method 2: Install for User

1. Run the installation command with the `--user` flag:
    ```sh
    python setup.py install --user
    ```

After installation, you can run the script from the command line:

```sh
github_to_freshdesk <github_username> <freshdesk_subdomain>
```

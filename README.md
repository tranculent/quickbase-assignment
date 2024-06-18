
# GitHub to Freshdesk Contact Sync

This command-line Python program retrieves information about a GitHub user and creates or updates a corresponding contact in Freshdesk.

## Requirements

- Python 3.x
- `requests` library

To install all requirements, run:

```sh
pip install -r requirements.txt
```

## Setting Environment Variables

Before running the program or tests, you need to set the GitHub and Freshdesk tokens as environment variables. You can use the provided `set_env.bat` script for this purpose.

1. Open `set_env.bat` and replace the placeholders with your actual tokens:
    ```bat
    $env:GITHUB_TOKEN=your_github_token_here
    $env:FRESHDESK_TOKEN=your_freshdesk_token_here
    ```

2. Run the script to set the environment variables:
    ```sh
    set_env.bat
    ```

Alternatively, you can set the environment variables directly in your shell:

### Windows (PowerShell)
```sh
$env:GITHUB_TOKEN=your_github_token_here
$env:FRESHDESK_TOKEN=your_freshdesk_token_here
```

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies using pip:
4. Set environment variables by navigating to the root directory and running `set_env.bat`. Make sure you replace the 'your_github_token' and 'your_freshdesk_token' with your personal tokens. Please note this will only set them during this session so it has to be run every time you want to run the program. You can also permanently set them via adding them as keys (GITHUB_TOKEN & FRESHDESK_TOKEN) in Environment Variables in the `User variables` section.

After installation, you can run the script from the command line:
```sh
python src/main.py <github_username> <freshdesk_subdomain>
```

## Run tests
```sh
python -m unittest discover tests
```

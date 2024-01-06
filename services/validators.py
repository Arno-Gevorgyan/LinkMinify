# Standard library imports
import re
import requests
from urllib.parse import urlparse

# Third-party imports
from starlette.exceptions import HTTPException


def validate_password_server(value):
    """ need this for admin and if password is wrong raise exception """

    password_regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')
    if not re.match(password_regex, value):
        raise HTTPException(status_code=400,
                            detail="Invalid password format. "
                                   "Your password must be at least 8 characters long and "
                                   "include at least one uppercase letter, one lowercase letter,"
                                   " one number, and one special character.")
    return value


def is_valid_url(url: str) -> bool:
    """
    Validates if the given string is a well-formed URL.

    This function parses the URL and checks if it has a valid scheme and netloc.
    It's used to ensure that the URL provided is structurally correct before any further processing.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_reachable_url(url: str) -> bool:
    """
    Checks if the given URL is reachable by making a head request.

    This function attempts to make a head request to the URL to determine if it's accessible.
    It's used to ensure the URL not only is well-formed but also reaches an active website.

    Args:
        url (str): The URL to check for reachability.

    Returns:
        bool: True if the URL is reachable (status code 200), False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

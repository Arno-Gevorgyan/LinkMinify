# Standard library imports
import re


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

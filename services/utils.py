import hashlib


def generate_short_url(full_url: str) -> str:
    """
    Generates a short URL from a given full URL.

    This function uses SHA-256 hashing to create a unique identifier from the full URL,
    and then truncates it to create a short ID. This ID is appended to a base URL to
    form the complete short URL.

    Args:
        full_url (str): The full URL to be shortened.

    Returns:
        str: The generated short URL.
    """
    hash_object = hashlib.sha256(full_url.encode())
    hash_digest = hash_object.hexdigest()
    short_id = hash_digest[:6]
    short_url = f"https://short.com/{short_id}"
    return short_url

from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_phone_number(phone_number: str) -> bool:
    """
    Validates the phone number format.

    The phone number must:
    - Start with an optional '+'.
    - Followed by an optional '1'.
    - Contain between 9 to 15 digits.

    Examples of valid formats:
    - +12345678901
    - 1234567890
    - +11234567890

    Args:
        phone_number (str): The phone number string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Define the regex pattern
    pattern = re.compile(r"^\+?1?\d{9,15}$")

    # Use fullmatch to ensure the entire string matches the pattern
    if pattern.fullmatch(phone_number):
        return True
    return False

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the hasher
ph = PasswordHasher()


def verify_password(hashed_password: str, confirm_password: str):
    try:
        return ph.verify(hashed_password, confirm_password)
    except VerifyMismatchError:
        return False


def hash_password(password: str):
    return ph.hash(password)

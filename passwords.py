"""
Password helpers using bcrypt.

bcrypt turns a password into a one-way "hash". We store only the hash.
When someone logs in, bcrypt hashes what they typed and compares.
Nobody (not even the database admin) can read the original password.
"""

import bcrypt

# bcrypt only looks at the first 72 bytes of a password, and newer
# versions of the library refuse longer ones, so we check this ourselves.
MAX_PASSWORD_BYTES = 72


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash (as text) for the given password."""
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()  # random salt, default cost factor 12
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def check_password(plain_password: str, stored_hash: str) -> bool:
    """Return True if the password matches the stored bcrypt hash."""
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > MAX_PASSWORD_BYTES:
        return False
    return bcrypt.checkpw(password_bytes, stored_hash.encode("utf-8"))
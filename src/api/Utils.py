import base64
import os


def hash_to_bytes(hashed: str):
    """Convert an Argon2 hash to bytes"""
    return base64.b64decode(hashed.split('$')[-1] + '=')


def get_dir():
    """Get the current working directory"""
    return os.getcwd() + '/'

#PROJECT AEGIS - STEGLAB
#Version 1.2.0

import os
import base64
import hashlib

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str) -> bytes:
    """
    Generate a 256-bit AES key from a password.
    """
    return hashlib.sha256(password.encode("utf-8")).digest()

def encrypt(text: str, password: str) -> str:
    """
    Encrypt text using AES-256 (CBC mode).
    """

    key = derive_key(password)

    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode("utf-8")) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode("utf-8")

def decrypt(ciphertext: str, password: str) -> str:
    """
    Decrypt AES-256 encrypted text.
    """

    key = derive_key(password)

    try:
        encrypted = base64.b64decode(ciphertext)

        iv = encrypted[:16]
        ciphertext = encrypted[16:]

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )

        decryptor = cipher.decryptor()

        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()

        plaintext = unpadder.update(padded) + unpadder.finalize()

        return plaintext.decode("utf-8")

    except Exception:
        raise ValueError("Invalid AES data or incorrect password.")
# PROJECT AEGIS - STEGLAB
# Version 1.3.0

"""Password-based AES-GCM encryption for AEGIS encrypted payload format v1.

Binary layout before Base64 encoding::

    8-byte magic | 1-byte version | 16-byte salt | 12-byte nonce |
    AES-GCM ciphertext | 16-byte authentication tag

The complete 37-byte header is authenticated as AES-GCM associated data.
Format v1 fixes scrypt parameters at N=2**15, r=8, p=3 (32 MiB working set).
The legacy CBC decoder is intentionally separate and cannot authenticate data.
"""

import base64
import binascii
import hashlib
import os
import struct

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"AEGISENC"
FORMAT_VERSION = 1
SALT_BYTES = 16
NONCE_BYTES = 12
TAG_BYTES = 16
KEY_BYTES = 32
SCRYPT_N = 2**15
SCRYPT_R = 8
SCRYPT_P = 3
HEADER_PREFIX = struct.Struct(">8sB")
HEADER_BYTES = HEADER_PREFIX.size + SALT_BYTES + NONCE_BYTES
INVALID_DATA_MESSAGE = "Invalid encrypted data or incorrect password."


def _password_bytes(password: str) -> bytes:
    if not isinstance(password, str):
        raise TypeError("Password must be text.")
    if not password:
        raise ValueError("Password cannot be empty.")
    return password.encode("utf-8")


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit v1 key from a password and its random 16-byte salt."""
    password_data = _password_bytes(password)
    if not isinstance(salt, (bytes, bytearray, memoryview)):
        raise TypeError("Salt must be bytes-like data.")
    salt = bytes(salt)
    if len(salt) != SALT_BYTES:
        raise ValueError(f"Salt must contain exactly {SALT_BYTES} bytes.")

    kdf = Scrypt(
        salt=salt,
        length=KEY_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return kdf.derive(password_data)


def encrypt(text: str, password: str) -> str:
    """Encrypt UTF-8 text into Base64-encoded AES-256-GCM format v1."""
    if not isinstance(text, str):
        raise TypeError("Plaintext must be text.")

    salt = os.urandom(SALT_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    header = HEADER_PREFIX.pack(MAGIC, FORMAT_VERSION) + salt + nonce
    key = derive_key(password, salt)
    encrypted = AESGCM(key).encrypt(nonce, text.encode("utf-8"), header)
    return base64.b64encode(header + encrypted).decode("ascii")


def decrypt(ciphertext: str, password: str) -> str:
    """Authenticate and decrypt a v1 payload; never try CBC automatically."""
    if not isinstance(ciphertext, str):
        raise TypeError("Encrypted payload must be Base64 text.")

    try:
        payload = base64.b64decode(ciphertext, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError(INVALID_DATA_MESSAGE) from None

    if len(payload) < HEADER_BYTES + TAG_BYTES:
        raise ValueError(INVALID_DATA_MESSAGE)

    header = payload[:HEADER_BYTES]
    magic, version = HEADER_PREFIX.unpack(header[: HEADER_PREFIX.size])
    if magic != MAGIC:
        raise ValueError(INVALID_DATA_MESSAGE)
    if version != FORMAT_VERSION:
        raise ValueError(f"Unsupported AES payload version: {version}.")

    salt_start = HEADER_PREFIX.size
    salt_end = salt_start + SALT_BYTES
    salt = header[salt_start:salt_end]
    nonce = header[salt_end:]

    try:
        key = derive_key(password, salt)
        # AESGCM returns plaintext only after the tag and AAD authenticate.
        plaintext = AESGCM(key).decrypt(nonce, payload[HEADER_BYTES:], header)
        return plaintext.decode("utf-8")
    except (InvalidTag, UnicodeDecodeError, TypeError, ValueError):
        raise ValueError(INVALID_DATA_MESSAGE) from None


def decrypt_legacy_cbc(ciphertext: str, password: str) -> str:
    """Best-effort v1.2 CBC decryption; this legacy format is unauthenticated.

    This function is never called by :func:`decrypt`. Even when CBC padding and
    UTF-8 decoding succeed, callers cannot determine whether the ciphertext was
    modified or whether the password was correct.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("Encrypted payload must be Base64 text.")

    try:
        encrypted = base64.b64decode(ciphertext, validate=True)
        if len(encrypted) < 32 or (len(encrypted) - 16) % 16 != 0:
            raise ValueError("Invalid legacy CBC length.")

        password_data = _password_bytes(password)
        key = hashlib.sha256(password_data).digest()
        iv, encrypted_data = encrypted[:16], encrypted[16:]
        decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return plaintext.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, TypeError, ValueError):
        raise ValueError(
            "Invalid legacy CBC data or incorrect password; CBC is unauthenticated."
        ) from None

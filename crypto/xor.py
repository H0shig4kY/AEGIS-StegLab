# PROJECT AEGIS - STEGLAB
# Version 1.2.0

import base64


def encrypt(text: str, key: str) -> str:
    """
    Encrypt text using XOR and encode the result in Base64.
    """

    text_bytes = text.encode("utf-8")
    key_bytes = key.encode("utf-8")

    encrypted = bytearray()

    for i, byte in enumerate(text_bytes):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])

    return base64.b64encode(encrypted).decode("ascii")


def decrypt(text: str, key: str) -> str:
    """
    Decode Base64 and decrypt using XOR.
    """

    key_bytes = key.encode("utf-8")

    try:
        encrypted = base64.b64decode(text)
    except Exception:
        raise ValueError("Invalid encrypted data.")

    decrypted = bytearray()

    for i, byte in enumerate(encrypted):
        decrypted.append(byte ^ key_bytes[i % len(key_bytes)])

    return decrypted.decode("utf-8")
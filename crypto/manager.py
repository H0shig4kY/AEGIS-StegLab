# PROJECT AEGIS - STEGLAB
# Version 1.2.0

from crypto.caesar import encrypt as caesar_encrypt
from crypto.caesar import decrypt as caesar_decrypt

from crypto.xor import encrypt as xor_encrypt
from crypto.xor import decrypt as xor_decrypt


def encrypt(data: str, algorithm: str, key):
    """
    Encrypt data using the selected algorithm.
    """

    algorithm = algorithm.lower()

    if algorithm == "caesar":
        return caesar_encrypt(data, int(key))

    elif algorithm == "xor":
        return xor_encrypt(data, key)

    raise ValueError("Unsupported encryption algorithm.")


def decrypt(data: str, algorithm: str, key):
    """
    Decrypt data using the selected algorithm.
    """

    algorithm = algorithm.lower()

    if algorithm == "caesar":
        return caesar_decrypt(data, int(key))

    elif algorithm == "xor":
        try:
            return xor_decrypt(data, key)
        except Exception:
            raise ValueError("Invalid XOR data or incorrect password.")

    raise ValueError("Unsupported encryption algorithm.")
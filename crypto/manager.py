# PROJECT AEGIS - STEGLAB
# Version 1.2.0

from crypto.caesar import encrypt as caesar_encrypt
from crypto.caesar import decrypt as caesar_decrypt

from crypto.xor import encrypt as xor_encrypt
from crypto.xor import decrypt as xor_decrypt

from crypto.vigenere import encrypt as vigenere_encrypt
from crypto.vigenere import decrypt as vigenere_decrypt


def encrypt(data: str, algorithm: str, key):
    """
    Encrypt data using the selected algorithm.
    """

    algorithm = algorithm.lower()

    if algorithm == "caesar":
        return caesar_encrypt(data, int(key))

    elif algorithm == "xor":
        return xor_encrypt(data, key)
    elif algorithm == "vigenere":
        return vigenere_encrypt(data, key)

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
    elif algorithm == "vigenere":
        return vigenere_decrypt(data, key)

    raise ValueError("Unsupported encryption algorithm.")
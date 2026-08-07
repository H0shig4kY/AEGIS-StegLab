# PROJECT AEGIS - STEGLAB
# Version 1.2.0


def encrypt(text: str, key: str) -> str:
    """
    Encrypt text using the Vigenère cipher.
    """

    result = []
    key = key.lower()
    key_index = 0

    for char in text:

        if char.isalpha():

            shift = ord(key[key_index % len(key)]) - ord("a")

            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))

            key_index += 1

        else:
            result.append(char)

    return "".join(result)


def decrypt(text: str, key: str) -> str:
    """
    Decrypt text using the Vigenère cipher.
    """

    result = []
    key = key.lower()
    key_index = 0

    for char in text:

        if char.isalpha():

            shift = ord(key[key_index % len(key)]) - ord("a")

            if char.isupper():
                result.append(chr((ord(char) - 65 - shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 - shift) % 26 + 97))

            key_index += 1

        else:
            result.append(char)

    return "".join(result)
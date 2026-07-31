#PROJECT AEGIS - STEGLAB
#Version 1.0.0

# Function to encrypt file text
# Using file given in input by user
# Create another file to save the encrypt result
"""
Caesar cipher implementation.
"""

def encrypt(text: str, shift: int) -> str:
    """
    Encrypt text using the Caesar cipher.
    """
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char.isalpha():

            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)

            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)

        else:
            result += char

    return result

def decrypt(text: str, shift: int) -> str:
    """
    Decrypt text using the Caesar cipher.
    """
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char.isalpha():

            if char.isupper():
                result += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) - shift - 97) % 26 + 97)

        else:
            result += char

    return result
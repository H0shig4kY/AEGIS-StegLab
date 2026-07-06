import codecs
from bitstring import BitArray
import binascii


def rgb2hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to a hexadecimal color string.
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex2rgb(hexcode: str):
    """
    Convert a hexadecimal color string to an RGB tuple.
    """
    if hexcode is None:
        return None

    return tuple(codecs.decode(hexcode[1:], "hex"))

def hex2bit(hexcode: str) -> str:
    """
    Convert a hexadecimal color string to its binary representation.
    """
    hexcode = hexcode.replace("#", "0x")
    bitstring = BitArray(hexcode)
    return bitstring.bin

def bit2hex(bitstring: str):
    """
    Convert a binary string to a hexadecimal color string.
    """
    # TODO(M1): Investigate duplicated condition inherited from legacy.py.

    for i in range(4, 20, 4):
        bits = "0" * i

        if bitstring[:i] == bits:
            return "#000000"

        elif bitstring[:i] == bits:
            hexcode = hex(int(bitstring, 2))
            hexcode = "#" + "0" * (i % 4) + hexcode[2:]
            return hexcode

    if bitstring == "":
        return None

    hexcode = hex(int(bitstring, 2))
    hexcode = hexcode.replace("0x", "#")

    return hexcode

def str2bin(message: str) -> str:
    """
    Convert a string into its binary representation.
    """
    binary = bin(int(binascii.hexlify(message.encode()), 16))
    return binary[2:]

def bin2str(binary: str) -> str:
    """
    Convert a binary string back into a UTF-8 string.
    """
    binary = int("0b" + binary, 2)
    message = binary.to_bytes(
        (binary.bit_length() + 7) // 8,
        "big"
    ).decode()

    return message
# PROJECT AEGIS - STEGLAB
# Version 1.3.0

"""Small, width-preserving conversions used by the StegLab core."""


def _validate_rgb_component(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 255:
        raise ValueError("RGB components must be integers from 0 to 255.")


def rgb2hex(r: int, g: int, b: int) -> str:
    """Convert three 8-bit RGB components to a six-digit hex color."""
    for component in (r, g, b):
        _validate_rgb_component(component)
    return f"#{r:02x}{g:02x}{b:02x}"


def hex2rgb(hexcode: str) -> tuple[int, int, int]:
    """Convert a six-digit RGB hex color, with or without ``#``, to RGB."""
    if not isinstance(hexcode, str):
        raise ValueError("Hex color must be a string.")
    value = hexcode.removeprefix("#")
    if len(value) != 6:
        raise ValueError("Hex color must contain exactly six hexadecimal digits.")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise ValueError("Hex color contains a non-hexadecimal character.") from exc


def hex2bit(hexcode: str) -> str:
    """Convert a six-digit RGB color into exactly 24 bits."""
    r, g, b = hex2rgb(hexcode)
    return f"{(r << 16) | (g << 8) | b:024b}"


def bit2hex(bitstring: str) -> str:
    """Convert exactly 24 RGB bits to a six-digit hex color."""
    if len(bitstring) != 24 or any(bit not in "01" for bit in bitstring):
        raise ValueError("RGB bit strings must contain exactly 24 bits.")
    return f"#{int(bitstring, 2):06x}"


def bytes2bin(data: bytes | bytearray | memoryview) -> str:
    """Convert bytes to a byte-aligned binary string without dropping zeros."""
    return "".join(f"{byte:08b}" for byte in bytes(data))


def bin2bytes(binary: str) -> bytes:
    """Convert a byte-aligned binary string back to its exact byte sequence."""
    if len(binary) % 8 != 0 or any(bit not in "01" for bit in binary):
        raise ValueError("Binary payload must contain only bits in complete bytes.")
    return bytes(int(binary[i : i + 8], 2) for i in range(0, len(binary), 8))


def str2bin(message: str | bytes | bytearray | memoryview) -> str:
    """UTF-8 encode text, or preserve supplied bytes, as byte-aligned bits."""
    if isinstance(message, str):
        data = message.encode("utf-8")
    elif isinstance(message, (bytes, bytearray, memoryview)):
        data = bytes(message)
    else:
        raise TypeError("Message must be text or bytes-like data.")
    return bytes2bin(data)


def bin2str(binary: str) -> str:
    """Decode byte-aligned binary data as UTF-8 text."""
    return bin2bytes(binary).decode("utf-8")

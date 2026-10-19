# PROJECT AEGIS - STEGLAB
# Version 1.3.0

"""Explicit best-effort reader for the v1.2.0 blue-channel LSB format.

The legacy format is UTF-8 text bits followed by the 16-bit sentinel 0xfffe.
It carries no length or integrity check, so sentinel-like content can truncate
the message and malformed data may be unrecoverable. This module is isolated
from the current versioned decoder and is never selected automatically.
"""

from pathlib import Path
import os

from PIL import Image

from core.decoder import _atomic_write_bytes

LEGACY_SENTINEL = "1111111111111110"


def extract_v12_text(filename: str | Path) -> str:
    """Best-effort extraction of a v1.2.0 UTF-8 text payload."""
    with Image.open(filename) as source:
        image = source.convert("RGBA")

    pixels = image.load()
    width, height = image.size
    bits = []
    for index in range(width * height):
        x, y = index % width, index // width
        bits.append(str(pixels[x, y][2] & 1))
        if len(bits) >= len(LEGACY_SENTINEL) and "".join(bits[-len(LEGACY_SENTINEL):]) == LEGACY_SENTINEL:
            payload_bits = "".join(bits[:-len(LEGACY_SENTINEL)])
            if not payload_bits:
                return ""
            value = int(payload_bits, 2)
            payload = value.to_bytes((value.bit_length() + 7) // 8, "big")
            return payload.decode("utf-8")

    raise ValueError("No complete v1.2.0 LSB sentinel was found.")


def retr_legacy_v12(filename: str | Path, filetosave: str | Path) -> str:
    """Explicitly extract a legacy v1.2.0 message to an output file."""
    source, destination = Path(filename), Path(filetosave)
    same_file = source.resolve() == destination.resolve()
    if not same_file:
        try:
            same_file = os.path.samefile(source, destination)
        except (FileNotFoundError, OSError):
            pass
    if same_file:
        return "[ERROR] Output file cannot overwrite the source image."
    try:
        text = extract_v12_text(filename)
        _atomic_write_bytes(destination, text.encode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return f"[ERROR] Legacy v1.2.0 extraction failed: {exc}"
    return "[SUCCESS] Legacy v1.2.0 message extracted (best effort)."

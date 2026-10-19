# PROJECT AEGIS - STEGLAB
# Version 1.3.0

from pathlib import Path
import os
import tempfile

from PIL import Image

from core.framing import frame_payload


def encode(bitstring: str, digit: str) -> str:
    """Replace the low bit of a 24-bit RGB string with one payload bit."""
    if len(bitstring) != 24 or any(bit not in "01" for bit in bitstring):
        raise ValueError("RGB bit strings must contain exactly 24 bits.")
    if digit not in ("0", "1"):
        raise ValueError("Payload digit must be '0' or '1'.")
    return bitstring[:-1] + digit


def _as_bytes(message: str | bytes | bytearray | memoryview) -> bytes:
    if isinstance(message, str):
        return message.encode("utf-8")
    if isinstance(message, (bytes, bytearray, memoryview)):
        return bytes(message)
    raise TypeError("Message must be text or bytes-like data.")


def _same_path(source: str | Path, destination: str | Path) -> bool:
    source_path = Path(source)
    destination_path = Path(destination)
    if source_path.resolve() == destination_path.resolve():
        return True
    try:
        return os.path.samefile(source_path, destination_path)
    except (FileNotFoundError, OSError):
        return False


def _atomic_save_png(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
        image.save(temp_path, format="PNG")
        os.replace(temp_path, destination)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def hide(
    filename: str | Path,
    output_image: str | Path,
    message: str | bytes | bytearray | memoryview,
    *,
    overwrite_source: bool = False,
) -> str:
    """Embed a byte-framed payload in the blue-channel LSB of a PNG.

    Each pixel carries one bit. The encoder checks capacity itself, preserves
    alpha, and refuses to overwrite the source unless explicitly requested.
    """
    destination = Path(output_image)
    if destination.suffix.lower() != ".png":
        raise ValueError("LSB output must use the .png extension.")
    if _same_path(filename, output_image) and not overwrite_source:
        raise ValueError("Output image cannot overwrite the source image.")

    payload = _as_bytes(message)
    framed = frame_payload(payload)

    with Image.open(filename) as source:
        image = source.convert("RGBA")

    width, height = image.size
    capacity_bits = width * height
    required_bits = len(framed) * 8
    if required_bits > capacity_bits:
        raise ValueError(
            f"Payload requires {required_bits} bits, but the image holds "
            f"{capacity_bits} bits."
        )

    pixels = image.load()
    for bit_index in range(required_bits):
        x, y = bit_index % width, bit_index // width
        byte = framed[bit_index // 8]
        bit = (byte >> (7 - (bit_index % 8))) & 1
        red, green, blue, alpha = pixels[x, y]
        pixels[x, y] = (red, green, (blue & 0xFE) | bit, alpha)

    _atomic_save_png(image, destination)
    return "[SUCCESS] Message hidden successfully."

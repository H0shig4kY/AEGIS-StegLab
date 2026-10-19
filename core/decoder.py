# PROJECT AEGIS - STEGLAB
# Version 1.3.0

from pathlib import Path
import os
import tempfile

from PIL import Image

from core.framing import HEADER, frame_size_for_length, parse_header, unframe_payload
from core.path_safety import paths_alias


def decode(bitstring: str) -> str | None:
    """Extract the least significant bit from an RGB bit string."""
    if bitstring and bitstring[-1] in ("0", "1"):
        return bitstring[-1]
    return None


def _read_lsb_bytes(image: Image.Image, bit_count: int) -> bytes:
    width, height = image.size
    if bit_count > width * height:
        raise ValueError("StegLab frame is truncated or exceeds image capacity.")
    pixels = image.load()
    result = bytearray((bit_count + 7) // 8)
    for bit_index in range(bit_count):
        x, y = bit_index % width, bit_index // width
        bit = pixels[x, y][2] & 1
        result[bit_index // 8] |= bit << (7 - (bit_index % 8))
    return bytes(result)


def extract_payload(filename: str | Path) -> bytes:
    """Read and validate a versioned LSB frame, returning exact payload bytes."""
    with Image.open(filename) as source:
        image = source.convert("RGBA")

    header_bits = HEADER.size * 8
    header = _read_lsb_bytes(image, header_bits)
    payload_length = parse_header(header)
    frame_size = frame_size_for_length(payload_length)
    framed = _read_lsb_bytes(image, frame_size * 8)
    return unframe_payload(framed)


def _atomic_write_bytes(destination: Path, payload: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(payload)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, destination)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def retr(filename: str | Path, filetosave: str | Path) -> str:
    """Extract a framed payload and write its bytes to the requested file."""
    source_path, destination = Path(filename), Path(filetosave)
    try:
        if paths_alias(source_path, destination):
            return "[ERROR] Output file cannot overwrite the source image."
        payload = extract_payload(filename)
        _atomic_write_bytes(destination, payload)
    except (OSError, ValueError) as exc:
        return f"[ERROR] {exc}"
    return "[SUCCESS] Message extracted successfully."

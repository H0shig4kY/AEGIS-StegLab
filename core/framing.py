# PROJECT AEGIS - STEGLAB
# Version 1.3.0

"""Versioned byte framing for LSB payloads.

Frame v1 layout (all lengths are in bytes):
    8-byte magic | 1-byte version | 4-byte big-endian payload length |
    payload | 4-byte big-endian CRC-32 of payload

CRC-32 detects accidental damage; it is not a cryptographic authenticator.
"""

import struct
import zlib

MAGIC = b"AEGISSTG"
FORMAT_VERSION = 1
HEADER = struct.Struct(">8sBI")
CHECKSUM = struct.Struct(">I")
FRAME_OVERHEAD_BYTES = HEADER.size + CHECKSUM.size
MAX_PAYLOAD_BYTES = (1 << 32) - 1


def frame_size_for_length(payload_length: int) -> int:
    """Return total v1 frame size in bytes, validating its length field."""
    if not isinstance(payload_length, int) or payload_length < 0:
        raise ValueError("Payload length must be a non-negative integer.")
    if payload_length > MAX_PAYLOAD_BYTES:
        raise ValueError("Payload is too large for StegLab frame version 1.")
    return FRAME_OVERHEAD_BYTES + payload_length


def frame_payload(payload: bytes | bytearray | memoryview) -> bytes:
    """Create a v1 frame for any bytes-like payload, including empty data."""
    data = bytes(payload)
    frame_size_for_length(len(data))
    header = HEADER.pack(MAGIC, FORMAT_VERSION, len(data))
    checksum = CHECKSUM.pack(zlib.crc32(data) & 0xFFFFFFFF)
    return header + data + checksum


def parse_header(header: bytes) -> int:
    """Validate a v1 header and return the declared payload length."""
    if len(header) != HEADER.size:
        raise ValueError("Truncated StegLab frame header.")
    magic, version, payload_length = HEADER.unpack(header)
    if magic != MAGIC:
        raise ValueError("No StegLab payload was found in the image.")
    if version != FORMAT_VERSION:
        raise ValueError(f"Unsupported StegLab frame version: {version}.")
    frame_size_for_length(payload_length)
    return payload_length


def unframe_payload(frame: bytes) -> bytes:
    """Validate exact frame length and CRC-32, then return the payload bytes."""
    if len(frame) < HEADER.size:
        raise ValueError("Truncated StegLab frame.")
    payload_length = parse_header(frame[: HEADER.size])
    expected_size = frame_size_for_length(payload_length)
    if len(frame) != expected_size:
        raise ValueError("StegLab frame length does not match its header.")
    payload_start = HEADER.size
    payload_end = payload_start + payload_length
    payload = frame[payload_start:payload_end]
    (expected_crc,) = CHECKSUM.unpack(frame[payload_end:])
    if (zlib.crc32(payload) & 0xFFFFFFFF) != expected_crc:
        raise ValueError("StegLab payload checksum mismatch.")
    return payload

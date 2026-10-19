"""Read-only statistical inspection for AEGIS blue-channel LSB images.

This module reports descriptive indicators. It is not a general-purpose
steganography detector and does not extract or authenticate hidden payloads.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
import stat
import warnings

from PIL import Image, UnidentifiedImageError

from core.framing import (
    FORMAT_VERSION,
    FRAME_OVERHEAD_BYTES,
    HEADER,
    MAGIC,
)

MAX_ANALYSIS_FILE_BYTES = 64 * 1024 * 1024
MAX_ANALYSIS_PIXELS = 20_000_000
_SUPPORTED_FORMAT = "PNG"
_SUPPORTED_MODES = {"RGB", "RGBA"}
_CHANNEL_NAMES = ("R", "G", "B", "A")


class ImageAnalysisError(ValueError):
    """Base exception for an image that cannot be safely analyzed."""


class UnsupportedImageError(ImageAnalysisError):
    """Raised for image formats, modes, or frame layouts outside the API."""


class ImageResourceLimitError(ImageAnalysisError):
    """Raised when the input exceeds a configured analysis resource limit."""


def _channel_summary(histogram: list[int], pixel_count: int) -> dict[str, object]:
    nonzero_bins = [index for index, count in enumerate(histogram) if count]
    mean = sum(index * count for index, count in enumerate(histogram)) / pixel_count
    variance = (
        sum(count * (index - mean) ** 2 for index, count in enumerate(histogram))
        / pixel_count
    )
    return {
        "minimum": nonzero_bins[0],
        "maximum": nonzero_bins[-1],
        "mean": mean,
        "standard_deviation": math.sqrt(variance),
        "histogram": histogram,
    }


def _binary_entropy(zeros: int, ones: int) -> float:
    total = zeros + ones
    entropy = 0.0
    for count in (zeros, ones):
        if count:
            probability = count / total
            entropy -= probability * math.log2(probability)
    return entropy


def _inspect_lsb_header(image: Image.Image, pixel_count: int) -> dict[str, object]:
    header_bits = HEADER.size * 8
    result: dict[str, object] = {
        "status": "truncated_header",
        "header_valid": False,
        "declared_length_bytes": None,
        "verification_scope": "header_only",
        "payload_crc_verified": False,
        "plaintext_exposed": False,
    }
    if pixel_count < header_bits:
        return result

    pixels = image.load()
    raw_header = bytearray(HEADER.size)
    width = image.width
    for bit_index in range(header_bits):
        x, y = bit_index % width, bit_index // width
        bit = pixels[x, y][2] & 1
        raw_header[bit_index // 8] |= bit << (7 - bit_index % 8)

    magic, version, declared_length = HEADER.unpack(raw_header)
    if magic != MAGIC:
        result["status"] = "signature_not_found"
    else:
        result["declared_length_bytes"] = declared_length
        if version != FORMAT_VERSION:
            result["status"] = "unsupported_version"
        elif (FRAME_OVERHEAD_BYTES + declared_length) * 8 > pixel_count:
            result["status"] = "declared_length_exceeds_capacity"
        else:
            result["status"] = "valid_header"
            result["header_valid"] = True
    return result


def _validate_image_header(image: Image.Image) -> tuple[int, int, int]:
    if image.format != _SUPPORTED_FORMAT:
        raise UnsupportedImageError("Only PNG images are supported.")
    if image.mode not in _SUPPORTED_MODES:
        raise UnsupportedImageError(
            "Only PNG images in RGB or RGBA mode are supported."
        )

    width, height = image.size
    pixel_count = width * height
    if width <= 0 or height <= 0:
        raise ImageAnalysisError("Image dimensions must be positive.")
    if pixel_count > MAX_ANALYSIS_PIXELS:
        raise ImageResourceLimitError(
            f"Image exceeds the {MAX_ANALYSIS_PIXELS}-pixel limit."
        )
    if getattr(image, "n_frames", 1) != 1:
        raise UnsupportedImageError(
            "Animated or multi-frame PNG images are not supported."
        )
    return width, height, pixel_count


def _build_report(
    image: Image.Image,
    *,
    file_size: int,
    width: int,
    height: int,
    pixel_count: int,
) -> dict[str, object]:
    histogram_data = image.histogram()
    band_count = len(histogram_data) // 256
    channel_names = _CHANNEL_NAMES[:band_count]
    channels = {
        name: _channel_summary(
            histogram_data[index * 256 : (index + 1) * 256],
            pixel_count,
        )
        for index, name in enumerate(channel_names)
    }

    blue_histogram = histogram_data[2 * 256 : 3 * 256]
    lsb_zeros = sum(blue_histogram[::2])
    lsb_ones = sum(blue_histogram[1::2])
    lsb = {
        "channel": "B",
        "zero_count": lsb_zeros,
        "one_count": lsb_ones,
        "zero_ratio": lsb_zeros / pixel_count,
        "one_ratio": lsb_ones / pixel_count,
        "shannon_entropy_bits": _binary_entropy(lsb_zeros, lsb_ones),
    }
    framing = _inspect_lsb_header(image, pixel_count)

    return {
        "analysis_version": 1,
        "image": {
            "format": image.format,
            "width": width,
            "height": height,
            "mode": image.mode,
            "analyzed_pixels": pixel_count,
            "file_size_bytes": file_size,
        },
        "capacity": {
            "algorithm": "aegis-lsb-blue-v1",
            "bits_per_pixel": 1,
            "raw_capacity_bits": pixel_count,
            "maximum_payload_bytes": max(
                0,
                pixel_count // 8 - FRAME_OVERHEAD_BYTES,
            ),
        },
        "channels": channels,
        "lsb": lsb,
        "framing": framing,
        "interpretation": (
            "Descriptive indicators only; they do not prove or "
            "exclude steganography."
        ),
    }


def analyze_image(image_path: str | Path) -> dict[str, object]:
    """Analyze a static RGB/RGBA PNG without modifying or extracting its data.

    Limits are fixed at 64 MiB for the compressed file and 20 million pixels.
    Only PNG images in RGB or RGBA mode are accepted; no implicit mode
    conversion is performed. A valid framing result means only that the
    signature, version, and declared length fit. The payload and CRC are not
    read or verified.
    """
    path = Path(image_path)
    try:
        source_file = path.open("rb")
    except OSError as exc:
        raise ImageAnalysisError("Unable to open the image file.") from exc

    with source_file:
        try:
            file_stat = os.fstat(source_file.fileno())
            if not stat.S_ISREG(file_stat.st_mode):
                raise ImageAnalysisError("Image input must be a regular file.")
            file_size = file_stat.st_size
            if file_size > MAX_ANALYSIS_FILE_BYTES:
                raise ImageResourceLimitError(
                    f"Image file exceeds the {MAX_ANALYSIS_FILE_BYTES}-byte limit."
                )

            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(source_file) as probe:
                    _validate_image_header(probe)
                    # PNG verify catches missing or malformed chunks. It
                    # invalidates the decoder, so reopen the same file handle.
                    probe.verify()

                source_file.seek(0)
                with Image.open(source_file) as image:
                    width, height, pixel_count = _validate_image_header(image)
                    # Decode only after format, mode, dimensions, and file size
                    # have passed their limits. No converted image is made.
                    image.load()
                    return _build_report(
                        image,
                        file_size=file_size,
                        width=width,
                        height=height,
                        pixel_count=pixel_count,
                    )
        except (Image.DecompressionBombWarning, Image.DecompressionBombError) as exc:
            raise ImageResourceLimitError(
                "Pillow rejected the image as a decompression-bomb risk."
            ) from exc
        except (UnidentifiedImageError, OSError, SyntaxError) as exc:
            raise ImageAnalysisError("Invalid or corrupt PNG image.") from exc

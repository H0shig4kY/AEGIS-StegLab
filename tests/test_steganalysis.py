import hashlib
import math
import struct
import warnings

import pytest
from PIL import Image

from core.encoder import hide
from core.framing import FORMAT_VERSION, MAGIC
from core.steganalysis import (
    ImageAnalysisError,
    ImageResourceLimitError,
    UnsupportedImageError,
    analyze_image,
)


def _save_rgb(path, size, pixels=None, color=(0, 0, 0)):
    image = Image.new("RGB", size, color)
    if pixels is not None:
        image.putdata(pixels)
    image.save(path, format="PNG")
    return path


def _write_lsb_header(path, size, header, color=(10, 20, 30)):
    image = Image.new("RGB", size, color)
    pixels = image.load()
    width = image.width
    for bit_index in range(len(header) * 8):
        x, y = bit_index % width, bit_index // width
        bit = (header[bit_index // 8] >> (7 - bit_index % 8)) & 1
        red, green, blue = pixels[x, y]
        pixels[x, y] = (red, green, (blue & 0xFE) | bit)
    image.save(path, format="PNG")
    return path


def test_rgb_metadata_histograms_and_lsb_statistics_are_exact(tmp_path):
    path = tmp_path / "synthetic.png"
    _save_rgb(
        path,
        (2, 2),
        pixels=[(10, 20, 0), (20, 30, 0), (30, 40, 255), (40, 50, 254)],
    )

    result = analyze_image(path)

    assert result["image"] == {
        "format": "PNG",
        "width": 2,
        "height": 2,
        "mode": "RGB",
        "analyzed_pixels": 4,
        "file_size_bytes": path.stat().st_size,
    }
    assert result["channels"]["R"]["minimum"] == 10
    assert result["channels"]["R"]["maximum"] == 40
    assert result["channels"]["R"]["mean"] == 25
    assert result["channels"]["R"]["standard_deviation"] == pytest.approx(
        math.sqrt(125)
    )
    assert sum(result["channels"]["R"]["histogram"]) == 4
    assert result["lsb"]["channel"] == "B"
    assert result["lsb"]["zero_count"] == 3
    assert result["lsb"]["one_count"] == 1
    assert result["lsb"]["zero_ratio"] == 0.75
    assert result["lsb"]["one_ratio"] == 0.25
    assert result["lsb"]["shannon_entropy_bits"] == pytest.approx(0.8112781244591328)
    assert result["capacity"]["maximum_payload_bytes"] == 0
    assert result["framing"]["status"] == "truncated_header"


def test_uniform_rgba_image_reports_channel_histograms_and_zero_entropy(tmp_path):
    path = tmp_path / "uniform-rgba.png"
    Image.new("RGBA", (8, 8), (11, 21, 40, 123)).save(path, format="PNG")

    result = analyze_image(path)

    assert result["image"]["mode"] == "RGBA"
    assert set(result["channels"]) == {"R", "G", "B", "A"}
    assert result["channels"]["A"]["minimum"] == 123
    assert result["channels"]["A"]["maximum"] == 123
    assert result["lsb"]["zero_count"] == 64
    assert result["lsb"]["one_count"] == 0
    assert result["lsb"]["shannon_entropy_bits"] == 0
    assert result["capacity"]["maximum_payload_bytes"] == 0


def test_capacity_accounts_for_frame_overhead_at_exact_boundaries(tmp_path):
    exactly_overhead = _save_rgb(tmp_path / "overhead.png", (17, 8))
    one_payload_byte = _save_rgb(tmp_path / "one-byte.png", (18, 8))

    assert analyze_image(exactly_overhead)["capacity"]["maximum_payload_bytes"] == 0
    assert analyze_image(one_payload_byte)["capacity"]["maximum_payload_bytes"] == 1


@pytest.mark.parametrize(
    ("size", "declared_length"),
    [((17, 8), 0), ((18, 8), 1)],
)
def test_framing_header_length_fits_exact_capacity_boundary(
    tmp_path, size, declared_length
):
    path = tmp_path / f"header-{declared_length}.png"
    header = struct.pack(">8sBI", MAGIC, FORMAT_VERSION, declared_length)
    _write_lsb_header(path, size, header)

    framing = analyze_image(path)["framing"]

    assert framing["status"] == "valid_header"
    assert framing["header_valid"] is True
    assert framing["declared_length_bytes"] == declared_length
    assert framing["payload_crc_verified"] is False


def test_known_aegis_payload_reports_valid_header_without_verifying_payload(
    tmp_path,
):
    cover = _save_rgb(tmp_path / "cover.png", (64, 64), color=(12, 30, 42))
    stego = tmp_path / "stego.png"
    payload = b"secret payload"
    hide(cover, stego, payload)

    framing = analyze_image(stego)["framing"]

    assert framing["status"] == "valid_header"
    assert framing["header_valid"] is True
    assert framing["declared_length_bytes"] == len(payload)
    assert framing["verification_scope"] == "header_only"
    assert framing["payload_crc_verified"] is False
    assert framing["plaintext_exposed"] is False
    assert "secret payload" not in repr(framing)


def test_payload_corruption_does_not_get_reported_as_crc_verified(tmp_path):
    cover = _save_rgb(tmp_path / "cover.png", (64, 64), color=(12, 30, 42))
    stego = tmp_path / "stego.png"
    hide(cover, stego, b"payload")
    with Image.open(stego) as source_image:
        image = source_image.copy()
    x = 13 * 8 % image.width
    y = 13 * 8 // image.width
    red, green, blue, alpha = image.getpixel((x, y))
    image.putpixel((x, y), (red, green, blue ^ 1, alpha))
    corrupted = tmp_path / "corrupted-payload.png"
    image.save(corrupted, format="PNG")

    framing = analyze_image(corrupted)["framing"]

    assert framing["status"] == "valid_header"
    assert framing["payload_crc_verified"] is False


def test_unsupported_header_version_is_reported(tmp_path):
    path = tmp_path / "unsupported-version.png"
    header = struct.pack(">8sBI", MAGIC, FORMAT_VERSION + 1, 0)
    _write_lsb_header(path, (16, 8), header)

    framing = analyze_image(path)["framing"]

    assert framing["status"] == "unsupported_version"
    assert framing["header_valid"] is False
    assert framing["declared_length_bytes"] == 0


def test_declared_payload_length_beyond_image_capacity_is_rejected(tmp_path):
    path = tmp_path / "overclaimed-length.png"
    header = struct.pack(">8sBI", MAGIC, FORMAT_VERSION, 1)
    _write_lsb_header(path, (13, 8), header)

    framing = analyze_image(path)["framing"]

    assert framing["status"] == "declared_length_exceeds_capacity"
    assert framing["header_valid"] is False
    assert framing["declared_length_bytes"] == 1


def test_non_aegis_lsb_stream_is_not_detected(tmp_path):
    path = _save_rgb(tmp_path / "clean.png", (32, 32), color=(40, 50, 60))

    framing = analyze_image(path)["framing"]

    assert framing["status"] == "signature_not_found"
    assert framing["header_valid"] is False
    assert framing["declared_length_bytes"] is None


def test_unsupported_format_and_png_mode_are_rejected(tmp_path):
    jpeg = tmp_path / "image.jpg"
    Image.new("RGB", (16, 16)).save(jpeg, format="JPEG")
    palette = tmp_path / "palette.png"
    Image.new("P", (16, 16)).save(palette, format="PNG")

    with pytest.raises(UnsupportedImageError, match="Only PNG"):
        analyze_image(jpeg)
    with pytest.raises(UnsupportedImageError, match="RGB or RGBA"):
        analyze_image(palette)


def test_animated_png_is_rejected_instead_of_analyzing_only_one_frame(tmp_path):
    path = tmp_path / "animated.png"
    first = Image.new("RGBA", (8, 8), (10, 20, 30, 255))
    second = Image.new("RGBA", (8, 8), (11, 21, 31, 255))
    first.save(path, format="PNG", save_all=True, append_images=[second])

    with pytest.raises(UnsupportedImageError, match="multi-frame"):
        analyze_image(path)


def test_invalid_and_truncated_png_files_raise_controlled_errors(tmp_path):
    invalid = tmp_path / "invalid.png"
    invalid.write_bytes(b"not a PNG")
    truncated = _save_rgb(tmp_path / "valid.png", (32, 32))
    truncated.write_bytes(truncated.read_bytes()[:-12])

    with pytest.raises(ImageAnalysisError, match="Invalid or corrupt PNG"):
        analyze_image(invalid)
    with pytest.raises(ImageAnalysisError, match="Invalid or corrupt PNG"):
        analyze_image(truncated)


def test_pixel_limit_is_checked_before_image_load(tmp_path, monkeypatch):
    path = _save_rgb(tmp_path / "pixels.png", (2, 2))
    monkeypatch.setattr("core.steganalysis.MAX_ANALYSIS_PIXELS", 4)
    assert analyze_image(path)["image"]["analyzed_pixels"] == 4

    monkeypatch.setattr("core.steganalysis.MAX_ANALYSIS_PIXELS", 3)

    with pytest.raises(ImageResourceLimitError, match="3-pixel limit"):
        analyze_image(path)


def test_file_size_limit_is_checked_before_pillow_open(tmp_path, monkeypatch):
    path = _save_rgb(tmp_path / "file-size.png", (2, 2))
    monkeypatch.setattr(
        "core.steganalysis.MAX_ANALYSIS_FILE_BYTES", path.stat().st_size
    )
    assert analyze_image(path)["image"]["file_size_bytes"] == path.stat().st_size

    monkeypatch.setattr("core.steganalysis.MAX_ANALYSIS_FILE_BYTES", 1)

    with pytest.raises(ImageResourceLimitError, match="1-byte limit"):
        analyze_image(path)


def test_decompression_bomb_error_becomes_controlled_resource_error(
    tmp_path, monkeypatch
):
    path = _save_rgb(tmp_path / "bomb.png", (2, 2))

    def raise_bomb(*_args, **_kwargs):
        raise Image.DecompressionBombError("simulated oversized image")

    monkeypatch.setattr("core.steganalysis.Image.open", raise_bomb)
    with pytest.raises(ImageResourceLimitError, match="decompression-bomb"):
        analyze_image(path)


def test_decompression_bomb_warning_becomes_controlled_resource_error(
    tmp_path, monkeypatch
):
    path = _save_rgb(tmp_path / "bomb-warning.png", (2, 2))

    def warn_bomb(*_args, **_kwargs):
        warnings.warn(Image.DecompressionBombWarning("simulated warning"))

    monkeypatch.setattr("core.steganalysis.Image.open", warn_bomb)
    with pytest.raises(ImageResourceLimitError, match="decompression-bomb"):
        analyze_image(path)


def test_analysis_does_not_modify_the_input_image(tmp_path):
    path = _save_rgb(tmp_path / "read-only.png", (16, 16), color=(10, 20, 30))
    original = path.read_bytes()
    original_hash = hashlib.sha256(original).hexdigest()
    original_mtime = path.stat().st_mtime_ns

    analyze_image(path)

    assert path.read_bytes() == original
    assert hashlib.sha256(path.read_bytes()).hexdigest() == original_hash
    assert path.stat().st_mtime_ns == original_mtime

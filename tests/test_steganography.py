import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from core.decoder import extract_payload, retr
from core.encoder import hide
from core.framing import FRAME_OVERHEAD_BYTES, HEADER, frame_payload, unframe_payload
from core.image_handler import analyze_image
from core.legacy_decoder import extract_v12_text, retr_legacy_v12


class SteganographyTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def make_image(self, name="cover.png", size=(64, 64), mode="RGB"):
        path = self.directory / name
        if mode == "RGBA":
            image = Image.new(mode, size, (20, 30, 40, 73))
        else:
            image = Image.new(mode, size, (20, 30, 40))
        image.save(path, format="PNG")
        return path

    def test_empty_utf8_and_arbitrary_binary_payloads_round_trip(self):
        payloads = (
            b"",
            "Olá, StegLab 🛡️".encode("utf-8"),
            b"\x00leading\x00and trailing\x00",
            bytes(range(256)),
            b"\xff\xfe",  # The legacy terminator is ordinary payload data now.
        )
        for index, payload in enumerate(payloads):
            with self.subTest(payload_length=len(payload)):
                source = self.make_image(f"cover-{index}.png")
                output = self.directory / f"stego-{index}.png"
                self.assertTrue(hide(source, output, payload).startswith("[SUCCESS]"))
                self.assertEqual(extract_payload(output), payload)

    def test_text_input_is_encoded_as_utf8(self):
        source = self.make_image()
        output = self.directory / "stego.png"
        text = "Português: ação, Fafe"
        hide(source, output, text)
        self.assertEqual(extract_payload(output), text.encode("utf-8"))

    def test_rgb_and_rgba_images_are_supported(self):
        for mode in ("RGB", "RGBA"):
            with self.subTest(mode=mode):
                source = self.make_image(f"{mode}.png", mode=mode)
                output = self.directory / f"{mode}-stego.png"
                hide(source, output, b"payload")
                self.assertEqual(extract_payload(output), b"payload")

    def test_lsb_output_rejects_lossy_or_misleading_extension(self):
        source = self.make_image()
        output = self.directory / "stego.jpg"
        with self.assertRaisesRegex(ValueError, "must use the .png extension"):
            hide(source, output, b"payload")
        self.assertFalse(output.exists())

    def test_alpha_channel_is_preserved_exactly(self):
        source = self.make_image(mode="RGBA")
        output = self.directory / "transparent-stego.png"
        original_alpha = Image.open(source).getchannel("A")
        hide(source, output, b"payload")
        output_alpha = Image.open(output).getchannel("A")
        self.assertEqual(output_alpha.tobytes(), original_alpha.tobytes())

    def test_encoder_rejects_insufficient_capacity_before_creating_output(self):
        source = self.make_image(size=(1, 1))
        output = self.directory / "too-small.png"
        with self.assertRaisesRegex(ValueError, "holds 1 bits"):
            hide(source, output, b"")
        self.assertFalse(output.exists())

    def test_analyzer_accounts_for_versioned_frame_overhead(self):
        source = self.make_image(size=(17, 8))
        info = analyze_image(source, b"")
        self.assertEqual(info["capacity"], 136)
        self.assertEqual(info["payload"], FRAME_OVERHEAD_BYTES * 8)
        self.assertTrue(info["fits"])

    def test_source_image_is_not_overwritten_by_default(self):
        source = self.make_image()
        original = source.read_bytes()
        with self.assertRaisesRegex(ValueError, "cannot overwrite the source"):
            hide(source, source, b"payload")
        self.assertEqual(source.read_bytes(), original)

    def test_explicit_source_overwrite_is_supported(self):
        source = self.make_image()
        hide(source, source, b"payload", overwrite_source=True)
        self.assertEqual(extract_payload(source), b"payload")

    def test_checksum_rejects_modified_payload_bits(self):
        source = self.make_image()
        output = self.directory / "stego.png"
        hide(source, output, b"payload")
        image = Image.open(output).convert("RGBA")
        x, y = (HEADER.size * 8) % image.width, (HEADER.size * 8) // image.width
        red, green, blue, alpha = image.getpixel((x, y))
        image.putpixel((x, y), (red, green, blue ^ 1, alpha))
        corrupted = self.directory / "corrupted.png"
        image.save(corrupted)
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            extract_payload(corrupted)

    def test_extraction_writes_exact_bytes(self):
        source = self.make_image()
        output = self.directory / "stego.png"
        extracted = self.directory / "recovered.bin"
        payload = b"\x00\xffbytes\x00"
        hide(source, output, payload)
        self.assertEqual(retr(output, extracted), "[SUCCESS] Message extracted successfully.")
        self.assertEqual(extracted.read_bytes(), payload)

    def test_v1_frame_rejects_truncation_and_corruption(self):
        frame = frame_payload(b"data")
        self.assertEqual(unframe_payload(frame), b"data")
        with self.assertRaises(ValueError):
            unframe_payload(frame[:-1])
        changed = bytearray(frame)
        changed[HEADER.size] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            unframe_payload(bytes(changed))

    def test_independent_fixed_lsb_frame_fixture(self):
        expected = bytes.fromhex(
            "4145474953535447010000000d6669787475726500627974657355ae442a"
        )
        self.assertEqual(frame_payload(b"fixture\x00bytes"), expected)
        self.assertEqual(unframe_payload(expected), b"fixture\x00bytes")

    def test_hard_link_alias_is_protected(self):
        source = self.make_image()
        alias = self.directory / "alias.png"
        alias.hardlink_to(source)
        with self.assertRaisesRegex(ValueError, "cannot overwrite the source"):
            hide(source, alias, b"payload")

    def test_failed_atomic_image_write_cleans_temp_and_preserves_destination(self):
        source = self.make_image()
        output = self.directory / "existing.png"
        output.write_bytes(b"keep this")
        with patch("core.encoder.os.replace", side_effect=OSError("simulated failure")):
            with self.assertRaises(OSError):
                hide(source, output, b"payload")
        self.assertEqual(output.read_bytes(), b"keep this")
        self.assertEqual(list(self.directory.glob(".existing.png.*.tmp")), [])

    def test_explicit_legacy_v12_decoder_isolated_from_current_decode(self):
        source = self.make_image(size=(200, 1))
        image = Image.open(source).convert("RGBA")
        text_bytes = b"legacy"
        payload_bits = format(int.from_bytes(text_bytes, "big"), "b")
        bits = payload_bits + "1111111111111110"
        for index, bit in enumerate(bits):
            x, y = index % image.width, index // image.width
            red, green, blue, alpha = image.getpixel((x, y))
            image.putpixel((x, y), (red, green, (blue & 0xFE) | int(bit), alpha))
        legacy_image = self.directory / "legacy.png"
        image.save(legacy_image)
        self.assertEqual(extract_v12_text(legacy_image), "legacy")
        with self.assertRaises(ValueError):
            extract_payload(legacy_image)
        output = self.directory / "legacy.txt"
        self.assertTrue(retr_legacy_v12(legacy_image, output).startswith("[SUCCESS]"))
        self.assertEqual(output.read_bytes(), b"legacy")

    def test_current_retr_does_not_fall_back_to_legacy(self):
        source = self.make_image(size=(200, 1))
        image = Image.open(source).convert("RGBA")
        bits = format(int.from_bytes(b"legacy", "big"), "b") + "1111111111111110"
        for index, bit in enumerate(bits):
            x, y = index % image.width, index // image.width
            red, green, blue, alpha = image.getpixel((x, y))
            image.putpixel((x, y), (red, green, (blue & 0xFE) | int(bit), alpha))
        legacy_image = self.directory / "legacy-only.png"
        image.save(legacy_image)
        output = self.directory / "should-not-exist.bin"
        self.assertTrue(retr(legacy_image, output).startswith("[ERROR]"))
        self.assertFalse(output.exists())

    def test_failed_atomic_payload_write_cleans_temp_and_preserves_destination(self):
        source = self.make_image()
        stego = self.directory / "stego.png"
        hide(source, stego, b"new payload")
        output = self.directory / "existing.bin"
        output.write_bytes(b"old data")
        with patch("core.decoder.os.replace", side_effect=OSError("simulated failure")):
            result = retr(stego, output)
        self.assertTrue(result.startswith("[ERROR]"))
        self.assertEqual(output.read_bytes(), b"old data")
        self.assertEqual(list(self.directory.glob(".existing.bin.*.tmp")), [])


if __name__ == "__main__":
    unittest.main()

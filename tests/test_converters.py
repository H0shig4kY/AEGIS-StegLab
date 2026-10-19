import unittest

from core.converters import (
    bin2bytes,
    bin2str,
    bit2hex,
    bytes2bin,
    hex2bit,
    hex2rgb,
    rgb2hex,
    str2bin,
)


class ConversionTests(unittest.TestCase):
    def test_text_and_binary_conversions_preserve_empty_and_nul_bytes(self):
        for data in (b"", b"\x00A", b"A\x00", b"\x00\x00\xff"):
            self.assertEqual(bin2bytes(bytes2bin(data)), data)
            self.assertEqual(bin2bytes(str2bin(data)), data)

    def test_utf8_text_conversion_round_trips(self):
        text = "Olá, StegLab 🛡️"
        self.assertEqual(bin2str(str2bin(text)), text)

    def test_rgb_conversion_preserves_leading_zero_nibbles(self):
        self.assertEqual(hex2rgb("#012345"), (1, 35, 69))
        self.assertEqual(rgb2hex(1, 35, 69), "#012345")
        self.assertEqual(bit2hex(hex2bit("#012345")), "#012345")

    def test_binary_decoder_rejects_partial_bytes(self):
        with self.assertRaises(ValueError):
            bin2bytes("101")


if __name__ == "__main__":
    unittest.main()

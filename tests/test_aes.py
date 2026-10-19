import base64
import hashlib
import os
import struct

import pytest
import crypto.aes as aes_module
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from crypto.aes import (
    FORMAT_VERSION,
    HEADER_BYTES,
    MAX_ENVELOPE_BASE64_BYTES,
    MAX_ENVELOPE_BYTES,
    MAX_PLAINTEXT_BYTES,
    MAGIC,
    NONCE_BYTES,
    SALT_BYTES,
    SCRYPT_N,
    SCRYPT_P,
    SCRYPT_R,
    decrypt,
    decrypt_legacy_cbc,
    encrypt,
)


def _payload(encoded: str) -> bytearray:
    return bytearray(base64.b64decode(encoded, validate=True))


def _encoded(payload: bytes | bytearray) -> str:
    return base64.b64encode(payload).decode("ascii")


def _legacy_cbc_encrypt(text: str, password: str) -> str:
    """Create a v1.2 fixture using its original untagged CBC format."""
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded = padder.update(text.encode("utf-8")) + padder.finalize()
    key = hashlib.sha256(password.encode("utf-8")).digest()
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode("ascii")


@pytest.mark.parametrize("plaintext", ["", "Olá, StegLab 🛡️ — ação"])
def test_encrypt_decrypt_round_trip(plaintext):
    assert decrypt(encrypt(plaintext, "correct horse"), "correct horse") == plaintext


def test_repeated_encryptions_use_different_random_salt_and_nonce():
    first = _payload(encrypt("same plaintext", "password"))
    second = _payload(encrypt("same plaintext", "password"))
    assert first != second
    assert first[: 9 + SALT_BYTES] != second[: 9 + SALT_BYTES]
    assert first[9 + SALT_BYTES : HEADER_BYTES] != second[9 + SALT_BYTES : HEADER_BYTES]


def test_format_v1_header_and_authenticated_round_trip():
    encoded = encrypt("format check", "password")
    payload = base64.b64decode(encoded, validate=True)
    magic, version = struct.unpack(">8sB", payload[:9])
    assert magic == MAGIC == b"AEGISENC"
    assert version == FORMAT_VERSION == 1
    assert len(payload[9:25]) == SALT_BYTES == 16
    assert len(payload[25:37]) == NONCE_BYTES == 12
    assert len(payload[HEADER_BYTES:]) >= 16  # AES-GCM tag, including empty input.


def test_format_v1_scrypt_cost_is_fixed_and_documented():
    assert (SCRYPT_N, SCRYPT_R, SCRYPT_P) == (2**15, 8, 3)


def test_independent_fixed_aes_envelope_fixture():
    # Fixed salt/nonce known-answer fixture generated from the published v1
    # layout using hashlib.scrypt + AESGCM, independently of encrypt().
    fixture = "QUVHSVNFTkMBAAECAwQFBgcICQoLDA0OD6ChoqOkpaanqKmqq8l/2v/qQsmYtF1jUMvWfIkoLWeqLUjHDGBYBvAzpk33dQ=="
    assert decrypt(fixture, "fixture-pass") == "fixture plaintext"


@pytest.mark.parametrize("encoded", ["%%%", "QUVHSVNFTkM=", "QUVHSVNFTkMBAAECAwQFBgcICQoLDA0OD6ChoqOkpaanqKmqq8l/2v/qQsmYtF1jUMvWfIkoLWeqLUjHDGBYBvAzpk33dQ"])
def test_structural_errors_are_rejected_before_password_kdf(encoded, monkeypatch):
    def unexpected_kdf(*args, **kwargs):
        raise AssertionError("KDF must not run for structurally invalid input")

    monkeypatch.setattr(aes_module, "derive_key", unexpected_kdf)
    with pytest.raises(ValueError):
        decrypt(encoded, "password")


def test_unsupported_version_is_rejected_before_password_kdf(monkeypatch):
    payload = _payload(encrypt("version", "password"))
    payload[8] = 99
    monkeypatch.setattr(
        aes_module, "derive_key",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("KDF ran")),
    )
    with pytest.raises(ValueError, match="Unsupported AES payload version"):
        decrypt(_encoded(payload), "password")


@pytest.mark.parametrize("password", ["wrong password", ""])
def test_wrong_password_is_rejected(password):
    with pytest.raises(ValueError, match="Invalid encrypted data or incorrect password"):
        decrypt(encrypt("secret", "right password"), password)


def test_wrong_password_and_authentication_failure_share_one_error():
    encoded = encrypt("secret", "password")
    damaged = _payload(encoded)
    damaged[-1] ^= 0x01

    with pytest.raises(ValueError) as wrong_password:
        decrypt(encoded, "wrong password")
    with pytest.raises(ValueError) as changed_tag:
        decrypt(_encoded(damaged), "password")

    assert str(wrong_password.value) == str(changed_tag.value)
    assert wrong_password.value.__cause__ is None
    assert changed_tag.value.__cause__ is None


@pytest.mark.parametrize("field_index", [0, 9, 25, HEADER_BYTES, -1])
def test_modified_header_salt_nonce_ciphertext_or_tag_is_rejected(field_index):
    payload = _payload(encrypt("authenticated data", "password"))
    payload[field_index] ^= 0x01
    with pytest.raises(ValueError):
        decrypt(_encoded(payload), "password")


def test_truncated_payloads_are_rejected():
    payload = _payload(encrypt("data", "password"))
    for truncated in (b"", bytes(payload[:8]), bytes(payload[: HEADER_BYTES]), bytes(payload[:-1])):
        with pytest.raises(ValueError):
            decrypt(_encoded(truncated), "password")


def test_oversized_encrypted_input_is_rejected_before_base64_or_kdf(monkeypatch):
    monkeypatch.setattr(aes_module, "MAX_ENVELOPE_BASE64_BYTES", 88)

    def forbidden(*args, **kwargs):
        raise AssertionError("oversized data must be rejected before decoding/KDF")

    monkeypatch.setattr(aes_module.base64, "b64decode", forbidden)
    monkeypatch.setattr(aes_module, "derive_key", forbidden)
    with pytest.raises(ValueError, match="Invalid encrypted data"):
        decrypt("A" * 89, "password")


def test_encrypt_rejects_plaintext_that_cannot_fit_envelope(monkeypatch):
    monkeypatch.setattr(aes_module, "MAX_PLAINTEXT_BYTES", 11)
    with pytest.raises(ValueError, match="64 MiB AES envelope limit"):
        encrypt("x" * 12, "password")


def test_exact_plaintext_and_envelope_limits_are_accepted(monkeypatch):
    monkeypatch.setattr(aes_module, "MAX_ENVELOPE_BYTES", 64)
    monkeypatch.setattr(aes_module, "MAX_PLAINTEXT_BYTES", 11)
    monkeypatch.setattr(aes_module, "MAX_ENVELOPE_BASE64_BYTES", 88)

    encoded = encrypt("x" * 11, "password")
    assert len(_payload(encoded)) == aes_module.MAX_ENVELOPE_BYTES
    assert len(encoded) == aes_module.MAX_ENVELOPE_BASE64_BYTES
    assert decrypt(encoded, "password") == "x" * 11


def test_envelope_one_byte_over_limit_is_rejected_before_kdf(monkeypatch):
    monkeypatch.setattr(aes_module, "MAX_ENVELOPE_BYTES", 64)
    monkeypatch.setattr(aes_module, "MAX_PLAINTEXT_BYTES", 11)
    monkeypatch.setattr(aes_module, "MAX_ENVELOPE_BASE64_BYTES", 88)
    envelope = _payload(encrypt("x" * 11, "password"))
    oversized = _encoded(envelope + b"\x00")
    assert len(oversized) == aes_module.MAX_ENVELOPE_BASE64_BYTES
    monkeypatch.setattr(
        aes_module,
        "derive_key",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("KDF ran")),
    )
    with pytest.raises(ValueError, match="Invalid encrypted data"):
        decrypt(oversized, "password")


def test_aes_size_constants_account_for_header_tag_and_base64_expansion():
    assert MAX_PLAINTEXT_BYTES == MAX_ENVELOPE_BYTES - HEADER_BYTES - aes_module.TAG_BYTES
    assert MAX_ENVELOPE_BASE64_BYTES == 4 * ((MAX_ENVELOPE_BYTES + 2) // 3)


def test_unsupported_format_version_is_rejected():
    payload = _payload(encrypt("data", "password"))
    payload[8] = 2
    with pytest.raises(ValueError, match="Unsupported AES payload version"):
        decrypt(_encoded(payload), "password")


def test_default_decrypt_rejects_legacy_cbc_payload():
    legacy = _legacy_cbc_encrypt("legacy text", "password")
    with pytest.raises(ValueError, match="Invalid encrypted data"):
        decrypt(legacy, "password")


def test_explicit_legacy_decoder_recovers_v12_text_with_warning_in_docstring():
    legacy = _legacy_cbc_encrypt("legacy text", "password")
    assert decrypt_legacy_cbc(legacy, "password") == "legacy text"
    assert "unauthenticated" in decrypt_legacy_cbc.__doc__


def test_legacy_decoder_rejects_wrong_password():
    legacy = _legacy_cbc_encrypt("legacy text", "password")
    with pytest.raises(ValueError, match="CBC is unauthenticated"):
        decrypt_legacy_cbc(legacy, "wrong password")

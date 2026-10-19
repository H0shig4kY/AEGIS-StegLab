🛡️ Project AEGIS

# Project AEGIS – Aegis StegLab

Aegis StegLab is the steganography and classical cryptography module of Project AEGIS.

This tool provides a laboratory environment for combining cryptography and image steganography.

StegLab currently supports multiple educational encryption algorithms together with Least Significant Bit (LSB) steganography for hiding data inside PNG images.

> Current code: Version 1.3.0

---

# Features

## Cryptography

- Caesar Cipher
- XOR Cipher (Base64)
- Vigenère Cipher
- AES-256 Encryption
- Multiple cipher selection

## Steganography

- Hide text inside PNG images
- Extract hidden text from PNG images
- Image capacity analysis
- Payload validation
- Automatic UTF-8 text handling
- LSB (Least Significant Bit) embedding
- Safe output image generation

## File Operations

- Read text files
- Create output files
- Preserve original workflow from the legacy implementation

---

# Installation

Requires Python 3.10 or newer.

### Windows PowerShell

```bash
git clone https://github.com/H0shig4kY/AEGIS-StegLab.git
cd AEGIS-StegLab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### POSIX shell (Linux and macOS)

```sh
git clone https://github.com/H0shig4kY/AEGIS-StegLab.git
cd AEGIS-StegLab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# Requirements

- Python 3.10+
- Pillow
- NumPy
- bitstring
- colorama
- cryptography

---

# Running

```bash
python main.py
```

Run the automated tests with `python -m pip install pytest` followed by
`python -m pytest -q`.

---

# Menu

```
1 - Encrypt Text File
2 - Decrypt Text File
3 - Hide Text Inside Image
4 - Extract Hidden Text
5 - Exit
6 - About
7 - Extract v1.2.0 LSB (legacy, explicitly selected)
```

---

# Usage

## Encrypt

```text
1 - Caesar Cipher
2 - XOR Cipher
3 - Vigenère Cipher
4 - AES-256
```
---

# AES encrypted payload format

AES encryption writes Base64 text containing the versioned binary format below:

```text
8-byte magic "AEGISENC" | 1-byte version (1) | 16-byte salt |
12-byte nonce | AES-256-GCM ciphertext | 16-byte authentication tag
```

Format version 1 derives its key with scrypt using `N=2^15`, `r=8`, and `p=3`.
These parameters are fixed by the format version. The complete header (magic,
version, salt, and nonce) is authenticated as AES-GCM associated data. A wrong
password or modified authenticated data is rejected before plaintext is
returned. Empty passwords are rejected by the CLI and crypto API. Interactive
password entry disables terminal echo.

Encrypted envelopes are limited to 64 MiB, including the header and tag. This
bounds the CLI file read and rejects oversized input before Base64 decoding or
the scrypt KDF. Consequently, v1.3.0 encrypts at most 64 MiB minus the 53-byte
envelope overhead; larger plaintexts and previously created larger envelopes
are rejected. Split larger files before encryption if needed. A structurally
valid envelope still incurs the fixed scrypt cost (about 32 MiB working memory)
per decrypt attempt; the library does not provide request rate limiting.

New encryption uses AES-GCM only. AES-CBC files created by v1.2.0 are not
accepted by the default decrypt function. The explicitly named
`crypto.aes.decrypt_legacy_cbc()` function can attempt a best-effort recovery;
legacy CBC has no authentication, so a successful decrypt does not prove that
the password was correct or that the ciphertext was not modified.

The current LSB frame is versioned, length-based, and protected by CRC-32 for
accidental corruption detection (CRC-32 is not authentication). The v1.2.0
sentinel-based reader is only available through menu option 7 or the explicitly
named `core.legacy_decoder.retr_legacy_v12()` API. It can truncate at sentinel
collisions and cannot verify integrity. Current extraction never invokes it
automatically. v1.2.0 LSB content with leading NUL bytes may already have lost
those bytes in the original encoder and cannot be recovered by this reader.

Caesar, XOR, and Vigenère are classical educational demonstrations and must
not be used as secure encryption.

# Notes

- PNG images are recommended.
- Images are internally converted to RGBA.
- Output images do not overwrite the original image unless explicitly requested
  through the Python API; hard-link aliases are detected.
- LSB output is lossless PNG and requires a `.png` filename; Pillow-readable
  input image formats are converted to RGBA before embedding.
- Capacity is verified before embedding.
- UTF-8 text is fully supported.

---

# Legacy Compatibility

The project was originally developed as a single-file implementation (`legacy.py`).

The legacy script is retained for educational comparison. AES output in v1.3.0
uses the authenticated format documented above; v1.2.0 AES-CBC output requires
the explicitly selected legacy decrypt function.

---

# Implemented and planned work

## v1.3.0 compatibility notes

- AES output changes from v1.2.0 unauthenticated CBC to versioned AES-GCM.
  Default decryption rejects old CBC data; recovery requires explicit use of
  `decrypt_legacy_cbc()` and cannot authenticate it.
- LSB output changes to the versioned `AEGISSTG` length-and-checksum frame.
  Existing v1.2.0 sentinel images require explicit legacy extraction (menu 7).
- PNG writing and extracted payload output are replaced atomically where the
  filesystem supports same-directory atomic replacement.

The following are implemented in v1.3.0:

- Capacity validation
- RGB/RGBA compatibility
- AES-GCM and scrypt encrypted envelopes
- Versioned LSB framing, CRC-32 validation, and atomic output writes
- Explicit best-effort legacy v1.2.0 decoders

## Historical implementation notes

- Capacity validation
- RGB/RGBA compatibility improvements
- Improved error handling
- Output image selection

## Version 1.2 

- AES-256 Encryption
- XOR Cipher
- Vigenère Cipher
- Multiple cipher support
- Modular cryptography manager

## Planned features (not implemented)

- BMP and TIFF output support
- Selectable embedding channel (R/G/B)
- Additional image information and analysis

- GUI interface
- Drag-and-drop support
- Batch processing
- Plugin architecture
- Integration with other Project AEGIS tools

---

Project Structure

aegis_steglab/
│
├── aegis/
├── core/
├── crypto/
│   ├── aes.py
│   ├── caesar.py
│   ├── manager.py
│   ├── vigenere.py
│   └── xor.py
├── utils/
├── main.py
└── requirements.txt

# License

This project is part of **Project AEGIS**.

Developed for educational, research, and authorized security testing purposes only.

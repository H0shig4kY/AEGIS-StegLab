🛡️ Project AEGIS

# Project AEGIS – Aegis StegLab

Aegis StegLab is the steganography and classical cryptography module of Project AEGIS.

This tool provides a simple laboratory environment for hiding text inside images using Least Significant Bit (LSB) steganography and protecting text using Caesar cipher encryption.

> **Current Status:** Stable (Legacy Feature Parity)

---

# Features

## Cryptography

- Caesar Cipher Encryption
- Caesar Cipher Decryption
- Configurable encryption key (seed)

## Steganography

- Hide text inside PNG images
- Extract hidden text from PNG images
- Automatic UTF-8 text handling
- LSB (Least Significant Bit) embedding

## File Operations

- Read text files
- Create output files
- Preserve original workflow from the legacy implementation

# Notes

- PNG images are recommended.
- Images are internally converted to RGBA for compatibility.
- Larger images can store larger messages.
- Messages larger than the image capacity are not supported.

---

# Legacy Compatibility

The project was originally developed as a single-file implementation (`legacy.py`).

The current version preserves the original algorithms while introducing a modular architecture for easier maintenance and future expansion.

No functional changes have been intentionally introduced during the refactoring process.

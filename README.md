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

---

# Installation

Clone the repository

```bash
git clone <repository>
cd aegis_steglab
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

- Python 3.10+
- Pillow
- NumPy
- bitstring
- colorama

---

# Running

```bash
python main.py
```

---

# Menu

```
1 - Encrypt text file
2 - Decrypt text file
3 - Hide text inside image
4 - Extract text from image
5 - Exit
```

---

# Usage

## Encrypt

Input

```
hello.txt
```

Seed

```
5
```

Output

```
encrypted.txt
```

---

## Hide Message

Input image

```
image.png
```

Input text

```
secret.txt
```

The image will contain the hidden message after processing.

---

## Retrieve Message

Input image

```
image.png
```

Output

```
recovered.txt
```

---

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

---

# Roadmap

## Version 1.1

- Capacity validation
- RGB/RGBA compatibility improvements
- Improved error handling
- Output image selection

## Version 1.2

- AES encryption
- XOR encryption
- Multiple cipher support

## Version 1.3

- Image quality analysis
- Entropy calculation
- Payload statistics
- Detection resistance improvements

## Future

- GUI interface
- Drag-and-drop support
- Batch processing
- Plugin architecture
- Integration with other Project AEGIS tools

---

# License

This project is part of **Project AEGIS**.

Developed for educational, research, and authorized security testing purposes only.

🛡️ Project AEGIS

# Project AEGIS – Aegis StegLab

Aegis StegLab is the steganography and classical cryptography module of Project AEGIS.

This tool provides a laboratory environment for combining cryptography and image steganography.

StegLab currently supports multiple encryption algorithms together with Least Significant Bit (LSB) steganography for securely hiding text inside PNG images.

> > Current Status: Stable (Version 1.2.0)

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
- cryptography

---

# Running

```bash
python main.py
```

---

# Menu

```
1 - Encrypt Text File
2 - Decrypt Text File
3 - Hide Text Inside Image
4 - Extract Hidden Text
5 - Exit
6 - About
```

---

# Usage

## Encrypt

1 - Caesar Cipher
2 - XOR Cipher
3 - Vigenère Cipher
4 - AES-256
```
---

# Notes

- PNG images are recommended.
- Images are internally converted to RGBA.
- Output images never overwrite the original image.
- Capacity is verified before embedding.
- UTF-8 text is fully supported.

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

- AES-256 Encryption
- XOR Cipher
- Vigenère Cipher
- Multiple cipher support
- Modular cryptography manager

## Version 1.3

- BMP support
- TIFF support
- RGB/RGBA support
- Select embedding channel (R/G/B)
- Advanced image information

## Version 1.4

- Image statistics
- Payload analysis
- Remaining capacity
- Entropy calculation

## Future

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

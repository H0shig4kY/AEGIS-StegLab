# Changelog

## 1.3.0 — security and reliability remediation

- Replaced new AES-CBC output with versioned AES-256-GCM using scrypt and
  authenticated headers. v1.2.0 CBC data requires the explicit, unauthenticated
  legacy decoder; default decryption does not fall back.
- Replaced sentinel-delimited LSB output with a versioned, length-based binary
  frame. v1.2.0 LSB extraction is available only through an explicit legacy
  menu option/API and remains best effort.
- Added payload capacity checks, binary-safe framing, alpha preservation,
  same-file/hard-link overwrite checks, and atomic output replacement.
- LSB output is required to use a `.png` name, and CLI text files are read as
  UTF-8 without line-ending normalization.
- Interactive password input now disables terminal echo. Empty passwords are
  rejected.
- Corrected dependency installation instructions and documented compatibility
  changes. Caesar, XOR, and Vigenère remain educational algorithms, not secure
  encryption.

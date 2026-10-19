#PROJECT AEGIS - STEGLAB
#Version 1.3.0

from time import sleep
from os import system, name
from threading import Thread
from pathlib import Path
import os
import tempfile
import numpy as np

def clear() -> None:
    """
    Clear the terminal screen.
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")

def readfile(filename: str, *, max_bytes: int | None = None) -> str | None:
    """
    Read a UTF-8 text file without normalizing line endings.

    When provided, ``max_bytes`` bounds the read before the file is decoded.
    """
    try:
        with open(filename, "rb") as f:
            raw_content = f.read() if max_bytes is None else f.read(max_bytes + 1)
        if max_bytes is not None and len(raw_content) > max_bytes:
            print(f"[ERROR] Input file exceeds the {max_bytes}-byte limit.")
            return None
        content = raw_content.decode("utf-8")
        if content == "":
            print("[ERROR] Input file is empty.")
            return None
        return content

    except FileNotFoundError:
        print("[ERROR] Input file not found.")
        return None
    except UnicodeDecodeError:
        print("[ERROR] Input file must contain valid UTF-8 text.")
        return None
    except OSError:
        print("[ERROR] Cannot read input file.")
        return None

def creatfile(conteudo, filetosave) -> bool:
    destination = Path(filetosave)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", prefix=f".{destination.name}.",
            suffix=".tmp", dir=destination.parent or Path("."), delete=False,
        ) as f:
            temporary = Path(f.name)
            f.write(conteudo)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, destination)
        temporary = None
        return True
    except OSError:
        print("[ERROR] Cannot write output file.")
        return False
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

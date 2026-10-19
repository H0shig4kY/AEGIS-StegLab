#PROJECT AEGIS - STEGLAB
#Version 1.2.0

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

def readfile(filename: str) -> str:
    """
    Read a UTF-8 text file without normalizing its line endings.
    """
    try:
        with open(filename, encoding="utf-8", newline="") as f:
            content = f.read()
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

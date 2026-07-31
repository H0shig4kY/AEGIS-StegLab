#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from time import sleep
from os import system, name
from threading import Thread
import sys
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
    Read the entire contents of a text file.
    """
    conteudo = ""

    try:
        with open(filename) as f:
            line = f.readline()
            conteudo += line

            while line:
                line = f.readline()
                conteudo += line

            return conteudo

    except IOError as e:
        print(f"Couldn't open or write to file ({e})")
        sys.exit()

def creatfile(conteudo: str, filetosave: str) -> None:
    """
    Create a text file and write the provided content.
    """
    with open(filetosave, "w") as f:
        f.write(conteudo)
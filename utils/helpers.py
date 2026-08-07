#PROJECT AEGIS - STEGLAB
#Version 1.2.0

from time import sleep
from os import system, name
from threading import Thread
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

            if conteudo == "":
                    print("[ERROR] Input file is empty.")
                    return None

            return conteudo

    except FileNotFoundError:
        print("[ERROR] Input file not found.")
        return None

def creatfile(conteudo, filetosave):

    try:
        with open(filetosave, "w") as f:
            f.write(conteudo)

    except PermissionError:
        print("[ERROR] Cannot write output file.")
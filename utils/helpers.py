from time import sleep
from os import system, name
from threading import Thread

def clear() -> None:
    """
    Clear the terminal screen.
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")
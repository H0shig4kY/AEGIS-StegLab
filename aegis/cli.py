#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from colorama import init
from colorama import Fore
from threading import Thread
from os import system, name
import sys


from crypto.caesar import (
    encrypt,
    decrypt,
)

from utils.helpers import (
    clear,
    readfile,
    creatfile,
)

from core.decoder import (
        retr,
)

from core.encoder import (
        hide,
)

from core.image_handler import (
       print_image_info,
       validate_image
)

def initialize_cli() -> None:
    """Initialize CLI components."""
    init(autoreset=True)


# Function to use in main
# Threads for explain what append when encrypt the file text
def task1():
        """Display progress messages for text encryption."""
        print()
        print(Fore.RED + 'Processing...')

        print('[✓] Reading input file')

        print('[✓] Encrypting data')

        print('[✓] Writing output file')

        print('[SUCCESS] Encryption completed.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when decrypt the file text
def task2():
        """Display progress messages for text decryption."""
        print()
        print(Fore.GREEN + 'Processing...')

        print('[✓] Reading input file')

        print('[✓] Decrypting data')

        print('[✓] Writing output file')

        print('[SUCCESS] Decryption completed.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when hide the file text inside the image
def task3():
        """Display progress messages for text encryption."""
        print()
        print(Fore.YELLOW + 'Processing...')

        print()

        print('[✓] Opening image')

        print('[✓] Embedding payload')

        print('[✓] Writing Output Image')

        print('[SUCCESS] Message hidden successfully.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when get the file text from one image
def task4():
        """Display progress messages for text encryption."""
        print()

        print(Fore.BLUE + '[✓] Payload extracted')

        print('[✓] output file created')

        print('[SUCCESS] Hidden message extracted.')

        print(Fore.WHITE)

def print_banner() -> None:
    """
    Display the Project AEGIS banner.
    """
    print(Fore.CYAN)
    print(r"""
 █████╗ ███████╗ ██████╗ ██╗███████╗
██╔══██╗██╔════╝██╔════╝ ██║██╔════╝
███████║█████╗  ██║  ███╗██║███████╗
██╔══██║██╔══╝  ██║   ██║██║╚════██║
██║  ██║███████╗╚██████╔╝██║███████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝

          Security Research Toolkit
──────────────────────────────────────────────────────
 Tool    : StegLab
 Version : 1.0.0
 Author  : Carlos Ribeiro
──────────────────────────────────────────────────────
 MODULE  : StegLab
 Status  : Ready
──────────────────────────────────────────────────────
    """)
    print(Fore.WHITE)

def print_menu() -> None:
    """
    Display the main menu.
    """
    print_banner()
    print(Fore.CYAN + "")
    print("[ Cryptography ]                                      ")
    print("──────────────────────────────────────────────────────")
    print("                                                      ")
    print(Fore.GREEN + "[1]" + Fore.CYAN + " Encrypt Text File   ")
    print(Fore.GREEN + "[2]" + Fore.CYAN + " Decrypt Text File   ")
    print("                                                      ")
    print("[ Steganography ]                                     ")
    print("──────────────────────────────────────────────────────")
    print("                                                      ")
    print(Fore.GREEN + "[3]" + Fore.CYAN +" Hide Text Inside Image")
    print(Fore.GREEN + "[4]" + Fore.CYAN +" Extract Hidden Text  ")
    print("                                                      ")
    print("[ System ]                                            ")
    print("──────────────────────────────────────────────────────")
    print("                                                      ")
    print(Fore.GREEN + "[5]" + Fore.CYAN +" Exit                 ")
    print(Fore.GREEN + "[6]" + Fore.CYAN +" About                ")
    print("                                                      ")
    print("======================================================")
    print("© 2026 Carlos Ribeiro • v1.0.0                        ")
    print("                                                      ")
    print("Licensed for Educational & Research Use               ")
    print(Fore.WHITE + "")

def about() -> None:
    """Display information about Project AEGIS StegLab."""

    print(Fore.CYAN)
    print("============================================================")
    print("                     ABOUT STEGLAB")
    print("============================================================")

    print()
    print("Project : AEGIS")
    print("Module  : StegLab")
    print("Version : 1.0.0")
    print("Author  : Carlos Ribeiro")

    print()
    print("Description:")
    print("StegLab is a security research tool that combines")
    print("classical cryptography with image steganography.")
    print()

    print("Features:")
    print(" - Caesar Cipher Encryption")
    print(" - Caesar Cipher Decryption")
    print(" - Hide Text Inside PNG Images")
    print(" - Extract Hidden Messages")
    print()

    print("Libraries:")
    print(" - Pillow")
    print(" - Colorama")
    print(" - Bitstring")
    print()

    print("License:")
    print("Educational & Research Use")

    print()
    print("============================================================")
    print(Fore.WHITE)

def Main():
        while(True):
                print_menu()
                try:
                        option = int(input(Fore.GREEN + "AEGIS::StegLab > " + Fore.WHITE))
                except ValueError:
                        print('[ERROR] Please enter a valid number.')
                        continue
                        #Check what choice was entered and act accordingly
                if option == 1:

                        text = input("Input File    :")
                        # Run the encrypt Function
                        conteudo=readfile(text)
                        
                        if conteudo is None:
                                continue

                        # User can define seed to encrypt
                        try:
                                s = int (input("Cipher Key    :"))
                        except ValueError:
                                print("[ERROR] Cipher key must be an integer.")
                                continue
                        
                        encriptedcontent = encrypt(conteudo,s)

                        # User can define the name of file text to get the encrypt text
                        text = input("Output File   :")
                        creatfile(encriptedcontent, text)
                        
                        # Use function to get the thread and join
                        t1 = Thread(target=task1)
                        t1.start()

                        t1.join()

                        print()

                elif option == 2:

                        text = input("Input File    :")
                        # Run the decrypt Function
                        conteudo=readfile(text)

                        if conteudo is None:
                                continue

                        # User can define seed to Decrypt
                        # If not the same seed of encrypt dont get original text
                        try:
                               s = int (input("Cipher Key    :"))
                        except ValueError:
                                print("[ERROR] Cipher key must be an integer.")
                                continue
                        
                        decriptedcontent = decrypt(conteudo,s)

                        # User can define the name of file text to get the Decrypt text
                        text = input("Output File   :")
                        creatfile(decriptedcontent, text)

                        # Use function to get the thread and join
                        t2 = Thread(target=task2)
                        t2.start()

                        t2.join()

                        print()


                elif option == 3:

                        img = input("Input Image   : ")

                        if not validate_image(img):
                                continue

                        text = input("Input File    : ")

                        conteudo = readfile(text)

                        if conteudo is None:
                                continue

                        if not print_image_info(img, conteudo):
                                continue

                        output_img = input("Output Image  : ")

                        result = (hide(img, output_img, conteudo))

                        print(result)

                        if result.startswith("[SUCCESS]"):
                                t3 = Thread(target=task3)
                                t3.start()
                                t3.join()

                        print()


                elif option == 4:

                        img = input("Input Image   :")
                        if not validate_image(img):
                                continue
                        # Run retr Funciton to get a new file text from image if that have some text hide inside
                        # User define in argument the name of image to use
                        # User can define the name of file text to create e new one using the file text inside the image
                        text = input("Output File   :")
                        result = retr(img, text)

                        print(result)

                        if result.startswith("[SUCCESS]"):
                                t4 = Thread(target=task4)
                                t4.start()
                                t4.join()

                        print()

                elif option == 5:
                        print()
                        print(Fore.GREEN + "=========================================")
                        print(Fore.GREEN + "    Thank you for using Project AEGIS    ")
                        print(Fore.GREEN + "        Security Research Toolkit        ")
                        print(Fore.GREEN + "=========================================" + Fore.WHITE)
                        sys.exit()

                elif option == 6:
                        clear()
                        about()
                        input("\nPress ENTER to return to the menu...")
                        clear()
                else:
                        print()
                        # When nummber is not between 1 and 5, show this menssage
                        print("[ERROR] Invalid menu option.")
                print()
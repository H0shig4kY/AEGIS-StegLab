#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from colorama import init
from colorama import Fore
from threading import Thread
from os import system, name


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

def initialize_cli() -> None:
    """Initialize CLI components."""
    init(autoreset=True)


# Function to use in main
# Threads for explain what append when encrypt the file text
def task1():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.RED + 'Starting a task...')

        print('[✓]Reading file')

        print('[✓]Encrypting')

        print('[✓]Saving Output')

        print('[✓][SUCCESS] Encryption completed.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when decrypt the file text
def task2():
        """Display progress messages for text decryption."""
        print('')
        print(Fore.GREEN + 'Starting a task...')

        print('[✓]Reading file')

        print('[✓]Decrypting')

        print('[✓]Saving Output')

        print('[✓][SUCCESS] Decryption completed.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when hide the file text inside the image
def task3():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.YELLOW + 'Starting a task...')

        print('[✓]Opening image')

        print('[✓]Embedding Image')

        print('[✓]Writing Image')

        print('[✓][SUCCESS] Message hidden successfully.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when get the file text from one image
def task4():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.BLUE + 'Starting a task...')

        print('[✓]Opening image')

        print('[✓]Extracting Hidden Data')

        print('[✓]Saving Output')

        print('[✓][SUCCESS] Hidden message extracted.')

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
    print("                                                      ")
    print("======================================================")
    print("© 2026 Carlos Ribeiro • v1.0.0                        ")
    print("                                                      ")
    print("Licensed for Educational & Research Use               ")
    print(Fore.WHITE + "")

def Main():
        while(True):
                print_menu()
                try:
                        option = int(input(Fore.GREEN + "AEGIS::StegLab > " + Fore.WHITE))
                except:
                        print('[Error]Wrong input. Please enter a number')
                        #Check what choice was entered and act accordingly
                if option == 1:

                        text = input("Enter file name with the text to encrypt: ")
                        # Run the encrypt Function
                        conteudo=readfile(text)
                
                        # User can define seed to encrypt
                        s = int (input("Enter number of seed to use: "))
                        encriptedcontent = encrypt(conteudo,s)

                        # User can define the name of file text to get the encrypt text
                        text = input("Enter file name to get encripted message: ")
                        creatfile(encriptedcontent, text)
                        
                        # Use function to get the thread and join
                        t1 = Thread(target=task1)
                        t1.start()

                        t1.join()

                        print('')

                elif option == 2:

                        text = input("Enter file name with the text to decrypt: ")
                        # Run the decrypt Function
                        conteudo=readfile(text)

                        # User can define seed to Decrypt
                        # If not the same seed of encrypt dont get original text
                        s = int (input("Enter number of seed to use: "))
                        decriptedcontent = decrypt(conteudo,s)

                        # User can define the name of file text to get the Decrypt text
                        text = input("Enter file name to get decripted message: ")
                        creatfile(decriptedcontent, text)

                        # Use function to get the thread and join
                        t2 = Thread(target=task2)
                        t2.start()

                        t2.join()

                        print('')


                elif option == 3:

                        img = input("Enter file of image you wont to use: ")
                        # Run hide Funciton to hide file text inside image
                        # User define in argument the name of image to use
                        # User can define the name of file text to put inside the image
                        text = input("Enter file name to hide: ")
                        conteudo=readfile(text)
                        print (hide(img, conteudo))

                        # Use function to get the thread and join
                        t3 = Thread(target=task3)
                        t3.start()

                        t3.join()

                        print('')


                elif option == 4:

                        img = input("Enter file of image you wont to use: ")
                        # Run retr Funciton to get a new file text from image if that have some text hide inside
                        # User define in argument the name of image to use
                        # User can define the name of file text to create e new one using the file text inside the image
                        text = input("Enter file name to get Message: ")
                        print (retr(img, text))

                        # Use function to get the thread and join
                        t4 = Thread(target=task4)
                        t4.start()

                        t4.join()

                        print('')

                elif option == 5:
                        print('')
                        print(Fore.GREEN + "=========================================")
                        print(Fore.GREEN + "    Thank you for using Project AEGIS    ")
                        print(Fore.GREEN + "        Security Research Toolkit        ")
                        print(Fore.GREEN + "=========================================" + Fore.WHITE)
                        exit()

                else:
                        print('')
                        # When nummber is not between 1 and 5, show this menssage
                        print('Invalid option. Please enter a number between 1 and 5.')
                print('')
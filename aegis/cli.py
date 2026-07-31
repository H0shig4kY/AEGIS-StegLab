import optparse
import sys
from colorama import init
from colorama import Fore
import sys
from threading import Thread
from os import system, name
from time import sleep

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

# Function to clear CMD when finish execute some option
def clear():
        if name == 'nt':
                _ = system('cls')

# Function to use in main
# Threads for explain what append when encrypt the file text
def task1():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.RED + 'Starting a task...')
        sleep(0.5)
        print('Reading the file..')
        sleep(0.5)
        print('Encrypting file content...')
        sleep(0.5)
        print('Write the encrypted content in new file...')
        sleep(0.5)
        print('Saving the new file with the encrypted content...')
        sleep(1)
        print('Done.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when decrypt the file text
def task2():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.GREEN + 'Starting a task...')
        sleep(0.5)
        print('Reading the file..')
        sleep(0.5)
        print('Decrypting file content...')
        sleep(0.5)
        print('Write the decripted content in new file...')
        sleep(0.5)
        print('Saving the new file with the decrypted content...')
        sleep(1)
        print('Done.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when hide the file text inside the image
def task3():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.YELLOW + 'Starting a task...')
        sleep(0.5)
        print('Opening image..')
        sleep(0.5)
        print('Creating new pixel and using encode method to replace...')
        sleep(0.5)
        print('Add the new data to the image...')
        sleep(1)
        print('Done.')

        print(Fore.WHITE)

# Function to use in main
# Threads for explain what append when get the file text from one image
def task4():
        """Display progress messages for text encryption."""
        print('')
        print(Fore.BLUE + 'Starting a task...')
        sleep(0.5)
        print('Opening image..')
        sleep(0.5)
        print('searching for new data add on image...')
        sleep(0.5)
        print('Get the data from image and copy to new file text...')
        sleep(0.5)
        print('Saving the new file text with the data...')
        sleep(1)
        print('Done.')

        print(Fore.WHITE)

def print_menu() -> None:
    """
    Display the main menu.
    """
    print(Fore.CYAN + "")
    print("------------------------------------------------------------")
    print("------ 1 -- Encrypt one file text (.txt) - Encryption ------")
    print("------ 2 -- Decrypt one file text (.txt) - Encryption ------")
    print("------------------------------------------------------------")
    print("-- 3 - Hide file text (.txt) inside image - Steganography --")
    print("-- 4 - Get the file text (.txt) from image - Steganography -")
    print("------------------------------------------------------------")
    print("------------------------ 5 -- Exit -------------------------")
    print("------------------------------------------------------------")
    print(Fore.WHITE + "")

def Main():
        while(True):
                print_menu()
                try:
                        option = int(input('Enter your choice: '))
                except:
                        print('Wrong input. Please enter a number ...')
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

                        sleep(5)

                        clear()

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

                        sleep(5)

                        clear()

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

                        sleep(5)

                        clear()

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

                        sleep(5)

                        clear()

                elif option == 5:
                        print('')
                        print(Fore.MAGENTA + 'Thanks')
                        exit()

                else:
                        print('')
                        # When nummber is not between 1 and 5, show this menssage
                        print('Invalid option. Please enter a number between 1 and 5.')
                print('')
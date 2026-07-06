import optparse
import sys
from colorama import init
from colorama import Fore

def initialize_cli() -> None:
    """Initialize CLI components."""
    init(autoreset=True)

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
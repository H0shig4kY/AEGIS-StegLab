from time import sleep
from PIL import Image
import binascii
import optparse
import codecs
import numpy as np
import sys
from os import system, name
from threading import Thread
from bitstring import BitArray
from colorama import init
from colorama import Fore

# Start colorama to change color
init()

# Function to clear CMD when finish execute some option
def clear():
        if name == 'nt':
                _ = system('cls')

# Function to use in main
# Threads for explain what append when encrypt the file text
def task1():
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

# Function to encrypt file text
# Using file given in input by user
# Create another file to save the encrypt result
def encrypt(text,s):
        
        # Variavel clean to save the result
        result = ""
        
        # Function for encrypt text
        for i in range(len(text)):
                char = text[i]
                
                # Encrypt letters in plain text
                if char.isalpha() == True:
                        
                        # Encrypt uppercase characters in plain text
                        if (char.isupper()):
                                result += chr((ord(char) + s-65) % 26 + 65)
                        else:
                                
                                # Encrypt lowercase characters in plain text
                                result += chr((ord(char) + s - 97) % 26 + 97) 
                else:
                        result += char
        return result

# Function to decrypt file text
# Using file given in input by user
# Create another file to save the decrypt result
def decrypt(text,s):
        
        # Variavel clean to save the result
        result = ""
        
        # Function for decrypt text
        for i in range(len(text)):
                char = text[i]
               
                # Decrypt letter in plain text
                if char.isalpha() == True:
                        
                        # Decrypt uppercase characters in plain text
                        if (char.isupper()):
                                result += chr((ord(char) - s-65) % 26 + 65)
                        else:
                                
                                # Decrypt lowercase characters in plain text
                                result += chr((ord(char) - s -97) % 26 + 97)
                else:
                        result += char
        return result

# Reformats rgb value of pixel into hexadecimal
def rgb2hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        
# Decodes tuple of hex while stripping away the # at the beginning and revealing just rgb values
def hex2rgb(hexcode):
        if hexcode is None:
                return None
        return tuple(codecs.decode(hexcode[1:], 'hex'))
        
def hex2bit(hexcode):
        hexcode = hexcode.replace('#' , '0x')
        bitstring = BitArray(hexcode)
        return  bitstring.bin
        
def bit2hex(bitstring):
        for i in range(4, 20, 4):
                bits = '0'*i

                if(bitstring[:i] == bits):
                        return '#000000'
                elif(bitstring[:i] == bits):
                        hexcode = hex(int(bitstring, 2))
                        hexcode = '#' + '0'*(i%4) + hexcode[2:]
                        return hexcode

        if bitstring == '':
                return None
        
        hexcode = hex(int(bitstring, 2))
        hexcode = hexcode.replace('0x' , '#')
        return (hexcode)

# Encodes message into byte form and then turns message into binary while ignoring the '0b' value in the beginning
def str2bin(message):
        binary = bin(int(binascii.hexlify(message.encode()), 16))
        return binary[2:]
        
# Adds the '0b' back to the binary, transforms it into readable bytes and decodes it into utf-8 to be read as string
def bin2str(binary):
        binary = int(('0b' + binary), 2)
        message = binary.to_bytes((binary.bit_length() + 7) // 8, 'big').decode()
        return message

# Replaces last value of the rgb hexcode with the binary digit of the message
def encode(bitstring, digit):
        bitstring = bitstring[:-1] + digit
        return bitstring
                
# Looks at the last digit of the rgb hexcode and returns it to be added to binary
def decode(bitstring):
        if bitstring[-1] in ('0', '1'):
                return bitstring[-1]
        else:
                return None

# Function to hide a file into image
# Use input file of image
# Use input file of text to hide
def hide(filename, message):
        img = Image.open(filename)
        binary = str2bin(message)
        
        # Adds a breakpoint so we know where to stop
        binary = binary  + '1111111111111110'
        
        # Check if img is avaialble in rgba and convert it just in case
        if img.mode in ('RGBA'):
                img = img.convert('RGBA')
                datas = img.getdata()
                
                newData = []
                temp = ''
                digit = 0
                
                # Item corresponds to pixels
                for item in datas:
                        
                        # If digits is less than the binary length, create a new pixel and using encode method replace with corresponding position in binary value 
                        if(digit < len(binary)):
                                bitstring = encode(hex2bit(rgb2hex(item[0], item[1], item[2])), binary[digit])
                                newpix = bit2hex(bitstring)
                                
                                # If failed just add pixel to the newdata
                                if newpix == None:
                                        newData.append(item)
                                
                                # If success change new pixel to rgb and add it to new data
                                else:
                                        r, g, b = hex2rgb(newpix)
                                        newData.append((r,g,b,255))
                                        digit += 1
                        
                        # If we finished the length of the binary then just add back the normal pixels
                        else:
                                newData.append(item)

                # Add the new data to the image
                img.putdata(newData)
                img.save(filename, 'PNG')
                return ''
                
        else:
                return 'Incorrect image mode, could not hide.'

# Function to get a file from image
# Use input file of image
# Use input file of text to get the text
def retr(filename, filetosave):
        img = Image.open(filename)
        binary = ''
        
        if img.mode in ('RGBA'):
                img = img.convert('RGBA')
                datas = img.getdata()
                
                for item in datas:
                        digit = decode(hex2bit(rgb2hex(item[0], item[1], item[2])))
                        if digit == None:
                                pass
                        else:
                                binary = binary + digit
                                if((binary[-16:]) == '1111111111111110'):
                                        creatfile(bin2str(binary[:-16]), filetosave)
                                        return 'COMPLETED!'
                
                creatfile(bin2str(binary), filetosave)
                return ''
                
        else:
                return 'Incorrect image mode, could not retrieve.'

# Function to read file
# Read file name by user input
# Save the ile in variable conteudo
# Return conteudo
def readfile(filename):
        conteudo=""
        try:
                with open (filename) as f:
                        line = f.readline()
                        conteudo+=line
                        while line:
                                line = f.readline()
                                conteudo+=line
                        return conteudo
        except IOError as e:
                
                # Py3 f-strings
                print(f"Couldn't open or write to file ({e})")
                sys.exit()
        
# Function to create a new file
# Create file with name given in input by user
def creatfile(conteudo, filetosave):
        with open(filetosave, "w") as f:
                f.write(conteudo)

# Function to create a menu
# Use option from User choise
# Option 1 - encryt file text
# Option 2 - decrypt file text
# Option 3 - hide file text inside image
# Option 4 - get file text from image
# Option 5 - Exit program
def print_menu():
        print (Fore.CYAN + '')
        print ('------------------------------------------------------------')
        print ('------ 1 -- Encrypt one file text (.txt) - Encryption ------')
        print ('------ 2 -- Decrypt one file text (.txt) - Encryption ------')
        print ('------------------------------------------------------------')
        print ('-- 3 - Hide file text (.txt) inside image - Steganography --')
        print ('-- 4 - Get the file text (.txt) from image - Steganography -')
        print ('------------------------------------------------------------')
        print ('------------------------ 5 -- Exit -------------------------')
        print ('------------------------------------------------------------')
        print (Fore.WHITE + '')
        

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

# Main to run Function Main to run all choise User chose by input
if __name__ == '__main__':
        Main()

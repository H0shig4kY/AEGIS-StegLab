#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from PIL import Image

from core.converters import (
    rgb2hex,
    hex2bit,
    bin2str,
)

from utils.helpers import creatfile

def decode(bitstring: str):
    """
    Extract the least significant bit from a binary string.
    """
    if bitstring[-1] in ("0", "1"):
        return bitstring[-1]
    else:
        return None
    
# Function to get a file from image
# Use input file of image
# Use input file of text to get the text
def retr(filename, filetosave):
        img = Image.open(filename)
        binary = ''

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
                

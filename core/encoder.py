from PIL import Image



from core.converters import (
    str2bin,
    rgb2hex,
    hex2bit,
    bit2hex,
    hex2rgb,
)

def encode(bitstring: str, digit: str) -> str:
    """
    Replace the least significant bit with the payload bit.
    """
    bitstring = bitstring[:-1] + digit
    return bitstring

# Function to hide a file into image
# Use input file of image
# Use input file of text to hide
def hide(filename, message):
        img = Image.open(filename)
        binary = str2bin(message)
        
        # Adds a breakpoint so we know where to stop
        binary = binary  + '1111111111111110'
        
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
        print(f"Embedded bits: {digit}/{len(binary)}")
        img.save(filename, 'PNG')
        print("Saved to:", filename)
        img2 = Image.open(filename).convert("RGBA")

        first = next(iter(img2.getdata()))

        print("First saved pixel:", first)
        
        return ''
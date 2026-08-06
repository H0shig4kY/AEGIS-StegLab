#PROJECT AEGIS - STEGLAB
#Version 1.0.0

from PIL import Image, UnidentifiedImageError
from core.converters import str2bin


def get_image_capacity(filename: str) -> int:
    """
    Return the maximum payload capacity of the image in bits.
    One pixel stores one bit.
    """
    try:
        img = Image.open(filename)

    except (FileNotFoundError, UnidentifiedImageError, OSError):
        return 0
    
    img = img.convert("RGBA")

    width, height = img.size

    return width * height


def analyze_image(filename, message):
    try:
        img = Image.open(filename)

    except FileNotFoundError:
        print("[ERROR] Image file not found.")
        return None

    except UnidentifiedImageError:
        print("[ERROR] Invalid image format.")
        return None

    except OSError:
        print("[ERROR] Unable to open image.")
        return None

    width, height = img.size

    capacity = width * height
    payload = len(str2bin(message)) + 16
    remaining = capacity - payload
    fits = payload <= capacity

    return {
        "width": width,
        "height": height,
        "capacity": capacity,
        "payload": payload,
        "remaining": remaining,
        "fits": fits,
    }


def print_image_info(filename: str, message: str) -> bool:
    """
    Display image information and return whether the payload fits.
    """
    info = analyze_image(filename, message)

    if info is None:
        return False

    print("======================================================")
    print("                   Image Information                  ")
    print("======================================================")
    print(f"Resolution : {info['width']} x {info['height']}")
    print(f"Capacity   : {info['capacity']} bits")
    print(f"Payload    : {info['payload']} bits")
    print(f"Remaining  : {info['remaining']} bits")
    print()

    if info["fits"]:
        print("Status     : OK")
        print("======================================================")
    else:
        print("Status     : ERROR")
        print("======================================================")

    print()

    return info["fits"]

def validate_image(filename: str) -> bool:
    try:
        img = Image.open(filename)

        if img.width == 0 or img.height == 0:
            print("[ERROR] Invalid image.")
            return False

        return True

    except FileNotFoundError:
        print("[ERROR] Image file not found.")
        return False

    except UnidentifiedImageError:
        print("[ERROR] Invalid image format.")
        return False

    except OSError:
        print("[ERROR] Unable to open image.")
        return False
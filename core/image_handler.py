# PROJECT AEGIS - STEGLAB
# Version 1.3.0

from PIL import Image, UnidentifiedImageError
from core.framing import frame_size_for_length

def get_image_capacity(filename: str) -> int:
    """
    Return the maximum payload capacity of the image in bits.
    One pixel stores one bit.
    """
    try:
        with Image.open(filename) as img:
            width, height = img.size
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        return 0

    return width * height

def analyze_image(filename, message):
    try:
        with Image.open(filename) as img:
            width, height = img.size
    except FileNotFoundError:
        print("[ERROR] Image file not found.")
        return None
    except UnidentifiedImageError:
        print("[ERROR] Invalid image format.")
        return None
    except OSError:
        print("[ERROR] Unable to open image.")
        return None

    capacity = width * height
    try:
        if isinstance(message, str):
            payload_bytes = message.encode("utf-8")
        elif isinstance(message, (bytes, bytearray, memoryview)):
            payload_bytes = bytes(message)
        else:
            raise TypeError("Message must be text or bytes-like data.")
        payload = frame_size_for_length(len(payload_bytes)) * 8
    except (TypeError, ValueError) as exc:
        print(f"[ERROR] Invalid payload: {exc}")
        return None
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
        with Image.open(filename) as img:
            if img.width == 0 or img.height == 0:
                print("[ERROR] Invalid image.")
                return False
            img.verify()
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

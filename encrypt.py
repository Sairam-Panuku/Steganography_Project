import cv2
import numpy as np
from stegano import lsb

def encrypt_image(image_path, output_path, secret, passcode):
    image = cv2.imread(image_path)
    if image is None:
        return False

    # Embed secret message with passcode
    secret_data = f"{passcode}:{secret}"
    encoded_image = lsb.hide(image_path, secret_data)

    # Save encrypted image
    encoded_image.save(output_path)
    return True

import numpy as np
from PIL import Image, ImageEnhance
from pytesseract import pytesseract
import cv2


def parse_image(image_path, crop_region, scale=10, tesseract_config=r'--oem 3 --psm 6 tessedit_char_unblacklist=0123456789') -> str:
    image = Image.open(image_path)
    cropped_image = image.crop(crop_region)
    cropped_image = cropped_image.convert('L')
    cropped_image = cropped_image.point(lambda p: p > 128 and 255)
    cropped_image = cropped_image.resize((cropped_image.width * scale, cropped_image.height * scale),
                                         Image.LANCZOS)
    cropped_image = cropped_image.point(lambda p: p > 220 and 255)
    cropped_image.save('images/test.png')
    text = pytesseract.image_to_string(cropped_image, config=tesseract_config).strip()
    return text

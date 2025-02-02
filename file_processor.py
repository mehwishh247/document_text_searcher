import os
import pdfplumber
from pypdf import PdfReader

import pytesseract
import cv2

CACHE_FOLDER = 'temp'
UPLOAD_PATH = 'uploads'

def extract_images(page):
    count = 0

    for img in page.images:
        with open(os.path.join(CACHE_FOLDER, f'{str(count).zfill(3)}.png'), 'wb') as image:
            image.write(img.data)
        count += 1

def extract_text_from_image(image_number):
    image_path = os.path.join(CACHE_FOLDER, f'{str(image_number).zfill(3)}.png')
    
    im = cv2.imread(image_path)    
    im = cv2.resize(im, (0, 0), fx = 0.7, fy = 0.7)
    text = pytesseract.image_to_string(im)

    #os.remove(image_path)

    return text

def set_output(filename):
    text = pdfplumber.open(f'uploads/{filename}')
    file = PdfReader(f'uploads/{filename}')

    result = []

    for page in range(len(file.pages)):
        extract_images(file.pages[page])

        if text.pages[page].extract_text_simple() == '':
            for img in range(0, len(text.pages[page].images)):
                result.append({'type': 'image', 'content': extract_text_from_image(img)})

        breakdown = text.pages[page].extract_text_simple().split('\n \n')

        for img in range(0, len(breakdown) - 1):
            result.append({'type': 'paragraph', 'content': breakdown[img]})
            result.append({'type': 'image', 'content': extract_text_from_image(img)})

        result.append({'type': 'paragraph', 'content': breakdown[-1]})
    
    return result

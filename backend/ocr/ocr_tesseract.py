import pytesseract
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_tesseract(img):
    """
    Extract text using Tesseract OCR
    """
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    return data

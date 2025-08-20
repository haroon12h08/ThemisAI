import cv2
from preprocessing.image_preprocess import preprocess_image
from ocr.ocr_tesseract import extract_text_tesseract
from ocr.ocr_easyocr import extract_text_easyocr
from ocr.field_extractor import extract_fields
from detection.common_checks import compare_amounts

def process_cheque(img_path: str):
    """
    Pipeline for cheque processing:
    - Preprocess
    - OCR (Tesseract + EasyOCR)
    - Field extraction
    - Consistency check
    """
    img = preprocess_image(img_path)

    # Extract text with Tesseract
    tess_data = extract_text_tesseract(img)
    text_blocks = [t for t in tess_data["text"] if t.strip() != ""]

    # Extract text with EasyOCR (for handwritten fields)
    easyocr_text = extract_text_easyocr(img_path)
    text_blocks.extend(easyocr_text)

    # Extract cheque fields
    fields = extract_fields(text_blocks)

    # Compare amounts
    similarity = compare_amounts(fields["amount_digits"], fields["amount_words"])
    fields["amount_similarity"] = similarity

    return fields

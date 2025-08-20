import easyocr

reader = easyocr.Reader(['en'])

def extract_text_easyocr(img_path: str):
    """
    Extract text using EasyOCR for handwritten content
    """
    results = reader.readtext(img_path, detail=0)
    return results

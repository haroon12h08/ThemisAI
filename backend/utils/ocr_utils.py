import cv2
import re
from easyocr import Reader

reader = Reader(['en'], gpu=False)

def preprocess_image(image_path: str) -> str:
    """Preprocess image for better OCR accuracy."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    temp_path = "preprocessed.png"
    cv2.imwrite(temp_path, img)
    return temp_path

def extract_text(image_path: str):
    """Run OCR on cheque with preprocessing."""
    preprocessed_path = preprocess_image(image_path)
    text = reader.readtext(preprocessed_path, detail=0)
    print("📝 OCR Raw Output:", text)  # Debugging
    return text

def extract_cheque_details(text_list):
    """Extract structured cheque details from OCR text."""
    details = {
        "payee": None,
        "amount_words": None,
        "amount_digits": None,
        "date": None,
        "ifsc": None,
        "micr": None,
    }

    full_text = " ".join(text_list)

    # Payee
    payee_match = re.search(r"Pay\s+(?:to\s+the\s+order\s+of\s+)?([A-Za-z\s]+)", full_text, re.IGNORECASE)
    if payee_match:
        details["payee"] = payee_match.group(1).strip()

    # Amount digits
    digits_match = re.search(r"₹?\s?(\d{1,9}(?:,\d{2,3})*(?:\.\d{2})?)", full_text)
    if digits_match:
        details["amount_digits"] = digits_match.group(1)

    # Amount words
    words_match = re.search(r"Rupees\s+([A-Za-z\s]+)", full_text, re.IGNORECASE)
    if words_match:
        details["amount_words"] = words_match.group(1).strip()

    # Date
    date_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", full_text)
    if date_match:
        details["date"] = date_match.group(1)

    # IFSC
    ifsc_match = re.search(r"[A-Z]{4}0[A-Z0-9]{6}", full_text)
    if ifsc_match:
        details["ifsc"] = ifsc_match.group(0)

    # MICR
    micr_match = re.search(r"\b\d{9}\b", full_text)
    if micr_match:
        details["micr"] = micr_match.group(0)

    return details

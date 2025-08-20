import re

def extract_fields(text_blocks: list[str]):
    """
    Extract important fields from cheque OCR text
    """
    fields = {
        "payee": None,
        "amount_words": None,
        "amount_digits": None,
        "date": None,
        "ifsc": None,
        "micr": None
    }

    text = " ".join(text_blocks)

    # IFSC Code
    ifsc_match = re.search(r"[A-Z]{4}0[A-Z0-9]{6}", text)
    if ifsc_match:
        fields["ifsc"] = ifsc_match.group(0)

    # Date (dd/mm/yyyy or dd-mm-yyyy)
    date_match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
    if date_match:
        fields["date"] = date_match.group(0)

    # Amount digits (₹ or Rs.)
    amt_digit_match = re.search(r"(₹|Rs\.?)\s?\d+[,.]?\d*", text)
    if amt_digit_match:
        fields["amount_digits"] = amt_digit_match.group(0)

    # Amount in words (look for 'Rupees')
    amt_word_match = re.search(r"Rupees[\s\S]*?(only|Only)", text)
    if amt_word_match:
        fields["amount_words"] = amt_word_match.group(0)

    # Payee name (after 'Pay' or 'Pay to')
    payee_match = re.search(r"Pay\s+to\s+the\s+order\s+of\s+([A-Za-z\s]+)", text)
    if payee_match:
        fields["payee"] = payee_match.group(1).strip()

    return fields

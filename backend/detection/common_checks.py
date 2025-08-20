from rapidfuzz import fuzz

def compare_amounts(amount_digits: str, amount_words: str) -> float:
    """
    Compare numeric vs word representation of amount
    """
    if not amount_digits or not amount_words:
        return 0.0
    return fuzz.ratio(amount_digits.lower(), amount_words.lower())

import pytesseract
from typing import List
import numpy as np

from .config import TESSERACT_CONFIG


def extract_ocr_lines(image: np.ndarray, config: str = TESSERACT_CONFIG) -> List[str]:
    """
    Zwraca niepuste linie OCR po usunięciu zbędnych spacji.
    """
    text = pytesseract.image_to_string(image, config=config)
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]

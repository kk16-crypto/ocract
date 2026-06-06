import pytesseract
from typing import List
import numpy as np

from .config import TESSERACT_CONFIG


def extract_ocr_lines(image: np.ndarray, config: str = TESSERACT_CONFIG) -> list[str]:
    text = pytesseract.image_to_string(image, config=config)

    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def normalize_decimal_lines(lines: List[str]) -> List[str]:
    """
    Normalizuje format liczb zmiennoprzecinkowych w tekście OCR.

    Zamienia przecinki na kropki, co ujednolica format liczbowy.

    Args:
        lines (List[str]): Lista linii tekstu OCR.

    Returns:
        List[str]: Linie z ujednoliconym separatorem dziesiętnym.
    """

    return [line.replace(",", ".") for line in lines]

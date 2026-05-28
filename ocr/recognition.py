from concurrent.futures import ThreadPoolExecutor
import pytesseract
from typing import List
import numpy as np
from PIL import Image

from .config import TESSERACT_CONFIG
from .preprocessing import preprocess_crop_for_ocr


def extract_ocr_lines(image: np.ndarray, config: str = TESSERACT_CONFIG) -> List[str]:
    """
    Wykonuje OCR na obrazie i zwraca listę niepustych linii tekstu.

    Args:
        image (np.ndarray): Obraz wejściowy do OCR.
        config (str): Konfiguracja Tesseract OCR.

    Returns:
        List[str]: Lista linii tekstu po usunięciu pustych wartości i strip().
    """

    text = pytesseract.image_to_string(image, config=config)
    return [line.strip() for line in text.splitlines() if line.strip()]


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


def process_row(
    row_img: Image.Image,
    scale: float,
    config: str,
) -> str:
    """
    Przetwarza pojedynczy wycinek wiersza tabeli i wykonuje OCR.

    Args:
        row_img (Image.Image): Obraz pojedynczego wiersza.
        scale (float): Skala używana w preprocessingu obrazu.
        config (str): Konfiguracja Tesseract OCR.

    Returns:
        str: Rozpoznany tekst dla danego wiersza (po strip).
    """

    processed = preprocess_crop_for_ocr(np.array(row_img), scale)
    return pytesseract.image_to_string(processed, config=config).strip()


# def recognize_cells(
#     row_segments_len: int,
#     col_crop: Image.Image,
#     row_segments: list[tuple[int, int]],
#     scale: float = 3.41,
#     config: str = "stdout --oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.,",
# ):
#     """
#     Wykrywa i rozpoznaje tekst w komórkach kolumny na podstawie segmentów wierszy.

#     Funkcja:
#     - wycina obrazy poszczególnych wierszy z kolumny,
#     - przetwarza je równolegle (ThreadPoolExecutor),
#     - wykonuje OCR na każdym wycinku.

#     Args:
#         row_segments_len (int): Liczba segmentów wierszy (bez ostatniego domknięcia).
#         col_crop (Image.Image): Wycięta kolumna tabeli jako obraz.
#         row_segments (list[tuple[int, int]]): Lista (y_start, y_end) dla wierszy.
#         scale (float): Skala używana w preprocessingu OCR.
#         config (str): Konfiguracja Tesseract OCR.

#     Returns:
#         List[str]: Lista rozpoznanych wartości dla każdego wiersza.
#     """

#     row_images = []

#     # Tworzenie wycinków dla wszystkich pełnych wierszy
#     for i in range(row_segments_len - 1):
#         row_img = col_crop.crop(
#             (0, row_segments[i][0], col_crop.width, row_segments[i + 1][1])
#         )
#         row_images.append(row_img)

#     # Ostatni wiersz domykający zakres (do końca obrazu)
#     last_row = col_crop.crop((0, row_segments[-1][1], col_crop.width, col_crop.height))
#     row_images.append(last_row)

#     # Równoległe OCR dla wszystkich wierszy
#     with ThreadPoolExecutor() as executor:
#         results = list(
#             executor.map(
#                 lambda img: process_row(img, scale, config),
#                 row_images,
#             )
#         )

#     return results

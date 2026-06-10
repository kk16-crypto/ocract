import cv2
import numpy as np

from .config import DEFAULT_SCALE, DEFAULT_PADDING


def preprocess_crop_for_ocr(
    img: np.ndarray,
    scale: float = DEFAULT_SCALE,
    padding: int = DEFAULT_PADDING,
) -> np.ndarray:
    """
    Wykonuje preprocessing obrazu w celu poprawy jakości OCR.

    Pipeline obejmuje:
    - konwersję do skali szarości,
    - dodanie marginesu (padding),
    - skalowanie obrazu,
    - wygładzanie (Gaussian blur),
    - binaryzację adaptacyjną,
    - operację morfologiczną domknięcia.

    Args:
        img (np.ndarray): Obraz wejściowy w formacie BGR (OpenCV).
        scale (float): Współczynnik powiększenia obrazu przed OCR.
        padding (int): Rozmiar białej ramki dodawanej wokół obrazu.

    Returns:
        np.ndarray: Przetworzony obraz binarny gotowy do OCR.
    """

    # Konwersja do skali szarości (OCR działa stabilniej na grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Dodanie białego marginesu, aby poprawić rozpoznawanie znaków przy krawędziach
    gray = cv2.copyMakeBorder(
        gray,
        padding,
        padding,
        padding,
        padding,
        borderType=cv2.BORDER_CONSTANT,
        value=255,
    )

    # Skalowanie obrazu w celu zwiększenia czytelności małych znaków
    gray = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_LANCZOS4,
    )

    # Redukcja szumu przed binaryzacją
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptacyjna binaryzacja – lepsza dla nierównomiernego oświetlenia
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        12,
    )

    # Operacja domknięcia usuwa drobne przerwy w znakach (łączenie elementów)
    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        np.ones((2, 2), np.uint8),
    )

    return thresh

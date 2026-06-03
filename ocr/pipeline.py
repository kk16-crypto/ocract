from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import cv2
from PIL import Image
import pytesseract
import traceback
from .table_edges import detect_table_columns, detect_table_rows


# config
from .config import (
    TESSERACT_CONFIG,
    DEFAULT_TARGET_COLOR,
    DEFAULT_TOLERANCE,
)

# setup
# from .paths import configure_tesseract

# geometry / crops
from .crops import (
    build_crop_boxes,

)

#  OCR / processing
from .recognition import (
    extract_ocr_lines,
)
from .preprocessing import preprocess_crop_for_ocr



def run_ocr(
    image_path: str | Path,
    target_color: Tuple[int, int, int] = DEFAULT_TARGET_COLOR,
    tolerance: int = DEFAULT_TOLERANCE,
) -> Dict[str, List[str]]:
    """
    Przetwarza obraz tabeli i wykonuje pełny pipeline ekstrakcji danych OCR.

    Pipeline obejmuje:
    1. Detekcję struktury tabeli (kolumny i ostatni wiersz)
    2. Wyznaczenie obszarów (crop boxów) dla kolumn
    3. Wycięcie kolumn z obrazu
    4. Segmentację wierszy w każdej kolumnie
    5. OCR dla komórek tabeli
    6. Normalizację wyników liczbowych
    7. Złożenie wyniku do słownika

    Args:
        image_path (str | Path): Ścieżka do obrazu wejściowego.
        target_color (Tuple[int, int, int]): Kolor referencyjny do detekcji tabeli.
        tolerance (int): Tolerancja dopasowania koloru.

    Returns:
        Dict[str, List[str]]: Słownik mapujący klucze kolumn na listy wartości OCR.
    """

    try:
        img = Image.open(image_path)
    
        points = detect_table_columns(image_path, target_color)

        last_row = detect_table_rows(image_path, target_color, col_num=-1)

        crop_boxes = build_crop_boxes(points, last_row, len(points))

        col_crop = img.crop(crop_boxes[0])

        col_np_arr = np.array(col_crop)
        col_raw = cv2.cvtColor(col_np_arr, cv2.COLOR_RGB2BGR)

        prep_crop = preprocess_crop_for_ocr(col_np_arr)
        text = extract_ocr_lines(
            prep_crop,
            TESSERACT_CONFIG,
        )
        # text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)

        print(f"text:------------------ {text}")
        return text
    except Exception as e:
        print(traceback.format_exc())
        return f"[OCR ERROR] {str(e)}"
        

    # # 1. Detekcja struktury tabeli (kolumny + ostatni wiersz)
    # points = detect_table_columns_by_color(
    #     image_path, target_color=target_color, tolerance=tolerance
    # )

    # last_row = detect_table_last_row_by_color(
    #     image_path, target_color=target_color, tolerance=tolerance
    # )

    # # 2. Budowa bounding boxów dla kolumn
    # crop_boxes = build_crop_boxes(points, last_row)

    # if len(crop_boxes) != len(TABLE_KEYS):
    #     raise ValueError(
    #         f"Expected {len(TABLE_KEYS)} crop boxes, got {len(crop_boxes)}"
    #     )

    # # Nadpisanie zdjęcia z wyciętym pfragmentem tabeli
    # save_crop_image(image_path, image_path, points[9])

    # final_data: Dict[str, List[str]] = {}

    # # 3. Przetwarzanie kolumn
    # with Image.open(image_path) as image:
    #     for key, box, config in zip(TABLE_KEYS, crop_boxes, TESSERACT_CONFIG):
    #         # Wycięcie kolumny
    #         col_crop = image.crop(box)

    #         # Konwersja do OpenCV (dla detekcji wie
    #         col_np_arr = np.array(col_crop)
    #         col_raw = cv2.cvtColor(col_np_arr, cv2.COLOR_RGB2BGR)

    #         # Segmentacja wierszy w kolumnie
    #         row_segments = detect_row_segments_from_column(col_raw)
    #         row_segments_len = len(row_segments)

    #         # OCR zależnie od typu kolumny
    #         col_arr = []
    #         if key == TABLE_KEYS[1]:
    #             # Kolumna przetwarzana jako cały blok tekstu
    #             prep_crop = preprocess_crop_for_ocr(col_np_arr)
    #             col_arr = extract_ocr_lines(
    #                     prep_crop,
    #                     config,
    #                 )

    #         elif key == TABLE_KEYS[0]:
    #             # Kolumny tabelaryczne – OCR per komórka
    #             col_arr = recognize_cells(
    #                 row_segments_len,
    #                 col_crop,
    #                 row_segments,
    #                 scale=DEFAULT_SCALE[0],
    #                 config=config,
    #             )
    #         else:
    #             # Kolumny tabelaryczne – OCR per komórka z inną skalą
    #             col_arr = recognize_cells(
    #                 row_segments_len,
    #                 col_crop,
    #                 row_segments,
    #                 scale=DEFAULT_SCALE[1],
    #                 config=config,
    #             )

    #         # Normalizacja wartości liczbowych (kropka zamiast przecinka)
    #         if key in TABLE_KEYS[2:]:
    #             col_arr = normalize_decimal_lines(col_arr)

    #         # Usunięcie pustych wyników OC
    #         final_data[key] = [val for val in col_arr if val != ""]
    # return final_data

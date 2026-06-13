from pathlib import Path
from typing import Tuple, List

import cv2
import numpy as np
from .config import DEFAULT_TARGET_COLOR


SEPARATOR = np.array(DEFAULT_TARGET_COLOR, dtype=np.int16)


def _find_color_segments(
    pixels: np.ndarray,
    color: np.ndarray,
    tolerance: int = 10,
) -> List[Tuple[int, int]]:
    """
    Zwraca indeksy pikseli, które pasują do zadanego koloru w tolerancji.
    """

    diff = np.abs(pixels.astype(np.int16) - color)
    matches = np.all(diff <= tolerance, axis=1)

    transitions = np.diff(np.pad(matches.view(np.int8), (1, 1)))

    return np.flatnonzero(transitions == 1)


def detect_table_columns(
    image_path: str | Path,
    target_color: Tuple[int, int, int],
    segment_idx: int | None = None,
    tolerance: int = 10,
) -> Tuple[List[int], int | None]:
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Nie można wczytać obrazu: {image_path}")

    sample_row_y = image.shape[0] // 2

    if segment_idx is None:
        return _find_color_segments(image[sample_row_y], target_color, tolerance)

    return _find_color_segments(image[sample_row_y], target_color, tolerance)[
        segment_idx
    ]


def detect_table_rows(
    image_path: str | Path,
    target_color: Tuple[int, int, int],
    segment_idx: int | None = None,
    tolerance: int = 10,
) -> Tuple[List[int], int | None]:
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Nie można wczytać obrazu: {image_path}")

    sample_row_x = image.shape[1] // 2

    if segment_idx is None:
        return _find_color_segments(image[:, sample_row_x], target_color, tolerance)

    return _find_color_segments(image[:, sample_row_x], target_color, tolerance)[
        segment_idx
    ]

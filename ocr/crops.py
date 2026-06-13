from typing import List, Tuple


def build_crop_boxes(
    points: List[int], first_row: int, last_row: int, col_num: int
) -> List[Tuple[int, int, int, int]]:
    """
    Zbuduj bounding boxy dla kolumn tabeli na podstawie punktów granicznych.

    Args:
        points: Lista punktów granicznych wykrytych na osi X.
        first_row: Pozycja Y pierwszego wiersza tabeli.
        last_row: Pozycja Y ostatniego wiersza tabeli.
        col_num: Liczba kolumn do wycięcia.

    Returns:
        Lista prostokątów crop w formacie (left, top, right, bottom).
    """
    if last_row is None:
        return []

    # Korekty granic kolumn wynikające z detekcji linii tabeli
    # (np. pominięcie separatorów / marginesów między kolumnami)

    result = []

    # Każdy box obejmuje przestrzeń między sąsiednimi punktami granicznymi
    for i in range(col_num - 1):
        result.append((points[i], first_row, points[i + 1], last_row))

    return result

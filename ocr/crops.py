from typing import List, Tuple


def build_crop_boxes(
    points: List[int], last_row: int | None, col_num: int
) -> List[Tuple[int, int, int, int]]:
    """
    Buduje bounding boxy (crop boxes) dla kolumn tabeli na podstawie
    wykrytych punktów granicznych oraz pozycji ostatniego wiersza.

    Args:
        points (List[int]): Lista punktów granicznych wykrytych dla tabeli.
            Każda para punktów definiuje granice kolumn.
        last_row (int | None): Pozycja Y ostatniego wiersza tabeli.
            Jeśli None, zwracana jest pusta lista.

    Returns:
        List[Tuple[int, int, int, int]]: Lista prostokątów crop w formacie
        (left, top, right, bottom) dla każdej kolumny.
    """

    if last_row is None:
        return []

    # Korekty granic kolumn wynikające z detekcji linii tabeli
    # (np. pominięcie separatorów / marginesów między kolumnami)

    result = []

    for i in range(col_num-1):
        result.append((points[i], 0, points[i + 1], last_row))
        
    return result

from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image
import traceback

from .config import (
    TESSERACT_CONFIG,
    DEFAULT_TARGET_COLOR,
    DEFAULT_TOLERANCE,
)
from .table_edges import detect_table_columns, detect_table_rows
from .crops import build_crop_boxes
from .recognition import extract_ocr_lines
from .preprocessing import preprocess_crop_for_ocr


def run_ocr(
    image_path: str | Path,
    target_color: Tuple[int, int, int] = DEFAULT_TARGET_COLOR,
    tolerance: int = DEFAULT_TOLERANCE,
) -> Dict[str, List[str]]:

    try:
        img = Image.open(image_path)

        points = detect_table_columns(image_path, target_color)
        last_row = detect_table_rows(image_path, target_color, col_num=-1)
        first_row = detect_table_rows(image_path, target_color, col_num=1)

        crop_boxes = build_crop_boxes(points, first_row, last_row, len(points))

        columns = []
        max_rows = 0

        for box in crop_boxes:
            col_crop = img.crop(box)
            col_np_arr = np.array(col_crop)

            processed = preprocess_crop_for_ocr(col_np_arr)
            lines = extract_ocr_lines(processed, config=TESSERACT_CONFIG)

            columns.append(lines)
            max_rows = max(max_rows, len(lines))

        rows = []
        for i in range(max_rows):
            row = []
            for col in columns:
                row.append(col[i] if i < len(col) else "")
            rows.append("\t".join(row).rstrip())

        result = "\n".join(rows)
        return result

    except Exception as e:
        print(traceback.format_exc())
        return f"[OCR ERROR] {str(e)}"

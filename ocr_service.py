import pytesseract
from PIL import Image

def run_ocr(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="eng+pol")
        return text.strip()
    except Exception as e:
        return f"[OCR ERROR] {str(e)}"
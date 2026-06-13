from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout
from .drop_zone_widget import DropZoneWidget
from .text_editor_widget import TextEditorWidget
from ocr.pipeline import run_ocr
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCRact")
        self.setMinimumSize(800, 600)
        self.image_path = ""
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        self.drop_zone = DropZoneWidget()
        self.text_editor = TextEditorWidget()

        btn_layout = QHBoxLayout()
        self.btn_choose = QPushButton("Wybierz plik")
        self.btn_ocr = QPushButton("Uruchom OCR")
        btn_layout.addWidget(self.btn_choose)
        btn_layout.addWidget(self.btn_ocr)

        self.btn_save = QPushButton("Zapisz do .txt")

        self.btn_choose.clicked.connect(self.drop_zone.open_file_dialog)
        self.btn_ocr.clicked.connect(self.run_ocr)
        self.btn_save.clicked.connect(self.save_file)

        self.drop_zone.file_selected.connect(self.on_image_selected)
        self.drop_zone.invalid_file_selected.connect(self.on_message)
        self.text_editor.text_changed.connect(self.on_text_changed)

        layout.addWidget(self.drop_zone)
        layout.addLayout(btn_layout)
        layout.addWidget(self.text_editor)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def on_image_selected(self, path: str):
        self.image_path = path
        self.drop_zone.set_message(f"Wybrano: {Path(path).name}")

    def on_message(self, text: str):
        self.drop_zone.set_message(text)

    def on_text_changed(self, text: str):
        pass

    def run_ocr(self):
        if not self.image_path:
            self.drop_zone.set_message("Najpierw wybierz plik")
            return

        text = run_ocr(self.image_path)
        self.text_editor.set_text(text)

    def save_file(self):
        text = self.text_editor.get_text()

        if not text.strip():
            self.drop_zone.set_message("Brak danych do zapisania")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz plik",
            "",
            "Text Files (*.txt)"
        )

        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self.drop_zone.set_message(f"Zapisano: {path}")
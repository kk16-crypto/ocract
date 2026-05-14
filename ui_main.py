from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt

from ocr_service import run_ocr


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR App MVP")
        self.setMinimumSize(800, 600)

        self.image_path = None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # DROP / INFO
        self.info_label = QLabel("Przeciągnij obraz lub wybierz plik")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("border: 1px dashed gray; padding: 20px;")

        # BUTTONS
        btn_layout = QHBoxLayout()

        self.btn_choose = QPushButton("Wybierz plik")
        self.btn_ocr = QPushButton("Uruchom OCR")

        btn_layout.addWidget(self.btn_choose)
        btn_layout.addWidget(self.btn_ocr)

        # TEXT AREA
        self.text_edit = QTextEdit()

        # SAVE
        self.btn_save = QPushButton("Zapisz do .txt")

        # EVENTS
        self.btn_choose.clicked.connect(self.choose_file)
        self.btn_ocr.clicked.connect(self.run_ocr)
        self.btn_save.clicked.connect(self.save_file)

        # DROP ENABLE
        self.setAcceptDrops(True)

        layout.addWidget(self.info_label)
        layout.addLayout(btn_layout)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    # ---------------- FILE PICK ----------------

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if path:
            self.image_path = path
            self.info_label.setText(f"Wybrano: {path}")

    # ---------------- OCR ----------------

    def run_ocr(self):
        if not self.image_path:
            self.info_label.setText("Najpierw wybierz plik")
            return

        text = run_ocr(self.image_path)
        self.text_edit.setPlainText(text)

    # ---------------- SAVE ----------------

    def save_file(self):
        text = self.text_edit.toPlainText()

        if not text.strip():
            self.info_label.setText("Brak danych do zapisania")
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

            self.info_label.setText(f"Zapisano: {path}")

    # ---------------- DRAG & DROP ----------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()

        if path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            self.image_path = path
            self.info_label.setText(f"Drop: {path}")
        else:
            self.info_label.setText("Nieobsługiwany format")
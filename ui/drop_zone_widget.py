from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from pathlib import Path

class DropZoneWidget(QWidget):
    file_selected = Signal(str)
    invalid_file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel("Przeciągnij obraz lub wybierz plik")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(180)

        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_message(self, text: str):
        self.label.setText(text)

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if path:
            self.file_selected.emit(path)

    def mousePressEvent(self, event):
        self.open_file_dialog()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            event.ignore()
            return

        path = urls[0].toLocalFile()

        if path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            self.file_selected.emit(path)
            event.acceptProposedAction()
        else:
            self.invalid_file_selected.emit("Nieobsługiwany format")
            event.ignore()
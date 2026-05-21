from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Signal

class TextEditorWidget(QWidget):
    text_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def _on_text_changed(self):
        self.text_changed.emit(self.text_edit.toPlainText())

    def set_text(self, text: str):
        self.text_edit.blockSignals(True)
        self.text_edit.setPlainText(text)
        self.text_edit.blockSignals(False)

    def get_text(self) -> str:
        return self.text_edit.toPlainText()
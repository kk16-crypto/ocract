import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.resources import resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(resource_path("style.qss"), "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

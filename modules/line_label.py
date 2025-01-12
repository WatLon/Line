from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

class LineLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__("line", parent)
        font_path = 'fonts/NType82-Regular.otf'
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 50)
        self.setFont(font)
        self.setStyleSheet("color: white;")
        self.setAlignment(Qt.AlignCenter)
        self.setGeometry(100, 20, 150, 150)

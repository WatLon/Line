from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

class ClickableLink(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        font_path = 'fonts/NType82-Regular.otf'
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16)
        self.setFont(font)
        self.setStyleSheet("color: rgba(255, 255, 255, 32);")
        self.setOpenExternalLinks(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText('<a href="https://t.me/bloomofficialyt" style="color: rgba(255, 255, 255, 32);">t.me/bloomofficialyt</a>')
        self.setGeometry(85, 120, 180, 60)
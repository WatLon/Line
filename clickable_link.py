from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt
import tempfile
import os

class ClickableLink(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        temp_dir = tempfile.gettempdir()
        zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
        font_path = os.path.join(zapret_path, 'NType82-Regular.otf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16)  # Smaller font size
        self.setFont(font)
        self.setStyleSheet("color: rgba(255, 255, 255, 32);")  # White with 50% opacity
        self.setOpenExternalLinks(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText('<a href="https://t.me/bloomofficialyt" style="color: rgba(255, 255, 255, 32);">t.me/bloomofficialyt</a>')
        self.setGeometry(85, 120, 180, 60)  # Adjust the geometry as needed
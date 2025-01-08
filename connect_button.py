from PySide6.QtWidgets import QPushButton, QApplication
from PySide6.QtGui import QFont, QFontDatabase
import sys
import func
import tempfile
import os

class ConnectButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("connect", parent)
        temp_dir = tempfile.gettempdir()
        zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
        font_path = os.path.join(zapret_path, 'Dot-Matrix.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 32)
        self.setFont(font)

        # Устанавливаем стили без указания размера
        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(75, 75, 75);
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        self.setGeometry(35, 180, 280, 60)  # (x, y, width, height)

        self.clicked.connect(self.on_click)
        self.connected = False

    def on_click(self):
        if not self.connected:
            self.setText("connected")
            self.connected = True
            func.toggle_connection(self.connected)
        else:
            self.setText("connect")
            self.connected = False
            func.toggle_connection(self.connected)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = ConnectButton()
    button.show()
    sys.exit(app.exec())

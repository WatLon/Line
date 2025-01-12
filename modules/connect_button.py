from PySide6.QtWidgets import QPushButton, QApplication
from PySide6.QtGui import QFont, QFontDatabase
import core.func

class ConnectButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("connect", parent)
        font_path = 'fonts/Dot-Matrix.ttf'
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 32)
        self.setFont(font)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(75, 75, 75);
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        self.setGeometry(35, 180, 280, 60)

        self.clicked.connect(self.on_click)
        self.connected = False

    def on_click(self):
        if not self.connected:
            self.setText("connected")
            self.connected = True
            core.func.toggle_connection(self.connected)
        else:
            self.setText("connect")
            self.connected = False
            core.func.toggle_connection(self.connected)
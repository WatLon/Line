from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class WindowControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.minimize_button = QPushButton("—", self)
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("background-color: transparent; border: none; color: white; font-size: 16px;")
        self.minimize_button.clicked.connect(self.parent().showMinimized)
        self.close_button = QPushButton("⨉", self)
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("background-color: transparent; border: none; color: white; font-size: 16px;")
        self.close_button.clicked.connect(self.parent().close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

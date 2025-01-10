from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QFontDatabase, QFont
import func
import tempfile
import os

class ConfigFileSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.label = QLabel("Choose config file", self)

        # Load custom font
        temp_dir = tempfile.gettempdir()
        zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
        font_path = os.path.join(zapret_path, 'Dot-Matrix.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 20)

        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgb(75, 75, 75);
                color: white;
                border: 2px dashed white;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setGeometry(10, 400, 335, 100)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(('.cfg', '.txt')):
                self.label.setText("Success")
                event.acceptProposedAction()
                self.display_file_path(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(self, "Choose config file", "", "Config Files (*.cfg *.txt)")
            if file_path:
                self.label.setText("Success")
                self.display_file_path(file_path)

    def display_file_path(self, file_path):
        func.select_config(file_path)
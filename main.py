import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor
from line_label import LineLabel
from connect_button import ConnectButton
from autostart_checkbox import AutostartWidget
from autoupdate_checkbox import AutoupdateWidget
from window_controls import WindowControls
from config_file_selector import ConfigFileSelector
from clickable_link import ClickableLink 
import elevate
import func
import update
import tempfile
import os
import configparser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(355, 510)
        self.setStyleSheet("""
            MainWindow {
                background-color: rgb(40, 40, 40);
                border-radius: 17px;
            }
        """)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: rgb(40, 40, 40); border-radius: 17px;")
        self.setCentralWidget(self.central_widget)
        self.dragPosition = QPoint()

        self.line_label = LineLabel(self.central_widget)
        self.connect_button = ConnectButton(self.central_widget)
        self.autostart_checkbox = AutostartWidget(self.central_widget)
        self.autoupdate_checkbox =AutoupdateWidget(self.central_widget)
        self.config_file_selector = ConfigFileSelector(self.central_widget)
        self.clickable_link = ClickableLink(self.central_widget)
        self.window_controls = WindowControls(self)
        self.window_controls.setGeometry(self.width() - 65, 2, 60, 30)

        # Set cursor directly in Python code
        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.autostart_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.autoupdate_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.config_file_selector.setCursor(QCursor(Qt.PointingHandCursor))
        self.window_controls.setCursor(QCursor(Qt.PointingHandCursor))
        self.clickable_link.setCursor(QCursor(Qt.PointingHandCursor))
        

        # Initialize the background process variable
        self.background_process = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

    def closeEvent(self, event):
        func.toggle_connection(False)
        event.accept()

if __name__ == "__main__":
    elevate.elevate(show_console=False)
    func.stop_windivert_service()
    update.check_and_update(update=False) # delete to avoid uploading files
    config_file_path = os.path.join(tempfile.gettempdir(), 'zapret', 'scr', 'config.cfg')
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if int(config['Autoupdate']['enabled']) == 1:
        update.check_and_update(update=True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

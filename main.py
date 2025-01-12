import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor, QIcon, QAction
from modules.line_label import LineLabel
from modules.connect_button import ConnectButton
from modules.autostart_checkbox import AutostartWidget
from modules.autoupdate_checkbox import AutoupdateWidget
from modules.window_controls import WindowControls
from modules.config_file_selector import ConfigFileSelector
from modules.clickable_link import ClickableLink
import ctypes
import core.func
import core.update
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
        self.autoupdate_checkbox = AutoupdateWidget(self.central_widget)
        self.config_file_selector = ConfigFileSelector(self.central_widget)
        self.clickable_link = ClickableLink(self.central_widget)
        self.window_controls = WindowControls(self)
        self.window_controls.setGeometry(self.width() - 65, 2, 60, 30)

        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.autostart_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.autoupdate_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.config_file_selector.setCursor(QCursor(Qt.PointingHandCursor))
        self.window_controls.setCursor(QCursor(Qt.PointingHandCursor))
        self.clickable_link.setCursor(QCursor(Qt.PointingHandCursor))

        self.background_process = None

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))
        self.tray_icon.setToolTip('Line')
        self.tray_icon.setVisible(True)
        self.tray_menu = QMenu()
        self.show_action = QAction("Развернуть", self)
        self.quit_action = QAction("Закрыть", self)
        self.show_action.triggered.connect(self.show)
        self.quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

        self.closing_from_tray = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

    def closeEvent(self, event):
        if not self.closing_from_tray and self.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                "Line",
                "The application continues to run in the background.",
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
        else:
            event.accept()

    def quit_application(self):
        self.closing_from_tray = True
        core.func.toggle_connection(False)
        QApplication.instance().quit()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def check_system_bitness():
    return sys.maxsize > 2**32

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()

    app = QApplication(sys.argv)
    window = MainWindow()

    if not check_system_bitness():
        window.tray_icon.showMessage(
            "Warning",
            "Your system is 32-bit. The application may not work correctly.",
            QSystemTrayIcon.Warning,
            5000
        )

    core.func.stop_windivert_service()
    config_file_path = 'scr/config.cfg'
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if int(config['Autoupdate']['enabled']) == 1:
        core.update.check_and_update()

    window.show()
    sys.exit(app.exec())

import configparser
import os
import tempfile
import func
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QWidget, QLabel, QApplication
from PySide6.QtGui import QFont, QFontDatabase, Qt
from PySide6.QtCore import Qt

class AutostartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        temp_dir = tempfile.gettempdir()
        zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
        font_path = os.path.join(zapret_path, 'Dot-Matrix.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 24)

        self.label = QLabel("Auto start", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")

        self.checkbox = QCheckBox(self)
        temp_dir = tempfile.gettempdir()
        zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
        image_1_path = os.path.join(zapret_path, "1.png").replace("\\", "/")
        image_2_path = os.path.join(zapret_path, "2.png").replace("\\", "/")

        self.checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: white;
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
            }}
            QCheckBox::indicator:unchecked {{
                image: url({image_1_path});
            }}
            QCheckBox::indicator:checked {{
                image: url({image_2_path});
            }}
        """)

        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setGeometry(45, 250, 260, 100)

        self.label.mousePressEvent = self.on_label_clicked

        self.checkbox.stateChanged.connect(self.update_checkbox_state)

        self.config_path = os.path.join(tempfile.gettempdir(), 'zapret', 'scr', 'config.cfg')
        self.load_config()

    def on_label_clicked(self, event):
        if event.button() == Qt.LeftButton:
            self.checkbox.setChecked(not self.checkbox.isChecked())
            event.accept()

    def update_checkbox_state(self, state):
        is_checked = self.checkbox.isChecked()
        func.set_autostart(is_checked)
        self.save_config(is_checked)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if 'Autostart' in config and 'enabled' in config['Autostart']:
            enabled = config['Autostart'].getboolean('enabled')
            self.checkbox.setChecked(enabled)

    def save_config(self, enabled):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if 'Autostart' not in config:
            config.add_section('Autostart')
        config['Autostart']['enabled'] = '1' if enabled else '0'
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
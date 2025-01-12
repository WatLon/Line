import configparser
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QWidget, QLabel, QApplication
from PySide6.QtGui import QFont, QFontDatabase, Qt
from PySide6.QtCore import Qt

class AutoupdateWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        font_path = 'fonts/Dot-Matrix.ttf'
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 24)

        self.label = QLabel("Auto update", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")

        self.checkbox = QCheckBox(self)
        image_1_path = "images/1.png"
        image_2_path = "images/2.png"

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
        self.setGeometry(38, 310, 280, 100)

        self.label.mousePressEvent = self.on_label_clicked

        self.checkbox.stateChanged.connect(self.update_checkbox_state)

        self.config_path = 'scr/config.cfg'
        self.load_config()

    def on_label_clicked(self, event):
        if event.button() == Qt.LeftButton:
            self.checkbox.setChecked(not self.checkbox.isChecked())
            event.accept()

    def update_checkbox_state(self, state):
        is_checked = self.checkbox.isChecked()
        self.save_config(is_checked)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if 'Autoupdate' in config and 'enabled' in config['Autoupdate']:
            enabled = config['Autoupdate'].getboolean('enabled')
            self.checkbox.setChecked(enabled)

    def save_config(self, enabled):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if 'Autoupdate' not in config:
            config.add_section('Autoupdate')
        config['Autoupdate']['enabled'] = '1' if enabled else '0'
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
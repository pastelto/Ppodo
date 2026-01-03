"""
Settings dialog for Ppodo application.
Allows configuration of focus and break durations.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QGroupBox, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt, Signal


class SettingsDialog(QDialog):
    """Dialog for application settings."""

    # Signal emitted when language changes
    language_changed = Signal(str)

    def __init__(self, current_focus: int = 25, current_break: int = 5,
                 current_language: str = 'ko', lang_manager=None, theme_manager=None, parent=None):
        """
        Initialize settings dialog.

        Args:
            current_focus: Current focus duration in minutes
            current_break: Current break duration in minutes
            current_language: Current language code
            lang_manager: Language manager instance
            theme_manager: Theme manager instance for button colors
            parent: Parent widget
        """
        super().__init__(parent)
        self.lang_manager = lang_manager
        self.theme_manager = theme_manager
        self.setWindowTitle("⚙️ 설정" if not lang_manager else lang_manager.t('settings_title'))
        self.setModal(True)
        self.setMinimumWidth(400)

        self.focus_minutes = current_focus
        self.break_minutes = current_break
        self.current_language = current_language

        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Timer settings group
        timer_title = self.lang_manager.t('settings_timer') if self.lang_manager else "⏱️ 타이머 설정"
        timer_group = QGroupBox(timer_title)
        timer_layout = QFormLayout()
        timer_layout.setSpacing(15)

        # Focus duration
        self.focus_spinbox = QSpinBox()
        self.focus_spinbox.setMinimum(1)
        self.focus_spinbox.setMaximum(120)
        self.focus_spinbox.setValue(self.focus_minutes)
        suffix = self.lang_manager.t('settings_minutes') if self.lang_manager else " 분"
        self.focus_spinbox.setSuffix(suffix)

        # Get theme color for focus
        focus_color = self.theme_manager.get_focus_color() if self.theme_manager else "#E63946"

        self.focus_spinbox.setStyleSheet(f"""
            QSpinBox {{
                padding: 8px 35px 8px 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }}
            QSpinBox:focus {{
                border: 2px solid {focus_color};
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 26px;
                height: 20px;
                border-left: 2px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                border-top-right-radius: 3px;
                background: #FAFAFA;
            }}
            QSpinBox::up-button:hover {{
                background: #E8F4F8;
            }}
            QSpinBox::up-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-bottom: 10px solid #000000;
                margin-bottom: 2px;
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 26px;
                height: 20px;
                border-left: 2px solid #E0E0E0;
                border-top: 1px solid #E0E0E0;
                border-bottom-right-radius: 3px;
                background: #FAFAFA;
            }}
            QSpinBox::down-button:hover {{
                background: #E8F4F8;
            }}
            QSpinBox::down-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid #000000;
                margin-top: 2px;
            }}
        """)

        focus_text = self.lang_manager.t('settings_focus_time') if self.lang_manager else "집중 시간:"
        focus_label = QLabel(focus_text)
        focus_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        timer_layout.addRow(focus_label, self.focus_spinbox)

        # Break duration
        self.break_spinbox = QSpinBox()
        self.break_spinbox.setMinimum(1)
        self.break_spinbox.setMaximum(60)
        self.break_spinbox.setValue(self.break_minutes)
        self.break_spinbox.setSuffix(suffix)

        # Get theme color for break
        break_color = self.theme_manager.get_break_color() if self.theme_manager else "#E63946"

        self.break_spinbox.setStyleSheet(f"""
            QSpinBox {{
                padding: 8px 35px 8px 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }}
            QSpinBox:focus {{
                border: 2px solid {break_color};
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 26px;
                height: 20px;
                border-left: 2px solid #E0E0E0;
                border-bottom: 1px solid #E0E0E0;
                border-top-right-radius: 3px;
                background: #FAFAFA;
            }}
            QSpinBox::up-button:hover {{
                background: #E8F4F8;
            }}
            QSpinBox::up-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-bottom: 10px solid #000000;
                margin-bottom: 2px;
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 26px;
                height: 20px;
                border-left: 2px solid #E0E0E0;
                border-top: 1px solid #E0E0E0;
                border-bottom-right-radius: 3px;
                background: #FAFAFA;
            }}
            QSpinBox::down-button:hover {{
                background: #E8F4F8;
            }}
            QSpinBox::down-arrow {{
                image: none;
                width: 0;
                height: 0;
                border-left: 7px solid transparent;
                border-right: 7px solid transparent;
                border-top: 10px solid #000000;
                margin-top: 2px;
            }}
        """)

        break_text = self.lang_manager.t('settings_break_time') if self.lang_manager else "휴식 시간:"
        break_label = QLabel(break_text)
        break_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        timer_layout.addRow(break_label, self.break_spinbox)

        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)

        # Language settings group
        lang_group = QGroupBox("🌐 언어 설정" if not self.lang_manager else self.lang_manager.t('settings_language'))
        lang_layout = QFormLayout()
        lang_layout.setSpacing(15)

        self.language_combo = QComboBox()
        if self.lang_manager:
            for code, name in self.lang_manager.SUPPORTED_LANGUAGES.items():
                self.language_combo.addItem(name, code)
            # Set current language
            index = self.language_combo.findData(self.current_language)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)
        else:
            self.language_combo.addItem("한국어", "ko")
            self.language_combo.addItem("English", "en")
            self.language_combo.addItem("日本語", "ja")

        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 30px 8px 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }
            QComboBox:focus {
                border: 2px solid #E63946;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #000000;
            }
        """)

        lang_label = QLabel("언어:" if not self.lang_manager else self.lang_manager.t('settings_language_label'))
        lang_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        lang_layout.addRow(lang_label, self.language_combo)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Info label
        info_text = self.lang_manager.t('settings_info') if self.lang_manager else "💡 타이머가 실행 중이 아닐 때만 설정을 변경할 수 있습니다."
        info = QLabel(info_text)
        info.setStyleSheet("font-size: 12px; color: #666; padding: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()

        save_text = self.lang_manager.t('btn_save') if self.lang_manager else "💾 저장"
        self.save_button = QPushButton(save_text)
        self.save_button.clicked.connect(self.accept)

        # Use theme colors if available
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            focus_hover = self._darken_color(focus_color, 0.15)
        else:
            focus_color = "#27AE60"
            focus_hover = "#229954"

        self.save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {focus_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {focus_hover};
            }}
        """)

        cancel_text = self.lang_manager.t('btn_cancel') if self.lang_manager else "❌ 취소"
        self.cancel_button = QPushButton(cancel_text)
        self.cancel_button.clicked.connect(self.reject)

        # Use theme colors if available
        if self.theme_manager:
            break_color = self.theme_manager.get_break_color()
            break_hover = self._darken_color(break_color, 0.15)
        else:
            break_color = "#E74C3C"
            break_hover = "#C0392B"

        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {break_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {break_hover};
            }}
        """)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _darken_color(self, hex_color: str, factor: float = 0.2) -> str:
        """Darken a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def get_settings(self):
        """
        Get current settings.

        Returns:
            Tuple of (focus_minutes, break_minutes, language_code)
        """
        language_code = self.language_combo.currentData() if self.language_combo.currentData() else 'ko'
        return (self.focus_spinbox.value(), self.break_spinbox.value(), language_code)

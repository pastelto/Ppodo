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
                 current_language: str = 'ko', lang_manager=None, parent=None):
        """
        Initialize settings dialog.

        Args:
            current_focus: Current focus duration in minutes
            current_break: Current break duration in minutes
            current_language: Current language code
            lang_manager: Language manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.lang_manager = lang_manager
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
        timer_group = QGroupBox("⏱️ 타이머 설정")
        timer_layout = QFormLayout()
        timer_layout.setSpacing(15)

        # Focus duration
        self.focus_spinbox = QSpinBox()
        self.focus_spinbox.setMinimum(1)
        self.focus_spinbox.setMaximum(120)
        self.focus_spinbox.setValue(self.focus_minutes)
        self.focus_spinbox.setSuffix(" 분")
        self.focus_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }
            QSpinBox:focus {
                border: 2px solid #E63946;
            }
        """)

        focus_label = QLabel("집중 시간:")
        focus_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        timer_layout.addRow(focus_label, self.focus_spinbox)

        # Break duration
        self.break_spinbox = QSpinBox()
        self.break_spinbox.setMinimum(1)
        self.break_spinbox.setMaximum(60)
        self.break_spinbox.setValue(self.break_minutes)
        self.break_spinbox.setSuffix(" 분")
        self.break_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }
            QSpinBox:focus {
                border: 2px solid #E63946;
            }
        """)

        break_label = QLabel("휴식 시간:")
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
                padding: 8px;
                font-size: 14px;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
            }
            QComboBox:focus {
                border: 2px solid #E63946;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        lang_label = QLabel("언어:" if not self.lang_manager else self.lang_manager.t('settings_language_label'))
        lang_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        lang_layout.addRow(lang_label, self.language_combo)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Info label
        info = QLabel("💡 타이머가 실행 중이 아닐 때만 설정을 변경할 수 있습니다.")
        info.setStyleSheet("font-size: 12px; color: #666; padding: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("💾 저장")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)

        self.cancel_button = QPushButton("❌ 취소")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_settings(self):
        """
        Get current settings.

        Returns:
            Tuple of (focus_minutes, break_minutes, language_code)
        """
        language_code = self.language_combo.currentData() if self.language_combo.currentData() else 'ko'
        return (self.focus_spinbox.value(), self.break_spinbox.value(), language_code)

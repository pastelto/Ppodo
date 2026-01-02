"""
Mini window for Ppodo application.
Compact timer-only view for minimal distraction.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from core.timer import PomodoroTimer


class MiniWindow(QWidget):
    """Mini clock-only window."""

    # Signal to request return to main window
    restore_requested = Signal()

    def __init__(self, timer: PomodoroTimer, theme_manager=None):
        """
        Initialize mini window.

        Args:
            timer: PomodoroTimer instance
            theme_manager: ThemeManager instance
        """
        super().__init__()
        self.timer = timer
        self.theme_manager = theme_manager

        # Window flags for always on top and frameless
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        self._init_ui()
        self._connect_signals()
        self.update_display()

        # For dragging window
        self.dragging = False
        self.offset = None

    def _init_ui(self):
        """Initialize UI components."""
        self.setFixedSize(280, 180)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header with restore button
        header_layout = QHBoxLayout()

        app_name = "🍇 Ppodo"
        if self.theme_manager and hasattr(self.theme_manager, 'lang_manager'):
            app_name = f"🍇 {self.theme_manager.lang_manager.t('app_name')}"
        title = QLabel(app_name)
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E63946;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.restore_button = QPushButton("⬜")
        self.restore_button.setToolTip("전체 화면으로 돌아가기")
        self.restore_button.clicked.connect(self.restore_requested.emit)
        self.restore_button.setFixedSize(30, 30)
        self.restore_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        header_layout.addWidget(self.restore_button)

        self.close_button = QPushButton("✕")
        self.close_button.setToolTip("닫기")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        header_layout.addWidget(self.close_button)

        layout.addLayout(header_layout)

        # State indicator
        self.state_label = QLabel("⏸ 대기 중")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setStyleSheet("""
            font-size: 13px;
            font-weight: bold;
            color: #666;
            padding: 5px;
        """)
        layout.addWidget(self.state_label)

        # Timer display
        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setMinimumHeight(60)  # Ensure visibility
        font = QFont('Consolas', 42)
        font.setBold(True)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: #2B2D42; padding: 10px;")
        layout.addWidget(self.time_label)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_pause_button = QPushButton("▶")
        self.start_pause_button.setFixedSize(50, 40)
        self.start_pause_button.clicked.connect(self._on_start_pause)
        self.start_pause_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)

        self.stop_button = QPushButton("⏹")
        self.stop_button.setFixedSize(50, 40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #999999;
            }
        """)

        button_layout.addStretch()
        button_layout.addWidget(self.start_pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Apply theme
        self._apply_theme()

    def _apply_theme(self):
        """Apply current theme colors."""
        if self.theme_manager:
            is_focus = self.timer.is_focus()
            theme_color = self.theme_manager.get_current_color(is_focus)

            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #FFFFFF;
                    border: 3px solid {theme_color};
                    border-radius: 10px;
                }}
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    border: 3px solid #E63946;
                    border-radius: 10px;
                }
            """)

    def _connect_signals(self):
        """Connect timer signals."""
        self.timer.tick.connect(self.update_display)
        self.timer.state_changed.connect(self.update_state)

    def _on_start_pause(self):
        """Handle start/pause button click."""
        if self.timer.is_idle():
            self.timer.start_focus()
            self.start_pause_button.setText("⏸")
            self.stop_button.setEnabled(True)
        elif self.timer.is_paused():
            self.timer.resume()
            self.start_pause_button.setText("⏸")
            self.stop_button.setEnabled(True)
        elif self.timer.is_running():
            self.timer.pause()
            self.start_pause_button.setText("▶")

    def _on_stop(self):
        """Handle stop button click."""
        self.timer.stop()
        self.start_pause_button.setText("▶")
        self.stop_button.setEnabled(False)

    def update_display(self):
        """Update timer display."""
        minutes, seconds = self.timer.get_remaining_time()
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def update_state(self, state: str):
        """Update state indicator."""
        state_icons = {
            "idle": "⏸ 대기 중",
            "focus": "🔥 집중 중",
            "break": "☕ 휴식 중",
            "paused": "⏸ 일시정지"
        }

        # Get theme colors
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            break_color = self.theme_manager.get_break_color()
        else:
            focus_color = "#E63946"
            break_color = "#A8DADC"

        state_colors = {
            "idle": "#666",
            "focus": focus_color,
            "break": break_color,
            "paused": "#FFB703"
        }

        self.state_label.setText(state_icons.get(state, "⏸ 대기 중"))
        color = state_colors.get(state, "#666")
        self.state_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: bold;
            color: {color};
            padding: 5px;
        """)

        # Update button state
        if state == "idle":
            self.start_pause_button.setText("▶")
            self.stop_button.setEnabled(False)
        elif state in ("focus", "break"):
            self.start_pause_button.setText("⏸")
            self.stop_button.setEnabled(True)
        elif state == "paused":
            self.start_pause_button.setText("▶")
            self.stop_button.setEnabled(True)

        # Update theme border
        self._apply_theme()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if self.dragging and self.offset is not None:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def apply_theme(self):
        """Apply theme (called when theme changes)."""
        self._apply_theme()
        self.update_state(self.timer.state.value if hasattr(self.timer, 'state') else "idle")

"""
Timer display widget for Ppodo application.
Shows countdown timer with progress bar and state indicator.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.timer import PomodoroTimer


class TimerWidget(QWidget):
    """Widget for displaying Pomodoro timer."""

    def __init__(self, timer: PomodoroTimer, theme_manager=None):
        """
        Initialize timer widget.

        Args:
            timer: PomodoroTimer instance
            theme_manager: ThemeManager instance for dynamic theming
        """
        super().__init__()
        self.timer = timer
        self.theme_manager = theme_manager
        self._init_ui()
        self._connect_signals()
        self.update_display()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # State indicator
        self.state_label = QLabel("⏸ 대기 중")
        self.state_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.state_label)

        # Timer display (MM:SS)
        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setWordWrap(True)
        self.time_label.setMinimumHeight(80)  # Ensure minimum height for visibility
        layout.addWidget(self.time_label, 1)  # Give it stretch

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% 진행")
        layout.addWidget(self.progress_bar)

        # Current task label
        self.task_label = QLabel("")
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setWordWrap(True)
        layout.addWidget(self.task_label)

        layout.addStretch()
        self.setLayout(layout)

        # Update styles
        self._update_styles()

    def _update_styles(self):
        """Update widget styles based on current state and theme."""
        # Get theme colors
        if self.theme_manager:
            is_focus = self.timer.is_focus()
            theme_color = self.theme_manager.get_current_color(is_focus)
        else:
            theme_color = "#E63946"

        # State label style
        state_colors = {
            "idle": "#666",
            "focus": theme_color if self.theme_manager else "#E63946",
            "break": self.theme_manager.get_break_color() if self.theme_manager else "#A8DADC",
            "paused": "#FFB703"
        }

        current_state = self.timer.state.value if hasattr(self.timer, 'state') else "idle"
        color = state_colors.get(current_state, "#666")

        self.state_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {color};
            padding: 10px;
        """)

        # Timer label - responsive font size
        font = QFont('Consolas', 48)
        font.setBold(True)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("""
            color: #2B2D42;
            padding: 20px;
        """)

        # Task label
        self.task_label.setStyleSheet("""
            font-size: 14px;
            color: #666;
            padding: 5px;
        """)

        # Update progress bar color
        self._update_progress_bar_style()

    def _update_progress_bar_style(self):
        """Update progress bar style based on current state."""
        if self.theme_manager:
            is_focus = self.timer.is_focus()
            theme_color = self.theme_manager.get_current_color(is_focus)
        else:
            theme_color = "#E63946"

        state = self.timer.state.value if hasattr(self.timer, 'state') else "idle"

        if state == "focus":
            border_color = theme_color
            chunk_color = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {theme_color}, stop:1 {self._lighten_color(theme_color)})"
        elif state == "break":
            break_color = self.theme_manager.get_break_color() if self.theme_manager else "#A8DADC"
            border_color = break_color
            chunk_color = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {break_color}, stop:1 {self._lighten_color(break_color)})"
        else:
            border_color = "#999999"
            chunk_color = "#CCCCCC"

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 3px solid {border_color};
                border-radius: 10px;
                text-align: center;
                height: 30px;
                font-size: 13px;
                font-weight: bold;
                background-color: #F5F5F5;
            }}
            QProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 7px;
            }}
        """)

    def _lighten_color(self, hex_color: str, factor: float = 0.3) -> str:
        """Lighten a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def resizeEvent(self, event):
        """Handle resize event to adjust font size."""
        super().resizeEvent(event)
        # Adjust timer font size based on widget width
        width = self.width()
        height = self.height()

        # Use the smaller dimension to ensure text fits
        min_dimension = min(width, height)

        if min_dimension < 250:
            font_size = 28
        elif min_dimension < 350:
            font_size = 36
        elif min_dimension < 450:
            font_size = 48
        elif min_dimension < 550:
            font_size = 56
        else:
            font_size = 64

        font = QFont('Consolas', font_size)
        font.setBold(True)
        self.time_label.setFont(font)

    def _connect_signals(self):
        """Connect timer signals to update methods."""
        self.timer.tick.connect(self.update_display)
        self.timer.state_changed.connect(self.update_state)

    def update_display(self):
        """Update timer display."""
        minutes, seconds = self.timer.get_remaining_time()
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

        # Update progress bar
        progress = self.timer.get_progress_percent()
        self.progress_bar.setValue(int(progress))

    def update_state(self, state: str):
        """
        Update state indicator.

        Args:
            state: Timer state
        """
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

        # Update color based on state
        color = state_colors.get(state, "#666")
        self.state_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {color};
            padding: 10px;
        """)

        # Update progress bar style with theme colors
        self._update_progress_bar_style()

    def apply_theme(self):
        """Apply current theme to the widget."""
        self._update_styles()

    def set_current_task(self, task_title: str):
        """
        Set current task being worked on.

        Args:
            task_title: Task title to display
        """
        if task_title:
            self.task_label.setText(f"📝 {task_title}")
        else:
            self.task_label.setText("")

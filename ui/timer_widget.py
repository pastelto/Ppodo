"""
Timer display widget for Ppodo application.
Shows countdown timer with progress bar and state indicator.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from core.timer import PomodoroTimer


class TimerWidget(QWidget):
    """Widget for displaying Pomodoro timer."""

    def __init__(self, timer: PomodoroTimer):
        """
        Initialize timer widget.

        Args:
            timer: PomodoroTimer instance
        """
        super().__init__()
        self.timer = timer
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
        self.state_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #666;
            padding: 10px;
        """)
        self.state_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.state_label)

        # Timer display (MM:SS)
        self.time_label = QLabel("25:00")
        self.time_label.setStyleSheet("""
            font-size: 72px;
            font-weight: bold;
            font-family: 'Consolas', 'Courier New', monospace;
            color: #2B2D42;
            padding: 20px;
        """)
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% 진행")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 3px solid #E63946;
                border-radius: 10px;
                text-align: center;
                height: 30px;
                font-size: 13px;
                font-weight: bold;
                background-color: #F5F5F5;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                   stop:0 #E63946, stop:1 #FF6B6B);
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Current task label
        self.task_label = QLabel("")
        self.task_label.setStyleSheet("""
            font-size: 14px;
            color: #666;
            padding: 5px;
        """)
        self.task_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.task_label)

        layout.addStretch()
        self.setLayout(layout)

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

        state_colors = {
            "idle": "#666",
            "focus": "#E63946",
            "break": "#A8DADC",
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

        # Update progress bar color
        if state == "focus":
            chunk_color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E63946, stop:1 #FF6B6B)"
            border_color = "#E63946"
        elif state == "break":
            chunk_color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #A8DADC, stop:1 #B8E9EB)"
            border_color = "#A8DADC"
        else:
            chunk_color = "#CCCCCC"
            border_color = "#999999"

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

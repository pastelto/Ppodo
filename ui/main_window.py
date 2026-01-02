"""
Main window for Ppodo application.
Integrates all widgets and manages application flow.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QMessageBox, QComboBox, QLabel, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from core.database import Database
from core.timer import PomodoroTimer
from core.theme import ThemeManager
from ui.timer_widget import TimerWidget
from ui.grape_widget import GrapeWidget
from ui.level_widget import LevelWidget
from ui.task_widget import TaskWidget
from ui.stats_widget import StatsWidget
from ui.badge_widget import BadgeWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        # Initialize core components
        self.db = Database()
        self.timer = PomodoroTimer()
        self.theme_manager = ThemeManager()

        # Current session info
        self.current_session_id = None
        self.current_task_id = None
        self.current_task_title = None

        self._init_ui()
        self._connect_signals()
        self._apply_theme()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("🍇 Ppodo (뽀도) - 포도알 뽀모도로 타이머")
        self.setMinimumSize(1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header with theme selector
        header_layout = QHBoxLayout()

        title = QLabel("🍇 Ppodo (뽀도)")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E63946;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        theme_label = QLabel("🎨 테마:")
        theme_label.setStyleSheet("font-size: 13px;")
        header_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        self.theme_combo.setMaximumWidth(150)
        header_layout.addWidget(self.theme_combo)

        main_layout.addLayout(header_layout)

        # Level widget (always visible)
        self.level_widget = LevelWidget(self.db)
        main_layout.addWidget(self.level_widget)

        # Main content splitter (timer + grape on left, tabs on right)
        content_splitter = QSplitter(Qt.Horizontal)

        # Left panel: Timer + Grape
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        self.timer_widget = TimerWidget(self.timer)
        left_layout.addWidget(self.timer_widget)

        self.grape_widget = GrapeWidget(self.db)
        left_layout.addWidget(self.grape_widget)

        left_panel.setLayout(left_layout)
        content_splitter.addWidget(left_panel)

        # Right panel: Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        # Task tab
        self.task_widget = TaskWidget(self.db)
        self.tabs.addTab(self.task_widget, "📝 할 일")

        # Stats tab
        self.stats_widget = StatsWidget(self.db)
        self.tabs.addTab(self.stats_widget, "📊 통계")

        # Badge tab
        self.badge_widget = BadgeWidget(self.db)
        self.tabs.addTab(self.badge_widget, "🏆 뱃지")

        content_splitter.addWidget(self.tabs)
        content_splitter.setSizes([400, 600])

        main_layout.addWidget(content_splitter)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶ 시작")
        self.start_button.clicked.connect(self._on_start)
        self.start_button.setMinimumHeight(45)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                font-weight: bold;
                background-color: #27AE60;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)

        self.pause_button = QPushButton("⏸ 일시정지")
        self.pause_button.clicked.connect(self._on_pause)
        self.pause_button.setEnabled(False)
        self.pause_button.setMinimumHeight(45)

        self.stop_button = QPushButton("⏹ 중지")
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumHeight(45)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

    def _connect_signals(self):
        """Connect signals and slots."""
        # Timer signals
        self.timer.focus_completed.connect(self._on_focus_completed)
        self.timer.break_completed.connect(self._on_break_completed)

        # Task selection signal
        self.task_widget.task_selected.connect(self._on_task_selected)

    def _apply_theme(self):
        """Apply current theme to the application."""
        is_focus = self.timer.is_focus()
        stylesheet = self.theme_manager.apply_stylesheet("main", is_focus)
        self.setStyleSheet(stylesheet)

    def _on_theme_changed(self, theme_name: str):
        """Handle theme change."""
        self.theme_manager.set_theme(theme_name)
        self._apply_theme()

    def _on_start(self):
        """Handle start button click."""
        if self.timer.is_paused():
            # Resume from pause
            self.timer.resume()
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        else:
            # Start new focus session
            self.timer.start_focus()

            # Create session in database
            self.current_session_id = self.db.start_session(
                task_id=self.current_task_id,
                duration=25
            )

            # Update UI
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)

            # Update timer widget with current task
            if self.current_task_title:
                self.timer_widget.set_current_task(self.current_task_title)

    def _on_pause(self):
        """Handle pause button click."""
        self.timer.pause()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def _on_stop(self):
        """Handle stop button click."""
        # Confirm stop
        if self.timer.is_running():
            reply = QMessageBox.question(
                self,
                "중지 확인",
                "진행 중인 세션을 중지하시겠습니까?\n(진행 중인 포도알은 획득하지 못합니다)",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.No:
                return

        self.timer.stop()
        self.current_session_id = None
        self.current_task_id = None
        self.current_task_title = None

        # Update UI
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.timer_widget.set_current_task("")

    def _on_focus_completed(self):
        """Handle focus session completion."""
        # Complete session in database
        if self.current_session_id:
            self.db.complete_session(self.current_session_id)

        # Check for new badges
        new_badges = self.db.check_and_award_badges()

        # Show completion message
        profile = self.db.get_profile()
        message = f"""🎉 집중 완료!

🔥 25분 집중 완료!
🍇 포도알 +1 획득!
💫 경험치 +10 XP"""

        # Check for level up
        old_level = profile['level']
        new_profile = self.db.get_profile()
        if new_profile['level'] > old_level:
            message += f"\n\n🎉 레벨업! Level {new_profile['level']} 달성!"

        # Check for new badges
        if new_badges:
            message += f"\n\n🏆 새 뱃지 획득!"
            for badge in new_badges:
                message += f"\n  {badge['icon']} {badge['name']}"

        message += "\n\n이제 5분 휴식하세요."

        QMessageBox.information(self, "집중 완료", message)

        # Refresh all widgets
        self.grape_widget.refresh()
        self.level_widget.refresh()
        self.badge_widget.refresh()
        self.stats_widget.refresh()

        # Update button states (break starts automatically)
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

        # Clear current task
        self.timer_widget.set_current_task("")

    def _on_break_completed(self):
        """Handle break completion."""
        QMessageBox.information(
            self,
            "휴식 완료",
            "☕ 휴식 완료!\n\n다시 집중할 준비가 되었습니다."
        )

        # Reset button states
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        # Clear session
        self.current_session_id = None

    def _on_task_selected(self, task_id: int, task_title: str):
        """Handle task selection."""
        self.current_task_id = task_id
        self.current_task_title = task_title

        # If timer is running, update the display
        if self.timer.is_running():
            self.timer_widget.set_current_task(task_title)

    def closeEvent(self, event):
        """Handle window close event."""
        # Close database connection
        self.db.close()
        event.accept()

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
from ui.settings_dialog import SettingsDialog
from ui.mini_window import MiniWindow


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
        self.collect_grapes_on_complete = True  # Default: collect grapes

        # Mini window
        self.mini_window = None

        # Tabs visible state
        self.tabs_visible = True

        self._init_ui()
        self._connect_signals()
        self._apply_theme()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("🍇 Ppodo (뽀도) - 포도알 뽀모도로 타이머")
        self.setMinimumSize(900, 650)
        self.resize(1100, 750)  # Default size

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header with controls
        header_layout = QHBoxLayout()

        title = QLabel("🍇 Ppodo (뽀도)")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E63946;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Mini mode button
        self.mini_button = QPushButton("🔍 미니 모드")
        self.mini_button.setToolTip("작은 시계 화면으로 전환")
        self.mini_button.clicked.connect(self._show_mini_mode)
        self.mini_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        header_layout.addWidget(self.mini_button)

        # Toggle tabs button
        self.toggle_tabs_button = QPushButton("👁️ 탭 숨기기")
        self.toggle_tabs_button.setToolTip("할일/통계/뱃지 패널 숨기기/보이기")
        self.toggle_tabs_button.clicked.connect(self._toggle_tabs)
        self.toggle_tabs_button.setStyleSheet("""
            QPushButton {
                background-color: #9B59B6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8E44AD;
            }
        """)
        header_layout.addWidget(self.toggle_tabs_button)

        # Settings button
        self.settings_button = QPushButton("⚙️ 설정")
        self.settings_button.setToolTip("타이머 시간 설정")
        self.settings_button.clicked.connect(self._show_settings)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        header_layout.addWidget(self.settings_button)

        # Theme selector
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
        self.content_splitter = QSplitter(Qt.Horizontal)

        # Left panel: Timer + Grape
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        self.timer_widget = TimerWidget(self.timer, self.theme_manager)
        left_layout.addWidget(self.timer_widget)

        self.grape_widget = GrapeWidget(self.db)
        left_layout.addWidget(self.grape_widget)

        left_panel.setLayout(left_layout)
        self.content_splitter.addWidget(left_panel)

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

        self.content_splitter.addWidget(self.tabs)
        self.content_splitter.setSizes([400, 600])

        main_layout.addWidget(self.content_splitter)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶ 시작")
        self.start_button.clicked.connect(self._on_start)
        self.start_button.setMinimumHeight(45)
        # Style will be set by _apply_theme()

        self.pause_button = QPushButton("⏸ 일시정지")
        self.pause_button.clicked.connect(self._on_pause)
        self.pause_button.setEnabled(False)
        self.pause_button.setMinimumHeight(45)
        # Style will be set by _apply_theme()

        self.stop_button = QPushButton("⏹ 중지")
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumHeight(45)
        # Style will be set by _apply_theme()

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

        # Apply to timer widget
        if hasattr(self, 'timer_widget'):
            self.timer_widget.apply_theme()

        # Apply to mini window if exists
        if self.mini_window and self.mini_window.isVisible():
            self.mini_window.apply_theme()

        # Apply theme colors to control buttons
        if hasattr(self, 'start_button'):
            self._update_button_styles()

    def _on_theme_changed(self, theme_name: str):
        """Handle theme change."""
        self.theme_manager.set_theme(theme_name)
        self._apply_theme()

    def _update_button_styles(self):
        """Update control button styles based on current theme."""
        # Get theme colors
        focus_color = self.theme_manager.get_focus_color()
        break_color = self.theme_manager.get_break_color()

        # Use focus color for start button
        start_color = focus_color
        start_hover = self._darken_color(focus_color, 0.15)

        # Use a contrasting color for pause (amber/orange)
        pause_color = "#F39C12"
        pause_hover = "#E67E22"

        # Use break color for stop button
        stop_color = break_color
        stop_hover = self._darken_color(break_color, 0.15)

        # Apply styles
        self.start_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 15px;
                font-weight: bold;
                background-color: {start_color};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {start_hover};
            }}
        """)

        self.pause_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 15px;
                font-weight: bold;
                background-color: {pause_color};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {pause_hover};
            }}
            QPushButton:disabled {{
                background-color: #BDC3C7;
            }}
        """)

        self.stop_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 15px;
                font-weight: bold;
                background-color: {stop_color};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {stop_hover};
            }}
            QPushButton:disabled {{
                background-color: #BDC3C7;
            }}
        """)

    def _darken_color(self, hex_color: str, factor: float = 0.2) -> str:
        """Darken a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _show_settings(self):
        """Show settings dialog."""
        # Don't allow changing settings while timer is running
        if self.timer.is_running():
            QMessageBox.warning(
                self,
                "설정 불가",
                "타이머가 실행 중일 때는 설정을 변경할 수 없습니다.\n먼저 타이머를 중지해주세요."
            )
            return

        # Get current durations
        focus_mins = self.timer.focus_duration // 60
        break_mins = self.timer.break_duration // 60

        # Show dialog
        dialog = SettingsDialog(focus_mins, break_mins, self)
        if dialog.exec():
            focus, break_time = dialog.get_settings()
            self.timer.set_durations(focus, break_time)

            # Update timer display
            self.timer_widget.update_display()

            QMessageBox.information(
                self,
                "설정 완료",
                f"타이머 설정이 변경되었습니다.\n\n집중 시간: {focus}분\n휴식 시간: {break_time}분"
            )

    def _toggle_tabs(self):
        """Toggle tabs panel visibility."""
        self.tabs_visible = not self.tabs_visible

        if self.tabs_visible:
            self.tabs.show()
            self.toggle_tabs_button.setText("👁️ 탭 숨기기")
        else:
            self.tabs.hide()
            self.toggle_tabs_button.setText("👁️ 탭 보이기")

    def _show_mini_mode(self):
        """Show mini clock mode window."""
        # Create mini window if not exists
        if self.mini_window is None:
            self.mini_window = MiniWindow(self.timer, self.theme_manager)
            self.mini_window.restore_requested.connect(self._restore_from_mini)

        # Show mini window
        self.mini_window.show()
        self.mini_window.raise_()
        self.mini_window.activateWindow()

        # Hide main window
        self.hide()

    def _restore_from_mini(self):
        """Restore from mini mode."""
        if self.mini_window:
            self.mini_window.hide()

        self.show()
        self.raise_()
        self.activateWindow()

    def _on_start(self):
        """Handle start button click."""
        if self.timer.is_paused():
            # Resume from pause
            self.timer.resume()
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        else:
            # Get current timer duration
            duration_minutes = self.timer.focus_duration // 60

            # Check if duration is less than 15 minutes
            collect_grapes = True
            if duration_minutes < 15:
                reply = QMessageBox.warning(
                    self,
                    "⚠️ 포도알 수집 불가",
                    f"현재 집중 시간이 {duration_minutes}분으로 설정되어 있습니다.\n\n"
                    "🍇 포도알은 15분 이상 집중했을 때만 모을 수 있습니다.\n\n"
                    "15분 미만으로 진행하면 포도알을 획득할 수 없습니다.\n"
                    "그래도 진행하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    return
                else:
                    collect_grapes = False

            # Start new focus session
            self.timer.start_focus()

            # Create session in database
            self.current_session_id = self.db.start_session(
                task_id=self.current_task_id,
                duration=duration_minutes
            )

            # Store whether to collect grapes
            self.collect_grapes_on_complete = collect_grapes

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
        duration = self.timer.focus_duration // 60

        # Complete session in database (with or without grape collection)
        if self.current_session_id:
            self.db.complete_session(self.current_session_id, self.collect_grapes_on_complete)

        # Build completion message
        if self.collect_grapes_on_complete:
            # Check for new badges
            new_badges = self.db.check_and_award_badges()

            # Show completion message with grape
            profile = self.db.get_profile()
            message = f"""🎉 집중 완료!

🔥 {duration}분 집중 완료!
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
        else:
            # No grape collection message
            message = f"""🎉 집중 완료!

🔥 {duration}분 집중 완료!

⚠️ 15분 미만 집중이라 포도알을 획득하지 못했습니다.
다음부터는 15분 이상 집중하여 포도알을 모아보세요!"""

        break_mins = self.timer.break_duration // 60
        message += f"\n\n이제 {break_mins}분 휴식하세요."

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
        self.collect_grapes_on_complete = True  # Reset for next session

    def _on_task_selected(self, task_id: int, task_title: str):
        """Handle task selection."""
        self.current_task_id = task_id
        self.current_task_title = task_title

        # If timer is running, update the display
        if self.timer.is_running():
            self.timer_widget.set_current_task(task_title)

    def closeEvent(self, event):
        """Handle window close event."""
        # Close mini window if exists
        if self.mini_window:
            self.mini_window.close()

        # Close database connection
        self.db.close()
        event.accept()

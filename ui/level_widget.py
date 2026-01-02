"""
Level and XP widget for Ppodo application.
Displays user level, experience points, and streak information.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from core.database import Database


class LevelWidget(QWidget):
    """Widget for displaying level, XP, and streak information."""

    def __init__(self, db: Database):
        """
        Initialize level widget.

        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self._init_ui()
        self.refresh()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Level and XP section
        level_layout = QHBoxLayout()

        self.level_label = QLabel("⭐ Level 1")
        self.level_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E63946;")
        level_layout.addWidget(self.level_label)

        level_layout.addStretch()
        layout.addLayout(level_layout)

        # XP Progress bar
        self.xp_bar = QProgressBar()
        self.xp_bar.setMinimum(0)
        self.xp_bar.setMaximum(100)
        self.xp_bar.setValue(0)
        self.xp_bar.setFormat("%v / %m XP")
        self.xp_bar.setTextVisible(True)
        self.xp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E63946;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                   stop:0 #E63946, stop:1 #FF6B6B);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.xp_bar)

        # Stats section
        stats_layout = QHBoxLayout()

        # Streak
        self.streak_label = QLabel("🔥 연속: 0일")
        self.streak_label.setStyleSheet("font-size: 13px; font-weight: bold;")

        # Total time
        self.time_label = QLabel("⏰ 총 시간: 0.0h")
        self.time_label.setStyleSheet("font-size: 13px; font-weight: bold;")

        stats_layout.addWidget(self.streak_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.time_label)

        layout.addLayout(stats_layout)

        self.setLayout(layout)

    def refresh(self):
        """Refresh level and XP display."""
        profile = self.db.get_profile()

        # Update level
        level = profile['level']
        self.level_label.setText(f"⭐ Level {level}")

        # Update XP bar
        current_xp = profile['xp']
        required_xp = self.db.get_xp_for_next_level(level)

        self.xp_bar.setMaximum(required_xp)
        self.xp_bar.setValue(current_xp)
        self.xp_bar.setFormat(f"{current_xp} / {required_xp} XP")

        # Update streak
        streak = profile['streak_days']
        self.streak_label.setText(f"🔥 연속: {streak}일")

        # Update total time
        total_minutes = profile.get('total_focus_minutes', 0)
        total_hours = total_minutes / 60
        self.time_label.setText(f"⏰ 총 시간: {total_hours:.1f}h")

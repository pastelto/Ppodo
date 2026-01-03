"""
Level and XP widget for Ppodo application.
Displays user level, experience points, and streak information.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from core.database import Database


class LevelWidget(QWidget):
    """Widget for displaying level, XP, and streak information."""

    def __init__(self, db: Database, theme_manager=None):
        """
        Initialize level widget.

        Args:
            db: Database instance
            theme_manager: Theme manager for dynamic colors
        """
        super().__init__()
        self.db = db
        self.theme_manager = theme_manager
        self._init_ui()
        self.refresh()

    def _init_ui(self):
        """Initialize UI components."""
        # Ensure minimum height for full visibility (increase to avoid overlap)
        self.setMinimumHeight(140)

        layout = QVBoxLayout()
        layout.setSpacing(14)
        # give extra bottom margin so stats below the XP bar don't collide
        layout.setContentsMargins(10, 10, 10, 18)

        # Level and XP section
        level_layout = QHBoxLayout()

        self.level_label = QLabel("⭐ Level 1")
        self.level_label.setMinimumHeight(30)
        level_layout.addWidget(self.level_label)

        level_layout.addStretch()
        layout.addLayout(level_layout)

        # XP Progress bar with better visibility
        self.xp_bar = QProgressBar()
        self.xp_bar.setMinimum(0)
        self.xp_bar.setMaximum(100)
        self.xp_bar.setValue(0)
        self.xp_bar.setFormat("%v / %m XP")
        self.xp_bar.setTextVisible(True)
        self.xp_bar.setMinimumHeight(36)  # Ensure full visibility and avoid overlap
        layout.addWidget(self.xp_bar)

        # Small gap between XP bar and the stats labels to avoid visual overlap
        layout.addSpacing(8)

        # Stats section with better spacing
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(22)

        # Streak
        self.streak_label = QLabel("🔥 연속: 0일")
        self.streak_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2C3E50;
            padding: 6px 3px 3px 3px;
        """)

        # Total time
        self.time_label = QLabel("⏰ 총 시간: 0.0h")
        self.time_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2C3E50;
            padding: 6px 3px 3px 3px;
        """)

        stats_layout.addWidget(self.streak_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.time_label)

        layout.addLayout(stats_layout)

        self.setLayout(layout)

        # Apply initial theme
        self._apply_theme_styles()

    def _apply_theme_styles(self):
        """Apply theme colors to level widget."""
        # Get theme color
        if self.theme_manager:
            theme_color = self.theme_manager.get_focus_color()
            theme_color_light = self._lighten_color(theme_color, 0.2)
        else:
            theme_color = "#E63946"
            theme_color_light = "#FF6B6B"

        # Apply to level label
        self.level_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {theme_color};
            padding: 5px;
        """)

        # Apply to XP bar
        self.xp_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {theme_color};
                border-radius: 8px;
                text-align: center;
                min-height: 30px;
                font-size: 13px;
                font-weight: bold;
                background-color: #F5F5F5;
                padding-bottom: 2px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                   stop:0 {theme_color}, stop:1 {theme_color_light});
                border-radius: 6px;
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

    def apply_theme(self):
        """Apply current theme to the widget."""
        self._apply_theme_styles()

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

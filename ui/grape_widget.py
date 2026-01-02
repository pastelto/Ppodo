"""
Grape collection widget for Ppodo application.
Displays grape → bunch → box progression.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt
from core.database import Database


class GrapeWidget(QWidget):
    """Widget for displaying grape collection stats."""

    def __init__(self, db: Database):
        """
        Initialize grape widget.

        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self._init_ui()
        self.refresh()

    def _init_ui(self):
        """Initialize UI components."""
        self.setMinimumWidth(280)  # Ensure minimum width for visibility
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("🍇 포도 수확량")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Total stats group
        total_group = QGroupBox("전체 수확량")
        total_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; padding-top: 10px; }")
        total_layout = QVBoxLayout()
        total_layout.setSpacing(8)

        self.total_grapes_label = QLabel("🟣 포도알: 0개")
        self.total_grapes_label.setStyleSheet("font-size: 14px;")

        self.total_bunches_label = QLabel("🍇 포도송이: 0송이")
        self.total_bunches_label.setStyleSheet("font-size: 14px;")

        self.total_boxes_label = QLabel("📦 포도상자: 0상자")
        self.total_boxes_label.setStyleSheet("font-size: 14px;")

        total_layout.addWidget(self.total_grapes_label)
        total_layout.addWidget(self.total_bunches_label)
        total_layout.addWidget(self.total_boxes_label)
        total_group.setLayout(total_layout)
        layout.addWidget(total_group)

        # Today stats
        self.today_label = QLabel("⭐ 오늘: 0개")
        self.today_label.setStyleSheet("font-size: 14px; color: #E63946; font-weight: bold;")
        layout.addWidget(self.today_label)

        # Current bunch progress
        bunch_group = QGroupBox("현재 송이 진행도")
        bunch_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; padding-top: 10px; }")
        bunch_layout = QVBoxLayout()
        bunch_layout.setSpacing(8)

        self.bunch_progress_label = QLabel("[○○○○○○○○○○]")
        self.bunch_progress_label.setStyleSheet("font-size: 18px; font-family: monospace;")
        self.bunch_progress_label.setAlignment(Qt.AlignCenter)

        self.bunch_count_label = QLabel("0 / 10 포도알")
        self.bunch_count_label.setStyleSheet("font-size: 12px; color: #666;")
        self.bunch_count_label.setAlignment(Qt.AlignCenter)

        bunch_layout.addWidget(self.bunch_progress_label)
        bunch_layout.addWidget(self.bunch_count_label)
        bunch_group.setLayout(bunch_layout)
        layout.addWidget(bunch_group)

        # Current box progress
        box_group = QGroupBox("현재 상자 진행도")
        box_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; padding-top: 10px; }")
        box_layout = QVBoxLayout()
        box_layout.setSpacing(8)

        self.box_progress_label = QLabel("0 / 10 송이")
        self.box_progress_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.box_progress_label.setAlignment(Qt.AlignCenter)

        box_layout.addWidget(self.box_progress_label)
        box_group.setLayout(box_layout)
        layout.addWidget(box_group)

        layout.addStretch()
        self.setLayout(layout)

    def refresh(self):
        """Refresh grape collection display."""
        profile = self.db.get_profile()
        today_stats = self.db.get_today_stats()

        # Update total stats
        self.total_grapes_label.setText(f"🟣 포도알: {profile['total_grapes']}개")
        self.total_bunches_label.setText(f"🍇 포도송이: {profile['total_bunches']}송이")
        self.total_boxes_label.setText(f"📦 포도상자: {profile['total_boxes']}상자")

        # Update today stats
        self.today_label.setText(f"⭐ 오늘: {today_stats['grapes_earned']}개")

        # Update current bunch progress (visual)
        current_bunch_grapes = profile['current_bunch_grapes']
        bunch_visual = self._create_progress_visual(current_bunch_grapes, 10)
        self.bunch_progress_label.setText(bunch_visual)
        self.bunch_count_label.setText(f"{current_bunch_grapes} / 10 포도알")

        # Update current box progress
        current_box_bunches = profile['current_box_bunches']
        self.box_progress_label.setText(f"{current_box_bunches} / 10 송이")

    def _create_progress_visual(self, current: int, total: int) -> str:
        """
        Create visual progress indicator.

        Args:
            current: Current progress
            total: Total needed

        Returns:
            Visual progress string (e.g., "[●●●○○○○○○○]")
        """
        filled = "●" * current
        empty = "○" * (total - current)
        return f"[{filled}{empty}]"

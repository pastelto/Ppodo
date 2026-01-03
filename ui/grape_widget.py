"""
Grape collection widget for Ppodo application.
Displays grape → bunch → box → wine bottle → wine crate progression.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QGridLayout
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
        """Initialize UI components with 2x2 grid layout."""
        self.setMinimumWidth(320)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("🍇 포도 수확 단계")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #8B5A8D;")  # Purple grape theme
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Today stats
        self.today_label = QLabel("⭐ 오늘: 0개")
        self.today_label.setStyleSheet("font-size: 14px; color: #8B5A8D; font-weight: bold;")
        self.today_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.today_label)

        # 2x2 Grid for progression stages
        grid = QGridLayout()
        grid.setSpacing(10)

        # Stage 1: Grape Bunch (포도송이)
        bunch_box = self._create_stage_box("🍇", "포도송이", "total_bunches", "current_bunch")
        self.bunch_icon = bunch_box['icon']
        self.bunch_total = bunch_box['total']
        self.bunch_progress = bunch_box['progress']
        grid.addWidget(bunch_box['widget'], 0, 0)

        # Stage 2: Grape Box (포도상자)
        box_box = self._create_stage_box("📦", "포도상자", "total_boxes", "current_box")
        self.box_icon = box_box['icon']
        self.box_total = box_box['total']
        self.box_progress = box_box['progress']
        grid.addWidget(box_box['widget'], 0, 1)

        # Stage 3: Wine Bottle (와인병)
        bottle_box = self._create_stage_box("🍷", "와인병", "total_bottles", "current_bottle")
        self.bottle_icon = bottle_box['icon']
        self.bottle_total = bottle_box['total']
        self.bottle_progress = bottle_box['progress']
        grid.addWidget(bottle_box['widget'], 1, 0)

        # Stage 4: Wine Crate (와인상자)
        crate_box = self._create_stage_box("🍾", "와인상자", "total_crates", "current_crate")
        self.crate_icon = crate_box['icon']
        self.crate_total = crate_box['total']
        self.crate_progress = crate_box['progress']
        grid.addWidget(crate_box['widget'], 1, 1)

        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def _create_stage_box(self, icon: str, name: str, total_key: str, progress_key: str) -> dict:
        """Create a stage box for the 2x2 grid."""
        box = QGroupBox()
        box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                background-color: #FAFAFA;
                padding: 10px;
            }
        """)

        box_layout = QVBoxLayout()
        box_layout.setSpacing(5)

        # Icon (large)
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 36px;")
        icon_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(icon_label)

        # Name
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #2C3E50;")
        name_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(name_label)

        # Total count
        total_label = QLabel("0")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #8B5A8D;")
        total_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(total_label)

        # Progress (e.g., "3/10")
        progress_label = QLabel("0/10")
        progress_label.setStyleSheet("font-size: 11px; color: #666;")
        progress_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(progress_label)

        box.setLayout(box_layout)

        return {
            'widget': box,
            'icon': icon_label,
            'total': total_label,
            'progress': progress_label
        }

    def refresh(self):
        """Refresh grape collection display with wine progression."""
        profile = self.db.get_profile()
        today_stats = self.db.get_today_stats()

        # Update today stats
        self.today_label.setText(f"⭐ 오늘: {today_stats['grapes_earned']}개")

        # Update Stage 1: 포도송이 (Bunches)
        self.bunch_total.setText(str(profile['total_bunches']))
        self.bunch_progress.setText(f"{profile['current_bunch_grapes']}/10")

        # Update Stage 2: 포도상자 (Boxes)
        self.box_total.setText(str(profile['total_boxes']))
        self.box_progress.setText(f"{profile['current_box_bunches']}/10")

        # Update Stage 3: 와인병 (Wine Bottles)
        bottles = profile.get('total_wine_bottles', 0)
        bottle_progress = profile.get('current_bottle_boxes', 0)
        self.bottle_total.setText(str(bottles))
        self.bottle_progress.setText(f"{bottle_progress}/10")

        # Update Stage 4: 와인상자 (Wine Crates)
        crates = profile.get('total_wine_crates', 0)
        crate_progress = profile.get('current_crate_bottles', 0)
        self.crate_total.setText(str(crates))
        self.crate_progress.setText(f"{crate_progress}/10")

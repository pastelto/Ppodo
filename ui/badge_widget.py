"""
Badge collection widget for Ppodo application.
Displays all 15 badges with earned/unearned status.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from core.database import Database


class BadgeCard(QFrame):
    """Individual badge card widget."""

    def __init__(self, badge: dict):
        """
        Initialize badge card.

        Args:
            badge: Badge data dictionary
        """
        super().__init__()
        self.badge = badge
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(5)

        # Badge icon
        icon = QLabel(self.badge['icon'])
        icon.setStyleSheet("font-size: 40px;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        # Badge name
        name = QLabel(self.badge['name'])
        name.setStyleSheet("font-size: 13px; font-weight: bold;")
        name.setAlignment(Qt.AlignCenter)
        name.setWordWrap(True)
        layout.addWidget(name)

        # Badge description
        desc = QLabel(self.badge['description'])
        desc.setStyleSheet("font-size: 11px; color: #666;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Earned status
        if self.badge['earned']:
            status = QLabel("✓ 획득")
            status.setStyleSheet("""
                font-size: 11px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: #27AE60;
                padding: 4px 8px;
                border-radius: 3px;
            """)
            self.setStyleSheet("""
                BadgeCard {
                    border: 2px solid #27AE60;
                    border-radius: 10px;
                    background-color: #FFFFFF;
                    padding: 10px;
                }
            """)
        else:
            status = QLabel("미획득")
            status.setStyleSheet("""
                font-size: 11px;
                color: #999;
                background-color: #F0F0F0;
                padding: 4px 8px;
                border-radius: 3px;
            """)
            self.setStyleSheet("""
                BadgeCard {
                    border: 2px solid #E0E0E0;
                    border-radius: 10px;
                    background-color: #FAFAFA;
                    padding: 10px;
                    opacity: 0.6;
                }
            """)

        status.setAlignment(Qt.AlignCenter)
        layout.addWidget(status)

        self.setLayout(layout)
        self.setFixedWidth(140)
        self.setFixedHeight(180)


class BadgeWidget(QWidget):
    """Widget for displaying badge collection."""

    def __init__(self, db: Database):
        """
        Initialize badge widget.

        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container widget
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title
        title_layout = QHBoxLayout()
        title = QLabel("🏆 뱃지 컬렉션")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title)

        self.stats_label = QLabel("0 / 15 획득")
        self.stats_label.setStyleSheet("font-size: 14px; color: #666;")
        title_layout.addStretch()
        title_layout.addWidget(self.stats_label)

        layout.addLayout(title_layout)

        # Badge grid
        self.badge_grid = QGridLayout()
        self.badge_grid.setSpacing(15)
        layout.addLayout(self.badge_grid)

        layout.addStretch()
        container.setLayout(layout)

        scroll.setWidget(container)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def refresh(self):
        """Refresh badge collection display."""
        # Clear existing badges
        while self.badge_grid.count():
            item = self.badge_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get all badges
        badges = self.db.get_all_badges()

        # Group by category
        categories = {}
        for badge in badges:
            category = badge['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(badge)

        # Display badges by category
        row = 0
        for category, category_badges in categories.items():
            # Category header
            header = QLabel(f"【{category}】")
            header.setStyleSheet("font-size: 13px; font-weight: bold; color: #E63946; margin-top: 10px;")
            self.badge_grid.addWidget(header, row, 0, 1, 3)
            row += 1

            # Badge cards
            col = 0
            for badge in category_badges:
                card = BadgeCard(badge)
                self.badge_grid.addWidget(card, row, col)
                col += 1
                if col >= 3:  # 3 badges per row
                    col = 0
                    row += 1

            if col > 0:
                row += 1

        # Update stats
        earned_count = sum(1 for b in badges if b['earned'])
        total_count = len(badges)
        self.stats_label.setText(f"{earned_count} / {total_count} 획득")

"""
Task history widget for Ppodo application.
Shows completed tasks with creation and completion timestamps.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt
from datetime import datetime
from core.database import Database


class HistoryWidget(QWidget):
    """Widget for displaying completed task history."""

    def __init__(self, db: Database):
        """
        Initialize history widget.

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
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("✅ 완료된 할 일 기록")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title)

        # Table for completed tasks
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["할 일", "생성 시간", "완료 시간"])

        # Table styling
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                background-color: #FFFFFF;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F5F5F5;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: bold;
                font-size: 13px;
                color: #2C3E50;
            }
        """)

        # Resize columns to content
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Task title stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # Disable editing
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        layout.addWidget(self.table)

        # Stats label
        self.stats_label = QLabel("완료된 할 일: 0개")
        self.stats_label.setStyleSheet("font-size: 13px; color: #666; padding: 5px;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def refresh(self):
        """Refresh the completed tasks table."""
        # Get all completed tasks
        all_tasks = self.db.get_tasks()
        completed_tasks = [t for t in all_tasks if t.get('completed', False)]

        # Sort by completion time (most recent first)
        completed_tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)

        # Clear table
        self.table.setRowCount(0)

        # Add tasks to table
        for task in completed_tasks:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Task title
            title_item = QTableWidgetItem(f"✅ {task['title']}")
            title_item.setForeground(Qt.darkGreen)
            self.table.setItem(row, 0, title_item)

            # Creation time
            created_at = task.get('created_at', '')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    formatted = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted = created_at
            else:
                formatted = "N/A"
            created_item = QTableWidgetItem(formatted)
            created_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, created_item)

            # Completion time
            completed_at = task.get('completed_at', '')
            if completed_at:
                try:
                    dt = datetime.fromisoformat(completed_at)
                    formatted = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted = completed_at
            else:
                formatted = "N/A"
            completed_item = QTableWidgetItem(formatted)
            completed_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, completed_item)

        # Update stats
        self.stats_label.setText(f"완료된 할 일: {len(completed_tasks)}개")

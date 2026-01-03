"""
Task management widget for Ppodo application.
Allows creating, completing, and deleting tasks.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from core.database import Database


class TaskWidget(QWidget):
    """Widget for managing tasks."""

    # Signal emitted when a task is selected
    task_selected = Signal(int, str)  # task_id, task_title

    def __init__(self, db: Database, theme_manager=None):
        """
        Initialize task widget.

        Args:
            db: Database instance
            theme_manager: Theme manager for dynamic colors
        """
        super().__init__()
        self.db = db
        self.theme_manager = theme_manager
        self.selected_task_id = None
        self._init_ui()
        self.refresh()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Title
        title = QLabel("📝 할 일 관리")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Add task section
        add_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("새 할 일을 입력하세요...")
        self.task_input.returnPressed.connect(self.add_task)

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setMaximumWidth(80)

        add_layout.addWidget(self.task_input)
        add_layout.addWidget(self.add_button)
        layout.addLayout(add_layout)

        # Task list
        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self._on_task_clicked)
        self._apply_task_list_style()
        layout.addWidget(self.task_list)

        # Action buttons
        button_layout = QHBoxLayout()

        self.complete_button = QPushButton("✓ 완료")
        self.complete_button.clicked.connect(self.complete_task)
        self.complete_button.setEnabled(False)

        self.delete_button = QPushButton("✗ 삭제")
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setEnabled(False)

        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Stats label
        self.stats_label = QLabel("전체: 0 | 완료: 0 | 진행중: 0")
        self.stats_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def add_task(self):
        """Add a new task."""
        title = self.task_input.text().strip()
        if not title:
            return

        # Add to database
        self.db.add_task(title)

        # Clear input
        self.task_input.clear()

        # Refresh list
        self.refresh()

    def complete_task(self):
        """Mark selected task as completed."""
        if self.selected_task_id is None:
            return

        # Update database
        self.db.complete_task(self.selected_task_id)

        # Refresh list
        self.refresh()

        # Clear selection
        self.selected_task_id = None
        self.complete_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def delete_task(self):
        """Delete selected task."""
        if self.selected_task_id is None:
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "삭제 확인",
            "이 할 일을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Delete from database
            self.db.delete_task(self.selected_task_id)

            # Refresh list
            self.refresh()

            # Clear selection
            self.selected_task_id = None
            self.complete_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def _apply_task_list_style(self):
        """Apply theme-aware styling to task list."""
        # Get theme colors
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            hover_color = self._lighten_color(focus_color, 0.85)  # Very light version
        else:
            focus_color = "#E63946"
            hover_color = "#FFE5E8"

        # Use a slightly stronger divider color so separators are visible
        divider = "#E8E8E8"
        self.task_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                background-color: #FFFFFF;
                font-size: 13px;
            }}
            QListWidget::item {{
                padding: 12px 10px;
                border-bottom: 1px solid {divider};
                color: #2C3E50;
            }}
            QListWidget::item:last {{
                border-bottom: none;
            }}
            QListWidget::item:selected {{
                background-color: {focus_color};
                color: #FFFFFF;
            }}
            QListWidget::item:hover {{
                background-color: {hover_color};
                color: #1A1A1A;
            }}
        """)

    def _lighten_color(self, hex_color: str, factor: float = 0.3) -> str:
        """Lighten a hex color by blending with white."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        # Blend with white
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return f'#{r:02x}{g:02x}{b:02x}'

    def refresh(self):
        """Refresh task list showing both incomplete and completed tasks."""
        # Clear list
        self.task_list.clear()

        # Get all tasks
        all_tasks = self.db.get_tasks()

        # Separate completed and incomplete tasks
        incomplete_tasks = [t for t in all_tasks if not t['completed']]
        completed_tasks = [t for t in all_tasks if t['completed']]

        # Add incomplete tasks first
        for task in incomplete_tasks:
            item = QListWidgetItem(f"⬜ {task['title']}")
            item.setData(Qt.UserRole, task['id'])
            item.setData(Qt.UserRole + 1, False)  # Not completed
            self.task_list.addItem(item)

        # Add completed tasks with strikethrough
        for task in completed_tasks:
            item = QListWidgetItem(f"✅ {task['title']}")
            item.setData(Qt.UserRole, task['id'])
            item.setData(Qt.UserRole + 1, True)  # Completed

            # Apply strikethrough font
            font = QFont()
            font.setStrikeOut(True)
            item.setFont(font)

            # Make it slightly grayed out
            item.setForeground(Qt.gray)

            self.task_list.addItem(item)

        # Update stats
        self.stats_label.setText(
            f"전체: {len(all_tasks)} | 완료: {len(completed_tasks)} | 진행중: {len(incomplete_tasks)}"
        )

    def _on_task_clicked(self, item: QListWidgetItem):
        """Handle task item click."""
        self.selected_task_id = item.data(Qt.UserRole)
        task_title = item.text()

        # Enable buttons
        self.complete_button.setEnabled(True)
        self.delete_button.setEnabled(True)

        # Emit signal
        self.task_selected.emit(self.selected_task_id, task_title)

    def get_selected_task(self):
        """Get currently selected task."""
        if self.selected_task_id is None:
            return None

        current_item = self.task_list.currentItem()
        if current_item:
            return {
                'id': self.selected_task_id,
                'title': current_item.text()
            }
        return None

"""
Task management widget for Ppodo application.
Allows creating, completing, and deleting tasks.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QCheckBox,
    QInputDialog
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
        self.selected_task_completed = False  # Track if selected task is completed
        self.hide_completed = False  # Track hide completed checkbox state
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
        # Remove focus from input when clicking list items
        self.task_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #95A5A6;
            }
        """)

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setMaximumWidth(80)

        add_layout.addWidget(self.task_input)
        add_layout.addWidget(self.add_button)
        layout.addLayout(add_layout)

        # Hide completed checkbox
        self.hide_completed_checkbox = QCheckBox("완료된 항목 숨기기")
        self.hide_completed_checkbox.stateChanged.connect(self._on_hide_completed_changed)
        self.hide_completed_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                color: #666;
                padding: 5px;
            }
        """)
        layout.addWidget(self.hide_completed_checkbox)

        # Task list
        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self._on_task_clicked)
        self.task_list.itemDoubleClicked.connect(self._on_task_double_clicked)
        # Prevent focus on click
        self.task_list.setFocusPolicy(Qt.NoFocus)
        self._apply_task_list_style()
        layout.addWidget(self.task_list)

        # Action buttons
        button_layout = QHBoxLayout()

        # Button 1: Complete or Copy (depending on selection)
        self.complete_button = QPushButton("✓ 완료")
        self.complete_button.clicked.connect(self._on_action1)
        self.complete_button.setEnabled(False)

        # Button 2: Delete or Uncomplete (depending on selection)
        self.delete_button = QPushButton("✗ 삭제")
        self.delete_button.clicked.connect(self._on_action2)
        self.delete_button.setEnabled(False)

        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Stats label
        self.stats_label = QLabel("전체: 0 | 완료: 0 | 진행중: 0")
        self.stats_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

        # Apply initial button styles
        self._update_button_styles()

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

    def _on_hide_completed_changed(self, state):
        """Handle hide completed checkbox change."""
        self.hide_completed = (state == Qt.Checked)
        self.refresh()

    def _on_action1(self):
        """Handle button 1 click (Complete or Copy)."""
        if self.selected_task_id is None:
            return

        if self.selected_task_completed:
            # Copy task
            self._copy_task()
        else:
            # Complete task
            self._complete_task()

    def _on_action2(self):
        """Handle button 2 click (Delete or Uncomplete)."""
        if self.selected_task_id is None:
            return

        if self.selected_task_completed:
            # Uncomplete task
            self._uncomplete_task()
        else:
            # Delete task
            self._delete_task()

    def _complete_task(self):
        """Mark selected task as completed."""
        # Update database
        self.db.complete_task(self.selected_task_id)

        # Refresh list
        self.refresh()

        # Clear selection
        self._clear_selection()

    def _copy_task(self):
        """Copy selected completed task as a new incomplete task."""
        # Get task title
        current_item = self.task_list.currentItem()
        if not current_item:
            return

        task_title = current_item.text().replace("✅ ", "")

        # Add as new task
        self.db.add_task(task_title)

        # Refresh list
        self.refresh()

        QMessageBox.information(
            self,
            "복사 완료",
            f"'{task_title}'이(가) 새 할 일로 추가되었습니다."
        )

    def _uncomplete_task(self):
        """Mark selected completed task as incomplete."""
        # Update database
        self.db.uncomplete_task(self.selected_task_id)

        # Refresh list
        self.refresh()

        # Clear selection
        self._clear_selection()

    def _delete_task(self):
        """Delete selected task."""
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
            self._clear_selection()

    def _clear_selection(self):
        """Clear current selection and disable buttons."""
        self.selected_task_id = None
        self.selected_task_completed = False
        self.complete_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self._update_button_styles()

    def _apply_task_list_style(self):
        """Apply theme-aware styling to task list."""
        # Get theme colors
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            # Use a darker version of theme color for selection (more muted)
            selected_color = self._darken_color(focus_color, 0.25)
            hover_color = self._lighten_color(focus_color, 0.85)  # Very light version
        else:
            focus_color = "#E63946"
            selected_color = "#B82E3A"  # Darker red
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
                background-color: {selected_color};
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

    def _darken_color(self, hex_color: str, factor: float = 0.2) -> str:
        """Darken a hex color by reducing brightness."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        # Reduce brightness
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _update_button_styles(self):
        """Update button styles based on theme and enabled state."""
        # Get theme colors
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            break_color = self.theme_manager.get_break_color()
        else:
            focus_color = "#27AE60"  # Green for complete
            break_color = "#E74C3C"  # Red for delete

        # Complete button - use focus color when enabled
        complete_hover = self._darken_color(focus_color, 0.15)
        self.complete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {focus_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {complete_hover};
            }}
            QPushButton:disabled {{
                background-color: #E0E0E0;
                color: #999999;
            }}
        """)

        # Delete button - use break color when enabled
        delete_hover = self._darken_color(break_color, 0.15)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {break_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {delete_hover};
            }}
            QPushButton:disabled {{
                background-color: #E0E0E0;
                color: #999999;
            }}
        """)

    def apply_theme(self):
        """Apply current theme to the widget."""
        self._apply_task_list_style()
        self._update_button_styles()

    def refresh(self):
        """Refresh task list showing incomplete and optionally completed tasks."""
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

        # Add completed tasks if not hidden
        if not self.hide_completed:
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
        if self.hide_completed:
            self.stats_label.setText(
                f"진행중: {len(incomplete_tasks)} | 완료: {len(completed_tasks)} (숨김)"
            )
        else:
            self.stats_label.setText(
                f"전체: {len(all_tasks)} | 완료: {len(completed_tasks)} | 진행중: {len(incomplete_tasks)}"
            )

    def _on_task_clicked(self, item: QListWidgetItem):
        """Handle task item click."""
        is_completed = item.data(Qt.UserRole + 1)

        self.selected_task_id = item.data(Qt.UserRole)
        self.selected_task_completed = is_completed
        task_title_with_icon = item.text()

        # Remove status icon (⬜ or ✅) from title
        task_title = task_title_with_icon.replace("⬜ ", "").replace("✅ ", "")

        # Update button labels and enable based on completion status
        if is_completed:
            # Completed task: Show Copy and Uncomplete buttons
            self.complete_button.setText("📋 복사")
            self.delete_button.setText("↩ 완료 취소")
            self.complete_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            # Incomplete task: Show Complete and Delete buttons
            self.complete_button.setText("✓ 완료")
            self.delete_button.setText("✗ 삭제")
            self.complete_button.setEnabled(True)
            self.delete_button.setEnabled(True)

            # Emit signal for incomplete tasks only (for timer integration)
            self.task_selected.emit(self.selected_task_id, task_title)

        # Update button styles to show they're enabled
        self._update_button_styles()

        # Clear focus from input box
        self.task_input.clearFocus()

    def _on_task_double_clicked(self, item: QListWidgetItem):
        """Handle task item double-click for editing."""
        is_completed = item.data(Qt.UserRole + 1)

        # Only allow editing incomplete tasks
        if is_completed:
            return

        task_id = item.data(Qt.UserRole)
        current_title = item.text().replace("⬜ ", "")

        # Show input dialog
        new_title, ok = QInputDialog.getText(
            self,
            "할 일 수정",
            "새 제목:",
            QLineEdit.Normal,
            current_title
        )

        if ok and new_title.strip():
            # Update database
            self.db.update_task(task_id, new_title.strip())
            # Refresh list
            self.refresh()

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

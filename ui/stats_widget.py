"""
Statistics widget for Ppodo application.
Displays weekly focus time chart and task distribution pie chart.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from core.database import Database


class StatsWidget(QWidget):
    """Widget for displaying statistics and charts."""

    def __init__(self, db: Database, theme_manager=None):
        """
        Initialize stats widget.

        Args:
            db: Database instance
            theme_manager: Theme manager instance for color theming
        """
        super().__init__()
        self.db = db
        self.theme_manager = theme_manager
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        # Scroll area for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container widget
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title
        title = QLabel("📊 통계 분석")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Weekly chart
        weekly_label = QLabel("주간 집중 시간 (최근 7일)")
        weekly_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(weekly_label)

        self.weekly_canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.weekly_canvas)

        # Task distribution chart
        task_label = QLabel("오늘의 태스크 분포")
        task_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(task_label)

        self.task_canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.task_canvas)

        layout.addStretch()
        container.setLayout(layout)

        scroll.setWidget(container)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def refresh(self):
        """Refresh all charts."""
        self._draw_weekly_chart()
        self._draw_task_distribution()

    def _draw_weekly_chart(self):
        """Draw weekly focus time bar chart."""
        # Get weekly stats
        stats = self.db.get_weekly_stats()

        # Create full 7-day data (fill missing days with 0)
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        stats_dict = {date: minutes for date, minutes in stats}
        values = [stats_dict.get(date, 0) for date in dates]

        # Convert to hours
        hours = [v / 60 for v in values]

        # Format dates for display (MM/DD)
        labels = [datetime.fromisoformat(d).strftime("%m/%d") for d in dates]

        # Get theme colors
        if self.theme_manager:
            focus_color = self.theme_manager.get_focus_color()
            # Darken for edge color
            edge_color = self._darken_color(focus_color)
        else:
            focus_color = '#457B9D'  # Default Nordic blue
            edge_color = '#2C5F7D'

        # Clear previous chart
        self.weekly_canvas.figure.clear()

        # Create bar chart
        ax = self.weekly_canvas.figure.add_subplot(111)
        bars = ax.bar(labels, hours, color=focus_color, alpha=0.8, edgecolor=edge_color, linewidth=1.5)

        # Styling
        ax.set_xlabel('날짜', fontsize=11, fontweight='bold')
        ax.set_ylabel('시간 (h)', fontsize=11, fontweight='bold')
        ax.set_ylim(0, max(hours) * 1.2 if max(hours) > 0 else 5)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # Add value labels on bars
        for bar, hour in zip(bars, hours):
            if hour > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                       f'{hour:.1f}h',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')

        self.weekly_canvas.figure.tight_layout()
        self.weekly_canvas.draw()

    def _draw_task_distribution(self):
        """Draw task distribution pie chart."""
        # Get task distribution
        distribution = self.db.get_task_distribution()

        # Clear previous chart
        self.task_canvas.figure.clear()

        if not distribution:
            # No data - show message
            ax = self.task_canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, '오늘은 아직 집중한 태스크가 없습니다',
                   ha='center', va='center', fontsize=12, color='#999')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Create pie chart
            labels = [task[0] for task in distribution]
            sizes = [task[1] for task in distribution]

            # Limit to top 5 tasks
            if len(labels) > 5:
                labels = labels[:5] + ['기타']
                sizes = sizes[:5] + [sum(sizes[5:])]

            # Color palette - uses theme colors if available, otherwise Nordic palette
            if self.theme_manager:
                focus_color = self.theme_manager.get_focus_color()
                break_color = self.theme_manager.get_break_color()
                pause_color = self.theme_manager.get_pause_color()
                # Generate variations
                colors = [
                    focus_color,
                    break_color,
                    pause_color,
                    self._lighten_color(focus_color),
                    self._lighten_color(break_color),
                    self._darken_color(pause_color)
                ]
            else:
                # Default Nordic palette (no red)
                colors = ['#457B9D', '#A8DADC', '#E9C46A', '#2C5F7D', '#7FB8C0', '#D4A373']

            ax = self.task_canvas.figure.add_subplot(111)
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                colors=colors[:len(labels)],
                startangle=90,
                textprops={'fontsize': 10}
            )

            # Make percentage text bold and white
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)

            ax.axis('equal')

        self.task_canvas.figure.tight_layout()
        self.task_canvas.draw()

    def _darken_color(self, hex_color: str, factor: float = 0.7) -> str:
        """Darken a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _lighten_color(self, hex_color: str, factor: float = 1.3) -> str:
        """Lighten a hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

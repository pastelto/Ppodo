"""
Theme system for Ppodo application.
Provides 5 premium color themes for focus and break modes.
"""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Theme:
    """Theme data class."""
    name: str
    focus_color: str
    break_color: str
    concept: str


class ThemeManager:
    """Manages application themes."""

    # Premium theme palette (5 themes)
    THEMES = {
        "Classic": Theme(
            name="Classic",
            focus_color="#E63946",
            break_color="#A8DADC",
            concept="전통적인 뽀모도로의 열정과 휴식"
        ),
        "Midnight": Theme(
            name="Midnight",
            focus_color="#1B263B",
            break_color="#E0E1DD",
            concept="깊은 밤의 고요함과 차분함"
        ),
        "Forest": Theme(
            name="Forest",
            focus_color="#2D6A4F",
            break_color="#D8E2DC",
            concept="숲속의 안정감과 눈의 편안함"
        ),
        "Royal": Theme(
            name="Royal",
            focus_color="#5A189A",
            break_color="#FFB703",
            concept="창의성을 자극하는 보라와 황금빛"
        ),
        "Sunset": Theme(
            name="Sunset",
            focus_color="#FB5607",
            break_color="#3A86FF",
            concept="활기찬 에너지와 역동적인 변화"
        )
    }

    def __init__(self):
        """Initialize theme manager with Classic theme."""
        self.current_theme_name = "Classic"

    def get_theme(self, name: str = None) -> Theme:
        """
        Get theme by name.

        Args:
            name: Theme name. If None, returns current theme.

        Returns:
            Theme object
        """
        if name is None:
            name = self.current_theme_name

        return self.THEMES.get(name, self.THEMES["Classic"])

    def set_theme(self, name: str):
        """
        Set current theme.

        Args:
            name: Theme name
        """
        if name in self.THEMES:
            self.current_theme_name = name

    def get_all_themes(self) -> List[Theme]:
        """
        Get all available themes.

        Returns:
            List of Theme objects
        """
        return list(self.THEMES.values())

    def get_theme_names(self) -> List[str]:
        """
        Get all theme names.

        Returns:
            List of theme names
        """
        return list(self.THEMES.keys())

    def get_focus_color(self, theme_name: str = None) -> str:
        """
        Get focus color for a theme.

        Args:
            theme_name: Theme name. If None, uses current theme.

        Returns:
            Hex color string
        """
        theme = self.get_theme(theme_name)
        return theme.focus_color

    def get_break_color(self, theme_name: str = None) -> str:
        """
        Get break color for a theme.

        Args:
            theme_name: Theme name. If None, uses current theme.

        Returns:
            Hex color string
        """
        theme = self.get_theme(theme_name)
        return theme.break_color

    def get_current_color(self, is_focus: bool) -> str:
        """
        Get color based on current mode.

        Args:
            is_focus: True for focus mode, False for break mode

        Returns:
            Hex color string
        """
        theme = self.get_theme()
        return theme.focus_color if is_focus else theme.break_color

    def apply_stylesheet(self, widget, is_focus: bool = True) -> str:
        """
        Generate Qt stylesheet for a widget.

        Args:
            widget: Widget class name or identifier
            is_focus: True for focus mode, False for break mode

        Returns:
            Qt stylesheet string
        """
        color = self.get_current_color(is_focus)

        # Base stylesheet with theme color
        stylesheet = f"""
            QWidget {{
                background-color: #FFFFFF;
                color: #2B2D42;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}

            QPushButton {{
                background-color: {color};
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}

            QPushButton:pressed {{
                background-color: {self._darken_color(color, 0.3)};
            }}

            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #999999;
            }}

            QProgressBar {{
                border: 2px solid {color};
                border-radius: 5px;
                text-align: center;
                background-color: #F5F5F5;
            }}

            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}

            QLineEdit {{
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                background-color: #FFFFFF;
            }}

            QLineEdit:focus {{
                border: 2px solid {color};
            }}

            QListWidget {{
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                background-color: #FFFFFF;
            }}

            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }}

            QListWidget::item:selected {{
                background-color: {color};
                color: #FFFFFF;
            }}

            QListWidget::item:hover {{
                background-color: {self._lighten_color(color)};
            }}

            QLabel {{
                color: #2B2D42;
            }}

            QTabWidget::pane {{
                border: 1px solid #E0E0E0;
                border-radius: 5px;
            }}

            QTabBar::tab {{
                background-color: #F5F5F5;
                color: #666666;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}

            QTabBar::tab:selected {{
                background-color: {color};
                color: #FFFFFF;
            }}

            QTabBar::tab:hover {{
                background-color: {self._lighten_color(color)};
            }}
        """

        return stylesheet

    def _darken_color(self, hex_color: str, factor: float = 0.2) -> str:
        """
        Darken a hex color.

        Args:
            hex_color: Hex color string (e.g., '#E63946')
            factor: Darkening factor (0-1)

        Returns:
            Darkened hex color
        """
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))

        return f'#{r:02x}{g:02x}{b:02x}'

    def _lighten_color(self, hex_color: str, factor: float = 0.8) -> str:
        """
        Lighten a hex color.

        Args:
            hex_color: Hex color string (e.g., '#E63946')
            factor: Lightening factor (0-1)

        Returns:
            Lightened hex color
        """
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        return f'#{r:02x}{g:02x}{b:02x}'

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
    pause_color: str
    pause_hover: str
    concept: str


class ThemeManager:
    """Manages application themes."""

    # Premium theme palette (5 themes)
    THEMES = {
        # 1. Nordic (기존 Classic 대체): 차분하고 지적인 북유럽 스타일의 블루톤
        "Nordic": Theme(
            name="Nordic",
            focus_color="#457B9D",  # Steel Blue (차분한 집중)
            break_color="#A8DADC",  # Pale Blue (시원한 휴식)
            pause_color="#E9C46A",  # Sand Yellow (따뜻한 주의 환기)
            pause_hover="#D4A373",  # Muted Bronze
            concept="북유럽의 차분함과 지적인 분위기"
        ),

        # 2. Midnight: 깊은 밤의 몰입감 (다크 모드 선호 시 최적)
        "Midnight": Theme(
            name="Midnight",
            focus_color="#2B2D42",  # Dark Slate (깊은 몰입)
            break_color="#8D99AE",  # Cool Grey (눈이 편한 회색)
            pause_color="#FFD166",  # Sunglow (어두운 배경 위 확실한 강조)
            pause_hover="#FFC035",  # Deep Yellow
            concept="깊은 밤의 고요함과 완벽한 몰입"
        ),

        # 3. Forest: 자연의 편안함 (가장 눈이 편한 조합)
        "Forest": Theme(
            name="Forest",
            focus_color="#2D6A4F",  # Deep Green (숲의 깊이)
            break_color="#D8E2DC",  # Mist Green (안개 낀 숲)
            pause_color="#D4A373",  # Wood Brown (나무 색상으로 자연스러운 조화)
            pause_hover="#BC6C25",  # Caramel
            concept="숲속의 피톤치드와 같은 안정감"
        ),

        # 4. Lavender (기존 Royal 대체): 창의적이고 몽환적인 보라빛
        "Lavender": Theme(
            name="Lavender",
            focus_color="#7209B7",  # Vivid Violet (창의성 자극)
            break_color="#E0AAFF",  # Soft Lilac (부드러운 이완)
            pause_color="#4CC9F0",  # Vivid Sky Blue (보라색과 보색에 가까운 팝한 느낌)
            pause_hover="#4895EF",  # Dodger Blue
            concept="영감을 깨우는 감각적인 바이올렛"
        ),

        # 5. Cafe (기존 Sunset 대체): 따뜻하고 아늑한 커피 색상
        "Cafe": Theme(
            name="Cafe",
            focus_color="#6F4E37",  # Coffee Bean (따뜻한 브라운)
            break_color="#F5E0B7",  # Latte Foam (부드러운 베이지)
            pause_color="#E67E22",  # Carrot Orange (커피와 어울리는 따뜻한 포인트)
            pause_hover="#D35400",  # Pumpkin
            concept="카페에서의 여유롭고 따뜻한 집중"
        )
    }

    def __init__(self):
        """Initialize theme manager with Nordic theme."""
        self.current_theme_name = "Nordic"

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

        return self.THEMES.get(name, self.THEMES["Nordic"])

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

    def get_pause_color(self, theme_name: str = None) -> str:
        """
        Get pause color for a theme.

        Args:
            theme_name: Theme name. If None, uses current theme.

        Returns:
            Hex color string
        """
        theme = self.get_theme(theme_name)
        return theme.pause_color

    def get_pause_hover_color(self, theme_name: str = None) -> str:
        """
        Get pause hover color for a theme.

        Args:
            theme_name: Theme name. If None, uses current theme.

        Returns:
            Hex color string
        """
        theme = self.get_theme(theme_name)
        return theme.pause_hover

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

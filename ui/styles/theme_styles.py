"""
Theme-aware styling utilities for Ppodo application.
Provides centralized styling functions for consistent UI.
"""


def darken_color(hex_color: str, factor: float = 0.2) -> str:
    """
    Darken a hex color by a given factor.

    Args:
        hex_color: Hex color string (e.g., '#E63946')
        factor: Darkening factor (0.0 to 1.0)

    Returns:
        Darkened hex color string
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f'#{r:02x}{g:02x}{b:02x}'


def lighten_color(hex_color: str, factor: float = 0.3) -> str:
    """
    Lighten a hex color by a given factor.

    Args:
        hex_color: Hex color string (e.g., '#E63946')
        factor: Lightening factor (0.0 to 1.0)

    Returns:
        Lightened hex color string
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f'#{r:02x}{g:02x}{b:02x}'


def get_button_style(bg_color: str, hover_factor: float = 0.15,
                     padding: str = "10px 20px", font_size: str = "14px") -> str:
    """
    Get theme-aware button stylesheet.

    Args:
        bg_color: Background color for the button
        hover_factor: Darkening factor for hover state
        padding: CSS padding value
        font_size: CSS font size value

    Returns:
        Qt stylesheet string for button
    """
    hover_color = darken_color(bg_color, hover_factor)

    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            border-radius: 5px;
            padding: {padding};
            font-size: {font_size};
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:disabled {{
            background-color: #CCCCCC;
            color: #999999;
        }}
    """


def get_spinbox_style(focus_color: str = "#E63946") -> str:
    """
    Get spinbox stylesheet with arrow buttons.

    Args:
        focus_color: Color for focus state border

    Returns:
        Qt stylesheet string for spinbox
    """
    return f"""
        QSpinBox {{
            padding: 8px 30px 8px 8px;
            font-size: 14px;
            border: 2px solid #E0E0E0;
            border-radius: 5px;
        }}
        QSpinBox:focus {{
            border: 2px solid {focus_color};
        }}
        QSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #E0E0E0;
            border-bottom: 1px solid #E0E0E0;
            border-top-right-radius: 3px;
            background: #F5F5F5;
        }}
        QSpinBox::up-button:hover {{
            background: #E8E8E8;
        }}
        QSpinBox::up-arrow {{
            image: none;
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 6px solid #555;
        }}
        QSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-left: 1px solid #E0E0E0;
            border-top: 1px solid #E0E0E0;
            border-bottom-right-radius: 3px;
            background: #F5F5F5;
        }}
        QSpinBox::down-button:hover {{
            background: #E8E8E8;
        }}
        QSpinBox::down-arrow {{
            image: none;
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #555;
        }}
    """


def get_groupbox_style(font_size: str = "14px", padding_top: str = "10px") -> str:
    """
    Get GroupBox stylesheet.

    Args:
        font_size: Font size for group title
        padding_top: Top padding for group content

    Returns:
        Qt stylesheet string for GroupBox
    """
    return f"""
        QGroupBox {{
            font-size: {font_size};
            font-weight: bold;
            padding-top: {padding_top};
            color: #2C3E50;
        }}
    """


def get_header_button_style(bg_color: str, size: str = "small") -> str:
    """
    Get stylesheet for header buttons (mini mode, toggle, settings).

    Args:
        bg_color: Background color
        size: Size preset ('small', 'medium', 'large')

    Returns:
        Qt stylesheet string
    """
    sizes = {
        'small': {'padding': '6px 12px', 'font_size': '12px'},
        'medium': {'padding': '8px 15px', 'font_size': '13px'},
        'large': {'padding': '10px 20px', 'font_size': '14px'}
    }

    style_config = sizes.get(size, sizes['medium'])
    hover_color = darken_color(bg_color, 0.15)

    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            border-radius: 5px;
            padding: {style_config['padding']};
            font-size: {style_config['font_size']};
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """


def get_mini_button_style(bg_color: str, size: tuple = (55, 45)) -> str:
    """
    Get stylesheet for mini window buttons.

    Args:
        bg_color: Background color
        size: Button size as (width, height)

    Returns:
        Qt stylesheet string
    """
    hover_color = darken_color(bg_color, 0.15)

    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:disabled {{
            background-color: #CCCCCC;
            color: #999999;
        }}
    """

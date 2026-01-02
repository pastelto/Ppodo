"""
Ppodo (뽀도) - 포도알 뽀모도로 타이머
Main entry point for the application.

Author: Julie
Version: 2.1
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Set environment variable for better Qt scaling on Windows
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    # Enable high DPI scaling for better resolution support
    # Use Round policy for better compatibility at 1920x1080
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.Round
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Ppodo")
    app.setApplicationDisplayName("Ppodo (뽀도) - 포도알 뽀모도로 타이머")
    app.setOrganizationName("Julie")
    app.setOrganizationDomain("ppodo.app")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

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
    # Enable high DPI scaling for better resolution support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
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

"""
Ppodo (뽀도) - 포도알 뽀모도로 타이머
Main entry point for the application.

Author: Julie
Version: 2.0
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
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

"""
Mangapill Downloader - GUI Entry Point
Beautiful PyQt6 + QML interface for manga downloading.
"""

import sys
import os
from pathlib import Path

# Force Basic style to avoid Windows DLL issues
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

# Use software rendering to avoid GPU driver issues on some systems
# This fixes "COM error 0x887a0005: Device removed" errors
os.environ["QSG_RHI_BACKEND"] = "sw"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.bridge import MangaBridge


def main():
    """Launch the GUI application."""
    # Set application attributes
    app = QApplication(sys.argv)
    app.setApplicationName("Mangapill Downloader")
    app.setOrganizationName("Yui007")
    app.setApplicationVersion("1.0.0")
    
    # Create QML engine
    engine = QQmlApplicationEngine()
    
    # Create and register the bridge
    bridge = MangaBridge()
    engine.rootContext().setContextProperty("bridge", bridge)
    
    # Load the main QML file
    qml_file = Path(__file__).parent / "qml" / "main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        print("Error: Failed to load QML")
        sys.exit(-1)
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

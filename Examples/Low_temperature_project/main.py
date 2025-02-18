import sys
from PyQt6.QtWidgets import QApplication
from GUI.classes.setupDialog import setupDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    initialize_ui = setupDialog()
    sys.exit(app.exec())

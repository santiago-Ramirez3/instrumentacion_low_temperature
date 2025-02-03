from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFormLayout,
    QComboBox, QMenuBar, QStatusBar, QSplitter, QFrame
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("QTabWidget with Menu and Status Bar")
        self.setGeometry(100, 100, 600, 400)

        # Create the tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(self.createFirstWidget(), "Widget 1")
        tab_widget.addTab(self.createSecondWidget(), "Widget 2")
        tab_widget.addTab(self.createThirdWidget(), "Widget 3")

        # Create a vertical layout for the left forms
        left_forms_layout = QVBoxLayout()

        # Add forms for the devices
        left_forms_layout.addLayout(self.createPowerSupplyForm())
        left_forms_layout.addWidget(self.createSeparator())
        left_forms_layout.addLayout(self.createWaveGeneratorForm())
        left_forms_layout.addWidget(self.createSeparator())
        left_forms_layout.addLayout(self.createServoMotorForm())
        left_forms_layout.addStretch()

        left_forms_widget = QWidget()
        left_forms_widget.setLayout(left_forms_layout)

        # Use QSplitter for a resizable layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_forms_widget)
        splitter.addWidget(tab_widget)
        splitter.setStretchFactor(1, 1)

        # Set the splitter as the central widget
        self.setCentralWidget(splitter)

        # Add menu bar
        self.createMenuBar()

        # Add status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

    def createMenuBar(self):
        menu_bar = QMenuBar(self)

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Exit", self.close)

        # Help menu
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About")

        self.setMenuBar(menu_bar)

    def createSeparator(self):
        """Create a horizontal line as a separator."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def createPowerSupplyForm(self):
        """Create a form for the power supply."""
        form_layout = QFormLayout()
        form_layout.addRow("Voltage (V):", QComboBox())
        form_layout.addRow("Current (A):", QComboBox())
        form_layout.addRow("Power (W):", QComboBox())
        return form_layout

    def createWaveGeneratorForm(self):
        """Create a form for the wave generator."""
        form_layout = QFormLayout()
        form_layout.addRow("Wave Type:", QComboBox())
        form_layout.addRow("Frequency (Hz):", QComboBox())
        form_layout.addRow("Amplitude (V):", QComboBox())
        return form_layout

    def createServoMotorForm(self):
        """Create a form for the servo motor."""
        form_layout = QFormLayout()
        form_layout.addRow("Angle (°):", QComboBox())
        form_layout.addRow("Speed (RPM):", QComboBox())
        form_layout.addRow("Torque (Nm):", QComboBox())
        return form_layout

    def createFirstWidget(self):
        """Create the first widget."""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("This is the first widget")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def createSecondWidget(self):
        """Create the second widget."""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("This is the second widget")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def createThirdWidget(self):
        """Create the third widget."""
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("This is the third widget")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

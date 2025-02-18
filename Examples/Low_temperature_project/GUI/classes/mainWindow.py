from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout,
    QComboBox, QMenuBar, QStatusBar, QSplitter, QFrame, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from experiments.experimentDic import experimentDic
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, instruments:list):
        super().__init__()
        self.instruments = instruments
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(".\GUI\images\small_icon.png"))
        self.setGeometry(100, 100, 600, 400)

        # Add status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        # central tabWidgets
        self.centralExperiments()

        # Add menu bar
        self.createMenuBar()

    def centralExperiments(self):
        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        self.setCentralWidget(self.tab_widget)
    
    def remove_tab(self, index):
        """Eliminar una pestaña por índice."""
        self.tab_widget.removeTab(index)

    def instrumentsList(self):
        # Create a vertical layout for the left forms
        left_forms_layout = QVBoxLayout()

        # Add forms for the devices
        left_forms_layout.addWidget(self.createCenteredLabel('Instruments'))
        left_forms_layout.addLayout(self.instrumentsForm())
        left_forms_layout.addSpacing(20)

        left_forms_layout.addWidget(self.createSeparator())
        left_forms_layout.addWidget(self.createCenteredLabel('Power supply'))
        left_forms_layout.addLayout(self.createPowerSupplyForm())
        left_forms_layout.addSpacing(20)

        left_forms_layout.addWidget(self.createSeparator())
        left_forms_layout.addWidget(self.createCenteredLabel('Wave generator'))
        left_forms_layout.addLayout(self.createWaveGeneratorForm())
        left_forms_layout.addSpacing(20)

        left_forms_layout.addWidget(self.createSeparator())
        left_forms_layout.addWidget(self.createCenteredLabel('Servo motor'))
        left_forms_layout.addLayout(self.createServoMotorForm())
        left_forms_layout.addSpacing(20)

        left_forms_layout.addLayout(self.addButton())
        left_forms_layout.addStretch()


        left_forms_widget = QWidget()
        left_forms_widget.setLayout(left_forms_layout)
        left_forms_widget.setMaximumWidth(300)

        # Use QSplitter for a resizable layout
        #splitter = QSplitter(Qt.Orientation.Horizontal)
        #splitter.addWidget(left_forms_widget)
        #splitter.addWidget(tab_widget)
        #splitter.setStretchFactor(1, 1)

        # Set the splitter as the central widget

        

    def createMenuBar(self):
        menu_bar = QMenuBar(self)

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Exit", self.close)

        # Experiments menu
        experimetns_menu = menu_bar.addMenu("Experiments")
        for exp in experimentDic:
            
            experiment = experimentDic[exp](True,True,'data')
            #print(type(exp))
            action = experimetns_menu.addAction(exp)
            action.triggered.connect(partial(experiment.createWidget, tabWidget = self.tab_widget, currentInstruments=self.instruments[0]))

        # Help menu
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About")

        self.setMenuBar(menu_bar)

    def createCenteredLabel(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Usar CSS para cambiar la fuente y aplicar negrita
        label.setStyleSheet("font-size: 15px; font-weight: bold; font-family: Arial;")
    
        return label


    def createSeparator(self):
        """Create a horizontal line as a separator."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line
    
    def instrumentsForm(self):
        """Create a form for the power supply."""
        form_layout = QFormLayout()
        form_layout.addRow("Power Supply:", QComboBox())
        form_layout.addRow("Wave generator", QComboBox())
        form_layout.addRow("Servo motor", QComboBox())
        return form_layout
    
    def createPowerSupplyForm(self):
        """Create a form for the power supply."""
        form_layout = QFormLayout()
        form_layout.addRow("Voltage (V):", QLineEdit())
        form_layout.addRow("Current (A):", QLineEdit())
        form_layout.addRow("Power (W):", QLineEdit())
        return form_layout

    def createWaveGeneratorForm(self):
        """Create a form for the wave generator."""
        form_layout = QFormLayout()
        self.waveType = QComboBox()
        self.waveType.addItems(['Sine','Triangular','Squared'])
        form_layout.addRow("Wave Type:", self.waveType)
        form_layout.addRow("Frequency (Hz):", QLineEdit())
        form_layout.addRow("Amplitude (V):", QLineEdit())
        return form_layout

    def createServoMotorForm(self):
        """Create a form for the servo motor."""
        form_layout = QFormLayout()
        form_layout.addRow("Angle (°):", QLineEdit())
        form_layout.addRow("Speed (RPM):", QLineEdit())
        form_layout.addRow("Torque (Nm):", QLineEdit())
        return form_layout
    
    def addButton(self):
        layout = QHBoxLayout()

        stopButton = QPushButton('Stop')
        startButton = QPushButton('Start')

        # Estilo del botón Stop
        stopButton.setStyleSheet("""
            QPushButton {
                background-color: red;  /* Fondo rojo */
                color: white;           /* Texto blanco */
                border-radius: 10px;    /* Bordes redondeados */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: darkred; /* Fondo más oscuro al pasar el mouse */
            }
        """)

        # Estilo del botón Start
        startButton.setStyleSheet("""
            QPushButton {
                background-color: green;  /* Fondo verde */
                color: white;             /* Texto blanco */
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: darkgreen; /* Fondo más oscuro al pasar el mouse */
            }
        """)

        layout.addWidget(stopButton)
        layout.addWidget(startButton)
        return layout
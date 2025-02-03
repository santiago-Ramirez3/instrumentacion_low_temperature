from PyQt6.QtWidgets import (QWidget,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QComboBox,
                             QFrame,
                             QFormLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QFormLayout,
                             QTableWidget,
                             QHeaderView,
                             QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from GUI.classes.mainWindow import MainWindow

import pyvisa
from serial.tools import list_ports

class setupDialog(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initializeUI()

    #============================================================================================================
    def initializeUI(self):
        self.setGeometry(100,100,600,450)
        self.setFixedWidth(600)
        self.setWindowTitle("Setup Dialog")
        self.setWindowIcon(QIcon(".\GUI\images\small_icon.png"))

        self.generateForm()
        self.show()
    #============================================================================================================
    def generateForm(self):
        # Main vertical layout
        self.layout = QVBoxLayout(self)
        
        #-----------------------------------------------------------------
        # Tabla para los instrumentos
        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Instrumento", "Puerto", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Columna estrecha
        self.layout.addWidget(self.table)
        
        #-----------------------------------------------------------------
        # Botones para agregar y confirmar
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar Instrumento")
        self.confirm_button = QPushButton("Confirmar")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.confirm_button)
        self.layout.addLayout(self.button_layout)
        
        #-----------------------------------------------------------------
        # Conectar los botones
        self.add_button.clicked.connect(self.add_instrument_row)
        self.confirm_button.clicked.connect(self.confirm_data)
        self.show()

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def add_instrument_row(self):
        """Agrega una nueva fila a la tabla."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # ComboBox para el nombre del instrumento
        instrument_combo = QComboBox()
        instrument_combo.addItems(["Osciloscopio", "Multímetro", "Generador de Señales", "Fuente de Poder"])
        self.table.setCellWidget(row, 0, instrument_combo)
        
        # ComboBox para el puerto
        port_combo = QComboBox()
        port_combo.addItems(self.list_available_ports())
        self.table.setCellWidget(row, 1, port_combo)
        
        # Botón para eliminar la fila con icono
        delete_button = QPushButton()
        delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        delete_button.setIconSize(QSize(16, 16))  # Tamaño del icono
        delete_button.clicked.connect(self.remove_row)
        self.table.setCellWidget(row, 2, delete_button)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def list_available_ports(self) -> list:
        """
        Genera una lista de los puertos seriales disponibles y las direcciones GPIB detectadas.
        
        Returns:
            dict: Un diccionario con las claves 'serial_ports' y 'gpib_addresses'.
                  - 'serial_ports' contiene una lista de puertos seriales disponibles.
                  - 'gpib_addresses' contiene una lista de direcciones GPIB disponibles.
        """
        # Obtener los puertos seriales disponibles
        serial_ports = [port.device for port in list_ports.comports()]
    
        # Obtener las direcciones GPIB y otros recursos VISA
        rm = pyvisa.ResourceManager()
        visa_resources = rm.list_resources()
        print(visa_resources)
        
        # Filtrar las direcciones GPIB
        gpib_addresses = [resource for resource in visa_resources if 'GPIB' in resource]
    
        return serial_ports + gpib_addresses
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def remove_row(self):
        """Elimina la fila asociada al botón que disparó la señal."""
        button = self.sender()  # Identifica el botón que disparó la señal
        if button:
            # Obtén el índice de la celda del botón
            index = self.table.indexAt(button.pos())
            if index.isValid():
                self.table.removeRow(index.row())  # Elimina la fila correspondiente

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def confirm_data(self):
        """Recopila los datos y los imprime en consola."""
        instruments = []
        for row in range(self.table.rowCount()):
            instrument = self.table.cellWidget(row, 0).currentText()
            port = self.table.cellWidget(row, 1).currentText()
            instruments.append((instrument, port))
        print("Instrumentos confirmados:", instruments)

        #======================================================================================================
        #======================================================================================================

        self.window = MainWindow(instruments=instruments)
        self.window.show()
        self.close()
    
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout)

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setGeometry(100,100,400,150)
        self.setWindowTitle('Layout nested')
        self.generarFormulario()
        self.show()
    
    def generarFormulario(self):
        mensaje_principal = QLabel('Por favor ingrese los datos requeridos')

        nombre_label = QLabel('Nombres:')
        nombre_label.setFixedWidth(60)
        self.nombre_input = QLineEdit()

        apellidos_label = QLabel('Apellidos:')
        apellidos_label.setFixedWidth(60)
        self.apellidos_input = QLineEdit()

        edad_label = QLabel('Edad:')
        edad_label.setFixedWidth(60)
        self.edad_input = QLineEdit()

        email_label = QLabel('Email:')
        email_label.setFixedWidth(60)
        self.email_input = QLineEdit()

        direccion_label = QLabel('Direccion:')
        direccion_label.setFixedWidth(60)
        self.direccion_input = QLineEdit()

        telefono_label = QLabel('Telefono:')
        telefono_label.setFixedWidth(60)
        self.telefono_input = QLineEdit()

        enviar_boton = QPushButton('Enviar')
        #------------------------------------------------------------------
        vertical_layout_main = QVBoxLayout()
        #------------------------------------------------------------------
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()
        h_layout_3 = QHBoxLayout()

        h_layout_1.addWidget(nombre_label)
        h_layout_1.addWidget(self.nombre_input)
        h_layout_1.addWidget(email_label)
        h_layout_1.addWidget(self.email_input)

        h_layout_2.addWidget(apellidos_label)
        h_layout_2.addWidget(self.apellidos_input)
        h_layout_2.addWidget(direccion_label)
        h_layout_2.addWidget(self.direccion_input)

        h_layout_3.addWidget(edad_label)
        h_layout_3.addWidget(self.edad_input)
        h_layout_3.addWidget(telefono_label)
        h_layout_3.addWidget(self.telefono_input)
        #------------------------------------------------------------------

        vertical_layout_main.addWidget(mensaje_principal)
        vertical_layout_main.addLayout(h_layout_1)
        vertical_layout_main.addLayout(h_layout_2)
        vertical_layout_main.addLayout(h_layout_3)
        vertical_layout_main.addWidget(enviar_boton)

        #------------------------------------------------------------------
        self.setLayout(vertical_layout_main)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())
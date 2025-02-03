import sys
from PyQt6.QtWidgets import (QApplication,
                             QWidget, QLabel, QLineEdit,QPushButton,
                             QMessageBox, QCheckBox)

from PyQt6.QtGui import QFont, QPixmap

class crystalGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setGeometry(0,0,350,100)
        self.setWindowTitle('Control temperatura cristalizadora')
        self.generarInterfaz()
        self.show()
    
    def generarInterfaz(self):
        yi = 85
        n = 30
        self.arduinoIsConnected = False

        ports_label = QLabel(self)
        ports_label.setText('Puertos')
        ports_label.setFont(QFont('Arial', 10))
        ports_label.move(20,54)

        initial_temperature_label = QLabel(self)
        initial_temperature_label.setText('Initial temperature')
        initial_temperature_label.setFont(QFont('Arial', 10))
        initial_temperature_label.move(20,yi)

        final_time_label = QLabel(self)
        final_time_label.setText('Final time')
        final_time_label.setFont(QFont('Arial', 10))
        final_time_label.move(20,yi + n)

        delta_temp_label = QLabel(self)
        delta_temp_label.setText('Delta Temp')
        delta_temp_label.setFont(QFont('Arial', 10))
        delta_temp_label.move(20,yi + 2*n)

        p_label = QLabel(self)
        p_label.setText('P')
        p_label.setFont(QFont('Arial', 10))
        p_label.move(20,yi + 3*n)
        #-------------------------------------------------------------
        self.initial_temperature_input = QLineEdit(self)
        self.initial_temperature_input.resize(100,24)
        self.initial_temperature_input.move(100,yi)

        self.final_time_input = QLineEdit(self)
        self.final_time_input.resize(100,24)
        self.final_time_input.move(100,yi + n)

        self.delta_temp_input = QLineEdit(self)
        self.delta_temp_input.resize(100,24)
        self.delta_temp_input.move(100,yi + 2*n)

        self.p_input = QLineEdit(self)
        self.p_input.resize(100,24)
        self.p_input.move(100,yi + 3*n)

        #-------------------------------------------------------------
        '''
        password_label = QLabel(self)
        password_label.setText('password')
        password_label.setFont(QFont('Arial', 10))
        password_label.move(20,86)

        self.checkViewPassword = QCheckBox(self)
        self.checkViewPassword.setText('Ver contrasena')
        self.checkViewPassword.move(100,110)
        self.checkViewPassword.clicked.connect(self.mostrarContrasena)

        loginButton = QPushButton(self)
        loginButton.setText('Login')
        loginButton.resize(320,35)
        loginButton.move(40,140)
        loginButton.clicked.connect(self.iniciarMainView)

        registerButton = QPushButton(self)
        registerButton.setText('Registrarse')
        registerButton.resize(320,35)
        registerButton.move(40,1100)
        registerButton.clicked.connect(self.registrarUsuario)
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    interfaz = crystalGUI()
    sys.exit(app.exec())
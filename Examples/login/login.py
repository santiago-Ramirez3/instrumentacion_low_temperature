import sys
from newRegistro import RegistrarUsuarioView
from mainwindow import mainWindow
from PyQt6.QtWidgets import (QApplication,
                             QWidget, QLabel, QLineEdit,QPushButton,
                             QMessageBox, QCheckBox)

from PyQt6.QtGui import QFont, QPixmap

class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setGeometry(0,0,380,250)
        self.setWindowTitle('Login')
        self.generarFormulario()
        self.show()
    
    def generarFormulario(self):
        self.is_logged = False

        user_label = QLabel(self)
        user_label.setText('Usuario')
        user_label.setFont(QFont('Arial', 10))
        user_label.move(20,54)

        self.user_input = QLineEdit(self)
        self.user_input.resize(250,24)
        self.user_input.move(90,50)

        password_label = QLabel(self)
        password_label.setText('password')
        password_label.setFont(QFont('Arial', 10))
        password_label.move(20,86)

        self.password_input = QLineEdit(self)
        self.password_input.resize(250,24)
        self.password_input.move(90,82)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.checkViewPassword = QCheckBox(self)
        self.checkViewPassword.setText('Ver contrasena')
        self.checkViewPassword.move(90,110)
        self.checkViewPassword.toggled.connect(self.mostrarContrasena)

        print(self.checkViewPassword.toggled.connect(self.mostrarContrasena))

        loginButton = QPushButton(self)
        loginButton.setText('Login')
        loginButton.resize(320,35)
        loginButton.move(40,140)
        loginButton.clicked.connect(self.loginWindow)

        registerButton = QPushButton(self)
        registerButton.setText('Registrarse')
        registerButton.resize(320,35)
        registerButton.move(40,190)
        registerButton.clicked.connect(self.registrarUsuario)

    def mostrarContrasena(self, clicked):
        if clicked:
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

    def loginWindow(self):
        users = []
        user_path = 'usuarios.txt'
        try:
            with open(user_path, 'r') as f:
                for line in f:
                    users.append(line.strip('\n'))
            
            login_information = f'{self.user_input.text()},{self.password_input.text()}'

            if login_information in users:
                QMessageBox.information(self,'Inicio de sesión',
                                        'Inicio de seison exitoso',
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
                self.is_logged = True
                self.close()

                self.openMainWindow()
            else:
                QMessageBox.warning(self,'Error',
                                    'Usuario o constraseña invalidos',
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)
        except FileNotFoundError as e:
            QMessageBox.warning(self,'Error',
                                    f'Base de datos de usuarios no encontrada: {e}',
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)
        except Exception as e:
            QMessageBox.warning(self,'Error',
                                    f'Error en servidor: {e}',
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)


    def registrarUsuario(self):
        self.new_user_form = RegistrarUsuarioView()
        self.new_user_form.show()
    
    def openMainWindow(self):
        self.mainWindow = mainWindow()
        self.mainWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap

class RegistrarUsuarioView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)  # No interactuar con las demás ventanas
        self.generar_formulario()
    
    def generar_formulario(self):
        self.setGeometry(100,100,370,250)
        self.setWindowTitle('Formulario de registro')

        user_label = QLabel(self)
        user_label.setText('Usuario')
        user_label.setFont(QFont('Arial',10))
        user_label.move(20,44)

        self.user_input = QLineEdit(self)
        self.user_input.resize(250,24)
        self.user_input.move(110,40)

        password_1_label = QLabel(self)
        password_1_label.setText('password')
        password_1_label.setFont(QFont('Arial', 10))
        password_1_label.move(20,74)

        self.password_1_input = QLineEdit(self)
        self.password_1_input.resize(250,24)
        self.password_1_input.move(110,70)
        self.password_1_input.setEchoMode(QLineEdit.EchoMode.Password)

        password_2_label = QLabel(self)
        password_2_label.setText('Confirm password')
        password_2_label.setFont(QFont('Arial', 10))
        password_2_label.move(20,104)

        self.password_2_input = QLineEdit(self)
        self.password_2_input.resize(250,24)
        self.password_2_input.move(110,100)
        self.password_2_input.setEchoMode(QLineEdit.EchoMode.Password)

        create_buttom = QPushButton(self)
        create_buttom.setText('Crear usuario')
        create_buttom.resize(150,32)
        create_buttom.move(20,170)
        create_buttom.clicked.connect(self.crearUsuario)

        cancel_buttom = QPushButton(self)
        cancel_buttom.setText('Cancelar')
        cancel_buttom.resize(150,32)
        cancel_buttom.move(170,170)
        cancel_buttom.clicked.connect(self.cancelarRegistro)

    def cancelarRegistro(self):
        self.close()
    
    def crearUsuario(self):
        usersPath = 'usuarios.txt'
        usuario = self.user_input.text()
        password1 = self.password_1_input.text()
        password2 = self.password_2_input.text()

        if password1 == '' or password2 == '' or usuario == '':
            QMessageBox.warning(self, 'Error',
                                'Ingresar datos válidos',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        elif password1 != password2:
            QMessageBox.warning(self, 'Error',
                                'Contraseñas no coinciden',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        else:
            try:
                with open(usersPath, 'a+') as f:
                    f.write(f'{usuario},{password1}\n')
                QMessageBox.information(self, 'Registro exitoso',
                                        'Usuario creado correctamente',
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
                self.close()
            except FileNotFoundError as e:
                QMessageBox.warning(self, 'Error',
                                    f'La  base de datos de usuario no existe:{e}',
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout)
import sys

class mainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setMinimumWidth(600)
        self.setFixedHeight(80)
        self.setWindowTitle('Layout horizontal')
        self.generarFormulario()
        self.show()
    
    def generarFormulario(self):

        emailLabel = QLabel('Correo electronico')
        emailInput = QLineEdit()
        sendButton = QPushButton('Enviar')
        layout = QHBoxLayout()
        layout.addWidget(emailLabel)
        layout.addWidget(emailInput)
        layout.addWidget(sendButton)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())

from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox)
import sys

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setMinimumHeight(500)
        self.setFixedWidth(200)
        self.setWindowTitle('Vertical layout')
        self.generarFormulario()
        self.show()
    
    def generarFormulario(self):
        
        boton1 = QPushButton('Boton numero 1')
        boton2 = QPushButton('Boton numero 2')
        boton3 = QPushButton('Boton numero 3')
        boton4 = QPushButton('Boton numero 4')

        boton1.clicked.connect(self.imprimirNombreBoton)
        boton2.clicked.connect(self.imprimirNombreBoton)
        boton3.clicked.connect(self.imprimirNombreBoton)
        boton4.clicked.connect(self.imprimirNombreBoton)

        layout = QVBoxLayout()
        layout.addWidget(boton1)
        layout.addWidget(boton2)
        layout.addWidget(boton3)
        layout.addWidget(boton4)

        self.setLayout(layout)
    
    def imprimirNombreBoton(self):
        boton = self.sender()
        QMessageBox.information(self,'Boton apromido',
                                f'Oprimio el {boton.text()}',
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())
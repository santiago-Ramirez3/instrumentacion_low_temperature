from PyQt6.QtWidgets import (QDialog, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap

class mainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.inicializarGUI()
    
    def inicializarGUI(self):
        self.setGeometry(100,100,500,500)
        self.setWindowTitle('Ventana principal')
        self.generarContenido()
    
    def generarContenido(self):
        image_path = 'Capacitor.png'
        try:
            with open(image_path):
                image_label = QLabel(self)
                image_label.setPixmap(QPixmap(image_path))
        except FileNotFoundError as e:
            QMessageBox.warning(self, 'Error',
                                f'Imagen no encontrada: {e}',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        except Exception as e:
            QMessageBox.warning(self, 'Error',
                                f'Error en el servidor: {e}',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
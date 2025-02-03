import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QPushButton,
                             QDateEdit,
                             QLineEdit,
                             QComboBox,
                             QFormLayout,
                             QHBoxLayout,
                             QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate

class formulario(QWidget):
    def __init__(self):
        super().__init__()
        self.inicialziarUI()
    
    def inicialziarUI(self):
        self.setGeometry(100,100,200,600)
        self.setWindowTitle('Form layout')
        self.crear_formulario()
        self.show()
    
    def crear_formulario(self):
        titulo = QLabel('Solicitud de datos')
        titulo.setFont(QFont('Arial',18))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.nombre_edit = QLineEdit()
        self.nombre_edit.setPlaceholderText('Nombre')
        self.apellido_edit = QLineEdit()
        self.apellido_edit.setPlaceholderText('Apellido')

        self.genero_selection = QComboBox()
        self.genero_selection.addItems(['Masculino','Femenino'])

        self.fecha_nacimiento_edit = QDateEdit()
        self.fecha_nacimiento_edit.setDisplayFormat('yyyy-MM-dd')
        self.fecha_nacimiento_edit.setMaximumDate(QDate.currentDate())
        self.fecha_nacimiento_edit.setCalendarPopup(True)
        self.fecha_nacimiento_edit.setDate(QDate.currentDate())

        self.telefono = QLineEdit()
        self.telefono.setPlaceholderText('3xx xxx xxxx')

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.mostrar_info)
        submit_button.setMinimumWidth(300)
        submit_button.setMaximumWidth(500)
        #----------------------------------------------------------------
        primer_h_box = QHBoxLayout()
        primer_h_box.addWidget(self.nombre_edit)
        primer_h_box.addWidget(self.apellido_edit)

        vacio = QLabel('')
        button_h_box = QHBoxLayout()
        button_h_box.addWidget(vacio)
        button_h_box.addWidget(submit_button)
        button_h_box.addWidget(vacio)
        #----------------------------------------------------------------
        main_form = QFormLayout()
        main_form.addRow(titulo)
        main_form.addRow('Nombre: ', primer_h_box)
        main_form.addRow('Genero: ', self.genero_selection)
        main_form.addRow('Fecha: ',self.fecha_nacimiento_edit)
        main_form.addRow('Telefono: ', self.telefono)
        main_form.addRow(button_h_box)

        self.setLayout(main_form)
        #----------------------------------------------------------------
    
    def mostrar_info(self):
        QMessageBox.information(self,
                                'informacion',
                                f'Nombre: {self.nombre_edit.text()} {self.apellido_edit.text()}\n \
Genero: {self.genero_selection.currentText()}\n \
fehca: {self.fecha_nacimiento_edit.text()}\n \
telefono {self.telefono.text()}\n',
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = formulario()
    sys.exit(app.exec())
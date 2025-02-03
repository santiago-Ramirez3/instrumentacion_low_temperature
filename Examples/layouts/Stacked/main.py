import sys
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QPushButton,
                             QTextEdit,
                             QDateEdit,
                             QLineEdit,
                             QComboBox,
                             QFormLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QStackedLayout,
                             QMessageBox)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
    
    def initialize_ui(self):
        self.setFixedSize(500, 580)
        self.setWindowTitle('QStackedLayout')
        self.generate_window()
        self.show()
    
    def generate_window(self):
        boton_1 = QPushButton('ventana 1')
        boton_1.clicked.connect(self.change_window)
        boton_2 = QPushButton('ventana 2')
        boton_2.clicked.connect(self.change_window)
        boton_3 = QPushButton('ventana 3')
        boton_3.clicked.connect(self.change_window)

        grupo_botones = QHBoxLayout()
        grupo_botones.addWidget(boton_1)
        grupo_botones.addWidget(boton_2)
        grupo_botones.addWidget(boton_3)

        # Pagina 1
        title1 = QLabel('Mapa')
        title1.setFont(QFont('Arial', 18))
        title1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_map = QLabel()
        pixmap = QPixmap('images/mapa.jpg')
        image_map.setPixmap(pixmap)

        window_size = self.size()
        image_map.setMaximumSize(window_size)
        image_map.setScaledContents(True)

        page1_layout = QVBoxLayout()
        page1_layout.addWidget(title1)
        page1_layout.addWidget(image_map)

        container_1 = QWidget()
        container_1.setLayout(page1_layout)

        #==================================================================
        # Pagina 2
        titulo2 = QLabel('Solicitud de datos')
        titulo2.setFont(QFont('Arial',18))
        titulo2.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        #----------------------------------------------------------------
        primer_h_box = QHBoxLayout()
        primer_h_box.addWidget(self.nombre_edit)
        primer_h_box.addWidget(self.apellido_edit)
        #----------------------------------------------------------------
        main_form = QFormLayout()
        main_form.addRow(titulo2)
        main_form.addRow('Nombre: ', primer_h_box)
        main_form.addRow('Genero: ', self.genero_selection)
        main_form.addRow('Fecha: ',self.fecha_nacimiento_edit)
        main_form.addRow('Telefono: ', self.telefono)
        main_form.addRow(submit_button)

        self.setLayout(main_form)
        #----------------------------------------------------------------
        container_2 = QWidget()
        container_2.setLayout(main_form)
        #==================================================================
        # Pagina 3
        title3 = QLabel('Observaciones')
        title3.setFont(QFont('Arial',18))
        title3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.observations = QTextEdit()
        form_3 = QFormLayout()
        form_3.addRow(title3)
        form_3.addRow('observations', self.observations)

        container_3 = QWidget()
        container_3.setLayout(form_3)
        #==================================================================

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(container_1)
        self.stacked_layout.addWidget(container_2)
        self.stacked_layout.addWidget(container_3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grupo_botones)
        main_layout.addLayout(self.stacked_layout)
        self.setLayout(main_layout)

    def change_window(self):
        button = self.sender()  # Acceder al objeto que está llamando el metodo
        if button.text().lower() == 'ventana 1':
            self.stacked_layout.setCurrentIndex(0)
        elif button.text().lower() == 'ventana 2':
            self.stacked_layout.setCurrentIndex(1)
        elif button.text().lower() == 'ventana 3':
            self.stacked_layout.setCurrentIndex(2)

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
    window = MainWindow()
    sys.exit(app.exec())
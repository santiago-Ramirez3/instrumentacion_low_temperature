import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton, QGridLayout)
import operator

operation = {'+':operator.add,
             '-':operator.sub,
             '*':operator.mul,
             '/':operator.truediv}

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.primer_valor = ''
        self.segundo_valor = ''
        self.operador = ''
        self.pointer_flag = '1'
        self.after_equal = False
        self.after_operator = False

    def inicializarUI(self):
        self.setGeometry(100,100,600,400)
        self.setWindowTitle('Calculadora')
        self.generarInterfaz()
        self.show()
    
    def generarInterfaz(self):
        self.pantalla = QTextEdit()
        self.pantalla.setDisabled(True)

        num1 = QPushButton('1')
        num2 = QPushButton('2')
        num3 = QPushButton('3')
        num4 = QPushButton('4')
        num5 = QPushButton('5')
        num6 = QPushButton('6')
        num7 = QPushButton('7')
        num8 = QPushButton('8')
        num9 = QPushButton('9')
        nump = QPushButton('.')
        num0 = QPushButton('0')
        num00 = QPushButton('00')

        num1.clicked.connect(self.ingresar_datos)
        num2.clicked.connect(self.ingresar_datos)
        num3.clicked.connect(self.ingresar_datos)
        num4.clicked.connect(self.ingresar_datos)
        num5.clicked.connect(self.ingresar_datos)
        num6.clicked.connect(self.ingresar_datos)
        num7.clicked.connect(self.ingresar_datos)
        num8.clicked.connect(self.ingresar_datos)
        num9.clicked.connect(self.ingresar_datos)
        nump.clicked.connect(self.ingresar_datos)
        num0.clicked.connect(self.ingresar_datos)
        num00.clicked.connect(self.ingresar_datos)

        #-------------------------------------------------------

        suma = QPushButton('+')
        resta = QPushButton('-')
        multiplicacion = QPushButton('*')
        division = QPushButton('/')

        suma.clicked.connect(self.insertar_operador)
        resta.clicked.connect(self.insertar_operador)
        multiplicacion.clicked.connect(self.insertar_operador)
        division.clicked.connect(self.insertar_operador)

        #-------------------------------------------------------

        igual = QPushButton('=')
        ce = QPushButton('CE')
        borrar = QPushButton('<--')

        igual.clicked.connect(self.calcular_operacion)
        ce.clicked.connect(self.borrar_todo)
        borrar.clicked.connect(self.borrado_parcial)

        #-------------------------------------------------------

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.pantalla,0,0,2,4)
        self.mainLayout.addWidget(ce,2,0,1,2)
        self.mainLayout.addWidget(borrar,2,2)
        self.mainLayout.addWidget(suma,2,3)

        self.mainLayout.addWidget(num7,3,0)
        self.mainLayout.addWidget(num8,3,1)
        self.mainLayout.addWidget(num9,3,2)
        self.mainLayout.addWidget(division,3,3)

        self.mainLayout.addWidget(num4,4,0)
        self.mainLayout.addWidget(num5,4,1)
        self.mainLayout.addWidget(num6,4,2)
        self.mainLayout.addWidget(multiplicacion,4,3)

        self.mainLayout.addWidget(num1,5,0)
        self.mainLayout.addWidget(num2,5,1)
        self.mainLayout.addWidget(num3,5,2)
        self.mainLayout.addWidget(resta,5,3)

        self.mainLayout.addWidget(num0,6,0)
        self.mainLayout.addWidget(num00,6,1)
        self.mainLayout.addWidget(nump,6,2)
        self.mainLayout.addWidget(igual,6,3)

        self.setLayout(self.mainLayout)
    
    def ingresar_datos(self):
        boton_text = self.sender().text()
        if self.after_equal:
            self.primer_valor = ''
            self.pantalla.setText(self.primer_valor)
            self.after_equal = False
            self.pointer_flag = '1'

        if self.pointer_flag == '1':
            self.primer_valor += boton_text
            self.pantalla.setText(self.primer_valor)
            
        else:
            self.segundo_valor += boton_text
            self.pantalla.setText(self.pantalla.toPlainText() + boton_text)
    
    def insertar_operador(self):
        self.operador = self.sender().text()
        self.pointer_flag = '2'
        self.pantalla.setText(self.pantalla.toPlainText() + ' ' + self.operador + ' ')
        self.after_operator = True
    
    def borrar_todo(self):
        self.primer_valor = ''
        self.segundo_valor = ''
        self.operador = ''
        self.pointer_flag = '1'
        self.after_equal = False
        self.after_operator = False

        self.pantalla.setText('')
    
    def borrado_parcial(self):
        if self.after_equal:
            self.borrar_todo()
        
        elif self.pointer_flag == '1':
            self.primer_valor = self.primer_valor[:-1]
            self.pantalla.setText(self.primer_valor)
        
        elif self.pointer_flag == '2':
            self.segundo_valor = self.segundo_valor[:-1]
            self.pantalla.setText(self.segundo_valor)
    
    def calcular_operacion(self):
        resultado = str(operation[self.operador](float(self.primer_valor),float(self.segundo_valor)))
        self.pantalla.setText(resultado)
        self.primer_valor = resultado
        self.segundo_valor = ''
        self.after_equal = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())
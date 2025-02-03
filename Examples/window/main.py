import sys

from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QStatusBar,
                             QWidget,
                             QFileDialog,
                             QVBoxLayout,
                             QTextEdit)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import QStandardPaths

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet('background-color:white;')
        self.initialize_ui()
    
    def initialize_ui(self):
        self.setGeometry(100,100,500,500)
        self.setWindowTitle('QMainWindow')
        self.generate_window()
        self.show()

    def generate_window(self):
        self.create_action()
        self.create_menu()
        self.create_content()
    
    def create_content(self):
        layout = QVBoxLayout()
        self.editor_text = QTextEdit()
        layout.addWidget(self.editor_text)
        layout.setContentsMargins(30,30,30,30)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def create_action(self):
        self.open_action = QAction('Abrir', self)
        self.open_action.setShortcut(QKeySequence('Ctrl+O'))
        self.open_action.setStatusTip('Abrir archivos')
        self.open_action.triggered.connect(self.open)

        self.save_action = QAction('Guardar', self)
        self.save_action.setShortcut(QKeySequence('Ctrl+S'))
        self.save_action.setStatusTip('Guardar archivos')
        self.save_action.triggered.connect(self.save)

        self.export_action = QAction('Exportar', self)
        self.export_action.setShortcut(QKeySequence('Ctrl+E'))
        self.export_action.setStatusTip('Exportar archivos')
        self.export_action.triggered.connect(self.export)

        self.undo_action = QAction('Deshacer', self)
        self.undo_action.setShortcut(QKeySequence('Ctrl+Z'))
        self.undo_action.setStatusTip('Deshacer cambios')
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction('Rehacer', self)
        self.redo_action.setShortcut(QKeySequence('Ctrl+Y'))
        self.redo_action.setStatusTip('Rehacer cambios')
        self.redo_action.triggered.connect(self.redo)
    
    def create_menu(self):
        menu_archivo = self.menuBar().addMenu('Archivo')
        menu_archivo.addAction(self.open_action)
        menu_archivo.addAction(self.save_action)
        menu_archivo.addAction(self.export_action)

        menu_edit = self.menuBar().addMenu('Editar')
        menu_edit.addAction(self.undo_action)
        menu_edit.addAction(self.redo_action)
    #----------------------------------------------------------------------
    def open(self):
        options = (QFileDialog.Option.DontUseNativeDialog) # Escoger el estilo de ventana
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        file_types = 'Text Files (*.txt);;Imagenes (*.png);;All files (*)'
        self.file ,_ = QFileDialog.getOpenFileName(self, 'Open file', initial_dir,file_types) # el primer output es el archivo, el segundo el formato

        with open(self.file, 'r') as file:
            self.editor_text.setText(file.read())

    def save(self):
        print('Guardando archivo')

    def export(self):
        print('Exportando archivo')

    def undo(self):
        print('Deshaciendo cambios')
    
    def redo(self):
        print('Rehaciendo cambios')
    #----------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
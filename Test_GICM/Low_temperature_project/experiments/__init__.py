from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout,
    QComboBox, QMenuBar, QStatusBar, QSplitter, QFrame, QLineEdit, QPushButton
)

class Experimetn:
    def __init__(self, instruments_list:list,
                 starting_criteria:bool,
                 end_criteria:bool,
                 experimental_protocol,
                 saving_path:str):
        
        self.instruments_list = instruments_list
        self.starting_criteria = starting_criteria
        self.end_criteria = end_criteria
        self.saving_path = saving_path
        self.experiment_protocol = experimental_protocol
        #-----------------------------------------------------
        self.connectedInstruments = []
        #-----------------------------------------------------
    
    def updateConnectedInstruments(self, currentInstruments:list):
        self.connectedInstruments = currentInstruments

    def createWidget(self, tabWidget:QTabWidget, currentInstruments:list):
        self.updateConnectedInstruments(currentInstruments)
        self.experimentWidget = QWidget()

        self.leftWidget = QWidget()

        self.form = QFormLayout()

        for ins in self.instruments_list:
            combo = QComboBox()

            for conIns in self.connectedInstruments:
                #print(conIns)
                if type(ins) == type(conIns):
                    combo.addItem(conIns)

            self.form.addRow(ins.instrumentClass, combo)
        
        self.experimentWidget.setLayout(self.form)

        tabWidget.addTab(self.experimentWidget, 'Experimento test')

    def start_experiment(self):
        if self.starting_criteria:
            while not self.end_criteria:
                self.experiment_protocol()
        
        else:
            print('Starting criteria is not satisfied')
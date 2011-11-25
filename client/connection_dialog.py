# -*- coding: utf-8 -*-

from PyQt4.QtGui import *

class ConnectionDialog(QWidget):
    
    def __init__(self, clientApp):
        super(ConnectionDialog, self).__init__()
        
        self.clientApp = clientApp
        
        self.initUI()
        
    def initUI(self):
        serverLabel = QLabel('Serwer:')
        portLabel = QLabel('Port:')
        
        serverEdit = QLineEdit()
        serverEdit.setText(self.clientApp.ws_server)
        serverEdit.textChanged.connect(self.setServerName)
        serverEdit
        
        portSpin = QSpinBox()
        portSpin.setMinimum(1)
        portSpin.setMaximum(100000)
        portSpin.setValue(self.clientApp.ws_port)
        portSpin.valueChanged.connect(self.setServerPort)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(serverLabel, 1, 0)
        grid.addWidget(serverEdit, 1, 1)
        
        grid.addWidget(portLabel, 2, 0)
        grid.addWidget(portSpin, 2, 1)
        
        okButton = QPushButton("OK")
        closeButton = QPushButton("Zamknij")
        
        okButton.clicked.connect(self.reconnect)
        closeButton.clicked.connect(self.closeApp)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(closeButton)
        
        grid.addLayout(hbox, 3, 1)
        
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 120)
        self.setWindowTitle('Forum Tracker - Opcje polaczenia')      
    
        self.show()
    
    def closeApp(self):
        self.close()
        
    def reconnect(self):
        self.hide()
        
        self.clientApp.tryConnect()
        
    def setServerName(self):
        self.clientApp.ws_server = self.sender().text()
        
    def setServerPort(self):
        self.clientApp.ws_port = self.sender().value()

# -*- coding: utf-8 -*-


"""
Copyright (c) 2011, GrupaZP
 All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


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

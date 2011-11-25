# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtCore import *

class MainForm(QWidget):
    
    def __init__(self, clientApp):
        super(MainForm, self).__init__()
        
        self.clientApp = clientApp
        self.askGoogle = ''
        
        self.initUI()
        
    def initUI(self):
        
        askGoogleLabel = QLabel('Zapytaj Google:')
        
        askGoogleEdit = QLineEdit()
        askGoogleEdit.textChanged.connect(self.setAskGoogle)
        
        askGoogleButton = QPushButton('Szukaj')
        askGoogleButton.clicked.connect(self.doAskGoogle)
        
        linksLabel = QLabel('Wybierz forum do wyswietlenia:')
        
        self.linksList = QListWidget()
        self.linksList.itemSelectionChanged.connect(self.showForum)
        
        self.webView = QWebView()
        self.webView.load(QUrl("http://google.pl"))
        self.webView.show()
        # Nie chcemy robic przegladarki
        self.webView.setEnabled(False)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(askGoogleLabel, 1, 0)
        grid.addWidget(askGoogleEdit, 1, 1)
        grid.addWidget(askGoogleButton, 1, 2)
        
        grid.addWidget(linksLabel, 2, 0)
        grid.addWidget(self.linksList, 2, 1, 1, 2)
        
        grid.addWidget(self.webView, 3, 0, 10, 3)
        
        self.setLayout(grid)
        self.setGeometry(300, 300, 700, 650)
        self.setWindowTitle('Forum Tracker')      
    
        self.show()
        
    def setAskGoogle(self):
        self.askGoogle = self.sender().text()
        
    def doAskGoogle(self):
        # Uwaga! Wszystkie teksty pobierane z QLineEdit maja typ QString, a nie string!
        links = self.clientApp.askGoogle(str(self.askGoogle))
        
        # Najpierw czyscimy liste
        self.linksList.clear()
        
        for link in links:
            self.linksList.addItem(QListWidgetItem(link))
        
    def showForum(self):
        self.webView.load(QUrl(str(self.linksList.currentItem().text())))
        self.webView.setEnabled(True)



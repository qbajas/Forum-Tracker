# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from main_form import MainForm
from connection_dialog import ConnectionDialog

class Gui:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash = None
        self.app.processEvents()
        self.firstRun = True
    
    def display_splash_screen(self):
        # pokazujemy okienko do ladowania
        if self.splash == None:
            pixmap = QPixmap('splash.png')
            
            self.splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
            self.splash.setMask(pixmap.mask())
            
        self.splash.show()
    
    def close_splash_screen(self):
        # zamkniecie splasha powoduje jednoczesnie pokazanie glownego gui
        self.form.show()
        self.splash.finish(self.form)
        
        if self.firstRun == True:
            self.firstRun = False
            
            self.app.exec_()
    
    def display_connection_dialog(self, clientApp):
        # pokazujemy okno do zmiany danych o polaczeniu
        self.form = ConnectionDialog(clientApp)
        
        self.close_splash_screen()
        
    def display_main_form(self, clientApp):
        self.form = MainForm(clientApp)
        
        self.close_splash_screen()

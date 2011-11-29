# -*- coding: utf-8 -*-


"""
Copyright (c) 2011, GrupaZP
 All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from main_form import MainForm
from connection_dialog import ConnectionDialog

class Gui:
"""Klasa obsługująca interfejs graficzny"""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash = None
        self.app.processEvents()
        self.firstRun = True
    
    def display_splash_screen(self):
	"""Pokazuje splash screen"""
        # pokazujemy okienko do ladowania
        if self.splash == None:
            pixmap = QPixmap('splash.png')
            
            self.splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
            self.splash.setMask(pixmap.mask())
            
        self.splash.show()
    
    def close_splash_screen(self):
	"""Zamyka splash-screen i pokazuje główny element GUI"""
        # zamkniecie splasha powoduje jednoczesnie pokazanie glownego gui
        self.form.show()
        self.splash.finish(self.form)
        
        if self.firstRun == True:
            self.firstRun = False
            
            self.app.exec_()
    
    def display_connection_dialog(self, clientApp):
	"""Wyświetla okno do zmiany konfiguracji połączenia"""
        # pokazujemy okno do zmiany danych o polaczeniu
        self.form = ConnectionDialog(clientApp)
        
        self.close_splash_screen()
        
    def display_main_form(self, clientApp):
        self.form = MainForm(clientApp)
        
        self.close_splash_screen()

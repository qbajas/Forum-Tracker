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
from PyQt4.QtWebKit import *
from PyQt4.QtCore import *


class MainForm(QWidget):
    """Główny interfejs aplikacji"""
    def __init__(self, clientApp):
        super(MainForm, self).__init__()
        
        self.clientApp = clientApp
        self.askGoogle = ''
        
        self.initUI()
        
    def initUI(self):
        """Inicjalizacja interfejsu"""
        askGoogleLabel = QLabel('Zapytaj Google:')
        
        askGoogleEdit = QLineEdit()
        askGoogleEdit.textChanged.connect(self.setAskGoogle)
        
        askGoogleButton = QPushButton('Szukaj')
        askGoogleButton.clicked.connect(self.doAskGoogle)
        
        linksLabel = QLabel(u'Wybierz forum do wyświetlenia:')
        
        self.linksList = QListWidget()
        self.linksList.itemSelectionChanged.connect(self.showForum)
        
        self.webView = QWebView()
        self.webView.load(QUrl("http://google.pl"))
        self.webView.show()
        # Nie chcemy robic przegladarki
        self.webView.setEnabled(False)
        
        plotLabel = QLabel(u'Historia aktywności:')
        self.plot = QGraphicsView()
        self.plot.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(askGoogleLabel, 1, 0)
        grid.addWidget(askGoogleEdit, 1, 1)
        grid.addWidget(askGoogleButton, 1, 2)
        
        grid.addWidget(linksLabel, 2, 0)
        grid.addWidget(self.linksList, 2, 1, 1, 2)
        
        grid.addWidget(self.webView, 3, 0, 10, 3)
        grid.addWidget(plotLabel, 14, 0)
        grid.addWidget(self.plot, 14, 1, 1, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 700, 850)
        self.setWindowTitle('Forum Tracker')      
    
        self.show()
        
    def setAskGoogle(self):
        self.askGoogle = self.sender().text()
        
    def doAskGoogle(self):
        self.linksList.clear()
        self.linksList.addItem(QListWidgetItem('Wczytywanie...'))
        #rozłączamy slot na czas ładowania (zapobiega różnym dziwnym rzeczom ;))
        self.linksList.itemSelectionChanged.disconnect(self.showForum)
        self.thread = AskThread(self.clientApp, unicode(self.askGoogle))
        self.thread.finished.connect(self.getAskResults)

        self.thread.start()
        
        
    def drawStats(self):
        """Rysuje wykres aktywnośći na podstawie statystyk"""
        num = self.linksList.currentRow() #numer wybranego linka
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, self.plot.width() - 10, self.plot.height() - 10)

        if len(self.linkstats[num][1]) > 1:
            firstY = self.linkstats[num][1][0][0] / 2.3 * scene.height() #pierwszy punkt
            path = QPainterPath(QPointF(0, firstY))
            #odległość między kolejnymi punktami (na osi X)
            delta = scene.width() / (len(self.linkstats[num][1]) - 1)
            x = 0.0
            #rysowanie wykresu
            for stat in self.linkstats[num][1]:
                y = stat[0] / 2.3 * scene.height()
                path.lineTo(x, y)
                x = x + delta
            sceneItem = scene.addPath(path, QPen(QBrush(Qt.blue), 2))
            #ustawienie wykresu na QGraphicsScene
            sceneItem.scale(1,-1)
            sceneItem.translate(0, -scene.height())
        else: #jeśli jest tylko jedna ocena to nie ma z czego rysować wykresu
            textItem = scene.addText("Brak historii")
            textItem.setPos(scene.width()/2 - textItem.boundingRect().width()/2, 
                            scene.height()/2 - textItem.boundingRect().height()/2)
        self.plot.setScene(scene)

       
    def showForum(self):
        self.webView.load(QUrl(str(self.linksList.currentItem().text())))
        self.webView.setEnabled(True)
        self.drawStats()


    def getAskResults(self, results):
        """Slot wywoływany po zakończeniu pracy wątku AskThread (po pobraniu wyników)"""
        self.linkstats = results
        # Uwaga! Wszystkie teksty pobierane z QLineEdit maja typ QString, a nie string!

        # Najpierw czyscimy liste
        self.linksList.clear()

        for link in self.linkstats:
            self.linksList.addItem(QListWidgetItem(link[0]))
        
        self.linksList.itemSelectionChanged.connect(self.showForum)

#Wątek do pobierania rezultatów w tle
class AskThread(QThread):
    finished = pyqtSignal(list)
    
    def __init__(self, clientApp, topic):
        super(AskThread, self).__init__()
        self.topic = topic
        self.client = clientApp
#        self.finished.connect(main_form.getAskResults)

    def run(self):
        result = self.client.askGoogle(self.topic)
        self.finished.emit(result)
        

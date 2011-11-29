#!/usr/bin/python


"""
Copyright (c) 2011, GrupaZP
 All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


# -*- coding: utf-8 -*-

from websocket import create_connection
import pickle

import time, os, socket

from gui import Gui

class Client:
"""Główna klasa klienta"""
	def __init__(self):
		#self.ws_server = 'users.agh.edu.pl'
		self.ws_server = 'users.dsnet.agh.edu.pl'
		self.ws_port = 10001
		
		self.gui = Gui()
		
		self.tryConnect()
		
	def tryConnect(self):
	"""Połączenie z domyślnym serwerem."""
		try:
			self.gui.display_splash_screen()
			
			print "ws://%s:%s" % (self.ws_server, self.ws_port)
			
			self.ws = create_connection("ws://%s:%s" % (str(self.ws_server), self.ws_port))
			
			self.gui.display_main_form(self)
		except socket.error:
			# jezeli nie mozesz sie polaczyc, to niech wpisze inne dane
			self.gui.display_connection_dialog(self)
	
	def askGoogle(self, topic):
	"""Wysłanie zapytania do serwera"""
		self.ws.send('askGoogle###' + topic)
		
		print "Sent: '%s'\n" % topic
		
		result =  self.ws.recv()
		
		print "Received\n"# % result
		
		# lista linkow w formacie (link, [(ocena, data), ...])
		return pickle.loads(result)
		
	
	def getSections(self):
		linkNo = raw_input("Pokaż tematy dla forum (wybierz numer linka): \n>>> ")
		try:
			int(linkNo)
			
			self.ws.send('getSections###'+linkNo)
			print "Sent: '%s'\n" % linkNo
			
			result =  self.ws.recv()
			
			print "Received: '%s'\n" % result
		except ValueError:
			print "Cza było wybrać numer"
	
	def close(self):
		self.ws.close()
		exit()

def print_msg(message,next,obj):
	print(message)
	next(obj)
		
if __name__ == "__main__":
	client = Client()

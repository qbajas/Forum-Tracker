#!/usr/bin/python
# -*- coding: utf-8 -*-

from websocket import create_connection
import pickle

import time, os, socket

from gui import Gui

class Client:
	def __init__(self):
		#self.ws_server = 'users.agh.edu.pl'
		self.ws_server = 'users.dsnet.agh.edu.pl'
		self.ws_port = 10001
		
		self.gui = Gui()
		
		self.tryConnect()
		
	def tryConnect(self):
		try:
			self.gui.display_splash_screen()
			
			print "ws://%s:%s" % (self.ws_server, self.ws_port)
			
			self.ws = create_connection("ws://%s:%s" % (str(self.ws_server), self.ws_port))
			
			self.gui.display_main_form(self)
		except socket.error:
			# jezeli nie mozesz sie polaczyc, to niech wpisze inne dane
			self.gui.display_connection_dialog(self)
	
	def askGoogle(self, topic):
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

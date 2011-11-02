#!/usr/bin/python
# -*- coding: utf-8 -*-

from websocket import create_connection
import time, os


class Client:
	def __init__(self):
		self.ws = create_connection("ws://users.dsnet.agh.edu.pl:10001")
		print "Połączono z serwerem!\n"
		
	def askGoogle(self):
		topic = raw_input("Chciałbym zapytać o: \n>>> ")
		os.system("clear")
		self.ws.send('askGoogle###' + topic)
		print "Sent: '%s'\n" % topic
		result =  self.ws.recv()
		print "Received:\n%s\n" % result

	def getSections(self):
		linkNo = raw_input("Pokaż tematy dla forum (wybierz numer linka): \n>>> ")
		try:
			int(linkNo)
			os.system("clear")
			self.ws.send('getSections###'+linkNo)
			print "Sent: '%s'\n" % linkNo
			result =  self.ws.recv()
			print "Received: '%s'\n" % result
		except ValueError:
			print "Cza było wybrać numer"
	
	def close(self):
		self.ws.close()
		exit()

	def showMenu(self):
		print "-------------------------------------------\n"
		print "0 - koniec\n1 - nowa wiadomość\n"
		print "-------------------------------------------\n"
		option = raw_input("Twoj wybor: ")
		#return option
		if (option.isdigit() and int(option) in range(0,2)):
			os.system("clear")
			f = {
			'0' : self.close,
			'1' : self.showMes,
			}.get(option)()
		else: print_msg("Wybrano niepoprawną opcję (wybieraj z zakresu 0-1)\n",showMenu,obj)
	
	def showMes(self):
		print "-------------------------------------------\n"
		print "0 - koniec\n1 - Zapytaj Google'a\n2 - Pobierz tematy\n"
		print "-------------------------------------------\n"
		option = raw_input("Twoj wybor: ")
		#return option
		if (option.isdigit() and int(option) in range(0,3)):
			os.system("clear")
			f = {
			'0' : self.close,
			'1' : self.askGoogle,
			'2' : self.getSections,
			}.get(option)()
		else: print_msg("Wybrano niepoprawną opcję (wybieraj z zakresu 0-2)\n",showMes,obj)

def print_msg(message,next,obj):
	os.system("clear")
	print(message)
	next(obj)
		
if __name__ == "__main__":
	os.system("clear")
	client = Client()
	while True:
		client.showMenu()

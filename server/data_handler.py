 # -*- coding: utf-8 -*-
""" 
Klasa obslugujaca dane
umozliwia dodawanie danych, zapis i odczyt z pliku
UZYCIE:
1. stworzenie instancji klasy
2. uzycie metody 'add_search' i 'load_search'aby cache'owac wyszukiwanie
3. uzycie metod 'add_link' i 'load_link' aby cache'owac oceny linkow
"""
# load_link zwraca listę tupli (ocena, data_wystawienia_oceny). Jeśli udałoby się to przepchnąć przez protokół sieciowy # i wyświetlić w kliecie to mamy statystyki
__version__ = "1.0"

import pickle,collections,datetime

class DataHandler:
"""Klasa do obsługi danych."""
# przy tworzeniu obiektu dane sa wczytywane z pliku
	def __init__(self):
		self.search_data = {}
		self.link_data = {}
		self.load_from_file()

# dodawanie wpisu z danymi
# parametry: slowo kluczowe, linki
#
	def add_search(self, keyword, links):
	"""Dodawanie wpisu z danymi (slowo kluczowe, linki)."""
		self.search_data[keyword] = links
		self.save_to_file()

	def add_link(self, link, rating):
	"""Dodawanie linku (link, ocena)"""
		entry = (rating, datetime.datetime.now())
		try:
			self.link_data[link].append(entry)
		except KeyError:
			self.link_data[link] = [(entry)]
		self.save_to_file()
		
# wczytywanie linkow dla slowa kluczowego	
# KeyError jesli slowa nie ma w bazie	
	def load_search(self, keyword):
	"""Wczytywanie linkow dla slowa kluczowego"""
		return self.search_data[keyword]
	
	def load_link(self, link):
	"""Wczytywanie linku"""
		return self.link_data[link]
	
# obsluga plikow	
	def save_to_file(self):
	"""Zapis do pliku"""
		f = open('datafile','w')
		pickle.dump(self.search_data,f)
		pickle.dump(self.link_data,f)
		f.close()
		
	def load_from_file(self):
	"""Odczyt pliku"""
		try:
			f = open('datafile','r')
			self.search_data = pickle.load(f)
			self.link_data = pickle.load(f)
			f.close()
		except IOError as e:
			print 'no data file found'
		
		

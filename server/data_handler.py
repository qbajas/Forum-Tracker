# klasa obslugujaca dane
# umozliwia dodawanie danych, zapis i odczyt z pliku
# UZYCIE:
# 1. stworzenie instancji klasy
# 2. uzycie metody 'add_search' i 'load_search'aby cache'owac wyszukiwanie
# 3. uzycie metod 'add_link' i 'load_link' aby cache'owac oceny linkow

import pickle,collections

class DataHandler:
# format danych (zmienna 'data'):
# slownik: klucz - link, wartosc - ocena
	
# przy tworzeniu obiektu dane sa wczytywane z pliku
	def __init__(self):
		self.search_data = {}
		self.link_data = {}
		self.load_from_file()

# dodawanie wpisu z danymi
# parametry: slowo kluczowe, linki
	def add_search(self, keyword, links):
		self.search_data[keyword] = links
		self.save_to_file()

	def add_link(self, link, rating):
		self.link_data[link] = rating
		self.save_to_file()
		
# wczytywanie linkow dla slowa kluczowego	
# KeyError jesli slowa nie ma w bazie	
	def load_search(self, keyword):
		return self.search_data[keyword]
	
	def load_link(self, link):
		return self.link_data[link]
	
# obsluga plikow	
	def save_to_file(self):
		f = open('datafile','w')
		pickle.dump(self.search_data,f)
		pickle.dump(self.link_data,f)
		f.close()
		
	def load_from_file(self):
		try:
			f = open('datafile','r')
			self.search_data = pickle.load(f)
			self.link_data = pickle.load(f)
			f.close()
		except IOError as e:
			print 'no data file found'
		
		

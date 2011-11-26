# klasa obslugujaca dane
# umozliwia dodawanie danych, zapis i odczyt z pliku
# UZYCIE:
# 1. stworzenie instancji klasy
# 2. uzycie metody 'add_entry'

import pickle,collections

class DataHandler:
# format danych (zmienna 'data'):
# slownik: klucz - slowo kluczowe, wartosc - linki
	
# przy tworzeniu obiektu dane sa wczytywane z pliku
	def __init__(self):
		self.data = {}
		self.load_from_file()

# dodawanie wpisu z danymi
# parametry: slowo kluczowe, linki
	def add_entry(self, keyword, links):
		self.data[keyword] = links
		self.save_to_file()
		
# wczytywanie linkow dla slowa kluczowego	
# KeyError jesli slowa nie ma w bazie	
	def load_links(self, keyword):
		return self.data[keyword]
	
# obsluga plikow	
	def save_to_file(self):
		f = open('datafile','w')
		pickle.dump(self.data,f)
		f.close()
		
	def load_from_file(self):
		try:
			f = open('datafile','r')
			self.data = pickle.load(f)
			f.close()
		except IOError as e:
			print 'no data file found'
		
		

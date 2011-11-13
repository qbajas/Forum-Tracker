# klasa obslugujaca dane
# umozliwia dodawanie danych, zapis i odczyt z pliku
# U¯YCIE:
# 1. stworzenie instancji klasy
# 2. uzycie metody 'add_entry'

import pickle,collections

class DataHandler:
# format danych (zmienna 'data'):
# {slowo_kluczowe, [(link1,ocena1.1,ocena1.2),(link2,ocena2.1,ocena2.2)...]} 	
# czyli: slownik, ktorego kluczami sa slowa kluczowe a wartosciami lista krotek
# zapewniona jest unikalnosc slow kluczowych
	
# przy tworzeniu obiektu dane sa wczytywane z pliku
	def __init__(self):
		self.data = collections.defaultdict(list)
		self.load_from_file()

# dodawanie wpisu z danymi
# parametry: slowo kluczowe, link, ocena1, ocena2
	def add_entry(self, keyword, link, rating1, rating2):
		self.data[keyword].append( (link,rating1, rating2) )
		self.save_to_file()
	
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
		
		
# mozliwe do zaimplementowania metody
		
	#def get_link_with_best_rating1(self, keyword)	
			
	#def get_link_with_best_rating2(self, keyword)
		
	
	
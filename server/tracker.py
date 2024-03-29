# -*- coding: utf-8 -*-
import re, BeautifulSoup, mechanize, time,urllib2, string, page_rater, pickle
from data_handler import DataHandler
from BeautifulSoup import BeautifulSoup
#from IPython.Shell import IPShellEmbed

class Tracker(object):
	def __init__(self):
		# mechanize.RobustFactory() pozwala na prawidlowe odczytywanie stron z bledami(niepozamykane znaczniki, itp.)
		self.br = mechanize.Browser(factory=mechanize.RobustFactory())
		# olewa reguły z robots.txt
		self.br.set_handle_robots(False)
		# musimy udawać prawdziwą przeglądarkę, inaczej google nas nie puści :D
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
		# inicjalizacja bazy
		self.db = DataHandler()
		
	def askGoogle(self,question):
		self.br.open('http://google.pl')
		#wybieramy sobie formularz na stronie (można wybierać też po nazwie, ale na googlach jest tylko jeden, stąd po numerku)
		self.br.select_form(nr=0)
		# probojemy zaladowac dane z bazy danych
		try:
			links = self.db.load_search(question)
		except KeyError:		
		# jesli danych nie ma w bazie to pytamy googla
			self.br.form['q'] = question + ' dyskusja' #chcemy tylko strony z dyskusją
			self.br.submit()
			#do results włazi po prostu otwarty html
			results = self.br.response().read()
			print results[string.find(results,"Około "):string.find(results, "wyników")]+"wyników:"
			#soup to obiekt gotowy do parsowania
			self.soup = BeautifulSoup(results)
			print self.soup.findAll('a', attrs={'class':'l'})
			links =   [x['href'] for x in self.soup.findAll('a', attrs={'class':'l'})]
			#druga strona wyników
			fl_tags = self.soup.findAll('a', attrs = {'class':'fl'})
			second_page = ''
			for tag in fl_tags:
				if tag.findAll(text = '2') != []:
					second_page = tag['href']
			print 'adres drugiej strony:',second_page
			self.br.open(second_page)
			self.soup = BeautifulSoup(self.br.response().read())
			links.extend([x['href'] for x in self.soup.findAll('a', attrs={'class':'l'})])
			print "\n".join(links)
			self.db.add_search(question,links)
                #wyrzucamy linki, ktore zbiorą ocenę 0.0 - raczej nie są interesujące
		links = filter(lambda url: page_rater.rate_URL(url, self.db) > 0.0, links)
		#sortujemy względem aktywności
		links.sort(key = lambda url: page_rater.rate_URL(url, self.db), reverse = True)
		print "Sorted"
		return links

	def getSerializedStats(self, links):
		return map(lambda link: pickle.dumps(self.db.load_link(link)), links)
	def getStats(self, link):
		return self.db.load_link(link)
	
	#tutaj dobrze by bylo sprawdzac, czy forum spelnia jakies tam wymagania (np. czy to phpBB)
	def openForum(self,URL):
		self.br.open(URL)
		results = self.br.response().read()
		self.soup = BeautifulSoup(results)
		return self.__getSections()
		
	def __getSections(self):
		res = []
		forumtitles = self.soup.findAll('a', attrs={'class':'forumtitle'})
		for forumtitle in forumtitles:
			title =  u'DZIAŁ: ' + forumtitle.next
			desc = u'OPIS: ' + forumtitle.next.next.next.strip()
			print title
			print desc
			print u'forumtitle: ' + forumtitle['href']
			print forumtitle.parent.findNextSibling('dd', attrs={'class':'topics'}).next.next.text + ':'
			print forumtitle.parent.findNextSibling('dd', attrs={'class':'topics'}).next
			print forumtitle.parent.findNextSibling('dd', attrs={'class':'posts'}).next.next.text + ':'
			print forumtitle.parent.findNextSibling('dd', attrs={'class':'posts'}).next
			print '-------------------------------'	
			res.append(title + '\n' + desc + '\n-------------------------------')
		return res
	
if __name__ == "__main__":
	topic = raw_input("Enter the topic you would like to look for: \n>>> ")
	trac = Tracker()
	firstSiteLinks = trac.askGoogle(topic)
	print len(firstSiteLinks)
	linkNo = raw_input("Wybierz numer linka: \n>>> ")
	#try:
	trac.openForum(firstSiteLinks[int(linkNo)-1])
	#except ValueError:
		#print "Cza było wybrać numer"
#	IPShellEmbed()()

# -*- coding: utf-8 -*-
import mechanize, re, BeautifulSoup,time,urllib2, string
from BeautifulSoup import BeautifulSoup
from IPython.Shell import IPShellEmbed

class Tracker(object):
	def __init__(self):
		# mechanize.RobustFactory() pozwala na prawidlowe odczytywanie stron z bledami(niepozamykane znaczniki, itp.)
		self.br = mechanize.Browser(factory=mechanize.RobustFactory())
		# olewa reguły z robots.txt
		self.br.set_handle_robots(False)
		# musimy udawać prawdziwą przeglądarkę, inaczej google nas nie puści :D
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
		
	def askGoogle(self,question):
		self.br.open('http://google.pl')
		#wybieramy sobie formularz na stronie (można wybierać też po nazwie, ale na googlach jest tylko jeden, stąd po numerku)
		self.br.select_form(nr=0)
		self.br.form['q'] = question
		self.br.submit()
		#do results włazi po prostu otwarty html
		results = self.br.response().read()
		print results[string.find(results,"Około "):string.find(results, "wyników")]+"wyników:"
		#soup to obiekt gotowy do parsowania
		self.soup = BeautifulSoup(results)
		links =   [x['href'] for x in self.soup.findAll('a', attrs={'class':'l'})]
		print "\n".join(links)
		return links
	
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
	linkNo = raw_input("Wybierz numer linka: \n>>> ")
	#try:
	trac.openForum(firstSiteLinks[int(linkNo)-1])
	#except ValueError:
		#print "Cza było wybrać numer"
	IPShellEmbed()()

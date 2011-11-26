# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
import operator
import mechanize
import data_handler

#Aby tego uzywać istotna jest tylko funkcja rate_page.
#Algorytm jest dosyć prosty i działa przez wyszukiwanie dat na stronie i porównywanie z datą
#aktualną. Strona dostanie wysoką ocenę jeśli zawiera aktualne dat. Jeśli 2 strony
#zawierają podobne daty, decyduje ilość ich wystąpień.
#Algorytm ma trochę dziur. Główny problem jest związany z tym, że fora często wyświetlają
#coś w stylu aktualnego czasu i czasu ostatniej wizyty. Na razie po prostu odrzucam
#dwie pierwsze i ostatnią datę na stronie, bo dla naszego projektu lepiej żeby aktualna
#strona nie została wyświetlona, niż żeby nieaktualna znalazła się na samej górze ;).
#Może jeszcze wymyślę jakiś ładny sposób, żeby to ulepszyć.

####

#Funkcje parsujące różne formaty dat
def parse_date1(regexout):
    months = (('sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz',
               'paz', 'lis', 'gru'),
              ('styczen', 'luty', 'marzec', 'kwiecien', 'maj', 'czerwiec', 'lipiec', 'sierpien', 'wrzesien',
               'pazdziernik', 'listopad', 'grudzien'),
              ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'),
              ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
               'october', 'november', 'december'))
    day, month, year, hour, minute = regexout
    monthnum = 0
    for ls in months:
        if month.lower() in ls:
            monthnum = ls.index(month.lower())

    return datetime(int(year), monthnum + 1, int(day),
                             int(hour), int(minute))

def parse_date2(regexout):
    year, month, day, hour, minute = regexout
    return datetime(int(year), int(month), int(day), int(hour), int(minute))

def parse_date3(regexout):
    rel_day, h, m = regexout
    d = datetime.today()
    if rel_day == 'Wczoraj' :
        d = d - timedelta(days = 1)    
    return d.replace(hour = int(h), minute = int(m))

def parse_date4(regexout):
    day, month, year, hour, minute = regexout
    return datetime(int(year), int(month), int(day), int(hour), int(minute))

def parse_date5(regexout):
    return parse_date1(regexout[2:] + regexout[:2])

def parse_date6(regexout):
    fullmonths = ('styczen', 'luty', 'marzec', 'kwiecien', 'maj', 'czerwiec', 'lipiec', 'sierpien', 'wrzesien',
                   'pazdziernik', 'listopad', 'grudzien')
    day, month, year, hour, minute = regexout
    if month.lower() not in fullmonths:
        month = 'styczen'
    return datetime(int(year), fullmonths.index(month.lower()) + 1, int(day),
                             int(hour), int(minute))
def parse_date7(regexout):
    print 
    l = list(regexout)
    l[0], l[1] = l[1], l[0]
    return parse_date1(l)

def parse_date8(regexout):
    print 'date8', regexout
    day, month, year = regexout
    return datetime(int(year), int(month), int(day))    


#Tutaj przechowywane są różne formaty dat w formie wyrażeń regularnych razem z funkcją,
#która potrafi sparsować dany format. Aby dodać nowy format, wystarczy dopisać kolejną parę
#(REGEXP, FUNCTION)
date_formats = (('(\d{1,2}) ([a-zA-Z]+),? (\d{4})(?:,| -)? (?:o |at )?(\d{1,2}):(\d\d)', parse_date1),
                ('(\d{4})-(\d{2})-(\d{1,2}),? (?:o |at )?(\d{1,2}):(\d{1,2})', parse_date2),
                ('(Wczoraj|Dzisiaj|wczoraj|dzisiaj),? (?:o |at )?(\d{1,2}):(\d\d)?', parse_date3),
                ('(\d{1,2})[\./-](\d\d)[\./-](\d{4}),? (?:o |at )?(\d{1,2}):(\d\d)?', parse_date4),
                ('(\d{1,2}):(\d\d),? (\d{1,2}) ([a-zA-Z]{3}),? (\d{4})', parse_date5),
#                ('(\d\d) ([a-zA-Z]+),? (\d{4})(?:,| -)? (?:o )?(\d{1,2}):(\d\d)?', parse_date6),
                ('([a-zA-Z]+),? (\d{1,2}),? (\d{4}),? (?:o |at )?(\d{1,2}):(\d\d)?', parse_date7))
#                ('(\d\d)[\./-](\d\d)[\./-](\d{4})', parse_date8))

#####

def find_date(form, s):
    """Znajduje daty w podanym formacie. Form jest parą (REGEXP, FUNCTION), a s to string,
    w którym będą szukane daty."""
    r = map(form[1], re.findall(form[0], s))[2:-1]
#    print r, form[0]
    return r

def find_all_dates(str):
    """Wyszukuje w str daty we wszystkich formatach podanych w date_formats."""
    return reduce(operator.add, map(lambda form: find_date(form, str), date_formats))

def count_delta_in_days(date1, date2):
    delta = date1 - date2
    return float(delta.days) + float(delta.seconds) / (3600 * 24)
        
def rate(str):
    dates = map(lambda date: count_delta_in_days(datetime.now(), date), find_all_dates(str))
    dates.sort()
    
    i = 1
    
    sum = 0.0
    for date in dates:
        rate = 1.0 / (date + 1) / i
        sum = sum + rate
        i = i * 2
    return sum
    
        
def replace_nonascii(str): 
    """Złe, brzydkie i nieeleganckie (ale szybko napisane :)) 
    podmienianie polskich znaków na odpowiedniki ASCII dla utf8 i iso-8859-2.
    Potrzebne, żeby dobrze rozpoznawać nazwy miesięcy. Na razie tylko ń ź, bo więcej 
    nie trzeba :)."""
    str = str.replace('\xc5\xba', 'z')  # ź w utf-8
    str = str.replace('\xbc', 'z') # ź w iso
    str = str.replace('\xc5\x84', 'n') # ń w utf-8
    str = str.replace('\xf1', 'n') # ń w iso
    return str

def rate_page(str):
    """Funkcja pobiera treść strony i wystawia jej ocenę aktualności w skali 0.0 ~ 2.0 (około).
    Im wyższa ocena tym bardziej aktualna strona."""
    return rate(replace_nonascii(str))

def rate_URL_no_cache(url):
    print 'wczytywanie:', url
    br = mechanize.Browser(factory = mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.set_handle_refresh(True)
    br.set_handle_equiv(True)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    try:
        br.open(url)
#        print br.response().read()
        r =  rate_page(br.response().read())
    except:
        return 0.0
    
    print url, r
    return r

def rate_URL(url, db):
    try:
        rating = db.load_link(url)[-1]
        if datetime.now() - rating[1] < timedelta(days = 1):
            return rating[0]
    except KeyError:
        pass
    r = rate_URL_no_cache(url)
    db.add_link(url, r)
    return r
        
    

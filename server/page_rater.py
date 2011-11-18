# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
import operator

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
    shortmonths = ('sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz',
                   'paz', 'lis', 'gru')
    day, shortmonth, year, hour, minute = regexout
    return datetime(int(year), shortmonths.index(shortmonth.lower()) + 1, int(day),
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


#Tutaj przechowywane są różne formaty dat w formie wyrażeń regularnych razem z funkcją,
#która potrafi sparsować dany format. Aby dodać nowy format, wystarczy dopisać kolejną parę
#(REGEXP, FUNCTION)
date_formats = (('(\d\d) ([a-zA-Zź]{3}) (\d{4}),? (\d\d):(\d\d)', parse_date1),
                ('(\d{4})-(\d{2})-(\d{2}),? (\d{1,2}):(\d\d)', parse_date2),
                ('(Wczoraj|Dzisiaj),? (\d\d):(\d\d)', parse_date3),
                ('(\d\d)[\./](\d\d)[\./](\d{4}),? (\d\d):(\d\d)', parse_date4))

#####

def find_date(form, s):
    """Znajduje daty w podanym formacie. Form jest parą (REGEXP, FUNCTION), a s to string,
    w którym będą szukane daty."""
    r = map(form[1], re.findall(form[0], s))[2:-1]
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
#    print sum
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
    """Funkcja pobiera treść strony i wystawia jej ocenę aktualności w skali 0.0 - 2.0.
    Im wyższa ocena tym bardziej aktualna strona."""
    return rate(replace_nonascii(str))



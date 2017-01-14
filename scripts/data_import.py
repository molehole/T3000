# -*- coding: utf-8 -*-
import time
import re
from stat import S_ISREG, ST_CTIME, ST_MODE
import os


# Glowna sciezka
main_path = os.path.join('/', 'media', 'Etykiety_TXT')

# Zmienne
elementy_regex = '(?<=\^FN921\^FD)(.*)(?=\^FS)'
element_regex = '(?<=\^FN922\^FD)(.*)(?=\^FS)'
informacje_regex = '(?<=\^FN949\^FD)(.*)(?=\^FS)'
nr_regex = '(?<=\^FN929\^FD)(.*)(?=\^FS)'
ilosc_regex = '(?<=\^FN934\^FD)(.*)(?= von 001\^FS)'
etykieta = '\^XF\S+.ZPL(.*?)\^FX End of job'

tablica_etykiet = []
tablica_kontrolna = []


class Etykieta_txt():
    ta = ''
    data = ''
    nr = ''
    tura = ''
    elementy = ''
    pozycja = ''
    element = ''
    ilosc = ''

    def setValues(self, nr, ta, tura, pozycja, data, elementy, element, ilosc):
        self.ta = ta
        self.nr = nr
        self.tura = tura
        self.pozycja = pozycja
        self.data = data
        self.elementy = elementy
        self.element = element
        self.ilosc = ilosc

    def __init__(self, nr, ta, tura, pozycja, data, elementy, element, ilosc):
        self.ta = ta
        self.nr = nr
        self.tura = tura
        self.pozycja = pozycja
        self.data = data
        self.elementy = elementy
        self.element = element
        self.ilosc = ilosc


def czytajPlikEtykiet(plik):
    with open(plik, 'r', encoding="utf8") as f:
        # Wyszukanie wszystkich etykiet
        match = re.findall(etykieta, f.read(), re.DOTALL)
        for i in match:
            nr_regex_match = re.search(nr_regex, i)
            elementy_match = re.search(elementy_regex, i)
            element_match = re.search(element_regex, i)
            informacje_match = re.search(informacje_regex, i)
            ilosc_match = re.search(ilosc_regex, i)
            info_splited = informacje_match.group(0).split('/')
            elementy_splited = elementy_match.group(0).split(',')

            # zmienne
            nr = int(nr_regex_match.group(0))
            ta = info_splited[3].strip()
            tura = info_splited[1].strip()
            pozycja = info_splited[4].strip()
            data = datetime.strptime(info_splited[2].strip(), "%d.%m.%Y")
            elementy = elementy_splited
            element = element_match.group(0).strip()
            ilosc = ilosc_match.group(0)

            # sprawdzenie czy dane TA juz nie wystapilo
            if (nr not in tablica_kontrolna):
                tablica_kontrolna.append(nr)
                tablica_etykiet.append(Etykieta_txt(nr=nr,
                                            ta=ta,
                                            tura=tura,
                                            pozycja=pozycja,
                                            data=data,
                                            elementy=elementy,
                                            element=element,
                                            ilosc=ilosc))
            else: # Aktualizacja danych istniejacego TA
                for e in tablica_etykiet:
                    if (e.nr == nr):
                        e.setValues(nr = nr,
                                    ta = ta,
                                    tura = tura,
                                    pozycja = pozycja,
                                    data = data,
                                    elementy = elementy,
                                    element = element,
                                    ilosc = ilosc)


def wyszukajPlikiPoDacie(sciezka):
    entries = (os.path.join(sciezka, fn) for fn in os.listdir(sciezka))
    entries = ((os.stat(path), path) for path in entries)
    entries = ((stat[ST_CTIME], path)
       for stat, path in entries if S_ISREG(stat[ST_MODE]))
    return entries


def UtworzEtykiete(etykieta):
    tura_index, created_tura = Tura.objects.get_or_create(nr = etykieta.tura, data = etykieta.data)
    ta_index, created_ta = TA.objects.get_or_create(tura = tura_index, nr = etykieta.ta)
    etykieta, created_e = Etykieta.objects.get_or_create(ta = ta_index, element = etykieta.element, pozycja = etykieta.pozycja, nr = etykieta.nr)


def WyszukajIlosci(TA_pelne):
    ilosc = set()
    Ta_dict = TA_pelne.etykieta_set.values('element').annotate(Ilosci=Count('element'))
    for row in Ta_dict:
        if 'kiss' not in row['element'].lower() and 'steckr' not in row['element'].lower():
            ilosc.add(row['Ilosci'])
    if ilosc == set():
        return 1
    return max(ilosc)


def UzupelnijStatus(TA_pelne):
    ta_index, ta_created = Status.objects.get_or_create(ta=TA_pelne)
    if ta_created:
        ilosc = WyszukajIlosci(TA_pelne)
        ta_index.szwalnia_ilosc = ilosc
        ta_index.stolarnia_ilosc = ilosc
        ta_index.tapicernia_ilosc = ilosc
        ta_index.save()
        TA_pelne.ilosc = ilosc
        TA_pelne.save()

def PrzeszukiwaniePlikow(lista_plikow = wyszukajPlikiPoDacie(main_path))
    for T, filenames in sorted(lista_plikow):
        czytajPlikEtykiet(filenames)

def DodajDoBazy():
    PrzeszukiwaniePlikow()
    for each in tablica_etykiet:
        UtworzEtykiete(each)

def DodawanieStatusow():
    for each in TA.objects.all():
        UzupelnijStatus(each)
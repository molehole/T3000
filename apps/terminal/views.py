from django.shortcuts import render
from apps.terminal.models import Etykieta, Wozek, Pole, Status, Tura, Kolejnosc, TA
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#scripts
from apps.terminal.scripts import data_import, xlsx_read

# Create your views here.
@csrf_exempt
def szwalnia_przekaz(request):
    try:
        nr_wozka = int(request.POST['wozek'])
        nr_etykiety = int(request.POST['etykieta'])
        Etyk = Etykieta.objects.get(nr=nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/szwalnia/przekaz.html',
        {'error': True, 'message': 'Niepoprawne dane!'})

    T = Etyk.ta
    s = Status.objects.get(ta = T)
    if s.szwalnia == True:
        return render(request, 'terminal/szwalnia/przekaz.html', {'error': True,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        w = Wozek(ta = T, wozek = nr_wozka)
        s.szwalnia_ilosc -= 1
        if s.szwalnia_ilosc == 0:
            s.szwalnia = True
        w.save()
        s.save()
        message_string = 'Dodano TA %s na wózek %s' % (T.nr, nr_wozka)
        context_dict = {
        'success': True,
        'message': message_string,
        }
        return render(request, 'terminal/szwalnia/przekaz.html', context_dict)

@csrf_exempt
def szwalnia_modelarnia(request):
    try:
        nr_etykiety = int(request.POST['etykieta'])
        Etyk = Etykieta.objects.get(nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/szwalnia/modelarnia.html', {'error': "Etykieta nie odnaleziona"})
    context_dict = {
    'success': True,
    'message': 'Zlecenie przekazane na modelarnie',
    }
    status = Etykieta.ta.status_set.get()
    status.szwalnia_modelarnia = True
    status.save()
    if szwalnia_modelarnia == True and stolarnia_modelarnia == True:
        Ta = Etykieta.Ta
        Ta.zakonczone = True
        Ta.save()
    return render(request, 'terminal/szwalnia/modelarnia.html', context_dict)

@csrf_exempt
def szwalnia_status(request):
    if not request.GET:
        return render(request, 'terminal/szwalnia/status.html', {})
    try:
        nowa_data = datetime.strptime(request.GET['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/szwalnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci = []
    lista_dat = []
    ordered_list = ()
    for each in kolejnosc:
        tury = Tura.objects.filter(nr = each.tura, data = each.data).first()
        ilosci_pozostale = tury.ta_set.filter(status__szwalnia=True).count()
        if ilosci_pozostale == 0:
            ilosci_pozostale = 0
        try:
            procent = int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent = 0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict = {
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/szwalnia/status.html', context_dict)

# ---------------------------------------------------------------------------
#STOLARNIA
@csrf_exempt
def stolarnia_przekaz(request):
    try:
        nr_pola = int(request.POST['pole'])
        nr_etykiety = int(request.POST['etykieta'])
        Etyk = Etykieta.objects.get(nr = nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/stolarnia/przekaz.html',
        {'error': True, 'message': 'Niepoprawne dane!'})

    T = Etyk.ta
    s = Status.objects.get(ta = T)
    if s.stolarnia == True:
        return render(request, 'terminal/stolarnia/przekaz.html', {'error': True,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        if  Pole.objects.filter(pole=nr_pola).count() == 11:
            for i in range(14):
                if Pole.objects.filter(pole=i).count() == 0:
                    message_string = 'Pole jest zapelnione! Proponowane puste pole {0}'.format(i)
            return render(request, 'terminal/stolarnia/przekaz.html', {'error': True,
                                                            'message': message_string})
        p = Pole(ta = T, pole = nr_pola)
        s.stolarnia_ilosc -= 1
        if s.stolarnia_ilosc == 0:
            s.stolarnia = True
        p.save()
        s.save()
        message_string = 'Dodano TA %s na pole %s' % (T.nr, nr_pola)
        context_dict = {
        'success': True,
        'message': message_string,
        }
        return render(request, 'terminal/stolarnia/przekaz.html', context_dict)

@csrf_exempt
def stolarnia_sprawdz(request):
    try:        
        nr_etykiety = int(request.POST['etykieta'])
        Etyk = Etykieta.objects.get(nr = nr_etykiety)
    except Exception as e:
        return render(request, 'terminal/stolarnia/sprawdz.html',
        {'error': True, 'message': 'Niepoprawne dane!'})

    Tura = Etyk.ta.tura
    temp = set()
    for each in Tura.ta_set.all():
        for i in each.pole_set.all():
            temp.add(i.pole)
    if len(temp) == 0:
        for i in range(0, 14):
            if Pole.objects.filter(pole=i+1).count() == 0:
                message_string = 'Podana tura nie ma jeszcze wyznaczonego pola. Proponowane pole {0}'.format(i+1)
                return render(request, 'terminal/stolarnia/sprawdz.html', {'message': message_string})
                break
            else:
                message_string = 'Wyglada na to ze wszystkie pola sa zajete przez jakas ture'
                return render(request, 'terminal/stolarnia/sprawdz.html', {'message': message_string})
                    
    elif len(temp) == 1:
        message_string = list(temp)[0]
        return render(request, 'terminal/stolarnia/sprawdz.html', {'message': message_string})
    elif len(temp) > 1:
        for pole in temp:
            if not Pole.objects.filter(pole=pole).count() == 11:
                message_string = pole
                return render(request, 'terminal/stolarnia/sprawdz.html', {'message': message_string})
    return render(request, 'terminal/stolarnia/sprawdz.html', {'message': len(temp)})

@csrf_exempt
def stolarnia_modelarnia(request):
    context_dict = {
    'success': True,
    'message': '',
    }
    return render(request, 'terminal/stolarnia/modelarnia.html', context)

@csrf_exempt
def stolarnia_status(request):
    if not request.GET:
        return render(request, 'terminal/stolarnia/status.html', {})
    try:
        nowa_data = datetime.strptime(request.GET['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/stolarnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci = []
    lista_dat = []
    ordered_list = ()
    for each in kolejnosc:
        tury = Tura.objects.filter(nr = each.tura, data = each.data).first()
        ilosci_pozostale = tury.ta_set.filter(status__stolarnia=True).count()
        try:
            procent = int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent = 0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict = {
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/stolarnia/status.html', context_dict)

@csrf_exempt
def stolarnia_wozki(request):
    if not request.POST:
        context_dict = {'Pola': Pole.objects.order_by('pole')}
        return render(request, 'terminal/stolarnia/wozki.html', context_dict)
    try:
        usun_date = datetime.strptime(request.POST['usun_date'],'%d.%m.%Y')        
        pola = Pole.objects.filter(ta__tura__data__startswith=usun_date.strftime('%Y-%m-%d'))
        pola.delete()
        context_dict = {'Pola': Pole.objects.order_by('pole'), 'test': pola}
        return render(request, 'terminal/stolarnia/wozki.html', context_dict)
    except ValueError as e:
        return render(request, 'terminal/stolarnia/wozki.html', {'alert': "NIE POPRAWNA DATA!"})
    context_dict = {'Pola': Pole.objects.order_by('pole')}
    return render(request, 'terminal/stolarnia/wozki.html', context_dict)

@csrf_exempt
def stolarnia_wozek_pojedynczy(request, wozek):
    return render(request, 'terminal/stolarnia/wozki_pojedyncze.html', {})

def usun_pole(request, pole):
    pola = Pole.objects.filter(pole=pole)
    if pola.count() > 0:
        pola.delete()
    return render(request, 'terminal/test.html', {})

# ---------------------------------------------------------------------------
# BUFOR
@csrf_exempt
def bufor_przekaz(request):
    etykieta = int(request.POST['etykieta'])
    try:
        Etyk = Etykieta.objects.get(nr = etykieta)
    except Exception as e:
        return render(request, 'terminal/bufor/przekaz.html',
        {'error': True, 'message': 'Niepoprawne dane!'})
    T = Etyk.ta
    s = Status.objects.get(ta = T)
    if s.tapicernia == True:
        return render(request, 'terminal/bufor/przekaz.html', {'error': True, 'message': 'Zlecenie zostalo juz zakończone'})
    else:
        # if T.TA_do_wydania == 0:
            # return render(request, 'terminal/bufor/przekaz.html', {'error': True, 'message': 'Wyglada na to ze nie ma kompletu dla tego zlecenia!'})
        s.tapicernia_ilosc -= 1
        if s.tapicernia_ilosc == 0:
            s.tapicernia = True
            T.zakonczone = True
            T.save()
            T.pole_set.all().delete()
        s.save()
        message_string = 'Wydano TA %s' % (T.nr)
        context_dict = {
        'success': True,
        'message': message_string,
        }
    return render(request, 'terminal/bufor/przekaz.html', context_dict)


@csrf_exempt
def bufor_oddaj(request):
    wozek = int(request.POST['wozek'])
    status_wozka = Wozek.objects.filter(wozek=wozek, odebrany=True)
    if len(status_wozka) == 0:
        return render(request, 'terminal/bufor/oddaj.html', {'error': True,
        'message': 'Wózek nie został odebrany, lub został już oddany!'})
    for each in status_wozka:
        each.delete()
    message_string = "Wozek %i oddany na szwalnie" % wozek
    context_dict = {
    'success': True,
    'message': message_string,
    }
    return render(request, 'terminal/bufor/oddaj.html', context_dict)


@csrf_exempt
def bufor_potwierdz(request):
    wozek = int(request.POST['wozek'])
    status_wozka = Wozek.objects.filter(wozek=wozek, odebrany=False)
    if len(status_wozka) == 0:
        return render(request, 'terminal/bufor/potwierdz.html', {'error': True,
            'message': 'Podany wozek nie ma kompletow, lub nie zostały one zeskanowane'})
    for each in status_wozka:
        s = each.ta.status_set.first()
        each.odebrany = True
        each.save()
    message_string = "Wozek %i przekazany do bufora" % wozek
    context_dict = {
    'success': True,
    'message': message_string,
    }
    return render(request, 'terminal/bufor/potwierdz.html',context_dict)


@csrf_exempt
def bufor_sprawdz(request):
    etykieta = int(request.POST['etykieta'])
    wozki = []
    pola = []
    status = Etykieta.objects.get(nr=etykieta).sprawdzenie_statusu()
    for wozek in status[0]:
        wozki.append(wozek.wozek)
    for pole in status[1]:
        pola.append(pole.pole)
    message_string = "Wózki: %s\nPola: %s" % (wozki, pola)
    context_dict = {
    'success': True,
    'message': message_string,
    }
    return render(request, 'terminal/bufor/wyszukaj.html', context_dict)

@csrf_exempt
def bufor_status(request):
    if not request.GET:
        return render(request, 'terminal/bufor/status.html', {})
    try:
        nowa_data = datetime.strptime(request.GET['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/bufor/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci = []
    lista_dat = []
    ordered_list = ()
    for each in kolejnosc:
        tury = Tura.objects.filter(nr = each.tura, data = each.data).first()
        ilosci_pozostale = tury.ta_set.all().filter(zakonczone = True).count()
        try:
            procent = int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent = 0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict = {
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/bufor/status.html', context_dict)


# ---------------------------------------------------------------------------
#ZESTAWIENIA
@csrf_exempt
def zestawienie(request):
    if not request.GET:
        return render(request, 'terminal/zestawienie.html', {})
    try:
        nowa_data = datetime.strptime(request.GET['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/zestawienie.html', {'alert': "NIE POPRAWNA DATA!"})
    
    kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci = []
    lista_dat = []
    ordered_list = ()
    for each in kolejnosc:
        tury = Tura.objects.filter(nr = each.tura, data = each.data).first()
        ilosci_pozostale = tury.ta_set.all().filter(zakonczone = True).count()
        try:
            procent = int((ilosci_pozostale/tury.ta_set.all().count())*100)
        except ZeroDivisionError as e:
            procent = 0
        lista_kolejnosci.append({'tura': tury, 'ilosci_pozostale': ilosci_pozostale, 'procent': procent})
    context_dict = {
        'tury': lista_kolejnosci,
        'wybrana_data':  nowa_data.strftime('%d.%m.%Y'),
    }
    return render(request, 'terminal/zestawienie.html', context_dict)

def zestawienie_pojedyncze(request, T):
    ta = TA.objects.get(nr = int(T))    
    return render(request, 'terminal/pojedyczne.html', {"TA": ta})

# ---------------------------------------------------------------------------
#SKRYPTY
def import_danych(request):    
    try:
        data_import.DodajDoBazy()
        data_import.DodawanieStatusow()
    except Exception as e:
        raise e    
    # return render(request, 'data_import.html', {})

def import_kolejnosci(request):    
    try:
        xlsx_read.DodajKolejnosc()
    except Exception as e:
        raise e    
    # return render(request, 'data_import.html', {})

# ---------------------------------------------------------------------------
#TESTOWE
def test(request):    
    return render(request, 'terminal/base.html', {'Pola': Pole.objects.order_by('pole')})

def test2(request):    
    return render(request, 'terminal/test.html', {'Pola': Pole.objects.order_by('pole')})

from django.shortcuts import render
from terminal.models import Etykieta, Wozek, Pole, Status, Tura, Kolejnosc
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


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



def szwalnia_status(request):
    if not request.POST:
        return render(request, 'terminal/szwalnia/status.html', {})
    try:
        nowa_data = datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/szwalnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
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



def stolarnia_status(request):
    if not request.POST:
        return render(request, 'terminal/stolarnia/status.html', {})
    try:
        nowa_data = datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
    except ValueError as e:
        return render(request, 'terminal/stolarnia/status.html', {'alert': "NIE POPRAWNA DATA!"})
    kolejnosc = Kolejnosc.objects.filter(data = nowa_data.strftime('%Y-%m-%d'))
    lista_kolejnosci = []
    lista_dat = []
    ordered_list = ()
    for each in kolejnosc:              
        tury = Tura.objects.get(nr = each.tura, data = each.data)       
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
    return render(request, 'terminal/stolarnia/status.html', context_dict)


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
        return render(request, 'terminal/bufor/przekaz.html', {'error': true,
                                                        'message': 'Zlecenie zostalo juz zakończone'})
    else:
        if T.TA_do_wydania == 0:
            return render(request, 'terminal/bufor/przekaz.html', {'error': true,
                                                        'message': 'Wyglada na to ze nie ma kompletu dla tego zlecenia!'})    
        s.tapicernia_ilosc -= 1
        if s.tapicernia_ilosc == 0:
            s.tapicernia = True
            T.zakonczone = True            
            T.save
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
        'message': 'Blad krytyczny! Wezwij administratora sieci!'})
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
            'message': 'Podany wozek nie ma kompletow!'})
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
    if not request.POST:
        return render(request, 'terminal/bufor/status.html', {})
    try:
        nowa_data = datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
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
def zestawienie(request):
    if not request.POST:
        return render(request, 'terminal/zestawienie.html', {})
    try:
        nowa_data = datetime.strptime(request.POST['nowa_data'],'%d.%m.%Y')
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
from django.shortcuts import render, HttpResponseRedirect
from .models import Spotkania
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import DodawanieRozmowy, LoginForm

def index(request):
    dane = Spotkania.objects.order_by('data_rozmowy')
    if request.user.is_authenticated():
        auth = True
    else:
        auth = False
    return render(request, 'lista_rekrutacyjna/index.html', {'dane': dane, 'auth': auth})

@login_required
def usun(request, ID):
    Spotkania.objects.get(pk=ID).delete()
    return HttpResponseRedirect('/lista_r/')

@login_required
def dodaj(request):
    if request.method == 'POST':
        form = DodawanieRozmowy(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            imie = data['imie']
            nazwisko = data['nazwisko']
            data_spotkania = data['data']
            godzina_spotkania = data['godzina']
            dodatkowe_informacje = data['dodatkowe_informacje']
            a = Spotkania(imie=imie, nazwisko=nazwisko, data_rozmowy=data_spotkania, godzina_rozmowy=godzina_spotkania, info = dodatkowe_informacje)
            a.save()            
            return HttpResponseRedirect('/lista_r/')
        else:
            return render(request, 'lista_rekrutacyjna/formularz.html', { 'form': form })        
    return render(request, 'lista_rekrutacyjna/index.html', {})

@login_required
def edytuj(request, ID):
    return render(request, 'lista_rekrutacyjna/edytuj.html', {})

@login_required
def formularz(request):
    form = DodawanieRozmowy()
    return render(request, 'lista_rekrutacyjna/formularz.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/lista_r/')
    form = LoginForm()
    return render(request, 'lista_rekrutacyjna/login.html', {'form': form})

def l_check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = data['user']
            password = data['password']

            user_check = authenticate(username=user, password=password)
            if user_check:
                if user_check.is_active:
                    login(request, user_check)
                    return HttpResponseRedirect('/lista_r/')
            else:
                return render(request, 'lista_rekrutacyjna/login.html', {'form': form, 'error': 'Logowanie nie poprawne'})
    return render(request, 'lista_rekrutacyjna/login.html', {'form': form, 'error': 'Logowanie nie poprawne'})
        

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/lista_r/')
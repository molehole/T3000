from django.db import models
from django.utils import timezone
from fractions import gcd


class Tura(models.Model):
    nr = models.IntegerField()
    data = models.DateField()

    def pokaz_niezakonczone(self):
        return self.ta_set.filter(zakonczone=False)

    def __str__(self):
        return_string = str(self.nr) + "(" + str(self.data) + ")"
        return str(return_string)


class TA(models.Model):
    tura = models.ForeignKey(Tura)
    nr = models.IntegerField()
    elementy = models.TextField()
    zakonczone = models.BooleanField(default=False)
    ilosc = models.IntegerField(default=1)

    def pokaz_wozki(self):
        temp = []
        for each in self.wozek_set.filter(odebrany=True):
            temp.append(str(each.wozek))
        return ','.join(temp)

    def pokaz_pola(self):
        temp = []
        for each in self.pole_set.all():
            temp.append(str(each.pole))
        return ','.join(temp)

    def pokaz_odebrane_wozki(self):
        return self.wozek_set.filter(odebrany=True)

    def pokaz_nieodebrane_wozki(self):
        return self.wozek_set.filter(odebrany=False)

    def kolor_na_buforze(self):
        if self.pokaz_odebrane_wozki().count() >= 1 or self.pole_set.all().count() >= 1 :
            return str('#EEE842')
        if self.TA_do_wydania() > 0:
            return str('#3A941A')
        else:
            return str('')

    def TA_do_wydania(self):
        if self.status_set.first().tapicernia_ilosc == 0:
            return 0
        else:
            return gcd(self.pokaz_odebrane_wozki().count(), self.pole_set.all().count())

    def __str__(self):
        return str(self.nr)


# Create your models here.
class Etykieta(models.Model):
    ta = models.ForeignKey(TA)
    nr = models.IntegerField()
    pozycja = models.IntegerField(null=True)
    element = models.TextField(null=True)

    def sprawdzenie_statusu(self):
        return (self.ta.wozek_set.filter(odebrany=True), self.ta.pole_set.all())

    def __str__(self):
        return str(self.nr)


# Tabela odkladcza na Szwalni
class Wozek(models.Model):
    wozek = models.IntegerField()
    data_dodania = models.DateTimeField(default=timezone.now)
    data_wydania = models.DateTimeField(null=True)
    ta = models.ForeignKey(TA)
    odebrany = models.BooleanField(default=False)

    def __str__(self):
        return str(self.wozek)


# Tabela odkladcza na Stolarni
class Pole(models.Model):
    pole = models.IntegerField()
    data_dodania = models.DateTimeField(default=timezone.now)
    data_wydania = models.DateTimeField(null=True)
    ta = models.ForeignKey(TA)

    def __str__(self):
        return str(self.pole)


# Tabela Statusów
class Status(models.Model):
    ta = models.ForeignKey(TA)
    szwalnia = models.BooleanField(default=False)
    stolarnia = models.BooleanField(default=False)
    tapicernia = models.BooleanField(default=False)
    szwalnia_ilosc = models.IntegerField(default=1)
    stolarnia_ilosc = models.IntegerField(default=1)
    tapicernia_ilosc = models.IntegerField(default=1)

    def __str__(self):
        return str(self.ta.nr)


class Kolejnosc(models.Model):
    tura = models.TextField()
    data = models.DateField()

    def __str__(self):
        return_string = str(self.tura) + "(" + str(self.data) + ")"
        return return_string

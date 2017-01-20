# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class Spotkania(models.Model):
    imie = models.TextField(default=None)
    nazwisko = models.TextField(default=None)
    data_rozmowy = models.DateField(default=None)
    godzina_rozmowy = models.TimeField(default=None)
    info = models.TextField(default='')

    @property
    def przedawnione(self):
        return date.today() == self.data_rozmowy

    def __str__(self):
        return ', '.join((" ".join((self.imie, self.nazwisko)), self.data_rozmowy.isoformat(), self.godzina_rozmowy.isoformat()))
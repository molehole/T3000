from django.contrib import admin
from apps.terminal.models import Etykieta, Wozek, Pole, Status, TA, Tura, Kolejnosc

# Register your models here.
admin.site.register(Etykieta)
admin.site.register(Wozek)
admin.site.register(Pole)
admin.site.register(Status)
admin.site.register(TA)
admin.site.register(Tura)
admin.site.register(Kolejnosc)

from django.conf.urls import url, include
from django.contrib import admin
from apps.lista_rekrutacyjna import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dodaj/$', views.dodaj, name='dodaj'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^l_check/$', views.l_check, name='l_check'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^usun/(?P<ID>[\d+])/$', views.usun, name='usun'),
    url(r'^edytuj/(?P<ID>[\d+])/$', views.edytuj, name='edytuj'),
    url(r'^formularz/$', views.formularz, name='formularz'),
]

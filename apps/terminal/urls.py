"""T3000 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from apps.terminal import views

urlpatterns = [
    url(r'^szwalnia/status/$', views.szwalnia_status, name='szwalnia_status'),
    url(r'^szwalnia/przekaz/$', views.szwalnia_przekaz, name='szwalnia_przekaz'),
    url(r'^szwalnia/modelarnia/$', views.szwalnia_modelarnia, name='szwalnia_modelarnia'),
    url(r'^stolarnia/status/$', views.stolarnia_status, name='stolarnia_status'),
    url(r'^stolarnia/przekaz/$', views.stolarnia_przekaz, name='stolarnia_przekaz'),
    url(r'^stolarnia/modelarnia/$', views.stolarnia_modelarnia, name='stolarnia_modelarnia'),
    url(r'^stolarnia/sprawdz/$', views.stolarnia_sprawdz, name='stolarnia_sprawdz'),
    url(r'^stolarnia/wozki/', views.stolarnia_wozki, name='stolarnia_wozki'),
    url(r'^bufor/status/$', views.bufor_status, name='bufor_status'),
    url(r'^bufor/przekaz/$', views.bufor_przekaz, name='bufor_przekaz'),
    url(r'^bufor/oddaj/$', views.bufor_oddaj, name='bufor_oddaj'),
    url(r'^bufor/potwierdz/$', views.bufor_potwierdz, name='bufor_potwierdz'),
    url(r'^bufor/sprawdz/$', views.bufor_sprawdz, name='bufor_sprawdz'),
    url(r'^zestawienie/$', views.zestawienie, name='zestawienie'),
    url(r'^zestawienie/(?P<T>[\d]+)/$', views.zestawienie_pojedyncze, name='zestawienie_pojedyncze'),
    url(r'^import_danych/1$', views.import_danych, name='import_danych'),
    url(r'^import_kolejnosci/1$', views.import_kolejnosci, name='import_kolejnosci'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test2/$', views.test2, name='test2'),
]

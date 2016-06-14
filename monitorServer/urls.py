from django.conf.urls import url
from django.contrib import admin
from monitorServer.views import index,entrar,sortir,login
from cardiac.views import dades,chart,chart2,chart3, chart4, usuari, usuari_master, master, borrar, seguiment
urlpatterns = [
    url(r'^$',index),
    url(r'^dades/', dades),
    url(r'^usuari/$', usuari),
    url(r'^usuari/(?P<id>\w+)/', usuari),
    url(r'^usuari_master/(?P<id>\w+)/', usuari_master),
    url(r'^master/', master),
    url(r'^seguiment/', seguiment),
    url(r'^chart/(?P<chart>\w+)/', chart),
    url(r'^chart2/(?P<chart>\w+)/', chart2),
    url(r'^chart3/(?P<chart>\w+)/', chart3),
    url(r'^chart4/(?P<chart>\w+)/', chart4),
    url(r'^borrar/(?P<id>\w+)/', borrar),
    url(r'^entrar/$',entrar),
    url(r'^login/',login),
    url(r'^sortir/$',sortir),
    url(r'^admin/', admin.site.urls),
]

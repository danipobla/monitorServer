from django.conf.urls import url
from django.contrib import admin
from monitorServer.views import index,entrar,sortir
from cardiac.views import dades,chart,chart2,usuari,borrar
urlpatterns = [
    url(r'^$',index),
    url(r'^dades/', dades),
    url(r'^usuari/', usuari),
    url(r'^chart/', chart),
    url(r'^chart2/(?P<chart>\w+)/', chart2),
    url(r'^borrar/(?P<id>\w+)/', borrar),
    url(r'^entrar/$',entrar),
    url(r'^sortir/$',sortir),
    url(r'^admin/', admin.site.urls),
]

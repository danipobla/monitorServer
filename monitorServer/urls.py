from django.conf.urls import url
from django.contrib import admin
from monitorServer.views import index,entrar,sortir
from cardiac.views import dades,chart,chart2,chart_zoom,usuari,borrar
urlpatterns = [
    url(r'^$',index),
    url(r'^dades/', dades),
    url(r'^usuari/', usuari),
    url(r'^chart/', chart),
    url(r'^chart2/(?P<chart>\w+)/', chart2),
    url(r'^chart_zoom/(?P<chart>\w+)/', chart_zoom),
    url(r'^borrar/(?P<id>\w+)/', borrar),
    url(r'^entrar/$',entrar),
    url(r'^sortir/$',sortir),
    url(r'^admin/', admin.site.urls),
]

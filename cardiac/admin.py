from django.contrib import admin
from cardiac.models import Health, Hrm, Master, Relation

admin.site.register(Master)
admin.site.register(Relation)
admin.site.register(Health)
admin.site.register(Hrm)

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Master(models.Model):
	user = models.ForeignKey(User)
        class Meta:
                ordering = ['user']
        def __unicode__(self):
                return unicode(self.user)
	
class Relation(models.Model):
	master= models.ForeignKey(Master)
	slave = models.ManyToManyField(User)
        class Meta:
                ordering = ['master']
        def __unicode__(self):
                return unicode(self.master)

class Health(models.Model):
	date = models.DateTimeField(null=True)
	user = models.ForeignKey(User)
	master = models.ForeignKey(Master,null=True)
	age = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	maxim = models.IntegerField(null=True)
	minim = models.IntegerField(null=True)
	averagehr = models.IntegerField(null=True)
	averagehrv = models.IntegerField(null=True)

class Hrm(models.Model):
	date = models.DateTimeField()
	hr = models.IntegerField()
	intensity =  models.CharField(max_length=10)
	comment = models.CharField(max_length=50)
	hrv = models.IntegerField()
	health = models.ForeignKey('Health')

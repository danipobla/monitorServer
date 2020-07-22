from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Main(models.Model):
	user = models.ForeignKey(User)
        class Meta:
                ordering = ['user']
        def __unicode__(self):
                return unicode(self.user)
	
class Relation(models.Model):
	main= models.ForeignKey(Main)
	subordinate = models.ManyToManyField(User)
        class Meta:
                ordering = ['main']
        def __unicode__(self):
                return unicode(self.main)

class Health(models.Model):
	date = models.DateTimeField(null=True)
	user = models.ForeignKey(User)
	main = models.ForeignKey(Main,null=True)
	age = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	maxim = models.IntegerField(null=True)
	minim = models.IntegerField(null=True)
	averagehr = models.IntegerField(null=True)
	averagehrv = models.IntegerField(null=True)
	datend = models.DateTimeField(null=True)

class Hrm(models.Model):
	date = models.DateTimeField()
	hr = models.IntegerField()
	intensity =  models.CharField(max_length=10)
	comment = models.CharField(max_length=50)
	hrv = models.IntegerField()
	health = models.ForeignKey('Health')

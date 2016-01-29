from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Health(models.Model):
	user = models.ForeignKey(User)
	age = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	maxim = models.IntegerField(null=True)
	minim = models.IntegerField(null=True)
	average = models.IntegerField(null=True)

class Hrm(models.Model):
	date = models.DateTimeField()
	hr = models.IntegerField()
	state = models.CharField(max_length=10)
	intensity =  models.CharField(max_length=10)
	comment = models.CharField(max_length=50)
	health = models.ForeignKey('Health')

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Health(models.Model):
	user = models.ForeignKey(User)
	age = models.IntegerField()
	height = models.IntegerField()
	weight = models.IntegerField()

class Hrm(models.Model):
	date = models.DateTimeField()
	hr = models.IntegerField()
	state = models.CharField(max_length=10)
	intensity =  models.CharField(max_length=10)
	comment = models.CharField(max_length=50)
	health = models.ForeignKey('Health')

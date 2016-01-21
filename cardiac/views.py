from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from cardiac.models import Health,Hrm
from django.contrib.auth.models import User
import json

@csrf_exempt
def dades(request):
	json_data = request.read()
	data = json.loads(json_data)
	health = Health(user=User.objects.get(id=1), age=int(data['age']),height=int(data['height']),weight=int(data['weight']))
	health.save()

	for i in data['hrm']:
 		hrm=Hrm(health=Health.objects.get(id=health.id),date=i['date'],hr=int(i['hr']),state=i['state'],intensity=i['intensity'],comment=i['comment'])
		hrm.save()	

	return HttpResponse(health.id)

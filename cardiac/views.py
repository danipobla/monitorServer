from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from cardiac.models import Health,Hrm
from django.contrib.auth.models import User
from django.utils import timezone
import json
from collections import OrderedDict as SortedDict
from chartit import DataPool, Chart
from django.shortcuts import render_to_response

@csrf_exempt
def dades(request):
	json_data = request.read()
	data = json.loads(json_data)
	health = Health(user=User.objects.get(id=1), age=int(data['age']),height=int(data['height']),weight=int(data['weight']))
	health.save()

	for i in data['hrm']:
 		hrm=Hrm(health=Health.objects.get(id=health.id),date=(i['date']),hr=int(i['hr']),state=i['state'],intensity=i['intensity'],comment=i['comment'])
		hrm.save()	

	return HttpResponse(hrm.id)

def chart(request):

	hrm_data=Hrm.objects.filter(health=Health.objects.latest('id'))

	hrm = DataPool(
        series=	[{'options': {
            	  'source': hrm_data},
          	  'terms': [ 'date',
            		     'hr']}
         ])

	cht = Chart(
        datasource = hrm, 
        series_options = 
          [{'options':{
              'type': 'line',
              'stacking': False},
            'terms':{
              'date': [
                'hr']
              }}],
        chart_options = 
          {'title': {
               'text': 'HRMesurement'},
           'xAxis': {
                'title': {
                   'text': 'DATA'}}})
	return render(request,'weatherchart.html',{'hrmchart':cht})

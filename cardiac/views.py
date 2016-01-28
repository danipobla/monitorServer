from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import HttpResponse
from cardiac.models import Health,Hrm
from django.contrib.auth.models import User
from django.utils import timezone
import json
from collections import OrderedDict as SortedDict
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from nvd3 import lineWithFocusChart
import random
import datetime
import time

@csrf_exempt
def dades(request):
	json_data = request.read()
	data = json.loads(json_data)
	health = Health(user=User.objects.get(id=1), age=int(data['age']),height=int(data['height']),weight=int(data['weight']))
	health.save()

	for i in data['hrm']:
 		hrm=Hrm(health=Health.objects.get(id=health.id),date=(i['date']),hr=int(i['hr']),state=i['state'],intensity=i['intensity'],comment=i['comment'])
		hrm.save()	

	return HttpResponse("OK")

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

def chart2(request,chart=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	    hrm_data=Hrm.objects.filter(health=Health.objects.get(id=chart))
	    xdata=[]
	    ydata2=[]
	    ydata=[]
	    for i in hrm_data:
		xdata.append(int(time.mktime(i.date.timetuple()) * 1000))
		ydata2.append(int(float(i.intensity)))
		ydata.append(i.hr)

	    chartdata = {'x': xdata, 
	                 'name1':'HRM','y1': ydata,
	                 'name2':'MOV','y2': ydata2,}
	    charttype = "lineChart"
	    charttype1 = "lineWithFocusChart"
	    chartcontainer = "chart_container"
	    chartcontainer1 = "chart_container1"
	    chartdata1 = chartdata
	    data = {
	        'charttype': charttype,
	        'chartdata': chartdata,
		'chartcontainer':chartcontainer,
	        'charttype1': charttype1,
	        'chartdata1': chartdata1,
		'chartcontainer1':chartcontainer1,
		'extra': {
	            'x_is_date': True,
	            'x_axis_format': '%H:%M:%S',
		    'tag_script_js': True,
	            'jquery_on_ready': False,
	        },
		'extra1': {
	            'x_is_date': True,
	            'x_axis_format': '%H:%M:%S',
		    'tag_script_js': True,
	            'jquery_on_ready': False,
	        },
	    }
	    return render_to_response('chart2.html', data)

def usuari(request):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
	   	usuari=Health.objects.filter(user=request.user.id).order_by('-id')
    		return render_to_response('usuari.html', {'usuari':usuari})

def borrar(request,id=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	        Hrm.objects.filter(health=id).delete()
		Health.objects.get(id=id).delete()
		return redirect('/usuari/')

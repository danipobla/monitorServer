from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.http import HttpResponse
from cardiac.models import Health,Hrm,Relation,Master
from django.contrib.auth.models import User
from django.utils import timezone
import json
from collections import OrderedDict as SortedDict
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from nvd3 import lineWithFocusChart
from django.db.models import Avg,Max,Min
import time
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import ColumnDataSource,HoverTool, Range1d,LinearAxis

@csrf_exempt
def dades(request):
	json_data = request.read()
	data = json.loads(json_data)
	health = Health(date=data['hrm'][0]['date'],datend=data['hrm'][-1]['date'],user=User.objects.get(id=int(data['user'])), age=int(data['age']),height=int(data['height']),weight=int(data['weight']))
	health.save()

	for i in data['hrm']:
 		hrm=Hrm(health=Health.objects.get(id=health.id),date=(i['date']),hr=int(i['hr']),hrv=int(i['hrv']),intensity=int(i['intensity']),comment=i['comment'])
		hrm.save()	

	mma=Hrm.objects.filter(health=health.id,hrv__lte=1950,hrv__gte=10,hr__gte=1).aggregate(Max('hr'),Min('hr'),Avg('hr'),Avg('hrv'))
	health.maxim=mma['hr__max']
	health.minim=mma['hr__min']
	health.averagehr=mma['hr__avg']
	health.averagehrv=mma['hrv__avg']
	health.save()
	return HttpResponse("SAVED")


def chart4(request,chart=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	        hrm_data=Hrm.objects.filter(health=Health.objects.get(id=chart),hrv__lte=1950,hrv__gte=10)
    		xdata=[]
 		ymov=[]
    		yhr=[]
		comment=[]
		ycomment=[]
    		for i in hrm_data:
			xdata.append(int(time.mktime(i.date.timetuple()) * 1000))
			ymov.append(int(float(i.intensity)))
			yhr.append(i.hrv)
			if (str(i.comment)==""):
				 ycomment.append(float('nan'))
			else:
				 ycomment.append(i.hrv)
 
			comment.append(i.comment)

   

    		source = ColumnDataSource(
        		data=dict(
            			x=xdata,
            			y=yhr,
				c=comment,
        			)
    			)
			
    		source2 = ColumnDataSource(
        		data=dict(
            			x=xdata,
            			y=yhr,
				c=comment,
        			)
    			)

    		hover = HoverTool(
        		tooltips=[
            			("HRV", "@y"),
            			("comment", "@c"),
        		]
    		)

    		plot = figure(title="HRV MESUREMENT",x_axis_type="datetime", y_range=(900,1100),tools=[hover, 'pan', 'wheel_zoom','box_zoom','reset','resize','save'],plot_width=1000, plot_height=600)
		plot.xaxis.axis_label = 'Time (ms)'
		plot.yaxis.axis_label = 'Heart Rate Variability (ms)'
		
		plot.circle(x=xdata, y=ycomment, source=source2,color="orange", fill_color="red", size=14,legend="Comentari")
		plot.line(x=xdata, y=yhr,source=source, color="red", legend="Heart Rate Variability")
    		plot.extra_y_ranges = {"foo": Range1d(start=0, end=30)}
    		plot.line(x=xdata, y=ymov, color="blue", legend="Movement",y_range_name="foo")
    		plot.add_layout(LinearAxis(y_range_name="foo",axis_label="Movement (m/s2)"), 'right')

		script, div = components(plot, CDN)
		if Master.objects.filter(user=request.user.id).exists():
			return render(request, "chart_master.html", {"the_script":script, "the_div":div})
		else:
			return render(request, "chart.html", {"the_script":script, "the_div":div})


def chart(request,chart=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	        hrm_data=Hrm.objects.filter(health=Health.objects.get(id=chart))
    		xdata=[]
 		ymov=[]
    		yhr=[]
		comment=[]
		ycomment=[]
    		for i in hrm_data:
			xdata.append(int(time.mktime(i.date.timetuple()) * 1000))
			ymov.append(int(float(i.intensity)))
			yhr.append(i.hr)
			if (str(i.comment)==""):
				 ycomment.append(float('nan'))
			else:
				 ycomment.append(i.hr)
 
			comment.append(i.comment)

   

    		source = ColumnDataSource(
        		data=dict(
            			x=xdata,
            			y=yhr,
				c=comment,
        			)
    			)
			
    		source2 = ColumnDataSource(
        		data=dict(
            			x=xdata,
            			y=yhr,
				c=comment,
        			)
    			)

    		hover = HoverTool(
        		tooltips=[
            			("HR", "@y"),
            			("comment", "@c"),
        		]
    		)

    		plot = figure(title="HR MESUREMENT",x_axis_type="datetime", y_range=(0,220),tools=[hover, 'pan', 'wheel_zoom','box_zoom','reset','resize','save'],plot_width=1000, plot_height=600)
	 	plot.yaxis.axis_label = 'Heart Rate (bpm)'
		plot.circle(x=xdata, y=ycomment, source=source2,color="orange", fill_color="red", size=14,legend="Comment")
		plot.line(x=xdata, y=yhr,source=source, color="red", legend="Heart Rate")
    		plot.extra_y_ranges = {"foo": Range1d(start=0, end=30)}
    		plot.line(x=xdata, y=ymov, color="blue", legend="Movement",y_range_name="foo")
    		plot.add_layout(LinearAxis(y_range_name="foo",axis_label="Movement (m/s2)"), 'right')

		plot.xaxis.axis_label = 'Time (ms)'
		script, div = components(plot, CDN)
    		

		if Master.objects.filter(user=request.user.id).exists():
			return render(request, "chart_master.html", {"the_script":script, "the_div":div})
		else:
			return render(request, "chart.html", {"the_script":script, "the_div":div})
			

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
	    charttype = "lineWithFocusChart"
	    chartcontainer = "chart_container"
	    data = {
	        'charttype': charttype,
	        'chartdata': chartdata,
		'chartcontainer':chartcontainer,
		'extra': {
	            'x_is_date': True,
	            'x_axis_format': '%H:%M:%S',
		    'tag_script_js': True,
	            'jquery_on_ready': False,
	            'color_category':'category10' 
		},
	    }
	    return render_to_response('chart2.html', data)

def chart3(request,chart=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	        hrm_data=Hrm.objects.filter(health=Health.objects.get(id=chart))

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
		return render(request,'chart3.html',{'hrmchart':cht})

def seguiment(request):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
	   	usuari=Relation.objects.filter(master=Master.objects.get(user=request.user.id)).values_list('slave__id','slave__username','slave__first_name','slave__last_name')
		return render_to_response('seguiment.html', {'usuari':usuari})

def master(request):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
	   	usuari=Health.objects.filter(user=request.user.id).order_by('-id')
    		return render_to_response('master.html', {'usuari':usuari})

def usuari_master(request,id=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
		if (id==0):
			id=request.user.id

	   	usuari=Health.objects.filter(user=id).order_by('-id')
		return render_to_response('usuari_master.html', {'usuari':usuari})
def usuari(request,id=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
		if (id==0):
			id=request.user.id

	   	usuari=Health.objects.filter(user=id).order_by('-id')
		if Master.objects.filter(user=request.user.id).exists():
			return render_to_response('master.html', {'usuari':usuari})
		else:
			return render_to_response('usuari.html', {'usuari':usuari})

def borrar(request,id=0):
        if not request.user.is_authenticated():
                return render(request,'error.html')
        else:
  	        Hrm.objects.filter(health=id).delete()
		Health.objects.get(id=id).delete()

		if Master.objects.filter(user=request.user.id).exists():
			return redirect('/master/')
		else:
			return redirect('/usuari/')



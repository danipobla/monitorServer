from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponse
from cardiac.models import Main
import json

def index(request):
	return render(request,'index.html')

def entrar(request):
        usuari = request.POST.get('username')
        clau = request.POST.get('password')
        user = auth.authenticate(username=usuari, password=clau)
        if user is not None and user.is_active:
                auth.login(request,user)
		if Main.objects.filter(user=user.id).exists():
			return redirect ('/main/')
		else:
			return redirect ('/usuari/', id=request.user.id)
        else:
                return render(request,'error.html')

def sortir(request):
        auth.logout(request)
        return redirect('/')

@csrf_exempt
def login(request):
	json_data = request.read()
        data = json.loads(json_data)
        usuari = data['username']
        clau = data['password']
        user = auth.authenticate(username=usuari, password=clau)
        if user is not None and user.is_active:
                return HttpResponse(user.id)
        else:
                return HttpResponse("USER CREDENTIALS DOESN'T EXIST")

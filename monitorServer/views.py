from django.shortcuts import render,redirect
from django.contrib import auth

def index(request):
	return render(request,'index.html')

def entrar(request):
        usuari = request.POST.get('username')
        clau = request.POST.get('password')
        user = auth.authenticate(username=usuari, password=clau)
        if user is not None and user.is_active:
                auth.login(request,user)
                return redirect ('/usuari/')
        else:
                return render(request,'error.html')

def sortir(request):
        auth.logout(request)
        return render(request,'index.html')



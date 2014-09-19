from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from passlib.hash import django_pbkdf2_sha256 as handler

def index(request):
	return render(request, 'home.html')
def auth_view(request):
	sessionlogin=request.session['login-session']
	name = request.POST.get('Username', '')
	pwd = request.POST.get('Password', '')
	h=handler.encrypt(pwd,salt_size =12,rounds=12000)
	details = User.objects.filter(username=name,password=pwd)
	questions = [d.username for d in details]

	request.session['login-session'] = questions
	return render(request, 'home.html', {'questions': request.session['login-session'] })
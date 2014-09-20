from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#from passlib.hash import django_pbkdf2_sha256 as handler
from django import http
from django.conf import settings
from datetime import timedelta, date
from django.template import RequestContext
from django.core.context_processors import csrf


def index(request):
	loginsession = request.session.get('loginsession')
	return render(request, 'home.html', {'questions': loginsession })
def auth_view(request):
	name = request.POST.get('Username', '')
	pwd = request.POST.get('Password', '')
	remember = request.POST.get('remember', '')
	#h=handler.encrypt(pwd,salt_size =12,rounds=12000)
	details = User.objects.filter(username=name,password=pwd)
	questions = [d.username for d in details]
	if remember == "":
          request.session.set_test_cookie()
	request.session['loginsession']=questions
	#response = HttpResponse()
	response = render(request,'home.html', {'questions': questions})

	response.set_cookie('logged_in_status', pwd) 
	return response
	#return response
	#return render(request, 'home.html', {'questions': questions })
def logout(request):
	request.session['loginsession'] = ''
	id=request.COOKIES.get('logged_in_status') 
	return render(request, 'login.html',id)
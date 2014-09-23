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
from django.core.mail import send_mail,EmailMultiAlternatives


def index(request):
	return render(request, 'register.html',{'msg':''})
def signup(request):
	first_name = request.POST.get('First_name', '')
	last_name = request.POST.get('Last_name', '')
	username = request.POST.get('Username', '')
	email = request.POST.get('Email', '')
	password = request.POST.get('Password', '')
	company_name = request.POST.get('Company_name', '')
	details = User.objects.filter(username=username).count()
	if details > 0:
		return render(request, 'register.html',{'msg':'Username is already exist!'})
	else:
		user = User.objects.create_user(username,email,'')
		user.first_name = first_name
		user.last_name =last_name
		user.password =password
		user.company_name =company_name
		user.save()
		return render(request, 'login.html',{'msg':'Register Successfull!!'})
def chk_user(request):
	username = request.POST['username']
	details = User.objects.filter(username=username).count()
	if details > 0:
		return HttpResponse('yes')
	else:
		return HttpResponse('no')
	
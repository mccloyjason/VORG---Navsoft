from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from passlib.hash import django_pbkdf2_sha256 as handler
from django import http
from django.conf import settings
from datetime import timedelta, date
from django.template import RequestContext

def index(request):
	loginsession = request.session.get('loginsession')
	if loginsession == "":
		return render(request, 'login.html')
	else:
		return HttpResponseRedirect("/home/")
	
	

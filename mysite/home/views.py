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
from django.template import loader, Context



def index(request):
	loginsession = request.session.get('loginsession')
	if loginsession == '':
		return render(request, 'login.html', {'questions': loginsession })
	else:
		return render(request, 'after-login.html', {'questions': loginsession })
def auth_view(request):
	name = request.POST.get('Username', '')
	pwd = request.POST.get('Password', '')
	remember = request.POST.get('remember', '')
	#h=handler.encrypt(pwd,salt_size =12,rounds=12000)
	details1 = User.objects.filter(username=name,password=pwd).count()
	details = User.objects.filter(username=name,password=pwd)
	questions = [d.username for d in details]
	if remember == "":
          request.session.set_test_cookie()
	request.session['loginsession']=questions
	#response = HttpResponse()
	#response = render(request,'after-login.html', {'questions': questions})

	#response.set_cookie('logged_in_status', pwd) 
	#return response
	#return response
	#return render(request, 'home.html', {'questions': questions })
	if details1 == 0:
		return render(request, 'login.html', {'questions': questions, 'msg':'Authentication Failed..!!' })
	else:
		return render(request, 'after-login.html', {'questions': questions })
def logout(request):
	request.session['loginsession'] = ''
	id=request.COOKIES.get('logged_in_status') 
	return render(request, 'login.html',{'msg':''})
def forgot(request):
	return render(request, 'forgot.html')
def change_password(request):
	email = request.POST.get('Email', '')
	details = User.objects.filter(email=email).count()
	
	#return HttpResponse(details[0])
	#return HttpResponse(User.objects.filter(email="'"+email+"'").query)
	if details == 0:
		return render(request, 'forgot.html',{'msg':'Email is not registred!'})
	else:
		u = User.objects.get(email = email)
		msg="Please click on bellow link to change password:"
		msg="Please click on link to change password:" + request.get_host() +"/home/change_password_view/" + u.username
		send_mail('Change Password-VORG', msg, 'hima.shah@navsoft.in',
    [email])
		return render(request,'message.html')
def change_password_view(request,id):
	u = User.objects.get(username = id)
	return render(request,'change_password.html', {'id': id})
def confirm_password(request,id):
	pwd = request.POST.get('Password', '')
	u = User.objects.get(username=id)
	#u.set_password(pwd)
	u.password=pwd
	u.save()
	return render(request,'success.html')
def spreadsheet_download(request):
	import csv
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

	writer = csv.writer(response)
	writer.writerow(['Roles', 'User Name', 'Report-to-Name', 'Email'])
	#writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

	return response	
def chk_email(request):
	email = request.POST['email']
	details = User.objects.filter(email=email).count()
	if details > 0:
		return HttpResponse('yes')
	else:
		return HttpResponse('no')
	
from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#from passlib.hash import django_pbkdf2_sha256 as handler
from django import http
from django.conf import settings
from datetime import timedelta, datetime
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template import loader, Context
from home.models import user_details
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	loginsession = request.session.get('loginsession')
	if not loginsession:
		return render(request, 'login.html', {'questions': loginsession })
	else:
		data = user_details.objects.filter(userid=loginsession).order_by('-id')
		paginator = Paginator(data, 10) # Show 25 contacts per page

		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts})
def auth_view(request):
	loginsession = request.session.get('loginsession')
	if request.method=='POST':
		name = request.POST.get('Username', '')
		pwd = request.POST.get('Password', '')
		remember = request.POST.get('remember', '')
		#h=handler.encrypt(pwd,salt_size =12,rounds=12000)
		details1 = User.objects.filter(username=name,password=pwd).count()
		details = User.objects.filter(username=name,password=pwd)
		questions = [d.username for d in details]
		if remember == "":
			  request.session.set_test_cookie()
		request.session['loginsession']=name
		#response = HttpResponse()
		#response = render(request,'after-login.html', {'questions': questions})

		#response.set_cookie('logged_in_status', pwd) 
		#return response
		#return response
		#return render(request, 'home.html', {'questions': questions })
		if details1 == 0:
			return render(request, 'login.html', {'questions': questions, 'msg':'Authentication Failed..!!' })
		else:
			loginsession = request.session.get('loginsession')
			data = user_details.objects.filter(userid=loginsession).order_by('-id')
			paginator = Paginator(data, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				contacts = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				contacts = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				contacts = paginator.page(paginator.num_pages)
			return render(request, 'after-login.html', {'questions': questions,'data':contacts})
	else :
			loginsession = request.session.get('loginsession')
			data = user_details.objects.filter(userid=loginsession).order_by('-id')
			paginator = Paginator(data, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				contacts = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				contacts = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				contacts = paginator.page(paginator.num_pages)
			loginsession = request.session.get('loginsession')
			return render(request, 'after-login.html', {'questions': loginsession,'data':contacts})
	
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
	writer.writerow(['username', 'role', 'email', 'report_to'])
	#writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

	return response	
def chk_email(request):
	email = request.POST['email']
	details = User.objects.filter(email=email).count()
	if details > 0:
		return HttpResponse('yes')
	else:
		return HttpResponse('no')
def upload(request):
	import csv
	import codecs
	loginsession = request.session.get('loginsession')
	
	if request.method=='POST':
		#return HttpResponse(request.FILES['csvData'].content_type)
		if request.FILES['csvData'].content_type == "text/csv" or request.FILES['csvData'].content_type == "application/vnd.ms-excel":
			file = request.FILES['csvData']
			utf8_file = codecs.EncodedFile(file,"utf-8")
			#data = [row for row in csv.reader(utf8_file)]
			#return HttpResponse(utf8_file)
			i=0
			for row in codecs.EncodedFile(file,"utf-8"):
				if i == 0:
					i += 1
				else:
					row1=row.split(b',')
					user = user_details()
					user.username = row1[0]
					user.role =row1[1]
					user.email =row1[2]
					user.report_to =row1[3]
					user.date =datetime.now()
					user.status ='Active'
					user.userid =loginsession
					user.save()
			data = user_details.objects.filter(userid=loginsession).order_by('-id')
			paginator = Paginator(data, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				contacts = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				contacts = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				contacts = paginator.page(paginator.num_pages)
			loginsession = request.session.get('loginsession')
			return render(request, 'after-import.html', {'questions': loginsession ,'data':contacts})
		else:
			data = user_details.objects.filter(userid=loginsession).order_by('-id')
			paginator = Paginator(data, 10) # Show 25 contacts per page

			page = request.GET.get('page')
			try:
				contacts = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				contacts = paginator.page(1)
			except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
				contacts = paginator.page(paginator.num_pages)
			
			loginsession = request.session.get('loginsession')
			return render(request, 'import-unsuccess.html', {'questions': loginsession,'data':contacts })
	else:
		data = user_details.objects.filter(userid=loginsession).order_by('-id')
		paginator = Paginator(data, 10) # Show 25 contacts per page

		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			contacts = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)

		
		loginsession = request.session.get('loginsession')
		return render(request, 'user-list.html', {'questions': loginsession,'data':contacts })
		
def listinactive(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Inactive'
	u.save()
	return HttpResponse('yes')
def listactive(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Active'
	u.save()
	return HttpResponse('yes')
def removelist(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.delete()
	return HttpResponse('yes')
def activeslt(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Active'
	u.save()
	return HttpResponse('yes')
def inactiveslt(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Inactive'
	u.save()
	return HttpResponse('yes')
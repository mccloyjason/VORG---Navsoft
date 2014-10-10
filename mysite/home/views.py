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
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.utils.translation import ugettext as _

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
		count=user_details.objects.filter(userid=loginsession).count()
		return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts,'count':count})
def auth_view(request):
	loginsession = request.session.get('loginsession')
	if request.method=='POST':
		name = request.POST.get('Email', '')
		pwd = request.POST.get('Password', '')
		remember = request.POST.get('remember', '')
		#h=handler.encrypt(pwd,salt_size =12,rounds=12000)
		details1 = User.objects.filter(email=name,password=pwd).count()
		details = User.objects.filter(email=name,password=pwd)
		questions = [d.username for d in details]
		#return HttpResponse(questions[0])
		if remember == "":
			  request.session.set_test_cookie()
		
		if details1 > 0 :
			request.session['loginsession']=questions[0]
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
			count=user_details.objects.filter(userid=loginsession).count()
			return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts,'count':count})
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
			count=user_details.objects.filter(userid=loginsession).count()
			return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts,'count':count})
	
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
	writer.writerow(['First Name','Last Name','username', 'role', 'email', 'report_to'])
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
	import re
	loginsession = request.session.get('loginsession')
	
	if request.method=='POST':
		#return HttpResponse(request.FILES['csvData'].content_type)
		if request.FILES['csvData'].content_type == "text/csv" or request.FILES['csvData'].content_type == "application/vnd.ms-excel":
			file = request.FILES['csvData']
			utf8_file = codecs.EncodedFile(file,"utf-8")
			#data = [row for row in csv.reader(utf8_file)]
			#return HttpResponse(utf8_file)
			i=0
			j=0
			k=0
			total = 0
			inserted = 0
			for row in codecs.EncodedFile(file,"utf-8"):
				if i == 0:
					i += 1
				else:
					row1=row.split(b',')
					
					newarray = row1
					#return HttpResponse(validate_email('sdkskd.com')=='Enter a valid email address.')
					if re.match(b'^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$', row1[4]):
						cnt=user_details.objects.filter(username=row1[2]).count()
						cnt1=user_details.objects.filter(email=row1[4]).count()
						if cnt > 0 or cnt1 > 0:
							j += 1
						else:
							inserted += 1
							user = user_details()
							user.first_name = row1[0]
							user.last_name = row1[1]
							user.username = row1[2]
							user.role =row1[3]
							user.email =row1[4]
							user.report_to =row1[5]
							user.date =datetime.now()
							user.status ='Active'
							user.userid =loginsession
							user.save()
							username=user.username.decode('utf-8')
							email=user.email.decode('utf-8')
							first_name=user.first_name.decode('utf-8')
							last_name=user.last_name.decode('utf-8')
							users=User.objects.create_user(username , email ,'')
							users.first_name = first_name
							users.last_name = last_name
							users.save()
							msg="Please click on link to Set password:" + request.get_host() +"/home/change_password_view/" + username
							send_mail('Change Password-VORG', msg, 'hima.shah@navsoft.in',[email])
					else:
						k += 1
				total += 1
							
					
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
			count=user_details.objects.filter(userid=loginsession).count()
			return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts,'count':count,'repeat':j,'valid':k,'total':total,'success':'true','inserted':inserted})
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

		
		count=user_details.objects.filter(userid=loginsession).count()
		return render(request, 'after-login.html', {'questions': loginsession ,'data':contacts,'count':count})
		
def listinactive(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Inactive'
	u.save()
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def listactive(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Active'
	u.save()
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def removelist(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.delete()
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def activeslt(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Active'
	u.save()
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def inactiveslt(request):
	id = request.POST['id']
	u = user_details.objects.get(id=id)
	u.status='Inactive'
	u.save()
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def priorg(request):
	
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def priorgdy(request):
	order = request.POST['order']
	loginsession = request.session.get('loginsession')
	data = user_details.objects.filter(userid=loginsession).order_by(order)
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
	dbsa= render_to_response('priorg.html', {'questions': loginsession ,'data':contacts,'page':page},context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def getuser(request):
	dbsa= render_to_response('adduser.html','',context_instance=RequestContext(request))
	return HttpResponse(dbsa)
def insertuser(request):
	loginsession = request.session.get('loginsession')
	first_name =request.POST['first_name']
	last_name =request.POST['last_name']
	username =request.POST['username']
	email =request.POST['email']
	role =request.POST['role']
	report_to =request.POST['report_to']
	user = user_details()
	user.first_name = first_name
	user.last_name = last_name
	user.username = username
	user.role =role
	user.email =email
	user.report_to =report_to
	user.date =datetime.now()
	user.status ='Active'
	user.userid =loginsession
	user.save()
	users=User.objects.create_user(username , email ,'')
	users.first_name = first_name
	users.last_name = last_name
	users.save()
	msg="Please click on link to Set password:" + request.get_host() +"/home/change_password_view/" + username
	send_mail('Set Password-VORG', msg, 'hima.shah@navsoft.in',[email])
	return HttpResponse('Yes')
def autouser(request):
	first_name =request.POST['term']
	user = user_details.objects.filter(first_name__icontains=first_name)
	dbsa= render_to_response('autouser.html', {'user': user },context_instance=RequestContext(request))
	return HttpResponse(dbsa)
	
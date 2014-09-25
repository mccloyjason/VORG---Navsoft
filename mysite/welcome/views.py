from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect

def index(request):
	loginsession = request.session.get('loginsession')
	if not loginsession:
		return render(request, 'login.html',{'msg':''})
	else:
		return HttpResponseRedirect("/home/")
	

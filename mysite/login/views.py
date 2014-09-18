from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect

def index(request):
	return render(request, 'login.html')
	

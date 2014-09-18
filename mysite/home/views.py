from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def index(request):
	return render(request, 'home.html')
def auth_view(request):
	name = request.POST.get('Username', '')
	pwd = request.POST.get('Password', '')
	details = User.objects.filter(username=name,password=pwd)
	questions = [d.username for d in details]
	return render(request, 'home.html', {'questions': questions})
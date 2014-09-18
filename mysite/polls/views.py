from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from polls.models import Choice
from polls.models import Question
def index(request):
#return render(request, 'poll.html')
	details = Question.objects.select_related().filter()
	questions = [d.question_text for d in details]
	return render(request, 'poll.html', {'questions': questions})
#return render(request, 'polls/index.html', {"foo": "bar"},
#content_type="application/xhtml+xml")
#return HttpResponse("Hello, world. You're at the poll index.")
def detail(request, poll_id):
 return HttpResponse("You're looking at poll %s." % poll_id)
def results(request, poll_id):
 return HttpResponse("You're looking at the results of poll %s." % poll_id)
def vote(request, poll_id):
 return HttpResponse("You're voting on poll %s." % poll_id)

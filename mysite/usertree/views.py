from django.shortcuts import render,render_to_response
from usertree.models import Genre
from django.template import RequestContext

# Create your views here.
def show_genres(request):
    return render_to_response("genres.html",
                          {'nodes':Genre.objects.all()},
                          context_instance=RequestContext(request))
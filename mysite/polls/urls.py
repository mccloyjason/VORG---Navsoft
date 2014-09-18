from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from polls import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

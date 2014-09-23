from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from register import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
	 url(r'^signup/$', views.signup, name='signup'),
	  url(r'^chk_user/$', views.chk_user, name='chk_user'),
	 
	  
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
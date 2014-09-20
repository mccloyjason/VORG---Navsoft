from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
	 url(r'^auth/$', views.auth_view, name='auth_view'),
	 url(r'^logout/$', views.auth_view, name='logout'),
	 url(r'^auth/logout/$', views.auth_view, name='logout'),
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

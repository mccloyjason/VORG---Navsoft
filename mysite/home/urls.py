from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
	 url(r'^auth/$', views.auth_view, name='auth_view'),
	 url(r'^logout/$', views.logout, name='logout'),
	 url(r'^home/logout/$', views.logout, name='logout'),
	 url(r'^forgot/$', views.forgot, name='forgot'),
	 url(r'^home/forgot/$', views.forgot, name='forgot'),
	 url(r'^home/change_password/$', views.change_password, name='change_password'),
	 url(r'^change_password/$', views.change_password, name='change_password'),
	 url(r'^confirm_password/(?P<id>\w+)/$', views.confirm_password, name='confirm_password'),
	 url(r'^home/confirm_password/(?P<id>\w+)/$', views.confirm_password, name='confirm_password'),
	  url(r'^home/change_password_view/(?P<id>\w+)/$', views.change_password_view, name='change_password_view'),
	 url(r'^change_password_view/(?P<id>\w+)/$', views.change_password_view, name='change_password_view'),
	 url(r'^spreadsheet_download/$', views.spreadsheet_download, name='spreadsheet_download'),
	 url(r'^chk_email/$', views.chk_email, name='chk_email'),
	  url(r'^upload/$', views.upload, name='upload'),
	  
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

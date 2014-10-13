from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from home import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^auth/$', views.auth_view, name='auth_view'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/logout/$', views.logout, name='logout'),
	url(r'^forgot/$', views.forgot, name='forgot'),
	url(r'^home/forgot/$', views.forgot, name='forgot'),
	url(r'^home/change_password/$', views.change_password, name='change_password'),
	url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^confirm_password/(?P<id>.+)/$', views.confirm_password, name='confirm_password'),
	url(r'^home/confirm_password/(?P<id>.+)/$', views.confirm_password, name='confirm_password'),
	url(r'^home/change_password_view/(?P<id>.+)/$', views.change_password_view, name='change_password_view'),
	url(r'^change_password_view/(?P<id>.+)/$', views.change_password_view, name='change_password_view'),
	url(r'^spreadsheet_download/$', views.spreadsheet_download, name='spreadsheet_download'),
	url(r'^chk_email/$', views.chk_email, name='chk_email'),
	url(r'^upload/$', views.upload, name='upload'),
	url(r'^listinactive/$', views.listinactive, name='listinactive'),
	url(r'^listactive/$', views.listactive, name='listactive'),
	url(r'^removelist/$', views.removelist, name='removelist'),
	url(r'^activeslt/$', views.activeslt, name='activeslt'),
	url(r'^inactiveslt/$', views.inactiveslt, name='inactiveslt'),
	url(r'^priorg/$', views.priorg, name='priorg'),
	url(r'^priorgdy/$', views.priorgdy, name='priorgdy'),
	url(r'^getuser/$', views.getuser, name='getuser'),
	url(r'^insertuser/$', views.insertuser, name='insertuser'),
	url(r'^autouser/$', views.autouser, name='autouser'),
	url(r'^welcomepage/$', views.welcomepage, name='welcomepage'),
	url(r'^hierarchy/$', views.hierarchy, name='hierarchy'),

		
	  
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

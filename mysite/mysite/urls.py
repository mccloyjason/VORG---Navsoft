from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls')),
	url(r'^home/', include('home.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('welcome.urls')),
	url(r'^login/', include('login.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )


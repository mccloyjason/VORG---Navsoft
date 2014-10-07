from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from usertree import views

urlpatterns = patterns('',
    (r'^$', 'usertree.views.show_genres'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

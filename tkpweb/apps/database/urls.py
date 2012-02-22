from django.conf.urls.defaults import patterns, include, url
from .views import DataBaseView


urlpatterns = patterns(
   '',
   url(r'^(?P<host>\w+):(?P<port>\d+)/(?P<database>\w+)/$', view=DataBaseView.as_view(), name='database-port'),
   url(r'^(?P<host>\w+)/(?P<database>\w+)/$', view=DataBaseView.as_view(), name='database-host'),
   url(r'^(?P<database>\w+)/$', view=DataBaseView.as_view(), name='database'),
   url(r'^$', view=DataBaseView.as_view(), name='index')
   )

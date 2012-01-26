from django.conf.urls.defaults import patterns, include, url
from .views import DataBaseView


urlpatterns = patterns(
   '',
   url(r'^(?P<database>\w+)/$', view=DataBaseView.as_view(), name='database'),
   url(r'^$', view=DataBaseView.as_view(), name='index')
   )
